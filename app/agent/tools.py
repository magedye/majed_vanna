import asyncio
import hashlib
import json
import os
import time
from pathlib import Path

from vanna.core.registry import ToolRegistry
from vanna.integrations.local import LocalFileSystem
from vanna.components import UiComponent
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool,
    SaveTextMemoryTool,
)
from vanna.tools import VisualizeDataTool
from app.agent.db import db_tool
import requests


def _safe_chart_tool():
    base_dir = Path(__file__).resolve().parent.parent / "static" / "charts"
    base_dir.mkdir(parents=True, exist_ok=True)

    class SafeVisualizer(VisualizeDataTool):
        def __init__(self):
            super().__init__(file_system=LocalFileSystem(working_directory=str(base_dir)))
            self.base_path = base_dir

        @staticmethod
        def _user_hash(context) -> str:
            user_id = getattr(getattr(context, "user", None), "id", "anonymous")
            return hashlib.sha256(user_id.encode()).hexdigest()[:16]

        def _sanitize_filename(self, filename: str) -> str:
            print(f"[DEBUG] Sanitizing filename: {filename}")
            name = os.path.basename(filename)
            name = name.replace("..", "").replace("/", "").replace("\\", "")
            return name

        def _ensure_user_dir(self, context):
            user_hash = self._user_hash(context)
            target_dir = self.base_path / user_hash
            target_dir.mkdir(parents=True, exist_ok=True)
            return target_dir, user_hash

        async def write_file(self, filename: str, content: str, context, overwrite: bool = True):
            safe_name = self._sanitize_filename(filename)
            target_dir, user_hash = self._ensure_user_dir(context)
            target = target_dir / safe_name
            print(f"[DEBUG] SafeVisualizer writing to: {target}")
            target.write_text(content, encoding="utf-8")
            return str(target)

        async def execute(self, context, args):
            # Run the default visualization, then persist the chart payload to sandboxed storage
            result = await super().execute(context, args)
            try:
                chart_dict = (result.metadata or {}).get("chart")
                if result.success and chart_dict:
                    filename = self._sanitize_filename(f"chart_{int(time.time())}.json")
                    chart_path = await self.write_file(
                        filename, json.dumps(chart_dict), context, overwrite=True
                    )
                    user_hash = self._user_hash(context)
                    chart_url = f"/charts/{user_hash}/{filename}"
                    result.metadata["chart_file"] = chart_path
                    result.metadata["chart_url"] = chart_url
                    result.result_for_llm = (
                        f"{result.result_for_llm} Chart saved to {chart_path} (url: {chart_url})."
                    )
                    if getattr(result, "ui_component", None) and getattr(
                        result.ui_component, "simple_component", None
                    ):
                        result.ui_component.simple_component.text = result.result_for_llm
            except Exception as exc:
                print(f"[DEBUG] SafeVisualizer failed to persist chart: {exc}")
            return result

    return SafeVisualizer()


visualizer = _safe_chart_tool()

tool_registry = ToolRegistry()
tool_registry.register_local_tool(db_tool, access_groups=["admin", "user"])
tool_registry.register_local_tool(visualizer, access_groups=["admin", "user"])
tool_registry.register_local_tool(SaveQuestionToolArgsTool(), access_groups=["admin"])
tool_registry.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=["admin", "user"])
tool_registry.register_local_tool(SaveTextMemoryTool(), access_groups=["admin", "user"])


class MemoryManagementTool:
    name = "MemoryManagementTool"
    description = "UI tool to reset or back up Vanna's memory."

    async def run(self, args, context):
        return UiComponent(
            type="form",
            title="Memory Manager",
            fields=[
                {"name": "action", "type": "select", "options": ["Backup", "Reset"]},
                {"name": "force", "type": "checkbox", "label": "Force Reset?"},
            ],
            submit_label="Execute",
            endpoint="/api/system/execute-memory-op",
        )


memory_tool = MemoryManagementTool()
tool_registry.register_local_tool(memory_tool, access_groups=["admin"])
