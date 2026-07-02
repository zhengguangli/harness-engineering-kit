# Skill Refactoring to A+ Level

## 状态
active

## 目标
将 13 个 SKILL.md 从平均 7.81 分（C 级）优化到 9.5+ 分（A+ 级），同时遵循官方渐进式披露原则精简内容。

## 范围
- 13 个 SKILL.md 文件的结构和内容优化
- Agent 提示词 heading 层级修复
- 缺失章节补充
- 冗余内容精简

## 非目标
- 不修改 references/ 目录下的参考文件
- 不修改 agents/openai.yaml 文件
- 不改变 skill 的功能逻辑
- 不新增 skill

## 步骤

### Phase 1: 结构修复（所有 skill 通用）
- [ ] 1.1 修复 Agent 提示词 heading 层级：`### <name>` → `## <name>`（影响全部 13 个文件）
- [ ] 1.2 为每个 skill 添加 `## 最佳实践` section（当前全部缺失）
- [ ] 1.3 为 harness-prompt-optimizer 添加 `## 边界情况处理` section

### Phase 2: 瘦身优化（按 skill 逐个处理）
- [ ] 2.1 harness-orchestration（291→目标 ≤200 行）：精简跨 skill 交接点详情，移入 references/
- [ ] 2.2 harness-commit-gate（343→目标 ≤200 行）：精简边界情况和 CI/CD 段
- [ ] 2.3 harness-architecture-boundaries（381→目标 ≤250 行）：精简示例代码，移入 references/
- [ ] 2.4 harness-verification-loop（321→目标 ≤200 行）：精简交接点详情
- [ ] 2.5 harness-bootstrap（269→目标 ≤200 行）：精简执行步骤重复描述
- [ ] 2.6 harness-repo-map（275→目标 ≤200 行）：精简校验流程描述
- [ ] 2.7 harness-project-intake（284→目标 ≤200 行）：精简采集步骤表格
- [ ] 2.8 harness-authoring（262→目标 ≤200 行）：精简设计模式描述
- [ ] 2.9 harness-skill-quality-assessor（325→目标 ≤200 行）：精简评估流程
- [ ] 2.10 harness-golden-principles（236→目标 ≤180 行）：小幅精简
- [ ] 2.11 harness-prompt-optimizer（220→目标 ≤180 行）：小幅精简
- [ ] 2.12 harness-exec-plans（229→目标 ≤180 行）：小幅精简
- [ ] 2.13 harness-observability-and-browser（229→目标 ≤180 行）：小幅精简

### Phase 3: 验证
- [ ] 3.1 运行自动化检查脚本，确认所有 skill ≥ 9.5 分
- [ ] 3.2 确认所有 SKILL.md 正文 ≤ 500 行
- [ ] 3.3 运行 `make triggers-all` 确保 frontmatter 校验通过

## 验收标准
- 所有 13 个 skill 自动化检查分数 ≥ 9.5（A+ 级）
- 所有 SKILL.md 正文 ≤ 500 行
- `make triggers-all` 全部通过
- 每个 skill 包含必需章节：核心原则、何时使用、何时不该用、方法论、关键要点、常见陷阱、边界情况处理、最佳实践、Agent 提示词
- Agent 提示词使用 `##` 层级标题

## 决策日志

### 2026-07-02: 重构策略决策
- **决策**：采用"结构修复 → 逐个瘦身 → 验证"三阶段策略
- **原因**：先修复所有 skill 共有的结构性问题（heading 层级、缺失章节），再逐个精简内容，最后统一验证
- **权衡**：考虑过一次性重写所有文件，但风险太高；分阶段可控制每步变更范围

### 2026-07-02: 瘦身策略决策
- **决策**：冗余 CI/CD 段保留在各 skill 中（不抽取为共享文件）
- **原因**：每个 skill 的 CI/CD 路径不同，抽取后反而增加维护成本；且 CI/CD 段本身不占太多 token
- **权衡**：考虑过创建共享 CI/CD 模板，但各 skill 路径不同导致模板化收益低

## 风险
- **低风险**：结构修复（heading 层级、添加缺失章节）不影响功能
- **中风险**：内容精简可能误删关键信息——需逐个对比验证
- **缓解**：每个 skill 精简后运行自动化检查，确认无回归
