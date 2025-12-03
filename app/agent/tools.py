from vanna.core.registry import ToolRegistry
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool, SaveTextMemoryTool
from app.agent.db import db_tool, visualizer

tool_registry=ToolRegistry()
tool_registry.register_local_tool(db_tool, access_groups=["admin","user"])
tool_registry.register_local_tool(visualizer, access_groups=["admin","user"])
tool_registry.register_local_tool(SaveQuestionToolArgsTool(), access_groups=["admin"])
tool_registry.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=["admin","user"])
tool_registry.register_local_tool(SaveTextMemoryTool(), access_groups=["admin","user"])
