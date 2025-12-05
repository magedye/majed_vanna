from pathlib import Path
from dbt_integration.doc_generator import SemanticDocGenerator


def test_doc_generator_build_outputs():
    gen = SemanticDocGenerator()
    result = gen.build()
    outputs = result.get("outputs", {})
    # Verify files written
    md_path = Path(outputs.get("md", ""))
    html_path = Path(outputs.get("html", ""))
    json_path = Path(outputs.get("json", ""))
    assert md_path.exists()
    assert html_path.exists()
    assert json_path.exists()
    # Content should not be empty and should include ready_files content
    content = result.get("content", "")
    assert content
    assert "ready_files" in content or "ready_files.md" in content
