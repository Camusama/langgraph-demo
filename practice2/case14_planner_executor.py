"""案例 14：计划-执行模式（逐步开启版）。"""

# 步骤：
# 1) 取消注释导入与 Planner/Executor 的定义。
# 2) 取消注释 build_graph，理解任务队列如何循环。
# 3) 取消 main 的调用，观察执行日志。

# from __future__ import annotations
# import operator
# from typing import Annotated, List, TypedDict
# from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
# from langgraph.graph import END, StateGraph
# from practice.model_provider import get_openrouter_model

# class PlanState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     tasks: Annotated[List[str], operator.add]
#     results: Annotated[List[str], operator.add]


# def build_planner():
#     return get_openrouter_model(temperature=0)
#
#
# def build_executor():
#     return get_openrouter_model(temperature=0)
#
#
# def build_graph():
#     planner = build_planner()
#     executor = build_executor()
#
#     def plan_node(state: PlanState):
#         sys = SystemMessage(content="把用户需求拆成 2-4 个可执行子任务，中文，列表形式。")
#         ai = planner.invoke([sys, *state["messages"]])
#         # 简单按行切分
#         new_tasks = [line.strip("- ").strip() for line in ai.content.splitlines() if line.strip()]
#         return {"tasks": new_tasks}
#
#     def exec_node(state: PlanState):
#         if not state["tasks"]:
#             return {"messages": [], "results": []}
#         current = state["tasks"][0]
#         sys = SystemMessage(content=f"执行子任务：{current}。给出简短结果。")
#         ai = executor.invoke([sys, *state["messages"]])
#         remaining = state["tasks"][1:]
#         return {"messages": [ai], "tasks": remaining, "results": [f"{current} -> {ai.content}"]}
#
#     def route(state: PlanState):
#         return "exec" if state["tasks"] else "plan"
#
#     graph = StateGraph(PlanState)
#     graph.add_node("plan", plan_node)
#     graph.add_node("exec", exec_node)
#     graph.add_edge("START", "plan")
#     graph.add_conditional_edges("plan", lambda _: "exec", {"exec": "exec"})
#     graph.add_conditional_edges("exec", route, {"plan": "plan", "exec": "exec", "END": END})
#     graph.add_edge("exec", END)  # 保底退出
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_graph()
#     # result = agent.invoke({"messages": [HumanMessage(content="为 LangGraph 新手写一份入门 checklist")], "tasks": [], "results": []})
#     # print("Results:", result["results"])
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释代码后运行。")
