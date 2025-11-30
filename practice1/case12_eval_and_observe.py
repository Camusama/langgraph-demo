"""案例 12：轻量观测与自测（逐步开启版）。"""

# from __future__ import annotations
# from langchain_core.messages import HumanMessage
# from practice1.case08_rag_graph_baseline import build_rag_agent
# from practice1.common import load_vectorstore


# def has_citation(text: str) -> bool:
#     return "[source" in text.lower()
#
#
# def main() -> None:
#     # STEP 1: 准备 RAG agent
#     # store = load_vectorstore(persist=True)
#     # retriever = store.as_retriever(search_kwargs={"k": 3})
#     # agent = build_rag_agent(retriever)
#
#     # STEP 2: 定义测试用例（可自行增加）
#     # tests = [
#     #     ("检查引用", "讲讲 RAG 基本流程", has_citation, True),
#     #     ("无命中兜底", "告诉我火星今天的气温", lambda t: "未命中" in t or "联网" in t, True),
#     # ]
#
#     # STEP 3: 运行自测
#     # for name, query, check_fn, expected in tests:
#     #     state = agent.invoke({"messages": [HumanMessage(content=query)]})
#     #     answer = state["messages"][-1].content
#     #     ok = check_fn(answer) == expected
#     #     status = "PASS" if ok else "FAIL"
#     #     print(f"[{status}] {name}: {answer}")
#
# if __name__ == "__main__":
#     # main()
#     print("逐步取消注释 STEP 1-3 后运行 main()。")
