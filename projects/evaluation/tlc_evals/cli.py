"""
tlc-evals CLI — command-line interface for TLC evaluation runs.

Usage:
    tlc-evals run [OPTIONS]
    tlc-evals check TEXT [OPTIONS]
    tlc-evals suite YAML_PATH [OPTIONS]
    tlc-evals report JSON_PATH [OPTIONS]
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

app = typer.Typer(
    name="tlc-evals",
    help="TLC constitutional evaluation library — grounded in Anthropic's research methodology.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def run(
    failure_types: Annotated[
        Optional[list[str]],
        typer.Option("--type", "-t", help="Failure types to evaluate: F1 F2 F3 F4 F5"),
    ] = None,
    model: Annotated[
        str,
        typer.Option("--model", "-m", help="Claude model ID for grading"),
    ] = "claude-sonnet-4-5",
    pattern_only: Annotated[
        bool,
        typer.Option("--pattern-only", help="Use pattern grader only (no API calls)"),
    ] = False,
    output_json: Annotated[
        Optional[str],
        typer.Option("--output-json", "-o", help="Write JSON results to path"),
    ] = None,
    output_vt: Annotated[
        Optional[str],
        typer.Option("--output-vt", help="Write V&T statement to path"),
    ] = None,
    output_sarif: Annotated[
        Optional[str],
        typer.Option("--output-sarif", help="Write SARIF report to path"),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Run the full TLC evaluation suite against built-in cases."""
    _check_api_key()

    from tlc_evals.core.runner import EvalRunner
    from tlc_evals.evals.suite import EvalSuite
    from tlc_evals.evals.f1_confident_false_claims import ConfidentFalseClaimsEval
    from tlc_evals.evals.f2_phantom_completion import PhantomCompletionEval
    from tlc_evals.evals.f3_persistence_under_correction import PersistenceUnderCorrectionEval
    from tlc_evals.evals.f4_harm_risk_coupling import HarmRiskCouplingEval
    from tlc_evals.evals.f5_cross_episode_recurrence import CrossEpisodeRecurrenceEval
    from tlc_evals.reporters.console_reporter import ConsoleReporter
    from tlc_evals.reporters.vt_reporter import VTReporter
    from tlc_evals.reporters.sarif_reporter import SARIFReporter
    from tlc_evals.reporters.json_reporter import JSONReporter

    _type_set = set(failure_types or ["F1", "F2", "F3", "F4", "F5"])
    _use_model = not pattern_only

    eval_map = {
        "F1": ConfidentFalseClaimsEval(use_model_grader=_use_model),
        "F2": PhantomCompletionEval(use_model_grader=_use_model),
        "F3": PersistenceUnderCorrectionEval(use_model_grader=_use_model),
        "F4": HarmRiskCouplingEval(use_model_grader=_use_model),
        "F5": CrossEpisodeRecurrenceEval(use_model_grader=_use_model),
    }

    active_evals = [v for k, v in eval_map.items() if k in _type_set]
    suite = EvalSuite.from_evals(*active_evals, name="tlc_cli_run")
    runner = EvalRunner(eval_classes=active_evals)

    typer.echo(f"Running {len(suite)} cases across {len(active_evals)} eval type(s)...")
    summary = runner.run(suite)

    ConsoleReporter(verbose=verbose).print(summary)

    if output_json:
        JSONReporter().write(summary, output_json)
        typer.echo(f"JSON results → {output_json}")

    if output_vt:
        VTReporter().write(summary, path=output_vt)
        typer.echo(f"V&T statement → {output_vt}")

    if output_sarif:
        SARIFReporter().write(summary, output_sarif)
        typer.echo(f"SARIF report → {output_sarif}")

    # Exit non-zero if any failures
    if summary.failed > 0:
        raise typer.Exit(code=1)


