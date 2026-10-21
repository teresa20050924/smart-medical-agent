from langchain_openai import ChatOpenAI
from app.config.settings import settings

def get_model():
    """获取 DeepSeek 模型"""
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=settings.DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1",
        temperature=0.3
    )