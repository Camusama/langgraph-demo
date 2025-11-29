"""案例 04：条件分支与兜底。

基于工具 Agent，增加路由：如果是算术问题走工具链，否则直接回复。
"""

# 目标：
# - route 节点：判断用户请求类型
# - respond_node：非算术请求的兜底回复
# - calc_flow：沿用案例 03 的 llm_call/tool_node 循环

import operator
from typing import Literal
from typing_extensions import Annotated, TypedDict

from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
from practice.model_provider import get_openrouter_model


# 工具定义（与案例 03 相同，可直接使用）
@tool
def add(a: int, b: int) -> int:
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    return a * b


TOOLS = [add, multiply]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# ---- 1) 路由节点 ----
def route(state: AgentState) -> Literal["llm_call", "respond_node"]:
    """简单关键词路由：含数字或运算符则走计算分支（llm_call），否则兜底回复。"""
    # text = state["messages"][-1].content
    # if any(ch.isdigit() for ch in text) or any(op in text for op in ["+", "-", "*", "×", "乘", "加"]):
    #     return "llm_call"
    # return "respond_node"
    raise NotImplementedError("完成路由逻辑后删除此行")


# ---- 2) llm_call（计算分支） ----
def llm_call(state: AgentState) -> AgentState:
    """算术分支的 LLM 节点，绑定工具。"""
    # model = get_openrouter_model(temperature=0)
    # model_with_tools = model.bind_tools(TOOLS)
    # system_prompt = SystemMessage(content="你是算术助手，使用 add/multiply 工具。")
    # ai_reply = model_with_tools.invoke([system_prompt] + state["messages"])
    # return {"messages": [ai_reply], "llm_calls": state.get("llm_calls", 0) + 1}
    raise NotImplementedError("完成模型调用后删除此行")


# ---- 3) tool_node（计算分支） ----
def tool_node(state: AgentState) -> AgentState:
    """执行工具调用。"""
    # outputs = []
    # for tc in state["messages"][-1].tool_calls:
    #     obs = TOOLS_BY_NAME[tc["name"]].invoke(tc["args"])
    #     outputs.append(ToolMessage(content=obs, tool_call_id=tc["id"]))
    # return {"messages": outputs}
    raise NotImplementedError("完成工具节点后删除此行")


def should_continue(state: AgentState) -> Literal["tool_node", END]:
    """计算分支条件：有 tool_calls -> tool_node，否则结束。"""
    # if state["messages"][-1].tool_calls:
    #     return "tool_node"
    # return END
    raise NotImplementedError("完成条件逻辑后删除此行")


# ---- 4) respond_node（兜底分支） ----
def respond_node(state: AgentState) -> AgentState:
    """非算术请求的直接回复。"""
    # text = state["messages"][-1].content
    # response = f"这个问题不是算术计算（收到：{text}），这里先不计算。"
    # return {"messages": [SystemMessage(content=response)]}
    raise NotImplementedError("完成兜底回复后删除此行")


# ---- 5) 组装图 ----
def build_agent():
    """图结构：
    START -> route -> (llm_call/tool_node 循环) or respond_node
    """
    # graph = StateGraph(AgentState)
    #
    # graph.add_node("route", route)
    # graph.add_node("llm_call", llm_call)
    # graph.add_node("tool_node", tool_node)
    # graph.add_node("respond_node", respond_node)
    #
    # graph.add_edge(START, "route")
    # graph.add_conditional_edges("route", route, ["llm_call", "respond_node"])
    #
    # # 计算分支：llm_call -> (tool_node -> llm_call) / END
    # graph.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
    # graph.add_edge("tool_node", "llm_call")
    #
    # # respond_node 直接结束
    # graph.add_edge("respond_node", END)
    #
    # return graph.compile()
    raise NotImplementedError("完成图构建后删除此行")


def main() -> None:
    # agent = build_agent()
    # print("算术输入：")
    # result = agent.invoke({"messages": [HumanMessage(content="请计算 2*3+5")]})
    # for m in result["messages"]:
    #     print(m)
    #
    # print("\n非算术输入：")
    # result = agent.invoke({"messages": [HumanMessage(content="写一首诗")], "llm_calls": 0})
    # for m in result["messages"]:
    #     print(m)
    print("完成注释内的实现后，运行脚本查看分支效果。")


if __name__ == "__main__":
    main()
