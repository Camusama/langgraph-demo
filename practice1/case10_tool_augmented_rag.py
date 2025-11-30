"""案例 10：RAG + 内置工具（搜索 / 计算 / HTTP）。"""

from __future__ import annotations

import operator
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


class ToolRAGState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    context: Annotated[List, replace_list]
    query: str
    turns: Annotated[int, operator.add]


def build_tool_rag_agent(retriever, *, temperature: float = 0):
    tools = [
        TavilySearchResults(max_results=3),
        PythonREPLTool(),
        RequestsGetTool(),
    ]
    tool_map: Dict[str, object] = {tool.name: tool for tool in tools}
    llm = get_openrouter_model(temperature=temperature).bind_tools(tools)

    def retrieve_node(state: ToolRAGState):
        query = state.get("query") or _latest_user_content(state["messages"])
        docs = retriever.get_relevant_documents(query)
        return {"context": docs, "query": query}

    def llm_node(state: ToolRAGState):
        context_text = format_docs(state.get("context", []))
        system = SystemMessage(
            content=(
                "你是多功能助理，优先利用已检索到的上下文回答，并在需要时调用工具。\n"
                f"检索上下文：\n{context_text}"
            )
        )
        ai_msg = llm.invoke([system, *state["messages"]])
        return {"messages": [ai_msg], "turns": 1}

    def tool_node(state: ToolRAGState):
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
                ToolMessage(
                    tool_call_id=call["id"],
                    name=name,
                    content=content,
                )
            )
        return {"messages": tool_messages}

    def should_continue(state: ToolRAGState):
        last = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else "end"

    graph = StateGraph(ToolRAGState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tool_node)

    graph.add_edge("START", "retrieve")
    graph.add_edge("retrieve", "llm")
    graph.add_conditional_edges("llm", should_continue, {"tools": "tools", "end": END})
    graph.add_edge("tools", "llm")

    return graph.compile()


def _latest_user_content(messages: List[AnyMessage]) -> str:
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content
    raise ValueError("state['messages'] 需要至少一条 HumanMessage")


def main() -> None:
    store = load_vectorstore(persist=True)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    agent = build_tool_rag_agent(retriever)

    state = agent.invoke(
        {"messages": [HumanMessage(content="总结 LangGraph 状态，再算一下 3*7+1。")]}
    )
    print("Final messages:")
    for msg in state["messages"]:
        print(f"- {msg.__class__.__name__}: {getattr(msg, 'content', '')}")


if __name__ == "__main__":
    main()
