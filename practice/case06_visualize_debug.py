"""案例 06：可视化与调试。

在已有图上使用 get_graph(xray=True).draw_mermaid_png() 和 stream。
可以先从案例 03/05 拷贝你的图构建函数，再补上可视化与流式观察。
"""

from IPython.display import Image, display

# 提示：从你的前序案例（如 case03 或 case05）复制 build_agent/build_graph。
# 下面提供占位符。把具体图构建好后，取消注释可视化/流式代码。


def build_graph():
    """复制并返回你自己的图对象。"""
    # from case03_tools_agent import build_agent as build_tools_agent
    # return build_tools_agent()
    raise NotImplementedError("从前序案例复制构建逻辑后删除此行")


def main() -> None:
    # agent = build_graph()
    #
    # # 1) 可视化：Mermaid PNG
    # png_bytes = agent.get_graph(xray=True).draw_mermaid_png()
    # display(Image(png_bytes))
    #
    # # 2) 流式执行示例（以工具 Agent 为例）
    # for step in agent.stream({"messages": [], "llm_calls": 0, "turns": 0}):
    #     print("Step chunk:", step)
    print("从前序案例复制图后，取消注释可视化/stream 片段进行调试。")


if __name__ == "__main__":
    main()
