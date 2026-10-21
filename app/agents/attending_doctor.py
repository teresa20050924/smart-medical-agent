from app.agents.state import MedicalAgentState
from app.agents.llm_setup import get_model
from app.agents.memory import get_user_long_memory
from langchain_core.messages import SystemMessage

def attending_doctor_node(state: MedicalAgentState):
    model = get_model()
    user_id = state["user_id"]
    
    # 读取长期记忆
    memory_text = get_user_long_memory(user_id)
    memory_prompt = f"\n【患者历史背景】：\n{memory_text}" if memory_text else ""
    
    # 注入到医生的系统提示词中
    system_prompt = f"你是一名专业的主治医生。请根据患者的描述提供医疗建议。{memory_prompt}\n注意：如果是处方药请建议就医。"
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = model.invoke(messages)
    response.content = "【主治医生】\n" + response.content
    return {"messages": [response]}