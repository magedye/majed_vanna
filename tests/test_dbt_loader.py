import json
from pathlib import Path

from dbt_integration.dbt_loader import DbtMetadataProvider


def test_missing_artifacts_does_not_crash(tmp_path: Path):
    provider = DbtMetadataProvider(
        manifest_path=tmp_path / "manifest.json",
        catalog_path=tmp_path / "catalog.json",
        run_results_path=tmp_path / "run_results.json",
        provider="oracle",
        context_limit=1000,
    )
    provider.load()  # should not raise
    ctx = provider.build_context()
    assert ctx == ""


def test_basic_parse(tmp_path: Path):
    manifest = {
        "nodes": {
            "model.proj.orders": {
                "name": "orders",
                "resource_type": "model",
                "database": "DB",
                "schema": "ANALYTICS",
                "description": "Orders fact",
                "columns": {"order_id": {"description": "PK"}, "amount": {"description": "Value"}},
                "parents": [],
            }
        }
    }
    catalog = {
        "nodes": {
            "model.proj.orders": {
                "columns": {"order_id": {"comment": "PK"}, "amount": {"comment": "Value SAR"}}
            }
        }
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (tmp_path / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

    provider = DbtMetadataProvider(
        manifest_path=tmp_path / "manifest.json",
        catalog_path=tmp_path / "catalog.json",
        provider="oracle",
        context_limit=500,
    )
    provider.load()
    ctx = provider.build_context()
    assert "ORDERS" in ctx
    assert "ORDER_ID" in ctx
    assert "Orders fact" in ctx
