"""
PROACTIVE Label Assigner — GitLab Label Management

Assigns severity labels to merge requests based on PROACTIVE analysis.
Handles label creation (if labels don't exist) and idempotent assignment.

Labels:
  safety-critical  (color: #FF0000) — I6 violations, merge blocked
  epistemic-risk   (color: #FFAA00) — I1-I5 violations, review needed
  phantom-work     (color: #FF6600) — F2 violations, implementation missing
  proactive-pass   (color: #00AA00) — No violations, safe to merge
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

__all__ = [
    "LabelConfig",
    "LabelAssigner",
    "LABEL_DEFINITIONS",
]

# ---------------------------------------------------------------------------
# Label definitions
# ---------------------------------------------------------------------------

LABEL_DEFINITIONS: Dict[str, Dict[str, str]] = {
    "safety-critical": {
        "color": "#FF0000",
        "description": "PROACTIVE: I6 violation detected. Merge is blocked.",
    },
    "epistemic-risk": {
        "color": "#FFAA00",
        "description": "PROACTIVE: I1-I5 violation detected. Review needed.",
    },
    "phantom-work": {
        "color": "#FF6600",
        "description": "PROACTIVE: F2 phantom completion detected. Implementation missing.",
    },
    "proactive-pass": {
        "color": "#00AA00",
        "description": "PROACTIVE: No violations. Safe to merge.",
    },
}


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LabelConfig:
    """Configuration for the label assigner."""

    token: str
    project_id: str
    mr_iid: str
    api_base: str = "https://gitlab.com/api/v4"

    @classmethod
    def from_env(cls) -> Optional["LabelConfig"]:
        """Build config from environment variables."""
        token = os.environ.get("GITLAB_TOKEN") or os.environ.get("CI_JOB_TOKEN") or ""
        project_id = os.environ.get("CI_PROJECT_ID", "")
        mr_iid = os.environ.get("CI_MERGE_REQUEST_IID", "")
        api_base = os.environ.get("CI_API_V4_URL", "https://gitlab.com/api/v4")

        if not all([token, project_id, mr_iid]):
            logger.warning("Missing env vars for label assignment")
            return None

        return cls(token=token, project_id=project_id, mr_iid=mr_iid, api_base=api_base.rstrip("/"))


# ---------------------------------------------------------------------------
# Label Assigner
# ---------------------------------------------------------------------------

class LabelAssigner:
    """Assigns PROACTIVE severity labels to GitLab merge requests."""

    def __init__(self, config: LabelConfig) -> None:
        self._config = config
        self._headers = {
            "Content-Type": "application/json",
            "PRIVATE-TOKEN": config.token,
        }
        if os.environ.get("CI_JOB_TOKEN") and not os.environ.get("GITLAB_TOKEN"):
            self._headers = {
                "Content-Type": "application/json",
                "JOB-TOKEN": config.token,
            }

    def _get(self, path: str) -> dict | list:
        url = f"{self._config.api_base}/{path.lstrip('/')}"
        req = urllib.request.Request(url, headers=self._headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GET {url} failed: {e.code} {body}") from e

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self._config.api_base}/{path.lstrip('/')}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=self._headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"POST {url} failed: {e.code} {body}") from e

    def _put(self, path: str, payload: dict) -> dict:
        url = f"{self._config.api_base}/{path.lstrip('/')}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=self._headers, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"PUT {url} failed: {e.code} {body}") from e

    def ensure_label_exists(self, label_name: str) -> None:
        """Create a label if it doesn't already exist."""
        definition = LABEL_DEFINITIONS.get(label_name, {})
        if not definition:
            logger.warning("Unknown label: %s", label_name)
            return

        path = f"projects/{self._config.project_id}/labels"
        try:
            self._post(path, {
                "name": label_name,
                "color": definition["color"],
                "description": definition["description"],
            })
            logger.info("Created label: %s", label_name)
        except RuntimeError as e:
            if "409" in str(e) or "already_exists" in str(e).lower():
                logger.debug("Label already exists: %s", label_name)
            else:
                logger.warning("Failed to create label %s: %s", label_name, e)

    def assign_labels(self, labels: List[str]) -> List[str]:
        """Assign labels to the MR. Creates labels if they don't exist.

        Args:
            labels: List of label names to assign.

        Returns:
            List of labels that were successfully assigned.
        """
        assigned = []

        for label in labels:
            self.ensure_label_exists(label)

        # Get current MR labels
        mr_path = f"projects/{self._config.project_id}/merge_requests/{self._config.mr_iid}"
        try:
            mr = self._get(mr_path)
            current_labels = [l for l in mr.get("labels", []) if isinstance(l, str)]
        except RuntimeError:
            current_labels = []

        # Remove old PROACTIVE labels
        proactive_labels = set(LABEL_DEFINITIONS.keys())
        new_labels = [l for l in current_labels if l not in proactive_labels]
        new_labels.extend(labels)

        # Update MR labels
        try:
            self._put(mr_path, {"labels": ",".join(new_labels)})
            assigned = labels
            logger.info("Assigned labels to MR !%s: %s", self._config.mr_iid, labels)
        except RuntimeError as e:
            logger.error("Failed to assign labels: %s", e)

        return assigned

    def remove_all_proactive_labels(self) -> None:
        """Remove all PROACTIVE labels from the MR."""
        mr_path = f"projects/{self._config.project_id}/merge_requests/{self._config.mr_iid}"
        try:
            mr = self._get(mr_path)
            current_labels = [l for l in mr.get("labels", []) if isinstance(l, str)]
            proactive_labels = set(LABEL_DEFINITIONS.keys())
            new_labels = [l for l in current_labels if l not in proactive_labels]
            self._put(mr_path, {"labels": ",".join(new_labels)})
            logger.info("Removed PROACTIVE labels from MR !%s", self._config.mr_iid)
        except RuntimeError as e:
            logger.error("Failed to remove labels: %s", e)
