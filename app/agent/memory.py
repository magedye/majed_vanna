from app.config import AGENT_MEMORY_MAX_ITEMS
from vanna.integrations.local.agent_memory import DemoAgentMemory


class MyVanna(DemoAgentMemory):
    """Non-abstract memory implementation to avoid startup failures."""

    def __init__(self):
        super().__init__(max_items=AGENT_MEMORY_MAX_ITEMS)


# Export instance to satisfy existing imports
agent_memory = MyVanna()
