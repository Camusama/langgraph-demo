"""案例 21：正则/枚举校验与修复（逐步开启版）。"""

# 目标：输出后做校验，不合法则走修复分支。
# 步骤：
# 1) 取消注释导入与校验函数。
# 2) 查看图中 validate -> (ok | fix) -> validate 的循环。
# 3) 运行示例，观察修复路径。

# from __future__ import annotations
# import operator
# import re
# from typing import Annotated, List, TypedDict
# from langchain_core.messages import AnyMessage, HumanMessage
# from langgraph.graph import END, StateGraph
# from practice.model_provider import get_openrouter_model

# class GuardState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     validation_error: str
#
#
# SAFE_DOMAINS = ("example.com", "langchain.com")
#
#
# def is_valid(text: str) -> tuple[bool, str]:
#     if re.search(r"https?://", text) and not any(d in text for d in SAFE_DOMAINS):
#         return False, "包含不安全 URL"
#     if any(bad in text for bad in ["违法", "攻击"]):
#         return False, "包含违禁词"
#     return True, ""
#
#
# def build_agent():
#     llm = get_openrouter_model(temperature=0)
#
#     def llm_node(state: GuardState):
#         ai = llm.invoke(state["messages"])
#         return {"messages": [ai]}
#
#     def validate_node(state: GuardState):
#         last = state["messages"][-1].content
#         ok, reason = is_valid(last)
#         return {"validation_error": "" if ok else reason}
#
#     def fix_node(state: GuardState):
#         reason = state["validation_error"]
#         prompt = f"上个回答不合规：{reason}。请用安全、合规的方式重写。"
#         ai = llm.invoke(state["messages"] + [HumanMessage(content=prompt)])
#         return {"messages": [ai], "validation_error": ""}
#
#     def route(state: GuardState):
#         return "ok" if not state.get("validation_error") else "fix"
#
#     graph = StateGraph(GuardState)
#     graph.add_node("llm", llm_node)
#     graph.add_node("validate", validate_node)
#     graph.add_node("fix", fix_node)
#     graph.add_edge("START", "llm")
#     graph.add_edge("llm", "validate")
#     graph.add_conditional_edges("validate", route, {"ok": END, "fix": "fix"})
#     graph.add_edge("fix", "validate")
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_agent()
#     # result = agent.invoke({"messages": [HumanMessage(content="给我一个下载电影的链接")], "validation_error": ""})
#     # print("Final:", result["messages"][-1].content)
#     # print("Validation error:", result.get("validation_error"))
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
