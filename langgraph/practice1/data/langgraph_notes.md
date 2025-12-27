# LangGraph 学习笔记
- LangGraph 使用 StateGraph 构建节点、边与条件分支，可形成循环。
- 状态本身就是内存，常见字段为 messages、turns、context。
- 可用 MemorySaver/SqliteSaver 持久化对话，支持恢复执行。
