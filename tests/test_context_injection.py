import pytest
import asyncio
from types import SimpleNamespace

from app.agent import builder


@pytest.fixture(autouse=True)
def patch_perf_logger(monkeypatch):
    logs = []

    def fake_log(logger, event, data):
        logs.append((event, data))

    monkeypatch.setattr(builder, "log_perf", fake_log)
    return logs


def make_request(message, role="user"):
    msg = SimpleNamespace(role=role, content=message)
    return SimpleNamespace(messages=[msg], metadata={})


def test_injection_appends_schema(monkeypatch, patch_perf_logger):
    # Mock schema DDL
    ddl = "CREATE TABLE sales_data(id INT, product TEXT);"
    class FakeDF:
        empty = False
        columns = ["type", "text"]

        def __getitem__(self, key):
            return self

        def __eq__(self, other):
            return self

        def dropna(self):
            return self

        def tolist(self):
            return [ddl]

        def __iter__(self):
            return iter([ddl])

    fake_df = FakeDF()
    monkeypatch.setattr(builder, "knowledge_base", SimpleNamespace(get_training_data=lambda: fake_df))

    req = make_request("What are the top 5 records?")
    mw = builder.LLMLog()

    # Run before_llm_request
    asyncio.run(mw.before_llm_request(req))

    updated = req.messages[-1].content
    assert "Use this schema" in updated
    assert ddl in updated
    # Logging captured
    assert any(event == "llm.prompt_size" for event, _ in patch_perf_logger)


def test_truncation_preserves_system(monkeypatch, patch_perf_logger):
    # Huge history + system prompt; ensure system survives
    ddl = "CREATE TABLE sales_data(id INT, product TEXT);" * 500  # very long
    class FakeDF:
        empty = False
        columns = ["type", "text"]

        def __getitem__(self, key):
            return self

        def dropna(self):
            return self

        def to_list(self):
            return [ddl]

        def __iter__(self):
            return iter([ddl])

    fake_df = FakeDF()
    monkeypatch.setattr(builder, "knowledge_base", SimpleNamespace(get_training_data=lambda: fake_df))

    system_msg = SimpleNamespace(role="system", content="SYSTEM")
    long_history = SimpleNamespace(role="user", content="x" * 20000)
    req = SimpleNamespace(messages=[system_msg, long_history], metadata={})

    mw = builder.LLMLog()
    asyncio.run(mw.before_llm_request(req))

    # System must remain intact
    assert req.messages[0].content == "SYSTEM"
    # History should be trimmed
    assert len(req.messages[-1].content) <= builder.LLM_MAX_PROMPT_CHARS
    # Logging captured
    assert any(event == "llm.prompt_size" for event, _ in patch_perf_logger)


def test_logging_structure(monkeypatch, patch_perf_logger):
    ddl = "CREATE TABLE t(id INT);"
    fake_df = SimpleNamespace(
        empty=False,
        columns=["type", "text"],
        __getitem__=lambda self, key: self,
        dropna=lambda self: self,
        to_list=lambda self: [ddl],
        __iter__=lambda self: iter([ddl]),
    )
    monkeypatch.setattr(builder, "knowledge_base", SimpleNamespace(get_training_data=lambda: fake_df))

    req = make_request("hi")
    mw = builder.LLMLog()
    asyncio.run(mw.before_llm_request(req))

    logged = [data for event, data in patch_perf_logger if event == "llm.prompt_size"]
    assert logged, "No prompt size log recorded"
    entry = logged[-1]
    assert "total_chars" in entry and "system_chars" in entry and "truncated" in entry
