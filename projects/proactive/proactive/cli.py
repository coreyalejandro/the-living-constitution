"""
PROACTIVE CLI
Entry point for running constitutional reviews on merge request data.

Exit codes (deterministic per I6 Fail-Closed):
    0 - APPROVED: No violations detected
    1 - BLOCKED: Violations detected, merge should be blocked
    2 - CONFIG_ERROR: Missing required configuration
    3 - API_FAILURE: GitLab API call failed
    4 - UNEXPECTED_ERROR: Unhandled exception (should not occur)
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from proactive.mr_analyzer import MRContext, analyze_mr
from proactive.report_formatter import format_review_comment

# Configure structured logging for observability
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


__all__ = ["run_review", "run_review_api", "run_vt_generate", "main"]


def run_review(mr_data_path: str) -> int:
    """Run a PROACTIVE review on MR data from a JSON file.

    Args:
        mr_data_path: Path to a JSON file containing MR context.

    Returns:
        0 if the MR is approved, 1 if blocked.
    """
    path = Path(mr_data_path)
    data = json.loads(path.read_text(encoding="utf-8"))

    context = MRContext(
        title=data.get("title", ""),
        description=data.get("description", ""),
        diff=data.get("diff", ""),
        test_artifacts_exist=data.get("test_artifacts_exist", False),
        comments=data.get("comments", []),
        linked_issues=data.get("linked_issues", []),
    )

    result = analyze_mr(context)
    review = format_review_comment(result)

    print(review)

    report = {
        "verdict": result.verdict,
        "trust_score": result.trust_score,
        "violations_count": len(result.violations),
        "claims_count": len(result.claims_found),
        "violations": [
            {
                "invariant": v.invariant,
                "severity": v.severity,
                "message": v.message,
            }
            for v in result.violations
        ],
    }
    print(json.dumps(report, indent=2))

    return 0 if result.verdict != "BLOCKED" else 1


def _save_report_artifacts(
    output_dir: str,
    review_markdown: str,
    report_json: dict,
) -> None:
    """Write PROACTIVE report artifacts to disk.

    Creates the output directory if it doesn't exist and writes:
    - proactive-report.md  (full markdown review)
    - proactive-report.json (structured JSON with verdict, scores, violations)

    Args:
        output_dir: Directory path for report files.
        review_markdown: The formatted markdown review string.
        report_json: Structured report dict.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    md_path = out / "proactive-report.md"
    md_path.write_text(review_markdown, encoding="utf-8")
    logger.info("Report saved: %s", md_path)

    json_path = out / "proactive-report.json"
    json_path.write_text(json.dumps(report_json, indent=2), encoding="utf-8")
    logger.info("Report saved: %s", json_path)


def run_review_api(output_dir: str = "proactive-reports") -> int:
    """Run a PROACTIVE review using the GitLab API.

    Fetches MR context from GitLab, runs analysis, posts the review
    as a comment on the merge request, and saves report artifacts
    to disk for CI artifact persistence.

    Environment variables required:
        GITLAB_TOKEN or CI_JOB_TOKEN
        CI_PROJECT_ID
        CI_MERGE_REQUEST_IID

    Args:
        output_dir: Directory to write report artifacts.

    Returns:
        0 if approved, 1 if blocked, 2 if configuration error,
        3 if API failure (deterministic halt per I6).
    """
    from proactive.gitlab_client import GitLabClient, GitLabConfig
    from proactive.llm_client import LLMClient

    config = GitLabConfig.from_env()
    if config is None:
        logger.error("CONFIG_ERROR: Missing required environment variables")
        print(
            "[PROACTIVE HALT] CONFIG_ERROR\n"
            "Reason: Missing required environment variables.\n"
            "Required: GITLAB_TOKEN (or CI_JOB_TOKEN), CI_PROJECT_ID, CI_MERGE_REQUEST_IID\n"
            "Set these variables and retry.",
            file=sys.stderr,
        )
        return 2

    llm_client = LLMClient.from_env()

    # Circuit breaker: LLM required for constitutional enforcement
    strict_mode = os.environ.get("PROACTIVE_STRICT_MODE", "true").lower() == "true"
    if strict_mode and not llm_client.enabled:
        logger.error("STRICT_MODE: LLM required but unavailable (no ANTHROPIC_API_KEY)")
        print(
            "[PROACTIVE HALT] CONFIG_ERROR\n"
            "Reason: LLM client required but not configured.\n"
            "Set ANTHROPIC_API_KEY or disable STRICT_MODE.",
            file=sys.stderr,
        )
        return 2

    logger.info("Starting PROACTIVE review for MR in project %s", config.project_id)

    try:
        with GitLabClient(config) as gl:
            # Fetch MR context with deterministic error handling
            try:
                context = gl.fetch_mr_context()
                logger.info("Successfully fetched MR context")
            except Exception as exc:
                logger.error("API_FAILURE: Failed to fetch MR context: %s", exc)
                print(
                    f"[PROACTIVE HALT] API_FAILURE\n"
                    f"Reason: Failed to fetch MR context from GitLab API\n"
                    f"Details: {exc}\n"
                    f"This may be due to network issues, invalid credentials, or GitLab downtime.",
                    file=sys.stderr,
                )
                return 3

            result = analyze_mr(context, llm_client=llm_client)
            review = format_review_comment(result)

            print(review)
            logger.info("Analysis complete: verdict=%s, violations=%d",
                       result.verdict, len(result.violations))

            # Post review comment with deterministic error handling
            try:
                gl.post_review_comment(review)
                logger.info("Review posted to MR !%s", config.mr_iid)
                print(f"Review posted to MR !{config.mr_iid}")
            except Exception as exc:
                logger.error("API_FAILURE: Failed to post comment: %s", exc)
                print(
                    f"[PROACTIVE HALT] API_FAILURE\n"
                    f"Reason: Failed to post review comment to GitLab API\n"
                    f"Details: {exc}\n"
                    f"The review was generated but could not be posted.",
                    file=sys.stderr,
                )
                return 3

        report = {
            "verdict": result.verdict,
            "trust_score": result.trust_score,
            "violations_count": len(result.violations),
            "claims_count": len(result.claims_found),
            "violations": [
                {
                    "invariant": v.invariant,
                    "severity": v.severity,
                    "message": v.message,
                    "suggested_fix": v.suggested_fix,
                }
                for v in result.violations
            ],
            "claims": [
                {
                    "text": c.text,
                    "claim_type": c.claim_type,
                    "source": c.source,
                }
                for c in result.claims_found
            ],
        }
        print(json.dumps(report, indent=2))

        # Persist report artifacts to disk
        try:
            _save_report_artifacts(output_dir, review, report)
        except OSError as exc:
            logger.warning("Failed to save report artifacts: %s", exc)
            # Non-fatal: the review was already posted to the MR

        exit_code = 0 if result.verdict != "BLOCKED" else 1
        logger.info("Exit code: %d", exit_code)
        return exit_code

    except Exception as exc:
        # Catch-all for truly unexpected errors (should not reach here)
        logger.critical("UNEXPECTED_ERROR: %s", exc, exc_info=True)
        print(
            f"[PROACTIVE HALT] UNEXPECTED_ERROR\n"
            f"Reason: An unexpected error occurred\n"
            f"Details: {exc}\n"
            f"Please report this as a bug.",
            file=sys.stderr,
        )
        return 4


