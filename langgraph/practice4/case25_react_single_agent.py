"""case25: create_react_agent 快速构建单 Agent，工具极简可本地运行。"""

from __future__ import annotations

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from practice.model_provider import get_openrouter_model


@tool
def echo_tool(text: str) -> str:
    """返回输入文本，演示普通工具。"""
    return text


@tool
def calc(expr: str) -> str:
    """计算简单表达式。"""
    try:
        return str(eval(expr))
    except Exception as exc:  # noqa: BLE001
        return f"error: {exc}"


def build_agent():
    llm = get_openrouter_model(temperature=0)
    return create_react_agent(llm, tools=[echo_tool, calc])


def main() -> None:
    agent = build_agent()
    res = agent.invoke({"messages": [{"role": "user", "content": "请计算 3*9+2，并重复回答的最后一句"}]})
    print(res["messages"][-1].content)


if __name__ == "__main__":
    main()
