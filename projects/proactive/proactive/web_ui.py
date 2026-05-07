"""
PROACTIVE Web UI — V&T Statement Generator Web Interface

A lightweight Flask web application for generating V&T statements
interactively. Provides a form for MR description + diff input
and displays the generated V&T statement with confidence breakdown.

Usage:
    python -m proactive.web_ui
    # Opens at http://localhost:5000

Or programmatically:
    from proactive.web_ui import create_app
    app = create_app()
    app.run()
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

__all__ = ["create_app"]


def create_app():
    """Create and configure the Flask application.

    Returns:
        Flask app instance.

    Raises:
        ImportError: If Flask is not installed.
    """
    try:
        from flask import Flask, request, render_template_string, jsonify
    except ImportError:
        raise ImportError(
            "Flask is required for the web UI. "
            "Install it with: pip install flask"
        )

    from proactive.vt_generator import generate_vt_statement

    app = Flask(__name__)
    secret_key = os.environ.get("FLASK_SECRET_KEY", "")
    if not secret_key:
        secret_key = os.urandom(24).hex()
        logger.warning(
            "FLASK_SECRET_KEY not set \u2014 using random key. "
            "Sessions will not persist across restarts. "
            "Set FLASK_SECRET_KEY env var for production use."
        )
    app.secret_key = secret_key

    INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROACTIVE V&T Generator</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0d1117; color: #c9d1d9; padding: 2rem;
            max-width: 900px; margin: 0 auto;
        }
        h1 { color: #58a6ff; margin-bottom: 0.5rem; }
        .subtitle { color: #8b949e; margin-bottom: 2rem; }
        label { display: block; font-weight: 600; margin: 1rem 0 0.5rem; color: #c9d1d9; }
        textarea, input[type="text"] {
            width: 100%; padding: 0.75rem; border: 1px solid #30363d;
            border-radius: 6px; background: #161b22; color: #c9d1d9;
            font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.9rem;
            resize: vertical;
        }
        textarea:focus, input:focus { border-color: #58a6ff; outline: none; }
        .btn {
            display: inline-block; padding: 0.75rem 1.5rem; margin: 1.5rem 0.5rem 1.5rem 0;
            border: none; border-radius: 6px; font-size: 1rem; font-weight: 600;
            cursor: pointer; transition: background 0.2s;
        }
        .btn-primary { background: #238636; color: #fff; }
        .btn-primary:hover { background: #2ea043; }
        .btn-secondary { background: #30363d; color: #c9d1d9; }
        .btn-secondary:hover { background: #484f58; }
        .result { margin-top: 2rem; padding: 1.5rem; background: #161b22;
                  border: 1px solid #30363d; border-radius: 6px; }
        .result h2 { color: #58a6ff; margin-bottom: 1rem; }
        .result pre {
            background: #0d1117; padding: 1rem; border-radius: 4px;
            overflow-x: auto; white-space: pre-wrap; font-size: 0.85rem;
        }
        .confidence-bar {
            height: 8px; border-radius: 4px; background: #30363d; margin: 0.5rem 0;
        }
        .confidence-fill {
            height: 100%; border-radius: 4px; transition: width 0.3s;
        }
        .conf-high { background: #238636; }
        .conf-med { background: #d29922; }
        .conf-low { background: #da3633; }
        .status-pass { color: #238636; }
        .status-warn { color: #d29922; }
        .status-block { color: #da3633; }
        footer { margin-top: 3rem; color: #484f58; font-size: 0.85rem; text-align: center; }
    </style>
</head>
<body>
    <h1>PROACTIVE V&T Generator</h1>
    <p class="subtitle">Generate Verification & Truth statements for merge requests</p>

    <form method="POST" action="/generate">
        <label for="title">MR Title (optional)</label>
        <input type="text" id="title" name="title" placeholder="e.g., Fix the login authentication bug"
               value="{{ title or '' }}">

        <label for="description">MR Description</label>
        <textarea id="description" name="description" rows="8"
                  placeholder="Paste your MR description here...">{{ description or '' }}</textarea>

        <label for="diff">Code Diff (optional)</label>
        <textarea id="diff" name="diff" rows="10"
                  placeholder="Paste your git diff here (optional)...">{{ diff or '' }}</textarea>

        <button type="submit" class="btn btn-primary" name="format" value="markdown">Generate V&T (Markdown)</button>
        <button type="submit" class="btn btn-secondary" name="format" value="json">Generate V&T (JSON)</button>
    </form>

    {% if result %}
    <div class="result">
        <h2>V&T Statement</h2>

        <div>
            <strong>Overall Confidence:</strong> {{ confidence_pct }}%
            <div class="confidence-bar">
                <div class="confidence-fill {{ confidence_class }}" style="width: {{ confidence_pct }}%"></div>
            </div>
        </div>

        <p><strong>Status:</strong>
            <span class="status-{{ status_class }}">{{ status }}</span>
        </p>

        <pre>{{ result }}</pre>
    </div>
    {% endif %}

    <footer>
        PROACTIVE - Constitutional AI Safety Agent - Enhancement #5
    </footer>
</body>
</html>
"""

    @app.route("/", methods=["GET"])
    def index():
        return render_template_string(INDEX_TEMPLATE)

    @app.route("/generate", methods=["POST"])
    def generate():
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        diff = request.form.get("diff", "")
        output_format = request.form.get("format", "markdown")

        if not description.strip():
            return render_template_string(
                INDEX_TEMPLATE,
                title=title,
                description=description,
                diff=diff,
                result="Error: Please provide an MR description.",
                confidence_pct=0,
                confidence_class="conf-low",
                status="ERROR",
                status_class="block",
                status_detail="No input provided",
            )

        vt_result = generate_vt_statement(description, diff, title)

        if output_format == "json":
            rendered = vt_result.as_json
        else:
            rendered = vt_result.markdown

        conf_pct = int(vt_result.overall_confidence * 100)
        if conf_pct >= 70:
            conf_class = "conf-high"
        elif conf_pct >= 40:
            conf_class = "conf-med"
        else:
            conf_class = "conf-low"

        status = vt_result.vt_statement.status if vt_result.vt_statement else "UNKNOWN"
        status_detail = vt_result.vt_statement.status_detail if vt_result.vt_statement else ""
        status_class = {"PASS": "pass", "WARN": "warn", "BLOCK": "block"}.get(status, "warn")

        return render_template_string(
            INDEX_TEMPLATE,
            title=title,
            description=description,
            diff=diff,
            result=rendered,
            confidence_pct=conf_pct,
            confidence_class=conf_class,
            status=status,
            status_class=status_class,
            status_detail=status_detail,
        )

    @app.route("/api/generate", methods=["POST"])
    def api_generate():
        """JSON API endpoint for programmatic access."""
        data = request.get_json(force=True)
        description = data.get("description", "")
        diff = data.get("diff", "")
        title = data.get("title", "")

        if not description.strip():
            return jsonify({"error": "description is required"}), 400

        vt_result = generate_vt_statement(description, diff, title)
        return jsonify({
            "markdown": vt_result.markdown,
            "json": vt_result.as_json,
            "confidence": vt_result.overall_confidence,
            "status": vt_result.vt_statement.status if vt_result.vt_statement else "UNKNOWN",
        })

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)
