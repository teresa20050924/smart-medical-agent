import os
from dotenv import load_dotenv

# 加载根目录下的 .env 文件
load_dotenv()

class Settings:
    # 数据库配置
    MYSQL_URL: str = os.getenv("MYSQL_URL")
    POSTGRES_SHORT_TERM_URL: str = os.getenv("POSTGRES_SHORT_TERM_URL")
    POSTGRES_LONG_TERM_URL: str = os.getenv("POSTGRES_LONG_TERM_URL")
    POSTGRES_SESSION_URL: str = os.getenv("POSTGRES_SESSION_URL")
    
    # API 密钥
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

settings = Settings()