"""
PROACTIVE GitLab Client — API Integration

Bridge between PROACTIVE analysis and the GitLab API. Fetches MR
context (title, description, diff, comments) and posts review
comments back to the merge request.

Configuration via environment variables:
- GITLAB_TOKEN or CI_JOB_TOKEN: Authentication
- CI_PROJECT_ID: Project ID
- CI_MERGE_REQUEST_IID: MR internal ID
- CI_API_V4_URL: GitLab API base URL (default: https://gitlab.com/api/v4)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urljoin

import urllib.request
import urllib.error
import json

from proactive.mr_analyzer import MRContext

logger = logging.getLogger(__name__)

__all__ = [
    "GitLabConfig",
    "GitLabClient",
]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GitLabConfig:
    """Configuration for the GitLab API client."""

    token: str
    project_id: str
    mr_iid: str
    api_base: str = "https://gitlab.com/api/v4"

    @classmethod
    def from_env(cls) -> Optional["GitLabConfig"]:
        """Build config from environment variables. Returns None if incomplete."""
        token = (
            os.environ.get("GITLAB_TOKEN")
            or os.environ.get("CI_JOB_TOKEN")
            or ""
        )
        project_id = os.environ.get("CI_PROJECT_ID", "")
        mr_iid = os.environ.get("CI_MERGE_REQUEST_IID", "")
        api_base = os.environ.get(
            "CI_API_V4_URL", "https://gitlab.com/api/v4"
        )

        if not all([token, project_id, mr_iid]):
            logger.error(
                "Missing required env vars: GITLAB_TOKEN/CI_JOB_TOKEN, "
                "CI_PROJECT_ID, CI_MERGE_REQUEST_IID"
            )
            return None

        return cls(
            token=token,
            project_id=project_id,
            mr_iid=mr_iid,
            api_base=api_base.rstrip("/"),
        )


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class GitLabClient:
    """GitLab API client for PROACTIVE review integration.

    Use as a context manager:
        with GitLabClient(config) as gl:
            context = gl.fetch_mr_context()
            gl.post_review_comment(review)
    """

    def __init__(self, config: GitLabConfig) -> None:
        self._config = config
        self._headers = {
            "Content-Type": "application/json",
            "PRIVATE-TOKEN": config.token,
        }
        # CI_JOB_TOKEN uses a different header
        if os.environ.get("CI_JOB_TOKEN") and not os.environ.get("GITLAB_TOKEN"):
            self._headers = {
                "Content-Type": "application/json",
                "JOB-TOKEN": config.token,
            }

    def __enter__(self) -> "GitLabClient":
        return self

    def __exit__(self, *args: object) -> None:
        pass

    # -----------------------------------------------------------------------
    # Internal HTTP helpers
    # -----------------------------------------------------------------------

    def _get(self, path: str) -> dict | list:
        """Make a GET request to the GitLab API."""
        url = f"{self._config.api_base}/{path.lstrip('/')}"
        req = urllib.request.Request(url, headers=self._headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"GitLab API GET {url} failed: {e.code} {e.reason} — {body}"
            ) from e

    def _post(self, path: str, payload: dict) -> dict:
        """Make a POST request to the GitLab API."""
        url = f"{self._config.api_base}/{path.lstrip('/')}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers=self._headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"GitLab API POST {url} failed: {e.code} {e.reason} — {body}"
            ) from e

    # -----------------------------------------------------------------------
    # MR context fetching
    # -----------------------------------------------------------------------

    def _fetch_mr(self) -> dict:
        path = (
            f"projects/{self._config.project_id}"
            f"/merge_requests/{self._config.mr_iid}"
        )
        return self._get(path)

    def _fetch_mr_diff(self) -> str:
        path = (
            f"projects/{self._config.project_id}"
            f"/merge_requests/{self._config.mr_iid}/diffs"
        )
        diffs = self._get(path)
        if not isinstance(diffs, list):
            return ""
        parts = []
        for d in diffs:
            if isinstance(d, dict) and d.get("diff"):
                parts.append(
                    f"--- a/{d.get('old_path', '')}\n"
                    f"+++ b/{d.get('new_path', '')}\n"
                    f"{d['diff']}"
                )
        return "\n".join(parts)

    def _fetch_mr_comments(self) -> List[str]:
        path = (
            f"projects/{self._config.project_id}"
            f"/merge_requests/{self._config.mr_iid}/notes"
        )
        notes = self._get(path)
        if not isinstance(notes, list):
            return []
        return [
            n["body"]
            for n in notes
            if isinstance(n, dict) and n.get("body") and not n.get("system")
        ]

    def _fetch_linked_issues(self, mr: dict) -> List[str]:
        """Extract issue references from MR description."""
        import re
        description = mr.get("description", "") or ""
        return re.findall(r"#(\d+)", description)

    def _pipeline_info(self, mr: dict) -> tuple[str, str, bool]:
        """Extract pipeline URL, status, and artifact existence hint from MR."""
        pipeline = mr.get("head_pipeline")
        if not pipeline:
            return "", "", False
        web_url = pipeline.get("web_url", "")
        status = pipeline.get("status", "")
        # Artifacts considered present if pipeline succeeded or is a relevant status
        artifacts_exist = status in ("success", "passed", "running", "pending")
        return web_url, status, artifacts_exist

    def fetch_mr_context(self) -> MRContext:
        """Fetch full MR context from GitLab API.

        Returns:
            MRContext ready to pass to analyze_mr().

        Raises:
            RuntimeError: If the API call fails.
        """
        logger.info(
            "Fetching MR !%s from project %s",
            self._config.mr_iid,
            self._config.project_id,
        )

        mr = self._fetch_mr()
        diff = self._fetch_mr_diff()
        comments = self._fetch_mr_comments()
        linked_issues = self._fetch_linked_issues(mr)

        pipeline_url, pipeline_status, artifacts_exist = self._pipeline_info(mr)

        return MRContext(
            title=mr.get("title", ""),
            description=mr.get("description", "") or "",
            diff=diff,
            test_artifacts_exist=artifacts_exist,
            pipeline_url=pipeline_url,
            pipeline_status=pipeline_status,
            comments=comments,
            linked_issues=linked_issues,
        )

    # -----------------------------------------------------------------------
    # Posting review
    # -----------------------------------------------------------------------

    def post_review_comment(self, body: str) -> None:
        """Post the PROACTIVE review as a comment on the MR.

        Args:
            body: Markdown review comment from format_review_comment().

        Raises:
            RuntimeError: If the API call fails.
        """
        path = (
            f"projects/{self._config.project_id}"
            f"/merge_requests/{self._config.mr_iid}/notes"
        )
        self._post(path, {"body": body})
        logger.info(
            "Posted review comment to MR !%s", self._config.mr_iid
        )