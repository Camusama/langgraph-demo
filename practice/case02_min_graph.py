"""案例 02：最小 LangGraph（单节点直线流）。

构建 StateGraph -> 添加一个 echo 节点 -> START -> echo_node -> END。
"""

# 目标：理解 StateGraph、节点、边、compile、invoke。
# 按注释逐步取消注释实现。

import operator
from typing_extensions import Annotated, TypedDict

from langchain.messages import AnyMessage, HumanMessage
from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict):
    # 使用 Annotated + operator.add 让消息列表在节点间自动合并
    messages: Annotated[list[AnyMessage], operator.add]


def echo_node(state: GraphState) -> GraphState:
    """示例节点：原样返回或附加固定前缀。"""
    # return {
    #     "messages": [
    #         HumanMessage(content="(echo) " + state["messages"][-1].content)
    #     ]
    # }
    raise NotImplementedError("取消上方注释后删除此行")


def build_graph():
    # builder = StateGraph(GraphState)
    # builder.add_node("echo_node", echo_node)
    # builder.add_edge(START, "echo_node")
    # builder.add_edge("echo_node", END)
    # return builder.compile()
    raise NotImplementedError("按照注释完成图构建后删除此行")


def main() -> None:
    # agent = build_graph()
    # result = agent.invoke({"messages": [HumanMessage(content="你好")]})
    # for m in result["messages"]:
    #     print(m)
    print("按照注释完成 echo_node、build_graph，再运行本脚本。")


if __name__ == "__main__":
    main()
