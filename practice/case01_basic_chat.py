"""案例 01：最基本的 LangChain ChatModel 调用（无图）。

默认使用 OpenRouter 的 deepseek/deepseek-v3.2-exp，从 .env 读取 OPENROUTER_API_KEY。
"""

# 目标：用 get_openrouter_model 调一次对话，理解 HumanMessage/AIMessage。

import json
from langchain.messages import HumanMessage
from practice.model_provider import get_openrouter_model


def main() -> None:
    # 1) 初始化模型：已封装为 OpenRouter + deepseek/deepseek-v3.2-exp
    model = get_openrouter_model(temperature=0)

    # 2) 构造输入消息（最简单的单轮人类消息）
    messages = [HumanMessage(content="你好")]

    messages_dict = [msg.model_dump() for msg in messages]
    messages_json = json.dumps(messages_dict, ensure_ascii=False, indent=2)
    print("输入消息（JSON）：\n", messages_json)

    # 3) 调用模型
    response = model.invoke(messages)
    result_dict = response.dict()  # 核心：LangChain 内置的字典转换
    result_json = json.dumps(result_dict, ensure_ascii=False, indent=2)

    print("invoke 结果的 JSON 序列化：\n", result_json)
    # 4) 打印返回的 AIMessage
    # print(response)


if __name__ == "__main__":
    main()
