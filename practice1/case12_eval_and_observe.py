"""case12: LangSmith 自动追踪最小示例。

说明：
- 如果环境变量已设置 `LANGSMITH_TRACING=true`（可选 `LANGSMITH_API_KEY`、`LANGSMITH_PROJECT` 等），LangChain 会自动把调用发送到 LangSmith。
- 如果未设置，脚本仍会本地运行并打印答案，不做额外处理。
"""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from practice1.case08_rag_graph_baseline import build_rag_agent
from practice1.common import load_vectorstore


def build_agent():
    store = load_vectorstore(persist=True)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    return build_rag_agent(retriever)


def main() -> None:
    # 自动加载根目录 .env，便于读取 LangSmith/OpenRouter 配置
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)

    agent = build_agent()
    query = "讲讲 RAG 基本流程，并给出引用"
    result = agent.invoke({"messages": [HumanMessage(content=query)]})
    print("Answer:", result["messages"][-1].content)


if __name__ == "__main__":
    main()
