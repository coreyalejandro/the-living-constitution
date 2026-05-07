"""
Tests for proactive/web_ui.py — V&T Generator Web Interface

Covers:
- App creation
- Index page rendering
- Form submission (markdown and JSON)
- API endpoint
- Error handling
- Empty input handling
"""

from __future__ import annotations

import json
import os
import pytest

os.environ.pop("ANTHROPIC_API_KEY", None)


try:
    import flask
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

skip_no_flask = pytest.mark.skipif(
    not HAS_FLASK,
    reason="Flask not installed",
)


@pytest.fixture
def app():
    if not HAS_FLASK:
        pytest.skip("Flask not installed")
    from proactive.web_ui import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@skip_no_flask
class TestAppCreation:

    def test_create_app_returns_flask_app(self, app):
        assert app is not None
        assert hasattr(app, "test_client")


@skip_no_flask
class TestIndexPage:

    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_contains_form(self, client):
        response = client.get("/")
        html = response.data.decode()
        assert "<form" in html
        assert "description" in html

    def test_index_contains_title(self, client):
        response = client.get("/")
        html = response.data.decode()
        assert "PROACTIVE" in html
        assert "V&T Generator" in html


@skip_no_flask
class TestFormSubmission:

    def test_generate_markdown(self, client):
        response = client.post("/generate", data={
            "title": "Fix login bug",
            "description": "Fix the login authentication bug. All tests pass.",
            "diff": "",
            "format": "markdown",
        })
        assert response.status_code == 200
        html = response.data.decode()
        assert "V&T Statement" in html

    def test_generate_json(self, client):
        response = client.post("/generate", data={
            "title": "Fix login bug",
            "description": "Fix the login authentication bug.",
            "diff": "",
            "format": "json",
        })
        assert response.status_code == 200
        html = response.data.decode()
        assert "overall_confidence" in html

    def test_empty_description_shows_error(self, client):
        response = client.post("/generate", data={
            "title": "",
            "description": "",
            "diff": "",
            "format": "markdown",
        })
        assert response.status_code == 200
        html = response.data.decode()
        assert "Error" in html or "error" in html

    def test_with_diff(self, client):
        response = client.post("/generate", data={
            "title": "Fix login",
            "description": "Fix the login authentication bug.",
            "diff": "+++ b/src/auth.py\n+def login(): pass",
            "format": "markdown",
        })
        assert response.status_code == 200


@skip_no_flask
class TestAPIEndpoint:

    def test_api_generate_returns_json(self, client):
        response = client.post("/api/generate",
            data=json.dumps({
                "description": "Fix the login bug.",
                "title": "Fix login",
            }),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "markdown" in data
        assert "json" in data
        assert "confidence" in data
        assert "status" in data

    def test_api_empty_description_returns_400(self, client):
        response = client.post("/api/generate",
            data=json.dumps({"description": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_api_with_diff(self, client):
        response = client.post("/api/generate",
            data=json.dumps({
                "description": "Fix the login bug.",
                "diff": "+++ b/src/auth.py\n+def login(): pass",
            }),
            content_type="application/json",
        )
        assert response.status_code == 200
