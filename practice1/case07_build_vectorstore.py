"""案例 07：构建与测试向量库（RAG 起步）。"""

from __future__ import annotations

from typing import List

from langchain_community.vectorstores import Chroma

from practice1.common import build_vectorstore, load_vectorstore, print_hits


def similarity_probe(store: Chroma, queries: List[str], k: int = 3) -> None:
    """对若干 query 做检索并打印命中。"""
    for query in queries:
        results = store.similarity_search_with_score(query, k=k)
        print_hits(query, results)


def main() -> None:
    # 若已存在持久化向量库则加载，否则重新构建。
    store = load_vectorstore(persist=True)

    sample_queries = [
        "什么是 LangGraph 的状态内存？",
        "有哪些常见的 LangChain 工具？",
        "RAG 的基本步骤是什么？",
    ]
    similarity_probe(store, sample_queries, k=3)


if __name__ == "__main__":
    main()
