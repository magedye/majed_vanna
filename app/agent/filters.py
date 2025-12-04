import re
from typing import List

from vanna.core.filter import ConversationFilter
from vanna.core.storage.models import Message


class SensitiveDataFilter(ConversationFilter):
    async def filter_messages(self, msgs: List[Message]) -> List[Message]:
        for m in msgs:
            if m.content:
                m.content = m.content.replace("password", "[REDACTED]")
        return msgs


class PromptSafetyFilter(ConversationFilter):
    """Phase 1.C: block meta-instruction / prompt-injection patterns before LLM."""

    BLOCK_PATTERNS = [
        re.compile(r"(?i)\bignore\b.+\binstruction"),
        re.compile(r"(?i)\byou are (now )?the (system|developer|assistant)\b"),
        re.compile(r"(?i)\bpretend to be\b"),
        re.compile(r"(?i)\bdo not follow the above\b"),
        re.compile(r"(?i)\bchange your role\b"),
        re.compile(r"(?i)\bdisable (safety|guardrails|filters)\b"),
        re.compile(r"(?i)\b(write|return|show) (the )?raw sql\b"),
        re.compile(r"(?i)\b(drop|truncate|alter)\s+table\b"),
    ]
    CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
    MAX_LEN = 4000

    async def filter_messages(self, msgs: List[Message]) -> List[Message]:
        if not msgs:
            return msgs

        latest = msgs[-1]
        if latest.role != "user" or not latest.content:
            return msgs

        content = latest.content.strip()
        if len(content) > self.MAX_LEN:
            raise ValueError("Prompt blocked: message too long")

        for pattern in self.BLOCK_PATTERNS:
            if pattern.search(content):
                raise ValueError("Prompt blocked by safety filter")

        sanitized = self.CONTROL_CHARS.sub(" ", content)
        sanitized = re.sub(r"\s+", " ", sanitized).strip()
        latest.content = sanitized
        return msgs


# Conversation filters are loaded by the agent in builder.py; PromptSafetyFilter enforces Phase 1.C guardrails.
conversation_filters = [SensitiveDataFilter(), PromptSafetyFilter()]
