# LangGraph + LangChain 进阶计划（practice3：函数调用 / 结构化输出 / Guardrails）

主题：聚焦 LangChain 1.x 的函数调用、Pydantic/JSON Schema 结构化输出、内容安全与约束执行，贴近 langmanus 的“可控/可审计”实践。

通用约定
- 目录：`practice3/`，案例编号延续 `case19_*`.py 起步。
- 运行：`uv run python practice3/<file>.py`，仍复用 `practice/model_provider.py` 与 practice1 的向量库/工具。
- 若用到外部检测（如禁词列表或正则校验），保持配置化，便于替换。

## 案例梯度

### case19_structured_output_basics（结构化输出起步）
- 目标：让 LLM 直接生成 Pydantic 模型或 JSON Schema 对应的结构体。
- 操作：定义 `AnswerSchema(title:str, summary:str, citations:list[str])`；使用 `with_structured_output`（或 `PydanticOutputParser`）返回对象；验证字段类型。
- 关注：错误处理与重试；打印解析失败时的原始文本。

### case20_function_calling_tools（函数调用与工具）
- 目标：对比 “工具绑定的函数调用” 与 “结构化输出” 的差异；练习解析 `tool_calls`。
- 操作：定义工具如 `lookup_doc(id)`、`calc(expr)`；模型 `bind_tools`；在图中 `llm -> tool_node -> llm` 循环，收集调用记录。
- 关注：工具返回的格式统一；异常时的兜底消息。

### case21_guardrails_regex_and_lists（简单 Guardrails）
- 目标：在结构化输出后做正则/枚举校验，演示“拒答/重试”路径。
- 操作：定义敏感词列表、URL 正则；若输出不合法则添加 `validation_error` 字段，再走一次 LLM 修复分支。
- 关注：`add_conditional_edges` 实现“校验失败 -> fix -> 再校验”；打印校验原因。

### case22_multi_turn_structured_rag（多轮结构化 RAG）
- 目标：结合 practice1 的 RAG，把回答固定成结构化格式（如 `{"short_answer":..., "citations":[...], "next_questions":[...]}`）。
- 图：`retrieve -> llm_structured -> validate -> END`，其中 validate 检查引用/字段完整性，不合格则让 LLM 重写。
- 关注：上下文引用编号与输出字段对应；合并策略避免旧 context 残留。

### case23_safety_and_content_filters（内容安全）
- 目标：加入安全检查节点，检测模型输出中的敏感内容；必要时改写/遮盖。
- 操作：使用自定义规则或简单分类器（如正则、LLM 审核）；当检测到违规时走“sanitize”节点对输出做脱敏或拒答。
- 关注：清晰的审计日志（检测结果、处理动作）；状态中保留原始输出与修订版。

### case24_contract_tests_and_eval（契约测试）
- 目标：为结构化/受控输出编写契约测试：字段必填、引用必有、不得含违禁词。
- 操作：写一个测试脚本，对 case19/22 的输出跑断言；若使用 LLM-as-judge，给出 prompt 与评分阈值。
- 关注：测试可重复、无外部依赖；对失败用例打印差异。

完成 practice3 后，你应具备用 LangGraph/LangChain 构建“可控、可验证、可审计”的工作流能力，可在 practice4 进一步探索部署、监控与成本优化。
