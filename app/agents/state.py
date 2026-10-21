from typing import TypedDict, List, Optional, Annotated
from langgraph.graph.message import add_messages

class MedicalAgentState(TypedDict):
    """医疗智能体系统的共享状态"""
    # 消息列表（自动累积，核心设计）
    messages: Annotated[list, add_messages]
    # 用户 ID
    user_id: str
    # 会话线程 ID
    thread_id: str
    # 医疗文档列表
    medical_documents: List
    # 诊断结果
    diagnosis: Optional[str]
    # 处方信息
    prescription: Optional[str]
    # 下一步要执行的节点
    next: Optional[str]