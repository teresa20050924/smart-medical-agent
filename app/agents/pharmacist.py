from app.agents.state import MedicalAgentState
from app.agents.llm_setup import get_model
from app.agents.memory import get_user_long_memory
from langchain_core.messages import SystemMessage

def pharmacist_node(state: MedicalAgentState):
    model = get_model()
    user_id = state["user_id"]
    
    # 读取长期记忆
    memory_text = get_user_long_memory(user_id)
    
    # 严苛的系统提示词
    if memory_text:
        system_prompt = f"""你是一名专业的药师。
【患者历史背景】：
{memory_text}

🚨 最高警告：患者有以上背景记录。如果在推荐用药时，你发现患者对某种药物过敏，你必须立刻停止推荐该药，并且用最醒目的方式警告患者！
请提供安全的用药指导。"""
    else:
        system_prompt = "你是一名专业的药师。请提供用药指导，并仔细询问患者是否有过敏史。"

    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = model.invoke(messages)
    response.content = "【药师】\n" + response.content
    return {"messages": [response]}