# LangGraph + LangChain 进阶计划（practice2：多 Agent / 计划与执行）

主题：在已掌握 RAG/工具的基础上，引入多 Agent 协同、路由与计划执行，逐步接近 langmanus 的“协作 + 可恢复”风格。

通用约定
- 目录：`practice2/`，案例编号延续 `case13_*`.py 起步，便于与 practice1 衔接。
- 运行：`uv run python practice2/<file>.py`，复用 `practice/model_provider.py`。需要检查点存储时可用内存版或 sqlite。
- 数据：可继续复用 `practice1/common.py` 的向量库，或自备简单业务文档用于测试。

## 案例梯度

### case13_dual_agent_chat（双 Agent 对话）
- 目标：建立简单的“专家 + 总结者”双节点流，练习跨 Agent 消息传递。
- 图示例：`START -> expert -> summarizer -> END`；状态包含 messages 与 notes。
- 关注：消息类型兼容；总结者基于专家输出生成短答。

### case14_planner_executor（计划-执行模式）
- 目标：实现 Planner 生成子任务列表，Executor 逐条执行（可调用工具或检索）。
- 设计：Planner 节点输出 `tasks: list[str]`；Executor 按队列执行并汇总结果；通过条件边控制“有剩余任务 -> Executor”循环。
- 关注：状态里的任务队列合并策略；避免死循环；输出最终报告。

### case15_multi_agent_router（多专家路由）
- 目标：依据主题把问题分配给不同专家 Agent（如“代码”、“产品”、“运营”）。
- 图：Router 节点返回专家标签，分支到对应专家子图，再回汇总节点。
- 关注：状态字段对齐；分支输出统一合并；打印路由决策供调试。

### case16_team_rag_tools（团队版 RAG + 工具）
- 目标：结合 practice1 的 RAG/工具，构造“研究员（检索+搜索）+ 分析员（归纳）+ 计算员（数学工具）”的协作。
- 图：Coordinator 分配到 Researcher/Calculator，再由 Analyst 汇总；必要时循环追加信息。
- 关注：保持 messages/context 的合并；工具调用与检索上下文的穿透。

### case17_checkpoints_and_resume（检查点与恢复）
- 目标：演示 `MemorySaver/SqliteSaver` 的多 Agent 执行恢复；支持“中断后继续”。
- 设计：使用 case16 的图，加一个控制脚本：执行一半后保存，再加载同线程继续；验证状态持久化。
- 关注：可配置 `thread_id`；在恢复后打印节点命中情况。

### case18_multi_agent_eval（轻量评估）
- 目标：对协作 Agent 输出做简单自动检查（是否包含行动列表、引用、风险提示）。
- 设计：写一个小测试脚本，对 case14/16 的输出跑几条断言；可选用 LLM-as-judge 评分。
- 关注：覆盖成功与失败路径；评估结果打印为 PASS/FAIL。

完成 practice2 后，你应能熟练使用 LangGraph 构建多 Agent 协同、任务路由与计划执行，并掌握检查点恢复的基本套路。后续可在 practice3 中继续探索结构化输出与 Guardrails。
