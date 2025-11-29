# LangGraph + LangChain 基础学习方案（渐进式案例）

目标：在 LangGraph 1.0 / LangChain 1.x 体系下，逐步理解“图式编排 + 语言模型 + 工具”的基础概念，并通过手把手的小案例动手实践。

- 预计时长：3–5 次碎片化学习，每次 40–60 分钟。
- 代码位置建议：每个案例新建一个脚本，例如 `practice/case01_*`.py，互不影响、便于回看。
- 环境：已安装 `langgraph>=1.0`、`langchain>=1.0`（本仓库 `pyproject.toml` 已满足）。运行命令统一用 `python <file>.py`。
- 模型默认：OpenRouter 的 `deepseek/deepseek-v3.2-exp`，`.env` 需设置 `OPENROUTER_API_KEY`（可选 `OPENROUTER_BASE_URL`），所有脚本通过 `practice/model_provider.py` 读取。

## 学习节奏与案例列表

### 0. 环境验证（5 分钟）
- 目的：确认模型、包版本和基础调用可用。
- 步骤：
  1) `uv run python - <<'PY'\nimport langchain, langgraph, sys\nprint(langchain.__version__, langgraph.__version__)\nPY`
  2) 在 `practice/` 下创建 `case00_ping.py`，调用一个最简单的 `print("ok")` 和 `from langchain.chat_models import init_chat_model` 看能否正常导入。

### 1. LangChain 消息与 ChatModel（不含图）（约 20 分钟）
- 目的：熟悉 LangChain 1.x 的消息对象、`init_chat_model`、基础调用。
- 操作：
  1) 新建 `practice/case01_basic_chat.py`。
  2) 使用 `init_chat_model("claude-...", temperature=0)` 初始化模型。
  3) 发送一条 `HumanMessage("你好，介绍一下 LangGraph 是什么？")`，打印返回的 `AIMessage`。
- 关注点：
  - LangChain 1.x 默认使用 LCEL（LangChain Expression Language）风格，模型调用 `invoke([...])` 返回消息。
  - 了解消息类型：`HumanMessage`、`AIMessage`，后续图里会用到。

### 2. 最小 LangGraph：单节点直线流（约 20 分钟）
- 目的：理解 `StateGraph`、节点、边、`compile()` 与 `invoke`。
- 操作：
  1) 新建 `practice/case02_min_graph.py`。
  2) 定义一个 `State`：`TypedDict` 包含 `messages: list[AnyMessage]`。
  3) 添加一个节点 `echo_node(state)`：返回原样消息或在前面加上一句固定回复。
  4) 图结构：`START -> echo_node -> END`，`compile()` 后 `agent.invoke({"messages": [HumanMessage(...)]})`。
- 关注点：
  - `StateGraph` 的类型安全：`Annotated[list[AnyMessage], operator.add]` 可叠加消息。
  - `agent.get_graph().draw_mermaid_png()` 可视化，用 `IPython.display` 查看。

### 3. LangChain 工具 + LangGraph 循环（约 30–40 分钟）
- 目的：把 LangChain 的工具（`@tool`）绑定到模型，借助图循环多轮调用。
- 操作（可参考仓库 `quickstart.py`，但尽量自己敲一遍）：
  1) 新建 `practice/case03_tools_agent.py`。
  2) 定义几个工具（如 `add/multiply/divide`），`tools = [add, ...]`，`model_with_tools = model.bind_tools(tools)`。
  3) 节点 `llm_call`：用 `model_with_tools.invoke(system + state["messages"])`，累积 `llm_calls` 计数。
  4) 节点 `tool_node`：遍历 `state["messages"][-1].tool_calls`，执行并返回 `ToolMessage`。
  5) 条件边 `should_continue`：有 `tool_calls` -> `tool_node`，否则 `END`；`tool_node -> llm_call` 形成循环。
  6) 运行：`agent.invoke({"messages": [HumanMessage("请计算 3*4+5")]})`，打印每条消息观察调用链。
- 关注点：
  - `tool_calls` 数据结构：`tool_call["name"]`、`tool_call["args"]`、`tool_call["id"]`。
  - LangGraph 的循环是通过边而不是 while 写死的逻辑。

### 4. 条件分支与错误兜底（约 25 分钟）
- 目的：学习 `add_conditional_edges` 的分支能力，增加“异常分支/兜底”。
- 操作：
  1) 基于 case03 复制为 `practice/case04_branching.py`。
  2) 添加一个 `route` 函数：如果用户提问与计算无关，则直接走 `respond_node` 给出说明；否则走工具链。
  3) 图示例：`START -> route -> (calc_flow | respond_node)`，其中 `calc_flow` 是 case03 的循环子图。
  4) 尝试两类输入：“加 2 和 3” 与 “写一首诗”，观察分支命中。
- 关注点：
  - 通过 `Literal["calc", "respond"]` 返回值映射到不同节点。
  - 保持状态合并：分支节点输出的 state 字段必须一致。

### 5. 状态与记忆（约 30 分钟）
- 目的：理解 LangGraph 的“状态即内存”思想，用 `Annotated` 合并策略管理对话历史。
- 操作：
  1) 新建 `practice/case05_memory.py`。
  2) `State` 中的 `messages: Annotated[list[AnyMessage], operator.add]` 会自动在节点间合并。
  3) 添加一个计数器字段 `turns: Annotated[int, operator.add]` 记录轮数，并在系统提示中使用。
  4) 运行多轮对话，观察 `turns` 如何累加、消息如何叠加。
- 关注点：
  - 了解合并策略：列表用 `operator.add` 叠加，标量可用 `max` / `min` / 自定义函数。
  - 记忆无需显式“存储器”对象，状态本身就是内存。

### 6. 可视化与调试（约 15 分钟）
- 目的：快速看清当前图的结构与执行轨迹。
- 操作：
  1) 在每个案例末尾调用 `agent.get_graph(xray=True).draw_mermaid_png()`，用 `IPython.display` 预览。
  2) 使用 `agent.stream(...)` 观察分步输出，体验 LangGraph 的流式执行。
  3) 若需要日志，添加简单的 `print("enter llm_call", state.keys())`，不要影响状态。
- 关注点：
  - `xray=True` 会把内部节点（如条件、工具调用）展示得更清晰，便于调试。

## 学完基础后的自然扩展（可择机继续）
- 事件驱动/中断恢复：使用 `checkpoints` 与存储后端。
- 多 Agent 协同：在图中组合多个 LLM 工作者。
- 部署：用 `langgraph-cli` 发布为 HTTP 服务或 CLI。

按照以上步骤完成后，你将对 LangGraph 的核心组成（StateGraph、节点/边、条件、循环、状态合并）与 LangChain 的模型/消息/工具有直观认知，并拥有若干可复用的最小案例脚本。祝学习顺利！
