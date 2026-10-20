import os


class Config:
    # LLM su Groq (compatibile con il client OpenAI)
    LLM_MODEL = "openai/gpt-oss-120b"
    LLM_MODEL_LOW = "openai/gpt-oss-120b"
    AI_API_URL = "https://api.groq.com/openai/v1"
    AI_API_KEY = os.environ["GROQ_API_KEY"]