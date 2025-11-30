"""案例 19：结构化输出起步（逐步开启版）。"""

# 步骤：
# 1) 取消注释导入与 Pydantic/JSON Schema 定义。
# 2) 取消 build_chain，体验 with_structured_output。
# 3) 在 main 中调用并打印解析结果与原始文本。

# from __future__ import annotations
# from typing import List
# from pydantic import BaseModel, Field
# from practice.model_provider import get_openrouter_model


# class AnswerSchema(BaseModel):
#     title: str = Field(..., description="一句话标题")
#     summary: str = Field(..., description="摘要")
#     citations: List[str] = Field(default_factory=list, description="引用标号")
#
#
# def build_chain():
#     model = get_openrouter_model(temperature=0)
#     return model.with_structured_output(AnswerSchema)
#
#
# def main() -> None:
#     # chain = build_chain()
#     # resp = chain.invoke("用三句话介绍 LangGraph，并给出引用编号占位")
#     # print("Parsed:", resp)
#     # print("title:", resp.title)
#
# if __name__ == "__main__":
#     # main()
#     print("取消注释代码后运行。")
