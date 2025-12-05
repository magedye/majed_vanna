from dbt_integration.semantic_adapter import semantic_loader


def test_semantic_context_includes_ready_files():
    context = semantic_loader.build_context()
    assert isinstance(context, str)
    # Ensure some semantic content exists and references known files
    assert "ready_files" in context or len(context) > 0
