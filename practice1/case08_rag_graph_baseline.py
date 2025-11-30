"""案例 08：最小 RAG 图（检索 + 答复 + 引用）。"""

from __future__ import annotations

import operator
from typing import Annotated, List, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langgraph.graph import END, StateGraph

from practice.model_provider import get_openrouter_model
from practice1.common import format_docs, load_vectorstore


def replace_list(_: List, right: List) -> List:
    return right


class RAGState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    context: Annotated[List, replace_list]  # list[Document]，类型省略以保持简洁
    query: str


def _latest_user_content(messages: List[AnyMessage]) -> str:
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content
    raise ValueError("state['messages'] 需要至少一条 HumanMessage")


def build_rag_agent(retriever, *, temperature: float = 0) -> Runnable:
    """构建 RAG 图：START -> retrieve -> answer -> END。"""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "你是简洁的技术助理，用中文回答，并在答案中附上引用，如 [source1]。\n"
                    "检索到的上下文：\n{context_text}\n"
                    "若上下文为空或无关，请直说“未命中知识库”并提示需要联网搜索。"
                ),
            ),
            ("placeholder", "{messages}"),
        ]
    )

    llm = get_openrouter_model(temperature=temperature)
    qa_chain = prompt | llm

    def retrieve_node(state: RAGState):
        query = state.get("query") or _latest_user_content(state["messages"])
        docs = retriever.get_relevant_documents(query)
        return {"context": docs, "query": query}

    def answer_node(state: RAGState):
        context_text = format_docs(state.get("context", []))
        response = qa_chain.invoke(
            {"context_text": context_text, "messages": state["messages"]}
        )
        return {"messages": [response]}

    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)
    graph.add_edge("START", "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def main() -> None:
    store = load_vectorstore(persist=True)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    agent = build_rag_agent(retriever)

    result = agent.invoke(
        {"messages": [HumanMessage(content="LangGraph 的状态记忆怎么工作的？")]}
    )
    final_messages = result["messages"]
    print("Answer:", final_messages[-1].content)


if __name__ == "__main__":
    main()
