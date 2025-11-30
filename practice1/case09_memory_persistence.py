"""案例：配置checkpointer实现真正的跨轮状态持久化"""

import operator
from typing_extensions import Annotated, TypedDict

from langchain.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver  # 导入内存检查点
from practice.model_provider import get_openrouter_model


# 定义状态
class MemoryState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    turns: Annotated[int, operator.add]


# 定义LLM节点
def llm_node(state: MemoryState) -> MemoryState:
    model = get_openrouter_model(temperature=0)
    system_prompt = SystemMessage(
        content=f"你正在对话，第 {state['turns']} 轮。请简短回答。"
    )
    ai_reply = model.invoke([system_prompt] + state["messages"])
    return {
        "messages": [ai_reply],
        "turns": 1,
    }


# 构建图：核心是传入checkpointer实例（内存持久化）
def build_graph():
    # 1. 初始化检查点（内存存储，也可替换为Redis/SQL检查点）
    checkpointer = MemorySaver()
    # 2. 创建graph时传入checkpointer
    graph = StateGraph(MemoryState)
    graph.add_node("llm_node", llm_node)
    graph.add_edge(START, "llm_node")
    graph.add_edge("llm_node", END)
    # 3. 编译graph时绑定checkpointer
    return graph.compile(checkpointer=checkpointer)


def main() -> None:
    # 初始化Agent（已绑定checkpointer）
    agent = build_graph()

    # 定义会话配置：configurable + thread_id
    thread_config = {"configurable": {"thread_id": "memory-demo"}}

    # 第一轮调用：初始化状态，会被checkpointer持久化
    print("=== 第一轮对话 ===")
    state = agent.invoke(
        {
            "messages": [HumanMessage(content="帮我总结下 LangGraph 的状态概念。")],
            "turns": 0,
        },
        config=thread_config,
    )
    for msg in state["messages"]:
        if isinstance(msg, AIMessage):
            print(f"AI：{msg.content}")
    print(f"当前轮次：{state['turns']}\n")

    # 第二轮调用：无需手动传递上一轮状态，checkpointer会通过thread_id自动加载
    print("=== 第二轮对话 ===")
    state = agent.invoke(
        {
            "messages": [HumanMessage(content="再详细说说状态的合并规则。")],
            # 无需传递turns，checkpointer会加载上一轮的turns并自动累加
        },
        config=thread_config,
    )
    for msg in state["messages"]:
        if isinstance(msg, AIMessage):
            print(f"AI：{msg.content}")
    print(f"当前轮次：{state['turns']}\n")


if __name__ == "__main__":
    main()