@app.command()
def check(
    text: Annotated[str, typer.Argument(help="Agent output text to check")],
    invariants: Annotated[
        Optional[list[str]],
        typer.Option("--invariant", "-i", help="Invariants to check: I1 I2 I3 I4 I5 I6"),
    ] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Quick constitutional invariant check on a text string."""
    from tlc_evals.invariants.checker import InvariantChecker
    from tlc_evals.core.types import Invariant

    active: list[Invariant] | None = None
    if invariants:
        active = []
        for s in invariants:
            try:
                active.append(Invariant(s))
            except ValueError:
                typer.echo(f"Unknown invariant: {s}", err=True)

    checker = InvariantChecker(active_invariants=active)
    result = checker.check(text)

    if json_output:
        output = {
            "passed": result.passed,
            "error_count": result.error_count,
            "warning_count": result.warning_count,
            "violations": [
                {
                    "invariant": v.invariant.value,
                    "description": v.description,
                    "evidence": v.evidence,
                    "severity": v.severity.value,
                }
                for v in result.violations
            ],
        }
        typer.echo(json.dumps(output, indent=2))
    else:
        if result.passed:
            typer.echo("✓ PASS — no constitutional violations detected.")
        else:
            typer.echo(
                f"✗ VIOLATIONS — {result.error_count} ERROR, {result.warning_count} WARNING"
            )
            for v in result.violations:
                symbol = "⚠" if v.severity.value == "ERROR" else "◦"
                typer.echo(f"  {symbol} [{v.invariant.value}] {v.description}")
                if v.evidence:
                    typer.echo(f"       Evidence: {v.evidence[:80]}...")

    raise typer.Exit(code=0 if result.passed else 1)


@app.command()
def suite(
    yaml_path: Annotated[str, typer.Argument(help="Path to YAML eval spec file")],
    model: str = typer.Option("claude-sonnet-4-5", "--model", "-m"),
    output_json: Optional[str] = typer.Option(None, "--output-json", "-o"),
    output_vt: Optional[str] = typer.Option(None, "--output-vt"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Run an eval suite from a YAML spec file."""
    _check_api_key()

    from tlc_evals.evals.suite import EvalSuite
    from tlc_evals.core.runner import EvalRunner
    from tlc_evals.reporters.console_reporter import ConsoleReporter
    from tlc_evals.reporters.vt_reporter import VTReporter
    from tlc_evals.reporters.json_reporter import JSONReporter

    eval_suite = EvalSuite.from_yaml(yaml_path)
    typer.echo(f"Loaded suite '{eval_suite.name}' with {len(eval_suite)} cases.")

    runner = EvalRunner()
    summary = runner.run(eval_suite)
    ConsoleReporter(verbose=verbose).print(summary)

    if output_json:
        JSONReporter().write(summary, output_json)
        typer.echo(f"JSON → {output_json}")
    if output_vt:
        VTReporter().write(summary, path=output_vt)
        typer.echo(f"V&T → {output_vt}")

    raise typer.Exit(code=0 if summary.failed == 0 else 1)


@app.command()
def report(
    json_path: Annotated[str, typer.Argument(help="Path to JSON results file")],
    format: Annotated[
        str,
        typer.Option("--format", "-f", help="Output format: vt, sarif, console"),
    ] = "console",
    output: Optional[str] = typer.Option(None, "--output", "-o"),
) -> None:
    """Generate a report from a previously-saved JSON results file."""
    from tlc_evals.reporters.json_reporter import JSONReporter
    from tlc_evals.reporters.vt_reporter import VTReporter
    from tlc_evals.reporters.sarif_reporter import SARIFReporter
    from tlc_evals.reporters.console_reporter import ConsoleReporter

    summary = JSONReporter().load(json_path)

    if format == "vt":
        reporter = VTReporter()
        reporter.write(summary, path=output)
    elif format == "sarif":
        if not output:
            typer.echo("--output is required for SARIF format", err=True)
            raise typer.Exit(1)
        SARIFReporter().write(summary, output)
        typer.echo(f"SARIF → {output}")
    else:
        ConsoleReporter(verbose=True).print(summary)


def _check_api_key() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        typer.echo(
            "⚠ ANTHROPIC_API_KEY not set. "
            "Set it or use --pattern-only for zero-API-cost grading.",
            err=True,
        )


if __name__ == "__main__":
    app()
