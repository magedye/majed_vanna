from app.config import LLM_PROVIDER, LLM_CONFIG
from vanna.integrations.openai import OpenAILlmService

def get_llm():
    cfg=LLM_CONFIG[LLM_PROVIDER]
    if LLM_PROVIDER=="lmstudio":
        return OpenAILlmService(model=cfg["model"], base_url=cfg["base_url"], api_key=cfg["api_key"])
    if LLM_PROVIDER=="openai":
        return OpenAILlmService(model=cfg["model"], api_key=cfg["api_key"])
    if LLM_PROVIDER=="groq":
        return OpenAILlmService(model=cfg["model"], api_key=cfg["api_key"], base_url="https://api.groq.com/openai/v1")
    if LLM_PROVIDER=="gemini":
        return OpenAILlmService(model=cfg["model"], api_key=cfg["api_key"], base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm=get_llm()
