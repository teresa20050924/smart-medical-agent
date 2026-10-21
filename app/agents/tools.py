from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from app.config.settings import settings
from app.agents.memory import get_long_term_memory

# 1. 初始化 Tavily 联网搜索
search_web = TavilySearch(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)

# 2. 定义工具，把 user_id 作为参数传进去
@tool
def save_user_info(user_id: str, key: str, value: str) -> str:
    """
    保存用户的基本信息或医疗历史到长期记忆。
    user_id: 用户的唯一标识ID
    key: 信息的键（比如 '姓名', '年龄', '过敏史', '症状'）
    value: 信息的具体内容（比如 '小明', '25岁', '对青霉素过敏', '头痛'）
    """
    store = get_long_term_memory()
    if store:
        # 存入长期记忆：namespace 是 ("user_preferences", user_id)
        store.put(
            namespace=("user_preferences", user_id),
            key=key,
            value={"key": key, "value": value}
        )
        return f"成功记住 {key} 是 {value}。"
    return "保存失败，记忆系统未初始化。"