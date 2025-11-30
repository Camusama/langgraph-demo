# LangGraph 进阶（practice4）：预构建 Agent 与 Command 边

聚焦 langgraph.prebuilt 的 `create_react_agent` 以及 `Command` 直接跳转写法，减少手工节点连线，快速构建多 Agent 协作流。

## 案例列表

### case25_react_single_agent
- 目标：用 `create_react_agent` 快速搭一个 ReAct Agent，工具仅保留本地可用的 Python 计算/echo，确保可运行。
- 看点：无需自建 tool_node，直接把工具传入 `create_react_agent`，`agent.invoke` 即可。

### case26_react_multi_agent
- 目标：用多组 `create_react_agent` 组合“research / coder”角色，示例性串联调用。
- 看点：不同 prompt + 工具集；复用 `get_llm_by_type` 思路，演示多 Agent 协作的最小骨架。

### case27_command_edges
- 目标：演示 `Command(next=...)` 写法，不用手工 `add_edge`，节点返回即指定下一个节点。
- 看点：StateGraph + Command；展示跳转与状态更新的直接方式。
