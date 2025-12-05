import json
import re
from pathlib import Path
from typing import List, Dict, Any

import markdown
import yaml


class SemanticDocGenerator:
    def __init__(self, config_path: Path = Path(__file__).parent.absolute() / "config.yaml"):
        self.config_path = Path(config_path)
        self.base_path = self.config_path.parent.absolute()
        self.config = self._load_config()
        self.output_path = Path(self.config.get("documentation_output_path", self.base_path / "docs"))
        self.formats = self.config.get("documentation_formats", ["md", "html", "json"])
        self.output_path.mkdir(parents=True, exist_ok=True)
        print(f"[DEBUG] Semantic Base Path = {self.base_path}")

    def _load_config(self) -> dict:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _build_toc(self, md_text: str) -> List[Dict[str, Any]]:
        toc: List[Dict[str, Any]] = []
        for line in md_text.splitlines():
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                title = line.lstrip("#").strip()
                anchor = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()
                toc.append({"level": level, "title": title, "anchor": anchor})
        return toc

    def _load_markdown_content(self) -> str:
        required_sources = [
            "ready_files.md",
            "code_implementation_package.md",
            "documentation_index.md",
            "quick_start_guide.md",
            "short_summary.md",
            "semantic_layer_final_plan.md",
            "vana_cbtcore.md",
        ]

        content_parts: List[str] = []

        # deterministic file discovery + ready_files first
        files = sorted(self.base_path.glob("*.md"), key=lambda p: 0 if p.name == "ready_files.md" else 1)
        print(f"[DEBUG] Files Found = {[p.name for p in files]}")

        for filename in required_sources:
            path = self.base_path / filename
            if path.exists():
                text = path.read_text(encoding="utf-8")
                if text.strip():
                    content_parts.append(f"# Source: {filename}\n{text.strip()}")
                else:
                    print(f"[WARNING] Empty content in: {filename}")
            else:
                print(f"[WARNING] Missing expected source: {filename}")

        content = "\n\n".join(content_parts).strip()
        if not content:
            # Fallback: attempt to merge whatever was discovered
            for p in files:
                try:
                    t = p.read_text(encoding="utf-8")
                    if t.strip():
                        content_parts.append(f"# Source: {p.name}\n{t.strip()}")
                except Exception:
                    continue
            content = "\n\n".join(content_parts).strip()

        if not content.strip():
            raise ValueError("DocGenerator: merged content is empty; markdown sources not loaded correctly.")

        return content

    def build(self) -> Dict[str, Any]:
        combined_md = self._load_markdown_content()
        toc = self._build_toc(combined_md) if combined_md else []

        outputs = {}
        if "md" in self.formats:
            md_path = self.output_path / "semantic_docs.md"
            md_path.write_text(combined_md, encoding="utf-8")
            outputs["md"] = str(md_path)
        if "html" in self.formats:
            html_path = self.output_path / "semantic_docs.html"
            html = markdown.markdown(combined_md, extensions=["toc", "fenced_code"])
            html_path.write_text(html, encoding="utf-8")
            outputs["html"] = str(html_path)
        if "json" in self.formats:
            json_path = self.output_path / "semantic_docs.json"
            json_path.write_text(
                json.dumps({"toc": toc, "content": combined_md}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            outputs["json"] = str(json_path)

        return {"toc": toc, "outputs": outputs, "content": combined_md}

    def preview(self) -> str:
        return self.build().get("content", "")

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        results: List[Dict[str, str]] = []
        for line in (self.build().get("content") or "").splitlines():
            if query_lower in line.lower():
                results.append({"match": line.strip()})
                if len(results) >= max_results:
                    break
        return results
