# 🏥 智能问诊 AI 多智能体客服系统

这是一个基于 LangChain 1.0 + LangGraph 构建的多智能体医疗问诊助手。通过自然语言交互，实现导诊、症状咨询、用药建议等功能。

## 🔗 在线体验 (Live Demo)
- **前端交互页面**：[点击这里体验](https://你的前端网址.onrender.com)
- **后端 API 文档**：[点击这里查看](https://你的后端网址.onrender.com/docs)

*(注：因部署在 Render 免费版，首次唤醒可能需要等待 30 秒左右)*

## ✨ 核心特性
- **多智能体协作**：中心辐射式架构。私人顾问（Supervisor）负责导诊路由，主治医生（Doctor）与药师（Pharmacist）负责专业解答。
- **双层记忆系统**：基于 PostgreSQL。短期记忆（PostgresSaver）实现会话级隔离；长期记忆（PostgresStore）实现跨会话记录用户姓名、过敏史等关键信息。
- **智能工具调用**：集成 Tavily 联网搜索；针对大模型“偷懒”不调用工具的问题，设计了 Python 正则拦截兜底策略。
- **全栈云端部署**：前端 Vue 3 + 后端 FastAPI + 数据库 Render PG，全程云端化。

## 🛠️ 技术栈
- **AI 框架**：LangChain, LangGraph
- **大模型**：DeepSeek API
- **后端**：FastAPI, SQLAlchemy, Uvicorn
- **数据库**：PostgreSQL (Render Cloud)
- **前端**：Vue 3 (CDN), HTML/CSS/JS

---
**⚠️ 免责声明**：本项目仅供技术交流与学习，AI 生成的医疗建议不能替代专业医生的面诊。