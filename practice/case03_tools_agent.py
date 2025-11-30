"""案例 03：LangChain 工具 + LangGraph 循环。

结合 @tool、bind_tools 和 LangGraph 条件边，实现模型 -> 工具 -> 模型的循环。
"""

# 目标：
# - 定义工具并绑定模型
# - 节点 llm_call：决定是否调用工具
# - 节点 tool_node：执行工具并返回 ToolMessage
# - 条件边 should_continue：有 tool_calls 则去工具节点，否则 END

import operator
from typing import Literal
from typing_extensions import Annotated, TypedDict

from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
from practice.model_provider import get_openrouter_model


# 简单打印当前消息列表，便于观察节点输入/输出。
def debug_messages(tag: str, messages: list[AnyMessage]) -> None:
    print(
        f"[{tag}]",
        [
            (
                msg.__class__.__name__,
                getattr(msg, "content", None),
                getattr(msg, "tool_calls", None),
            )
            for msg in messages
        ],
    )


# -------- 1) 定义工具 --------


@tool
def add(a: int, b: int) -> int:
    """加法示例工具。"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """乘法示例工具。"""
    return a * b


@tool
def divide(a: int, b: int) -> float:
    """除法示例工具（注意 b 不能为 0）。"""
    return a / b


TOOLS = [add, multiply, divide]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}


# -------- 2) 定义 State --------


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# -------- 3) 节点：模型调用 --------


def llm_call(state: AgentState) -> AgentState:
    """模型节点：决定是否要调用工具。"""
    model = get_openrouter_model(temperature=0)
    model_with_tools = model.bind_tools(TOOLS)
    #
    system_prompt = SystemMessage(
        content="你是一个会使用 add/multiply/divide 的算术助手。"
    )
    debug_messages("llm_call:input", state["messages"])
    ai_reply = model_with_tools.invoke([system_prompt] + state["messages"])
    debug_messages("llm_call:output", [ai_reply])
    #
    return {
        "messages": [ai_reply],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# -------- 4) 节点：工具执行 --------


def tool_node(state: AgentState) -> AgentState:
    """工具节点：执行上一步的 tool_calls 并返回 ToolMessage。"""
    debug_messages("tool_node:input", state["messages"])
    outputs = []
    for tc in state["messages"][-1].tool_calls:
        tool_fn = TOOLS_BY_NAME[tc["name"]]
        observation = tool_fn.invoke(tc["args"])
        outputs.append(ToolMessage(content=observation, tool_call_id=tc["id"]))
    debug_messages("tool_node:output", outputs)
    return {"messages": outputs}


# -------- 5) 条件边：决定下一步 --------


def should_continue(state: AgentState) -> Literal["tool_node", END]:
    """如果上一条消息包含 tool_calls，就去 tool_node，否则结束。"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print(f"[should_continue] tool_calls: {last_message.tool_calls}")
        return "tool_node"
    print("[should_continue] no tool_calls -> END")
    return END


# -------- 6) 组装图并运行 --------


def build_agent():
    """创建图：START -> llm_call -> (tool_node -> llm_call) / END"""
    graph = StateGraph(AgentState)
    graph.add_node("llm_call", llm_call)
    graph.add_node("tool_node", tool_node)
    #
    graph.add_edge(START, "llm_call")
    graph.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
    graph.add_edge("tool_node", "llm_call")
    #
    return graph.compile()


def main() -> None:
    agent = build_agent()
    result = agent.invoke(
        {"messages": [HumanMessage(content="请计算 3*4+5")], "llm_calls": 0}
    )
    for m in result["messages"]:
        m.pretty_print()
    print("按照注释完成后运行，观察模型-工具循环。")


if __name__ == "__main__":
    main()
