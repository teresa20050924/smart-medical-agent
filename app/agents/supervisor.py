from langchain_core.messages import SystemMessage, AIMessage
from app.agents.state import MedicalAgentState
from app.agents.llm_setup import get_model
from app.agents.tools import search_web, save_user_info
from langchain.agents import create_agent
from app.agents.memory import get_user_long_memory
import re # 引入正则

def supervisor_node(state: MedicalAgentState):
    model = get_model()
    messages = state["messages"]
    user_id = state["user_id"]
    
    # ===== 新增：Python 层面硬核拦截并保存 =====
    last_user_msg = messages[-1].content if messages else ""
    
    # 提取姓名
    name_match = re.search(r"我叫([^\s，。]+)", last_user_msg)
    if name_match:
        name = name_match.group(1)
        save_user_info.invoke({"user_id": user_id, "key": "姓名", "value": name})
        print(f"[系统拦截] 已提取并保存姓名: {name}")
        
    # 提取过敏史
    allergy_match = re.search(r"对([^\s，。]+)过敏", last_user_msg)
    if allergy_match:
        allergy = allergy_match.group(1)
        save_user_info.invoke({"user_id": user_id, "key": "过敏史", "value": allergy})
        print(f"[系统拦截] 已提取并保存过敏史: {allergy}")
    # ========================================

    # 1. 读取长期记忆
    memory_text = get_user_long_memory(user_id)
    if memory_text:
        print(f"[长期记忆] 已读取到用户信息:\n{memory_text}")
    
    # 2. 路由决策
    route_prompt = """你是一个私人医疗顾问，负责导诊。
    如果用户询问药品相关问题，请回复 'pharmacist'；
    如果是医疗咨询/症状，请回复 'attending_doctor'；
    如果是打招呼/闲聊/告诉你基本信息，请回复 'supervisor'。
    你只能回复一个单词，不要包含其他内容。"""
    
    if memory_text:
        route_prompt += f"\n\n用户的历史信息：\n{memory_text}"
        
    route_messages = [SystemMessage(content=route_prompt)] + messages
    route_response = model.invoke(route_messages)
    route_text = route_response.content.strip().lower()
    
    next_node = "supervisor"
    if "pharmacist" in route_text:
        next_node = "pharmacist"
    elif "attending_doctor" in route_text:
        next_node = "attending_doctor"
        
    print(f"[路由决策] 模型决定下一步: {next_node}")
    
    if next_node != "supervisor":
        return {"next": next_node}
        
    # 3. 自己处理（闲聊 / 收集信息）
    print("[私人顾问] 正在处理闲聊/导诊...")
    
    system_prompt = f"""你是一个友好的私人医疗顾问。当前用户的 user_id 是：{user_id}。
用户的历史记忆信息如下：
{memory_text if memory_text else "暂无历史信息"}

如果用户只是闲聊，你可以结合历史信息正常回复。"""
    
    agent = create_agent(
        model=model,
        tools=[search_web], # 工具列表里直接去掉 save_user_info，不让大模型调了，我们自己管
        system_prompt=system_prompt
    )
    
    response = agent.invoke({"messages": messages})
    
    final_message = response["messages"][-1]
    final_message.content = "【私人医疗顾问】\n" + final_message.content
    
    return {
        "messages": [final_message],
        "next": "__end__"
    }