# LangChain 工具提示
- LangChain 1.x 的工具需通过模型 bind_tools，再解析 tool_calls 执行。
- 常见工具：TavilySearchResults（联网）、PythonREPLTool（计算）、RequestsGetTool（拉取网页）。
- 工具返回 ToolMessage，携带 tool_call_id 以便模型继续推理。
