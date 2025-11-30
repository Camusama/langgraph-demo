"""案例 18：多 Agent 输出的轻量评估（逐步开启版）。"""

# 目标：对协作流程的输出做简单 PASS/FAIL 检查。
# 步骤：
# 1) 取消注释导入与待评估的 agent（可用 case14/16）。
# 2) 定义检查函数（引用、行动列表、风险提示等）。
# 3) 运行测试列表。

# from __future__ import annotations
# from langchain_core.messages import HumanMessage
# from practice2.case16_team_rag_tools import build_agent


# def has_action(text: str) -> bool:
#     return "行动" in text or "步骤" in text
#
#
# def main() -> None:
#     # agent = build_agent()
#     # tests = [
#     #     ("检查行动列表", "给出 LangGraph 学习行动清单", has_action, True),
#     # ]
#     # for name, query, check_fn, expected in tests:
#     #     state = agent.invoke({"messages": [HumanMessage(content=query)], "notes": [], "context": []})
#     #     answer = state["messages"][-1].content
#     #     ok = check_fn(answer) == expected
#     #     print(f"[{'PASS' if ok else 'FAIL'}] {name}: {answer}")
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
