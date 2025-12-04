import json
from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException

BASE_DIR = Path(__file__).resolve().parents[2]
METADATA_DIR = BASE_DIR / "metadata"

router = APIRouter()


def _load_json(name: str):
    path = METADATA_DIR / name
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{name} not found")
    with path.open(encoding="utf-8") as fp:
        return json.load(fp)


def _load_yaml(name: str):
    path = METADATA_DIR / name
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{name} not found")
    with path.open(encoding="utf-8") as fp:
        return yaml.safe_load(fp)


@router.get("/metadata/tables")
def tables():
    return _load_json("tables.json")


@router.get("/metadata/columns")
def columns():
    return _load_json("columns.json")


@router.get("/metadata/relationships")
def relationships():
    return _load_json("relationships.json")


@router.get("/metadata/semantic_model")
def semantic_model():
    return _load_yaml("semantic_model.yaml")