def run_vt_generate(args) -> int:
    """Generate a V&T statement from CLI arguments.

    Args:
        args: Parsed argparse namespace with description, title, diff-file, format.

    Returns:
        0 on success, 2 on input error.
    """
    from proactive.vt_generator import generate_vt_statement

    # Load description
    description = args.description
    if args.description_file:
        try:
            description = Path(args.description_file).read_text(encoding="utf-8")
        except (FileNotFoundError, PermissionError, OSError) as exc:
            print(f"Error: Cannot read description file: {exc}", file=sys.stderr)
            return 2

    if not description.strip():
        print("Error: --description or --description-file is required.", file=sys.stderr)
        return 2

    # Load diff
    diff = ""
    if args.diff_file:
        try:
            diff = Path(args.diff_file).read_text(encoding="utf-8")
        except (FileNotFoundError, PermissionError, OSError) as exc:
            print(f"Error: Cannot read diff file: {exc}", file=sys.stderr)
            return 2

    # Generate
    result = generate_vt_statement(description, diff=diff, title=args.title)

    # Output
    if args.format == "json":
        print(result.as_json)
    else:
        print(result.markdown)

    return 0


def main() -> None:
    """CLI entry point with argparse."""
    import argparse

    parser = argparse.ArgumentParser(description="PROACTIVE CLI")
    subparsers = parser.add_subparsers(dest="command")

    review_parser = subparsers.add_parser("review", help="Review an MR from JSON file")
    review_parser.add_argument("--mr-data", required=True, help="Path to MR data JSON")
    review_parser.add_argument(
        "--format", default="text", choices=["text", "json", "gitlab"]
    )
    review_parser.add_argument("--strict", default="true")

    review_api_parser = subparsers.add_parser(
        "review-api",
        help="Review an MR via GitLab API (requires env vars)",
    )
    review_api_parser.add_argument(
        "--output-dir",
        default="proactive-reports",
        help="Directory to write report artifacts (default: proactive-reports)",
    )

    vt_parser = subparsers.add_parser(
        "vt-generate",
        help="Generate a V&T statement from MR description and optional diff",
    )
    vt_parser.add_argument("--description", default="", help="MR description text")
    vt_parser.add_argument("--description-file", default=None, help="Path to file containing MR description")
    vt_parser.add_argument("--title", default="", help="MR title")
    vt_parser.add_argument("--diff-file", default=None, help="Path to diff file")
    vt_parser.add_argument(
        "--format", default="markdown", choices=["markdown", "json"],
        help="Output format (default: markdown)",
    )

    args = parser.parse_args()

    if args.command == "review":
        exit_code = run_review(args.mr_data)
        sys.exit(exit_code)
    elif args.command == "review-api":
        exit_code = run_review_api(output_dir=args.output_dir)
        sys.exit(exit_code)
    elif args.command == "vt-generate":
        exit_code = run_vt_generate(args)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
