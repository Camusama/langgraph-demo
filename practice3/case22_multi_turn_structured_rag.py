"""案例 22：多轮结构化 RAG（逐步开启版）。"""

# 目标：回答输出固定为结构化字段，并在校验失败时重写。
# 步骤：
# 1) 取消注释导入与数据结构。
# 2) 查看 retrieve -> llm_structured -> validate -> (rewrite|END) 的流程。
# 3) 运行示例，检查引用与字段完整性。

# from __future__ import annotations
# import operator
# from typing import Annotated, List, TypedDict
# from pydantic import BaseModel, Field, ValidationError
# from langchain_core.messages import AnyMessage, HumanMessage
# from langgraph.graph import END, StateGraph
# from practice.model_provider import get_openrouter_model
# from practice1.common import load_vectorstore, format_docs

# class RagOutput(BaseModel):
#     short_answer: str
#     citations: List[str]
#     next_questions: List[str] = Field(default_factory=list)
#
#
# class StructuredState(TypedDict):
#     messages: Annotated[List[AnyMessage], operator.add]
#     context: Annotated[List, operator.add]
#     parsed: RagOutput | None
#     error: str
#
#
# def build_agent():
#     store = load_vectorstore(persist=True)
#     retriever = store.as_retriever(search_kwargs={"k": 3})
#     llm = get_openrouter_model(temperature=0).with_structured_output(RagOutput)
#
#     def retrieve(state: StructuredState):
#         query = state["messages"][-1].content
#         docs = retriever.get_relevant_documents(query)
#         return {"context": docs}
#
#     def llm_structured(state: StructuredState):
#         ctx = format_docs(state.get("context", []))
#         prompt = f"根据上下文回答，并附上 citations（source 编号）。上下文：\n{ctx}"
#         parsed = llm.invoke(prompt)
#         return {"parsed": parsed, "messages": state["messages"] + [HumanMessage(content=str(parsed))]}
#
#     def validate(state: StructuredState):
#         parsed = state.get("parsed")
#         if not parsed:
#             return {"error": "missing output"}
#         if not parsed.citations:
#             return {"error": "缺少 citations"}
#         return {"error": ""}
#
#     def rewrite(state: StructuredState):
#         prompt = f"上次输出错误：{state['error']}。请补充或修正，保持结构化格式。"
#         fixed = llm.invoke(prompt)
#         return {"parsed": fixed, "error": ""}
#
#     def route(state: StructuredState):
#         return "ok" if not state.get("error") else "rewrite"
#
#     graph = StateGraph(StructuredState)
#     graph.add_node("retrieve", retrieve)
#     graph.add_node("llm_structured", llm_structured)
#     graph.add_node("validate", validate)
#     graph.add_node("rewrite", rewrite)
#     graph.add_edge("START", "retrieve")
#     graph.add_edge("retrieve", "llm_structured")
#     graph.add_edge("llm_structured", "validate")
#     graph.add_conditional_edges("validate", route, {"ok": END, "rewrite": "rewrite"})
#     graph.add_edge("rewrite", "validate")
#     return graph.compile()
#
#
# def main() -> None:
#     # agent = build_agent()
#     # result = agent.invoke({"messages": [HumanMessage(content="讲讲 LangGraph 的状态合并，并给引用")], "parsed": None, "error": ""})
#     # print("Parsed:", result["parsed"])
#     # print("Error:", result.get("error"))
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
