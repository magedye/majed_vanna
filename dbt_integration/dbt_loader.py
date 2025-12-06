import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class DbtNode:
    name: str
    resource_type: str
    database: str
    schema: str
    relation: str
    columns: Dict[str, str]
    description: str
    parents: List[str]
    children: List[str]


class DbtMetadataProvider:
    """Lightweight dbt artifact reader (manifest/catalog/run_results). Safe to call even if files are missing."""

    def __init__(
        self,
        manifest_path: Path,
        catalog_path: Optional[Path] = None,
        run_results_path: Optional[Path] = None,
        provider: str = "oracle",
        context_limit: int = 4000,
    ):
        self.manifest_path = manifest_path
        self.catalog_path = catalog_path
        self.run_results_path = run_results_path
        self.provider = provider.lower()
        self.context_limit = context_limit
        self.nodes: Dict[str, DbtNode] = {}

    def _load_json(self, path: Optional[Path]) -> dict:
        if not path or not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def load(self):
        manifest = self._load_json(self.manifest_path)
        catalog = self._load_json(self.catalog_path)
        catalog_cols = catalog.get("nodes", {})
        nodes = manifest.get("nodes", {})
        sources = manifest.get("sources", {})

        combined: Dict[str, dict] = {}
        combined.update(nodes)
        combined.update(sources)

        child_map: Dict[str, Set[str]] = {}
        for unique_id, node in combined.items():
            for parent in node.get("parents", []):
                child_map.setdefault(parent, set()).add(unique_id)

        for unique_id, node in combined.items():
            name = node.get("name") or unique_id.split(".")[-1]
            resource_type = node.get("resource_type", "")
            database = (node.get("database") or "").strip()
            schema = (node.get("schema") or "").strip()
            relation = self._normalize_relation(database, schema, name)
            description = node.get("description") or ""
            col_docs = {}
            cols = node.get("columns", {}) or {}
            cat_cols = catalog_cols.get(unique_id, {}).get("columns", {}) if catalog_cols else {}
            for cname, cmeta in cols.items():
                desc = cmeta.get("description") or ""
                if not desc and cat_cols:
                    desc = cat_cols.get(cname, {}).get("comment") or ""
                norm_cname = self._normalize_identifier(cname)
                col_docs[norm_cname] = desc
            parents = [self._normalize_unique_id(p) for p in node.get("parents", [])]
            children = [self._normalize_unique_id(c) for c in child_map.get(unique_id, [])]
            self.nodes[unique_id] = DbtNode(
                name=self._normalize_identifier(name),
                resource_type=resource_type,
                database=database,
                schema=schema,
                relation=relation,
                columns=col_docs,
                description=description,
                parents=parents,
                children=children,
            )

    def _normalize_identifier(self, ident: str) -> str:
        if self.provider == "oracle":
            return ident.upper()
        return ident.lower()

    def _normalize_relation(self, database: str, schema: str, name: str) -> str:
        parts = [p for p in [database, schema, name] if p]
        if not parts:
            return self._normalize_identifier(name)
        return ".".join(self._normalize_identifier(p) for p in parts)

    def _normalize_unique_id(self, uid: str) -> str:
        # dbt unique_id like model.project.my_table -> take tail
        tail = uid.split(".")[-1]
        return self._normalize_identifier(tail)

    def build_context(self) -> str:
        if not self.nodes:
            return ""
        lines: List[str] = []
        for node in self.nodes.values():
            if node.resource_type not in {"model", "source", "seed"}:
                continue
            lines.append(f"Table: {node.relation}")
            if node.description:
                lines.append(f"  Description: {node.description}")
            if node.columns:
                lines.append("  Columns:")
                for cname, desc in node.columns.items():
                    if desc:
                        lines.append(f"    - {cname}: {desc}")
            if node.parents:
                lines.append(f"  Parents: {', '.join(node.parents)}")
            if node.children:
                lines.append(f"  Children: {', '.join(node.children)}")
            lines.append("")
        ctx = "\n".join(lines).strip()
        if len(ctx) > self.context_limit:
            ctx = ctx[: self.context_limit]
        return ctx

    def health(self) -> Dict[str, bool]:
        return {
            "manifest_present": self.manifest_path.exists(),
            "catalog_present": bool(self.catalog_path and self.catalog_path.exists()),
            "run_results_present": bool(self.run_results_path and self.run_results_path.exists()),
            "nodes_loaded": bool(self.nodes),
        }
