"""案例 13：双 Agent 对话（逐步开启版）。"""

# 逐步操作指南：
# 1) 取消注释导入与 build_expert / build_summarizer。
# 2) 取消注释 build_graph，查看 START -> expert -> summarizer -> END 的结构。
# 3) 在 main 中取消示例调用，观察消息传递。

# from __future__ import annotations
# import operator
# from typing import Annotated, List, TypedDict
# from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
# from langgraph.graph import END, StateGraph
# from practice.model_provider import get_openrouter_model

# class DualState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     notes: Annotated[List[str], operator.add]


# def build_expert():
#     return get_openrouter_model(temperature=0)
#
#
# def build_summarizer():
#     return get_openrouter_model(temperature=0)
#
#
# def build_graph():
#     expert = build_expert()
#     summarizer = build_summarizer()
#
#     def expert_node(state: DualState):
#         sys = SystemMessage(content="你是技术专家，请给出要点。")
#         ai = expert.invoke([sys, *state["messages"]])
#         return {"messages": [ai]}
#
#     def summarize_node(state: DualState):
#         sys = SystemMessage(content="你是总结员，用 3 句话总结上文。")
#         ai = summarizer.invoke([sys, *state["messages"]])
#         return {"messages": [ai], "notes": [ai.content]}
#
#     graph = StateGraph(DualState)
#     graph.add_node("expert", expert_node)
#     graph.add_node("summarizer", summarize_node)
#     graph.add_edge("START", "expert")
#     graph.add_edge("expert", "summarizer")
#     graph.add_edge("summarizer", END)
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_graph()
#     # result = agent.invoke({"messages": [HumanMessage(content="介绍一下 LangGraph 的状态模型")], "notes": []})
#     # print("Summary:", result["messages"][-1].content)
#     # print("Notes:", result["notes"])
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释导入和 main 中的代码后运行。")
