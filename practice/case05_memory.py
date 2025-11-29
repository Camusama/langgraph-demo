"""案例 05：状态与记忆。

演示用 Annotated 合并策略保存对话历史和轮次计数。
"""

import operator
from typing_extensions import Annotated, TypedDict

from langchain.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from practice.model_provider import get_openrouter_model


class MemoryState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    turns: Annotated[int, operator.add]


def llm_node(state: MemoryState) -> MemoryState:
    """模型节点：读取 turns，告诉模型当前轮数。"""
    # model = get_openrouter_model(temperature=0)
    # system_prompt = SystemMessage(content=f"你正在对话，第 {state.get('turns', 0)} 轮。请简短回答。")
    # ai_reply = model.invoke([system_prompt] + state["messages"])
    # return {
    #     "messages": [ai_reply],
    #     "turns": state.get("turns", 0) + 1,
    # }
    raise NotImplementedError("完成模型节点后删除此行")


def build_graph():
    # graph = StateGraph(MemoryState)
    # graph.add_node("llm_node", llm_node)
    # graph.add_edge(START, "llm_node")
    # graph.add_edge("llm_node", END)
    # return graph.compile()
    raise NotImplementedError("完成图构建后删除此行")


def main() -> None:
    # agent = build_graph()
    #
    # # 多轮调用：依次传入前一轮的状态
    # state = {"messages": [HumanMessage(content="你好，介绍一下你自己")], "turns": 1}
    # state = agent.invoke(state)
    # for m in state["messages"]:
    #     print(m)
    #
    # state = agent.invoke({"messages": state["messages"] + [HumanMessage(content="再简单说说 LangGraph 是啥")], "turns": state["turns"]})
    # for m in state["messages"]:
    #     print(m)
    print("完成注释后运行，观察 turns 如何累加、消息如何合并。")


if __name__ == "__main__":
    main()
