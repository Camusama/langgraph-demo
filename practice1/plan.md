# LangGraph + LangChain 进阶计划（practice1：RAG + 内置工具）

目标：在基础 practice 的节点/循环/记忆掌握后，聚焦 RAG 记忆与 LangChain 内置工具的组合，技术栈参考「langmanus」：LangGraph + LangChain (LCEL) + 内置工具 + 矢量库（Chroma/FAISS 均可）+ OpenRouter/OpenAI 嵌入 + LangSmith 可选。

通用约定

- 目录：`practice1/`，文件名继续累加案例序号，如 `case07_*`.py，保证后续 practice2/3/4 还能渐进。
- 运行：`uv run python practice1/<file>.py`。复用 `practice/model_provider.py`，或在本目录创建轻量封装。
- 数据：优先用本地 Markdown/MDX 片段（可取仓库 README 或开源协议文档），便于可复现实验。

## 案例梯度

### case07_build_vectorstore（RAG 数据入门）

- 加载若干本地文档（`TextLoader` / `DirectoryLoader`），分段（`RecursiveCharacterTextSplitter`），嵌入（`OpenAIEmbeddings` 或 `VoyageEmbeddings`），存入 `Chroma` 或 `FAISS`。
- 写一个最小检索函数：给 query 返回前 k 条 `Document`，并打印 score、metadata，验证中文检索效果。

### case08_rag_graph_baseline（检索 + 答复）

- State 设计：`messages`（累加）+ `context`（list[Document]）+ `query`（最后一条用户问题）。
- 节点：`retrieve_node`（调用向量库）-> `answer_node`（把检索结果填入系统模板生成回答+引用）；结构：`START -> retrieve -> answer -> END`。
- 目标：跑通一次问答，输出回答 + 引用的 source ids。

### case09_memory_persistence（记忆与摘要）

- 在 case08 基础上加入 LangGraph `MemorySaver` 或 `SqliteSaver`，让对话轮次跨 run 保持；状态新增 `turns`。
- 增加 `summarize_node`：当历史消息超阈值时，将旧消息摘要并缩减上下文，演示“长对话+RAG”的内存管理。

### case10_tool_augmented_rag（内置工具融合）

- 引入 LangChain 内置工具（与 langmanus 常用栈对齐）：`TavilySearchResults`（联网搜索）、`llm_math` 或 `PythonREPLTool`（计算）、`RequestsGet`（HTTP 拉取）。
- 图：`llm_router` 产生 `tool_calls`；`tool_node` 执行；有检索需求时仍走 `retrieve_node`。形成“RAG + WebSearch + 计算”三路循环，观察工具调用消息格式。

### case11_router_rag_vs_tools（决策与兜底）

- 设计路由：当问题可用本地知识库直接回答 -> RAG；若检索相似度低或包含“最新/今天/价格”等关键词 -> Tavily；数学/统计问题 -> 计算工具；否则进入兜底回答。
- 通过 `add_conditional_edges` 实现分支，打印路由判定信息，确保可读性与可维护性。

### case12_eval_and_observe（可选：观测与轻量评估）

- 集成 `langsmith`（可选）记录 run，或者使用 `agent.stream` + mermaid 可视化查看执行路径。
- 对 case10/11 的回答做两个微型指标：是否包含 citation（source 标号）、是否拒答兜底正确；可写简单断言或用 LLM-as-judge 打分脚本。

完成 practice1 后可进入 practice2（多 Agent / 计划执行）、practice3（函数调用/结构化输出/Guardrails）、practice4（部署与成本优化）。保持每个案例独立且可复现，便于回顾与拆分迁移。
