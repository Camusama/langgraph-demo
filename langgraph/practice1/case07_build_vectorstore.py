"""案例 07：构建与测试向量库（逐步开启版）。

用法：按步骤依次取消注释 STEP 1/2/3，边学边跑。
- STEP 1 构建/加载向量库：调用 `load_vectorstore`，内部会：
  - 生成示例文档到 `practice1/data/`（若不存在）；
  - 用 `RecursiveCharacterTextSplitter` 切分；
  - 用 OpenRouter 的嵌入模型（`OPENROUTER_API_KEY`）做向量化；
  - 写入/加载 Chroma 本地持久化目录 `practice1/.chroma`。
- STEP 2 准备查询：列出要检索的自然语言问题。
- STEP 3 检索与打印：`similarity_probe` 调 `similarity_search_with_score`，打印命中文档的 score/source/预览，帮助检查中文检索效果。
"""

from __future__ import annotations
from typing import List
from langchain_chroma import Chroma
from practice1.common import build_vectorstore, load_vectorstore, print_hits


def similarity_probe(store: Chroma, queries: List[str], k: int = 3) -> None:
    """对若干 query 做检索并打印命中。"""
    for query in queries:
        results = store.similarity_search_with_score(query, k=k)
        print_hits(query, results)


def main() -> None:
    # STEP 1: 构建或加载向量库
    store = load_vectorstore(persist=True)  # 默认持久化到 practice1/.chroma

    # STEP 2: 准备查询
    sample_queries = [
        "什么是 LangGraph 的状态内存？",
        "有哪些常见的 LangChain 工具？",
        "RAG 的基本步骤是什么？",
    ]

    # STEP 3: 运行相似度检索并观察 score/source
    similarity_probe(store, sample_queries, k=3)


if __name__ == "__main__":
    main()
    print("逐步取消注释 STEP 1/2/3 后运行 main()。")
