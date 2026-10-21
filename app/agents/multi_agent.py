from langgraph.graph import StateGraph, END
from app.agents.state import MedicalAgentState
from app.agents.supervisor import supervisor_node
from app.agents.attending_doctor import attending_doctor_node
from app.agents.pharmacist import pharmacist_node

def create_medical_agent_system():
    """创建医疗智能体系统（暂不接数据库记忆）"""
    builder = StateGraph(MedicalAgentState)
    
    # 添加节点
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("attending_doctor", attending_doctor_node)
    builder.add_node("pharmacist", pharmacist_node)
    
    # 设置入口
    builder.set_entry_point("supervisor")
    
    # 条件路由
    builder.add_conditional_edges(
        "supervisor",
        lambda state: state.get("next", "__end__"),
        {
            "attending_doctor": "attending_doctor",
            "pharmacist": "pharmacist",
            "__end__": END
        }
    )
    
    # 子节点执行完直接结束
    builder.add_edge("attending_doctor", END)
    builder.add_edge("pharmacist", END)
    
    # 编译图（先不传 checkpointer）
    graph = builder.compile()
    return graph