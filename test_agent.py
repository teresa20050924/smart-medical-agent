from app.agents.multi_agent import create_medical_agent_system
from langchain_core.messages import HumanMessage
from app.agents.memory import get_user_long_memory
import time

def main():
    print("正在启动智能体...")
    graph = create_medical_agent_system()
    
    # 第一次会话：告诉系统个人信息
    config_a = {"configurable": {"user_id": "user_test_01", "thread_id": "thread_001"}}
    
    print("\n--- 第一步：告诉 AI 个人信息 ---")
    state1 = {
        "messages": [HumanMessage(content="你好，我叫王大明，我对头孢类药物过敏。")],
        "user_id": "user_test_01",
        "thread_id": "thread_001",
        "medical_documents": [],
        "next": None
    }
    result1 = graph.invoke(state1, config=config_a)
    print("AI回复：", result1["messages"][-1].content)
    
    time.sleep(1) # 等待数据库写入完成
    
    print("\n--- 第二步：直接查库，看是否写入成功 ---")
    memory_text = get_user_long_memory("user_test_01")
    print("数据库里存下的用户信息：\n", memory_text)
    
    # 第二次会话（新开 thread_002，证明跨会话记忆不丢失）
    config_b = {"configurable": {"user_id": "user_test_01", "thread_id": "thread_002"}}
    
    print("\n--- 第三步：新开一个会话，看 AI 是否记得 ---")
    state2 = {
        "messages": [HumanMessage(content="你好，我头有点痛，可以吃点什么药？")],
        "user_id": "user_test_01",
        "thread_id": "thread_002",
        "medical_documents": [],
        "next": None
    }
    result2 = graph.invoke(state2, config=config_b)
    print("AI回复：", result2["messages"][-1].content)

if __name__ == "__main__":
    main()