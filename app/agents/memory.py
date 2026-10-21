from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from app.config.settings import settings

# 全局变量
short_term_pool = None
long_term_pool = None
short_term_memory = None  # PostgresSaver
long_term_memory = None   # PostgresStore

def init_memory_system():
    """初始化记忆系统（连接池模式）"""
    global short_term_pool, long_term_pool, short_term_memory, long_term_memory
    
    if short_term_memory is None:
        # 短记忆连接池（对话历史）
        short_term_pool = ConnectionPool(
            conninfo=settings.POSTGRES_SHORT_TERM_URL,
            min_size=2,
            max_size=10,
            kwargs={"autocommit": True, "prepare_threshold": 0}
        )
        short_term_memory = PostgresSaver(short_term_pool)
        short_term_memory.setup() # 自动建表
        
        # 长记忆连接池（用户信息）
        long_term_pool = ConnectionPool(
            conninfo=settings.POSTGRES_LONG_TERM_URL,
            min_size=2,
            max_size=10,
            kwargs={"autocommit": True, "prepare_threshold": 0}
        )
        long_term_memory = PostgresStore(long_term_pool)
        long_term_memory.setup() # 自动建表

def get_short_term_memory():
    if short_term_memory is None:
        init_memory_system()
    return short_term_memory

def get_long_term_memory():
    if long_term_memory is None:
        init_memory_system()
    return long_term_memory

def get_user_long_memory(user_id: str) -> str:
    """获取用户的长期记忆（个人信息、医疗历史等）"""
    store = get_long_term_memory()
    if not store:
        return ""
    
    user_info = []
    # 获取用户基本信息
    preferences = store.search(("user_preferences", user_id))
    if preferences:
        # 过滤掉重复的 key
        pref_dict = {}
        for item in preferences:
            pref_dict[item.value.get('key')] = item.value.get('value')
            
        pref_text = "\n".join([f"{k}: {v}" for k, v in pref_dict.items()])
        user_info.append(pref_text)
        
    return "\n".join(user_info) if user_info else ""