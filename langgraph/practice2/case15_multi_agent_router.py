"""案例 15：多专家路由（逐步开启版）。"""

# 步骤：
# 1) 取消注释导入与专家模型定义。
# 2) 取消 build_router_agent 代码，理解路由 -> 专家 -> 汇总的流。
# 3) 在 main 中试不同输入，观察路由命中。

# from __future__ import annotations
# import operator
# from typing import Annotated, Dict, List, TypedDict
# from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
# from langgraph.graph import END, StateGraph
# from practice.model_provider import get_openrouter_model

# class RouteState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     route: str
#     notes: Annotated[List[str], operator.add]


# def build_experts():
#     return {
#         "code": get_openrouter_model(temperature=0),
#         "product": get_openrouter_model(temperature=0),
#         "ops": get_openrouter_model(temperature=0),
#     }
#
#
# def build_router_agent():
#     experts = build_experts()
#
#     def route_node(state: RouteState):
#         user_text = state["messages"][-1].content.lower()
#         if "代码" in user_text or "bug" in user_text:
#             return {"route": "code"}
#         if "用户" in user_text or "需求" in user_text:
#             return {"route": "product"}
#         return {"route": "ops"}
#
#     def expert_node(state: RouteState):
#         expert = experts[state["route"]]
#         sys = SystemMessage(content=f"你是 {state['route']} 专家，请给出简短建议。")
#         ai = expert.invoke([sys, *state["messages"]])
#         return {"messages": [ai], "notes": [f"{state['route']}: {ai.content}"]}
#
#     graph = StateGraph(RouteState)
#     graph.add_node("route", route_node)
#     graph.add_node("expert", expert_node)
#     graph.add_edge("START", "route")
#     graph.add_edge("route", "expert")
#     graph.add_edge("expert", END)
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_router_agent()
#     # queries = ["这个接口报 500 怎么排查？", "帮我设计一下登录页的用户引导", "社区运营怎么提升活跃？"]
#     # for q in queries:
#     #     result = agent.invoke({"messages": [HumanMessage(content=q)], "notes": []})
#     #     print(f"\n{q} -> {result['notes'][-1]}")
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
