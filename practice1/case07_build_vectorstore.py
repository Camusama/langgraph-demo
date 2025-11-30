"""案例 07：构建与测试向量库（逐步开启版）。

用法：按步骤依次取消注释 STEP 1/2/3，边学边跑。
"""

# from __future__ import annotations
# from typing import List
# from langchain_community.vectorstores import Chroma
# from practice1.common import build_vectorstore, load_vectorstore, print_hits


# def similarity_probe(store: Chroma, queries: List[str], k: int = 3) -> None:
#     """对若干 query 做检索并打印命中。"""
#     for query in queries:
#         results = store.similarity_search_with_score(query, k=k)
#         print_hits(query, results)


# def main() -> None:
#     # STEP 1: 构建或加载向量库
#     # store = load_vectorstore(persist=True)  # 默认持久化到 practice1/.chroma
#
#     # STEP 2: 准备查询
#     # sample_queries = [
#     #     "什么是 LangGraph 的状态内存？",
#     #     "有哪些常见的 LangChain 工具？",
#     #     "RAG 的基本步骤是什么？",
#     # ]
#
#     # STEP 3: 运行相似度检索并观察 score/source
#     # similarity_probe(store, sample_queries, k=3)
#
# if __name__ == "__main__":
#     # main()
#     print("逐步取消注释 STEP 1/2/3 后运行 main()。")
