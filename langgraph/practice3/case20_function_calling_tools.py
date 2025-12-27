"""案例 20：函数调用与工具对比（逐步开启版）。"""

# 步骤：
# 1) 取消注释导入与工具定义。
# 2) 取消图构建，观察 llm -> tool_node -> llm 循环。
# 3) 运行 main，查看 tool_calls 与 ToolMessage。

# from __future__ import annotations
# import operator
# from typing import Annotated, Dict, List, TypedDict
# from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, ToolMessage, SystemMessage
# from langgraph.graph import END, StateGraph
# from langchain_core.tools import tool
# from practice.model_provider import get_openrouter_model

# class ToolCallState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     calls: Annotated[List[str], operator.add]
#
#
# @tool
# def lookup_doc(doc_id: int) -> str:
#     """模拟查找文档。"""
#     return f"Doc {doc_id}: LangGraph basics..."
#
#
# @tool
# def calc(expr: str) -> str:
#     """计算表达式。"""
#     try:
#         return str(eval(expr))
#     except Exception as exc:
#         return f"error: {exc}"
#
#
# def build_agent():
#     tools = [lookup_doc, calc]
#     tool_map: Dict[str, object] = {t.name: t for t in tools}
#     llm = get_openrouter_model(temperature=0).bind_tools(tools)
#
#     def llm_node(state: ToolCallState):
#         ai = llm.invoke(state["messages"])
#         return {"messages": [ai]}
#
#     def tool_node(state: ToolCallState):
#         last = state["messages"][-1]
#         if not isinstance(last, AIMessage) or not last.tool_calls:
#             return {"messages": []}
#         tool_msgs: List[ToolMessage] = []
#         for call in last.tool_calls:
#             tool = tool_map[call["name"]]
#             result = tool.invoke(call.get("args", {}))
#             tool_msgs.append(ToolMessage(tool_call_id=call["id"], name=call["name"], content=str(result)))
#         return {"messages": tool_msgs, "calls": [call["name"] for call in last.tool_calls]}
#
#     def should_continue(state: ToolCallState):
#         last = state["messages"][-1]
#         return "tools" if getattr(last, "tool_calls", None) else "end"
#
#     graph = StateGraph(ToolCallState)
#     graph.add_node("llm", llm_node)
#     graph.add_node("tools", tool_node)
#     graph.add_edge("START", "llm")
#     graph.add_conditional_edges("llm", should_continue, {"tools": "tools", "end": END})
#     graph.add_edge("tools", "llm")
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_agent()
#     # result = agent.invoke({"messages": [HumanMessage(content="查一下文档 1，然后算 3*8")]})
#     # for m in result["messages"]:
#     #     print(f"- {m.__class__.__name__}: {getattr(m, 'content', '')}")
#     # print("tool calls:", result.get("calls"))
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
