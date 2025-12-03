from vanna.core.filter import ConversationFilter
class SensitiveDataFilter(ConversationFilter):
    async def filter_messages(self, msgs):
        for m in msgs:
            if m.content: m.content=m.content.replace("password","[REDACTED]")
        return msgs
conversation_filters=[SensitiveDataFilter()]
