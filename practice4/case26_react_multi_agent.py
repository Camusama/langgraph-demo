"""case26: create_react_agent 组合多角色（research/coder），最小协作示例。"""

from __future__ import annotations

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from practice.model_provider import get_openrouter_model


@tool
def calc(expr: str) -> str:
    """执行简单算式。"""
    try:
        return str(eval(expr))
    except Exception as exc:  # noqa: BLE001
        return f"error: {exc}"


@tool
def note_tool(text: str) -> str:
    """返回要点列表。"""
    return f"要点: {text}"


def build_research_agent():
    llm = get_openrouter_model(temperature=0)
    return create_react_agent(
        llm,
        tools=[note_tool],
        prompt=lambda state: f"你是研究员，总结关键信息。对话状态：{state}",
    )


def build_coder_agent():
    llm = get_openrouter_model(temperature=0)
    return create_react_agent(
        llm,
        tools=[calc],
        prompt=lambda state: f"你是编码助手，必要时用 calc 工具。对话状态：{state}",
    )


def main() -> None:
    research = build_research_agent()
    coder = build_coder_agent()

    question = "总结 LangGraph 的状态合并，并计算 3*8+1"
    res1 = research.invoke({"messages": [{"role": "user", "content": question}]})
    print("Research:", res1["messages"][-1].content)

    # 将研究结果作为输入交给 coder
    res2 = coder.invoke({"messages": res1["messages"]})
    print("Coder:", res2["messages"][-1].content)


if __name__ == "__main__":
    main()
