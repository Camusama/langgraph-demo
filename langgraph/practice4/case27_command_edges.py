"""case27: Command 跳转 + LLM 调用，节点直接返回下一个节点。"""

from __future__ import annotations

from typing import TypedDict

from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from practice.model_provider import get_openrouter_model


class MiniState(TypedDict):
    text: str


def build_graph():
    llm = get_openrouter_model(temperature=0)

    def first_node(state: MiniState):
        # LLM 先改写 text，然后跳转到 second
        sys = SystemMessage(content="把输入改写得更精简。")
        rewritten = llm.invoke([sys, SystemMessage(content=state["text"])]).content
        return Command(goto="second", update={"text": f"{rewritten} -> first"})

    def second_node(state: MiniState):
        sys = SystemMessage(content="再补一句总结。")
        summary = llm.invoke([sys, SystemMessage(content=state["text"])]).content
        return Command(goto=END, update={"text": f"{state['text']} -> {summary}"})

    g = StateGraph(MiniState)
    g.add_node("first", first_node)
    g.add_node("second", second_node)
    g.add_edge(START, "first")
    return g.compile()


def main() -> None:
    graph = build_graph()
    res = graph.invoke({"text": "LangGraph 的状态合并示例"})
    print(res["text"])


if __name__ == "__main__":
    main()
