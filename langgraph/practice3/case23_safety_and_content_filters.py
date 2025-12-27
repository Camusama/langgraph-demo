"""案例 23：内容安全过滤与脱敏（逐步开启版）。"""

# 目标：对模型输出做安全检查，必要时遮盖或拒答。
# 步骤：
# 1) 取消注释导入与检测函数 detect_issues。
# 2) 取消图构建，观察 detect -> (sanitize|pass) 流程。
# 3) 运行示例，验证违规内容被改写或拒绝。

# from __future__ import annotations
# import operator
# from typing import Annotated, List, TypedDict
# from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
# from langgraph.graph import END, StateGraph
# from practice.model_provider import get_openrouter_model

# class SafetyState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     raw: str
#     sanitized: str
#     issues: List[str]
#
#
# def detect_issues(text: str) -> List[str]:
#     issues = []
#     if "密码" in text:
#         issues.append("敏感信息")
#     if "暴力" in text:
#         issues.append("暴力内容")
#     return issues
#
#
# def build_agent():
#     llm = get_openrouter_model(temperature=0)
#
#     def llm_node(state: SafetyState):
#         ai = llm.invoke(state["messages"])
#         return {"messages": [ai], "raw": ai.content}
#
#     def detect_node(state: SafetyState):
#         issues = detect_issues(state["raw"])
#         return {"issues": issues}
#
#     def sanitize_node(state: SafetyState):
#         sys = SystemMessage(content=f"上个回答存在问题：{state['issues']}。请用合规方式重写或拒答。")
#         ai = llm.invoke([sys, *state["messages"]])
#         return {"sanitized": ai.content, "messages": [ai], "issues": []}
#
#     def route(state: SafetyState):
#         return "pass" if not state.get("issues") else "sanitize"
#
#     graph = StateGraph(SafetyState)
#     graph.add_node("llm", llm_node)
#     graph.add_node("detect", detect_node)
#     graph.add_node("sanitize", sanitize_node)
#     graph.add_edge("START", "llm")
#     graph.add_edge("llm", "detect")
#     graph.add_conditional_edges("detect", route, {"pass": END, "sanitize": "sanitize"})
#     graph.add_edge("sanitize", END)
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_agent()
#     # result = agent.invoke({"messages": [HumanMessage(content="告诉我常用的密码字典有哪些？")], "issues": []})
#     # print("Raw:", result.get("raw"))
#     # print("Issues:", result.get("issues"))
#     # print("Sanitized:", result.get("sanitized"))
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
