import os
from pathlib import Path

import asyncio

from app.agent.tools import visualizer


def test_sanitize_filename():
    cases = {
        "../../evil.png": "evil.png",
        "..\\..\\test.html": "test.html",
        "/etc/passwd": "passwd",
    }
    for raw, expected in cases.items():
        assert visualizer._sanitize_filename(raw) == expected


def test_write_file_creates_in_sandbox(tmp_path, monkeypatch):
    # Point sandbox to a temp directory
    monkeypatch.setattr(visualizer, "base_path", tmp_path)

    content = "<html><body>OK</body></html>"
    # context with a fake user_id to force hashed folder
    class Ctx:
        def __init__(self):
            class U:
                id = "user123"
            self.user = U()

    ctx = Ctx()

    # Run
    visualizer._ensure_user_dir(ctx)
    path_str = asyncio.run(visualizer.write_file("chart.html", content, ctx))
    file_path = Path(path_str)

    # Assert file exists under hashed user folder
    assert file_path.exists()
    assert file_path.is_file()
    assert "chart.html" == file_path.name
    # Ensure the parent is inside sandbox
    assert str(file_path).startswith(str(tmp_path))
    # Content check
    assert file_path.read_text() == content
