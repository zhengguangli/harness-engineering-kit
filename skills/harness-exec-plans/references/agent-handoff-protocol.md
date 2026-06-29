### plan-architect ↔ verification-loop-runner 协作

exec-plan 的生命周期由两个 agent 分阶段接力完成:

1. **plan-architect 负责创建**:把高层目标拆解为 exec-plan 文件(目标、步骤、验收标准、风险),写入 `docs/exec-plans/active/`。plan-architect 不写实现代码。
2. **verification-loop-runner 负责执行**:按 exec-plan 的步骤逐一实现,每步走自验证循环(实现→自检→测试→评审→修复),完成后在 exec-plan 中勾选步骤并补充决策日志。
3. **交接点**:plan-architect 完成计划后,告诉主对话"建议委派给 verification-loop-runner 按此计划执行";verification-loop-runner 开始前先读取 exec-plan 确认完成定义。
4. **回写约定**:只有 verification-loop-runner 可以修改 exec-plan 的步骤勾选状态和决策日志;plan-architect 只在用户要求调整计划时才修改目标/范围/步骤。

---
最后更新: 2026-06-29
