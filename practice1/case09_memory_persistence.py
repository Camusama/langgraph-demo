"""案例 09：带持久化的 RAG，对话过长时做摘要压缩。"""

from __future__ import annotations

import operator
from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from practice.model_provider import get_openrouter_model
from practice1.common import format_docs, load_vectorstore


def merge_messages(_: List[AnyMessage], right: List[AnyMessage]) -> List[AnyMessage]:
    """替换式合并，便于在摘要阶段丢弃旧消息。"""
    return right


class MemoryRAGState(TypedDict):
    messages: Annotated[List[AnyMessage], merge_messages]
    context: Annotated[List, merge_messages]
    query: str
    turns: Annotated[int, operator.add]
    summary: Optional[str]


SUMMARY_THRESHOLD = 6  # 超过多少条消息开始摘要


def build_memory_rag_agent(retriever, *, temperature: float = 0):
    """图结构：START -> maybe_summarize -> retrieve -> answer -> END。"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "你是 RAG 助理，使用中文，回答时附上引用 [source1]。\n"
                    "对话摘要（可能为空）：{summary_text}\n"
                    "检索上下文：\n{context_text}\n"
                    "若上下文为空，请提示未命中知识库，可以改为联网搜索。"
                ),
            ),
            ("placeholder", "{messages}"),
        ]
    )

    summarize_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "请用 100 字以内总结以下对话要点，中文输出，不要添加新信息：",
            ),
            ("human", "{history_text}"),
        ]
    )

    llm = get_openrouter_model(temperature=temperature)
    qa_chain = qa_prompt | llm
    summarizer = get_openrouter_model(temperature=0)

    def route_summary(state: MemoryRAGState):
        return "summarize" if len(state["messages"]) > SUMMARY_THRESHOLD else "skip"

    def router_node(state: MemoryRAGState):
        return state

    def summarize_node(state: MemoryRAGState):
        # 保留最后一条用户问题，其余合并成摘要。
        history_messages = state["messages"][:-1]
        if not history_messages:
            return {"summary": state.get("summary"), "messages": state["messages"]}

        history_text = "\n".join(
            f"{msg.__class__.__name__}: {msg.content}" for msg in history_messages
        )
        summary_msg = summarizer.invoke(
            summarize_prompt.format_prompt(history_text=history_text).to_messages()
        )
        summary_text = summary_msg.content

        compressed_messages: List[AnyMessage] = [
            SystemMessage(content=f"对话摘要：{summary_text}"),
            state["messages"][-1],
        ]
        return {"summary": summary_text, "messages": compressed_messages}

    def retrieve_node(state: MemoryRAGState):
        query = state.get("query") or _latest_user_content(state["messages"])
        docs = retriever.get_relevant_documents(query)
        return {"context": docs, "query": query}

    def answer_node(state: MemoryRAGState):
        context_text = format_docs(state.get("context", []))
        summary_text = state.get("summary") or "（暂无摘要）"
        ai_msg = qa_chain.invoke(
            {
                "summary_text": summary_text,
                "context_text": context_text,
                "messages": state["messages"],
            }
        )
        new_messages = state["messages"] + [ai_msg]
        return {"messages": new_messages, "turns": 1}

    graph = StateGraph(MemoryRAGState)
    graph.add_node("router", router_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)

    graph.add_edge("START", "router")
    graph.add_conditional_edges(
        "router",
        route_summary,
        {"summarize": "summarize", "skip": "retrieve"},
    )
    graph.add_edge("summarize", "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


def _latest_user_content(messages: List[AnyMessage]) -> str:
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content
    raise ValueError("state['messages'] 需要至少一条 HumanMessage")


def main() -> None:
    store = load_vectorstore(persist=True)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    agent = build_memory_rag_agent(retriever)

    thread_config = {"configurable": {"thread_id": "memory-demo"}}

    # 第一次提问
    state = agent.invoke(
        {"messages": [HumanMessage(content="帮我总结下 LangGraph 的状态概念。")], "turns": 0},
        config=thread_config,
    )
    print("Turn 1:", state["messages"][-1].content)

    # 第二次提问，复用 checkpoint，触发摘要逻辑（当消息变多时）。
    state = agent.invoke(
        {
            "messages": [HumanMessage(content="再说说工具调用和 MemorySaver 的关系。")],
            "turns": state["turns"],
            "summary": state.get("summary"),
        },
        config=thread_config,
    )
    print("Turn 2:", state["messages"][-1].content)


if __name__ == "__main__":
    main()
