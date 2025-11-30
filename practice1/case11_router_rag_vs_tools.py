"""案例 11：基于路由的 RAG / 搜索 / 计算 组合。"""

from __future__ import annotations

import operator
import re
from typing import Annotated, Dict, List, TypedDict

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, StateGraph

from langchain_community.tools import TavilySearchResults
from langchain_community.tools.python.tool import PythonREPLTool
from langchain_community.tools.requests.tool import RequestsGetTool

from practice.model_provider import get_openrouter_model
from practice1.common import format_docs, load_vectorstore


def replace_list(_: List, right: List) -> List:
    return right


class RouterState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    context: Annotated[List, replace_list]
    query: str
    turns: Annotated[int, operator.add]


FRESH_KEYWORDS = ("最新", "今天", "现在", "价格", "实时", "update", "news")


def build_router_agent(store, *, temperature: float = 0):
    retriever = store.as_retriever(search_kwargs={"k": 3})

    tools = [
        TavilySearchResults(max_results=3),
        PythonREPLTool(),
        RequestsGetTool(),
    ]
    tool_map: Dict[str, object] = {tool.name: tool for tool in tools}

    llm_tools = get_openrouter_model(temperature=temperature).bind_tools(tools)
    llm_rag = get_openrouter_model(temperature=temperature)

    def route_node(state: RouterState):
        query = state.get("query") or _latest_user_content(state["messages"])
        return {"query": query}

    def route_decision(state: RouterState):
        query = state["query"]
        if _looks_math(query):
            return "calc"
        if _looks_fresh(query):
            return "search"

        top_score = _top_relevance_score(store, query)
        if top_score is not None and top_score >= 0.45:
            return "rag"
        return "search"

    def retrieve_node(state: RouterState):
        docs = retriever.get_relevant_documents(state["query"])
        return {"context": docs}

    def rag_answer_node(state: RouterState):
        context_text = format_docs(state.get("context", []))
        system = SystemMessage(
            content=(
                "你是 RAG 助理，使用中文并附引用 [source1]。\n"
                f"检索上下文：\n{context_text}\n"
                "若上下文为空，请说明未命中知识库。"
            )
        )
        ai_msg = llm_rag.invoke([system, *state["messages"]])
        return {"messages": [ai_msg], "turns": 1}

    def llm_node(state: RouterState):
        context_text = format_docs(state.get("context", []))
        system = SystemMessage(
            content=(
                "你可以调用工具（搜索/计算/HTTP）。"
                "当需要外部信息或计算时请使用工具，若信息已在上下文中则直接回答。\n"
                f"上下文：\n{context_text}"
            )
        )
        ai_msg = llm_tools.invoke([system, *state["messages"]])
        return {"messages": [ai_msg], "turns": 1}

    def tool_node(state: RouterState):
        last_msg = state["messages"][-1]
        if not isinstance(last_msg, AIMessage) or not last_msg.tool_calls:
            return {"messages": []}

        tool_messages: List[ToolMessage] = []
        for call in last_msg.tool_calls:
            name = call["name"]
            args = call.get("args", {})
            tool = tool_map.get(name)
            if tool is None:
                content = f"未找到工具：{name}"
            else:
                result = tool.invoke(args)
                content = str(result)
            tool_messages.append(
                ToolMessage(tool_call_id=call["id"], name=name, content=content)
            )
        return {"messages": tool_messages}

    def tool_continue(state: RouterState):
        last = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else "end"

    graph = StateGraph(RouterState)
    graph.add_node("route", route_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("rag_answer", rag_answer_node)
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tool_node)

    graph.add_edge("START", "route")
    graph.add_conditional_edges(
        "route",
        route_decision,
        {"rag": "retrieve", "search": "llm", "calc": "llm"},
    )
    graph.add_edge("retrieve", "rag_answer")
    graph.add_edge("rag_answer", END)
    graph.add_conditional_edges("llm", tool_continue, {"tools": "tools", "end": END})
    graph.add_edge("tools", "llm")

    return graph.compile()


def _latest_user_content(messages: List[AnyMessage]) -> str:
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content
    raise ValueError("state['messages'] 需要至少一条 HumanMessage")


def _looks_math(query: str) -> bool:
    return bool(re.search(r"\d+(\s*[\+\-\*\/]\s*\d+)+", query))


def _looks_fresh(query: str) -> bool:
    lowered = query.lower()
    return any(k in query for k in FRESH_KEYWORDS) or "today" in lowered or "now" in lowered


def _top_relevance_score(store, query: str) -> float | None:
    try:
        hits = store.similarity_search_with_relevance_scores(query, k=1)
    except Exception:
        hits = []
    if not hits:
        return None
    _, score = hits[0]
    return score


def main() -> None:
    store = load_vectorstore(persist=True)
    agent = build_router_agent(store)

    examples = [
        "LangGraph 的状态合并怎么理解？",
        "今天硅谷的天气如何？",
        "3 * 8 + 5 等于多少？",
    ]
    for q in examples:
        print(f"\n=== Query: {q}")
        result = agent.invoke({"messages": [HumanMessage(content=q)]})
        print("Final:", result["messages"][-1].content)


if __name__ == "__main__":
    main()
