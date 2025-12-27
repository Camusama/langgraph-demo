"""案例 17：检查点与恢复（逐步开启版）。"""

# 目标：用 MemorySaver/SqliteSaver 保存执行状态，演示“中断后继续”。
# 步骤：
# 1) 取消注释导入与 build_agent（可复用 case16 的 build_agent）。
# 2) 取消 main 中的第一次/第二次调用，观察恢复效果。

# from __future__ import annotations
# from langgraph.checkpoint.memory import MemorySaver
# from practice2.case16_team_rag_tools import build_agent
# from langchain_core.messages import HumanMessage


# def main() -> None:
#     # agent = build_agent()
#     # memory = MemorySaver()
#     # agent = agent.with_config({"checkpointer": memory})
#     #
#     # thread = {"configurable": {"thread_id": "resume-demo"}}
#     #
#     # # 第一次执行到一半
#     # state1 = agent.invoke({"messages": [HumanMessage(content="给我一份 LangGraph 学习路线")], "notes": [], "context": []}, config=thread)
#     # print("First run last message:", state1["messages"][-1].content)
#     #
#     # # 模拟中断后恢复
#     # state2 = agent.invoke({"messages": [HumanMessage(content="继续上一轮，补充工具调用案例")], "notes": state1.get("notes", []), "context": []}, config=thread)
#     # print("Resumed message:", state2["messages"][-1].content)
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行，观察 thread_id 下的持久化。")
