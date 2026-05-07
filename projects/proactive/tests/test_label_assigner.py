"""Tests for PROACTIVE label assigner."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from proactive.label_assigner import (
    LabelConfig,
    LabelAssigner,
    LABEL_DEFINITIONS,
)


class TestLabelConfig:
    def test_from_env_with_all_vars(self):
        env = {
            "GITLAB_TOKEN": "test-token",
            "CI_PROJECT_ID": "123",
            "CI_MERGE_REQUEST_IID": "42",
            "CI_API_V4_URL": "https://gitlab.com/api/v4",
        }
        with patch.dict("os.environ", env, clear=False):
            config = LabelConfig.from_env()
            assert config is not None
            assert config.token == "test-token"
            assert config.project_id == "123"
            assert config.mr_iid == "42"

    def test_from_env_missing_token_returns_none(self):
        env = {
            "CI_PROJECT_ID": "123",
            "CI_MERGE_REQUEST_IID": "42",
        }
        with patch.dict("os.environ", env, clear=True):
            config = LabelConfig.from_env()
            assert config is None

    def test_from_env_uses_ci_job_token_fallback(self):
        env = {
            "CI_JOB_TOKEN": "job-token",
            "CI_PROJECT_ID": "123",
            "CI_MERGE_REQUEST_IID": "42",
        }
        with patch.dict("os.environ", env, clear=True):
            config = LabelConfig.from_env()
            assert config is not None
            assert config.token == "job-token"


class TestLabelDefinitions:
    def test_all_labels_have_color(self):
        for name, defn in LABEL_DEFINITIONS.items():
            assert "color" in defn, f"Label {name} missing color"

    def test_all_labels_have_description(self):
        for name, defn in LABEL_DEFINITIONS.items():
            assert "description" in defn, f"Label {name} missing description"

    def test_safety_critical_is_red(self):
        assert LABEL_DEFINITIONS["safety-critical"]["color"] == "#FF0000"

    def test_proactive_pass_is_green(self):
        assert LABEL_DEFINITIONS["proactive-pass"]["color"] == "#00AA00"

    def test_four_labels_defined(self):
        assert len(LABEL_DEFINITIONS) == 4


class TestLabelAssigner:
    def _make_assigner(self):
        config = LabelConfig(
            token="test-token",
            project_id="123",
            mr_iid="42",
            api_base="https://gitlab.com/api/v4",
        )
        return LabelAssigner(config)

    @patch.object(LabelAssigner, "_post")
    def test_ensure_label_exists_creates_label(self, mock_post):
        mock_post.return_value = {"name": "safety-critical"}
        assigner = self._make_assigner()
        assigner.ensure_label_exists("safety-critical")
        mock_post.assert_called_once()

    @patch.object(LabelAssigner, "_post")
    def test_ensure_label_exists_handles_conflict(self, mock_post):
        mock_post.side_effect = RuntimeError("409 Conflict")
        assigner = self._make_assigner()
        assigner.ensure_label_exists("safety-critical")
        # Should not raise

    @patch.object(LabelAssigner, "_put")
    @patch.object(LabelAssigner, "_get")
    @patch.object(LabelAssigner, "_post")
    def test_assign_labels_updates_mr(self, mock_post, mock_get, mock_put):
        mock_post.return_value = {}
        mock_get.return_value = {"labels": []}
        mock_put.return_value = {}
        assigner = self._make_assigner()
        result = assigner.assign_labels(["safety-critical"])
        assert "safety-critical" in result
        mock_put.assert_called_once()

    @patch.object(LabelAssigner, "_put")
    @patch.object(LabelAssigner, "_get")
    @patch.object(LabelAssigner, "_post")
    def test_assign_labels_removes_old_proactive_labels(self, mock_post, mock_get, mock_put):
        mock_post.return_value = {}
        mock_get.return_value = {"labels": ["proactive-pass", "bug"]}
        mock_put.return_value = {}
        assigner = self._make_assigner()
        assigner.assign_labels(["safety-critical"])
        call_args = mock_put.call_args[0][1]
        labels_str = call_args["labels"]
        assert "proactive-pass" not in labels_str
        assert "bug" in labels_str
        assert "safety-critical" in labels_str

    @patch.object(LabelAssigner, "_put")
    @patch.object(LabelAssigner, "_get")
    @patch.object(LabelAssigner, "_post")
    def test_assign_multiple_labels(self, mock_post, mock_get, mock_put):
        mock_post.return_value = {}
        mock_get.return_value = {"labels": []}
        mock_put.return_value = {}
        assigner = self._make_assigner()
        result = assigner.assign_labels(["safety-critical", "phantom-work"])
        assert len(result) == 2

    @patch.object(LabelAssigner, "_put")
    @patch.object(LabelAssigner, "_get")
    def test_remove_all_proactive_labels(self, mock_get, mock_put):
        mock_get.return_value = {"labels": ["safety-critical", "bug", "phantom-work"]}
        mock_put.return_value = {}
        assigner = self._make_assigner()
        assigner.remove_all_proactive_labels()
        call_args = mock_put.call_args[0][1]
        labels_str = call_args["labels"]
        assert "safety-critical" not in labels_str
        assert "phantom-work" not in labels_str
        assert "bug" in labels_str
