"""案例 16：团队版 RAG + 工具（逐步开启版）。"""

# 角色设计：Coordinator -> Researcher(检索/搜索) / Calculator(数学) -> Analyst(汇总)。
# 步骤：
# 1) 取消注释导入与各角色模型。
# 2) 查看图的分支与合并逻辑。
# 3) 在 main 中运行示例问题。

# from __future__ import annotations
# import operator
# from typing import Annotated, Dict, List, TypedDict
# from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage, AIMessage
# from langgraph.graph import END, StateGraph
# from langchain_community.tools import TavilySearchResults
# from langchain_community.tools.python.tool import PythonREPLTool
# from practice.model_provider import get_openrouter_model
# from practice1.common import format_docs, load_vectorstore

# class TeamState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     context: Annotated[List, operator.add]
#     route: str
#     notes: Annotated[List[str], operator.add]


# def build_models():
#     return {
#         "coord": get_openrouter_model(temperature=0),
#         "research": get_openrouter_model(temperature=0),
#         "analyst": get_openrouter_model(temperature=0),
#     }
#
#
# def build_agent():
#     models = build_models()
#     tools = [TavilySearchResults(max_results=3), PythonREPLTool()]
#     tool_map = {t.name: t for t in tools}
#     store = load_vectorstore(persist=True)
#     retriever = store.as_retriever(search_kwargs={"k": 3})
#
#     def coord_node(state: TeamState):
#         sys = SystemMessage(content="判断问题类型：research/compute/other。只输出其中之一。")
#         ai = models["coord"].invoke([sys, *state["messages"]])
#         route = "compute" if "compute" in ai.content.lower() else "research"
#         return {"route": route}
#
#     def research_node(state: TeamState):
#         docs = retriever.get_relevant_documents(state["messages"][-1].content)
#         ctx = format_docs(docs)
#         sys = SystemMessage(content=f"结合上下文回答，附引用。\n{ctx}")
#         ai = models["research"].invoke([sys, *state["messages"]])
#         return {"messages": [ai], "context": docs, "notes": [f"research: {ai.content}"]}
#
#     def compute_node(state: TeamState):
#         # 简化版：直接用 PythonREPLTool 计算表达式
#         last = state["messages"][-1].content
#         result = tool_map["python_repl"].invoke({"query": last}) if "python_repl" in tool_map else "tool missing"
#         tm = ToolMessage(tool_call_id="manual", name="python_repl", content=str(result))
#         ai = AIMessage(content=f"计算结果：{result}")
#         return {"messages": [tm, ai], "notes": [f"calc: {result}"]}
#
#     def analyst_node(state: TeamState):
#        sys = SystemMessage(content="汇总上文为 3 条要点，中文，若有引用保留。")
#        ai = models["analyst"].invoke([sys, *state["messages"]])
#        return {"messages": [ai], "notes": [f"summary: {ai.content}"]}
#
#     graph = StateGraph(TeamState)
#     graph.add_node("coord", coord_node)
#     graph.add_node("research", research_node)
#     graph.add_node("compute", compute_node)
#     graph.add_node("analyst", analyst_node)
#     graph.add_edge("START", "coord")
#     graph.add_conditional_edges("coord", lambda s: s["route"], {"research": "research", "compute": "compute"})
#     graph.add_edge("research", "analyst")
#     graph.add_edge("compute", "analyst")
#     graph.add_edge("analyst", END)
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_agent()
#     # q = "LangGraph 状态合并怎么理解？顺便算 3*9+2"
#     # result = agent.invoke({"messages": [HumanMessage(content=q)], "notes": [], "context": []})
#     # print("Notes:", result["notes"])
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
