from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agents.multi_agent import create_medical_agent_system
import uuid

app = FastAPI(title="智能问诊 AI 客服系统")

# 允许跨域，方便前端调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 Agent 图（全局只加载一次，提高响应速度）
graph = create_medical_agent_system()

# 请求体格式
class ChatRequest(BaseModel):
    message: str
    user_id: str
    thread_id: str = None

@app.get("/")
def read_root():
    return {"status": "ok", "message": "医疗 Agent 后端已启动"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # 如果没有传 thread_id，就生成一个新的
        thread_id = request.thread_id or str(uuid.uuid4())
        
        config = {
            "configurable": {
                "user_id": request.user_id,
                "thread_id": thread_id
            }
        }
        
        state = {
            "messages": [HumanMessage(content=request.message)],
            "user_id": request.user_id,
            "thread_id": thread_id,
            "medical_documents": [],
            "next": None
        }
        
        # 运行 Agent
        result = graph.invoke(state, config=config)
        
        # 提取 AI 回复
        ai_response = result["messages"][-1].content
        
        return {
            "success": True, 
            "reply": ai_response,
            "thread_id": thread_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    # 优先读取云端分配的端口，如果没有就用 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)