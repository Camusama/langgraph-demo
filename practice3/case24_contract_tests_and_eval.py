"""案例 24：契约测试与轻量评估（逐步开启版）。"""

# 目标：为结构化/受控输出写可重复的断言测试。
# 步骤：
# 1) 取消注释导入与待测 Agent（如 case22 的 build_agent）。
# 2) 定义断言函数：字段必填、引用存在、禁词过滤等。
# 3) 运行测试列表，打印 PASS/FAIL。

# from __future__ import annotations
# from langchain_core.messages import HumanMessage
# from practice3.case22_multi_turn_structured_rag import build_agent, RagOutput


# def require_citation(output: RagOutput) -> bool:
#     return bool(output.citations)
#
#
# def no_banned_words(text: str) -> bool:
#     return "攻击" not in text and "违法" not in text
#
#
# def main() -> None:
#     # agent = build_agent()
#     # tests = [
#     #     ("citation", lambda out: require_citation(out), True),
#     #     ("no banned", lambda out: no_banned_words(out.short_answer), True),
#     # ]
#     # state = agent.invoke({"messages": [HumanMessage(content="总结 LangGraph，并给出引用")], "parsed": None, "error": ""})
#     # output = state["parsed"]
#     # for name, fn, expected in tests:
#     #     ok = fn(output) == expected
#     #     print(f"[{'PASS' if ok else 'FAIL'}] {name}: {output}")
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释后运行。")
