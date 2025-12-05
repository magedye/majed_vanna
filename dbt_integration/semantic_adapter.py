import yaml
from pathlib import Path
from typing import List, Tuple


class SemanticContextLoader:
    def __init__(self, config_path: Path = Path(__file__).parent.absolute() / "config.yaml"):
        self.config_path = Path(config_path)
        self.base_path = self.config_path.parent.absolute()
        self.config = self._load_config()
        self.sources = self._resolve_sources()
        self.context_limit = int(self.config.get("semantic_context_limit", 6000))
        print(f"[DEBUG] Semantic Base Path = {self.base_path}")

    def _load_config(self) -> dict:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _resolve_sources(self) -> List[Path]:
        configured = self.config.get("semantic_sources") or []
        paths: List[Path] = []
        if configured:
            for p in configured:
                candidate = Path(p)
                if not candidate.is_absolute():
                    candidate = (self.base_path / p).resolve()
                if candidate.exists():
                    paths.append(candidate)
        else:
            paths = list(self.base_path.glob("*.md"))
        # deterministic with ready_files first
        paths = sorted(paths, key=lambda p: 0 if p.name == "ready_files.md" else 1)
        print(f"[DEBUG] Files Found = {[p.name for p in paths]}")
        return paths

    def load_sections(self) -> List[Tuple[str, str]]:
        sections: List[Tuple[str, str]] = []
        for path in self.sources:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                sections.append((path.name, text))
            except Exception:
                continue
        return sections

    def build_context(self) -> str:
        combined_parts = []
        for name, content in self.load_sections():
            if content.strip():
                combined_parts.append(f"# Source: {name}\n{content.strip()}\n")
        # Ensure ready_files is explicitly included if exists
        ready = self.base_path / "ready_files.md"
        if not ready.exists():
            raise FileNotFoundError(f"ready_files.md missing at: {ready}")
        ready_text = ready.read_text(encoding="utf-8", errors="ignore").strip()
        if ready_text:
            combined_parts.append(f"# Source: ready_files.md\n{ready_text}\n")
        combined = "\n\n".join(combined_parts).strip()
        if not combined:
            raise RuntimeError("Semantic context is empty — no content loaded from Markdown sources.")
        if len(combined) > self.context_limit:
            combined = combined[: self.context_limit]
        return combined


semantic_loader = SemanticContextLoader()
