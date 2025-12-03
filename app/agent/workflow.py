from vanna.core.workflow import WorkflowHandler, WorkflowResult
from vanna.components import RichTextComponent


class CommandWorkflowHandler(WorkflowHandler):
    async def try_handle(self, agent, user, conversation, message):
        if message == "/help":
            return WorkflowResult(
                should_skip_llm=True,
                components=[RichTextComponent(content="# Help Commands")],
            )

        return WorkflowResult(should_skip_llm=False)


workflow_handler = CommandWorkflowHandler()
