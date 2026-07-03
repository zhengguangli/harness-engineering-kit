# ARCHITECTURE.md

<!-- Canonical owner: harness-architecture-boundaries -->

这个文件定义 harness-engineering-kit 的领域划分与依赖方向规则。

## 领域划分

| 领域 | 简述 | 对应路径 |
|---|---|---|
| skills | 13 个 skill（方法论 + agent 提示词 + 模板） | `skills/harness-*/` |
| scripts | 校验脚本（frontmatter、关键词一致性、回归） | `scripts/` |
| tests | 触发回归用例与报告 | `tests/` |
| ci | GitHub Actions 工作流与 PR 模板 | `.github/` |

## Skill 分层与依赖方向

```
Layer 0 信息采集    harness-project-intake
       ↓
Layer 1 骨架搭建    harness-bootstrap
       ↓
Layer 2 知识与约束  harness-repo-map, harness-architecture-boundaries,
                    harness-golden-principles, harness-prompt-optimizer
       ↓
Layer 3 计划驱动    harness-exec-plans
       ↓
Layer 4 执行验证    harness-verification-loop, harness-observability-and-browser
       ↓
Layer 5 提交门      harness-commit-gate

元层                harness-orchestration, harness-authoring
```

- 依赖只能向下流动：Layer N 的 skill 可引用 Layer <N 的产出，不可反向。
- 同层 skill 之间可以并行，不互相依赖。
- 元层 skill 可被任意层调用（orchestration 负责路由，authoring 负责扩展体系本身）。

## 每个 Skill 的内部结构

```
skills/<name>/
├── SKILL.md          # 方法论正文 + agent 提示词（含跨平台 frontmatter）
├── agents/
│   └── openai.yaml   # Codex UI 元数据
└── references/       # 模板文件
```

Agent 提示词已内联到 SKILL.md 的 `## Agent 提示词` section，不再使用独立的 `agents/<name>.md` 文件。

## 支撑基础设施的依赖方向

```
scripts/ → skills/    （脚本校验 skill 的 frontmatter 和关键词）
tests/   → skills/    （回归用例验证 skill 的触发逻辑）
.github/ → scripts/   （CI 调用校验脚本）
```

- scripts/ 只读取 skills/ 的内容，不修改。
- tests/ 的回归用例依赖 scripts/ 中定义的关键词映射。
- .github/workflows/ 调用 `make triggers-all` 触发完整校验链。

## 数据边界规则

- 每个 `SKILL.md` 的 frontmatter 是 skill 与平台之间的契约——平台只读自己认识的字段，忽略未知字段。
- Agent 提示词的 canonical 版本在 `SKILL.md` 的 `## Agent 提示词` section。

## 机械强制现状

| 规则 | 强制方式 | 状态 |
|---|---|---|
| frontmatter 必填字段 | `scripts/validate-skill-triggers.sh` | ✅ 已强制 |
| 关键词一致性 | 回归测试中覆盖 | ⚠️ 已合并入回归检查 |
| 触发回归 | `scripts/run-trigger-regression.sh` | ✅ 已强制 |
| agent 提示词存在性 | `scripts/validate-agent-prompt-sync.sh` | ✅ 已强制 |
| skill 间无循环依赖 | 人工 review | ⚠️ 仅文档，未强制 |

## 经验教训

Skills质量三轮评估优化的关键经验教训：

1. **三轮迭代优化方法有效**：通过三轮迭代优化，skills质量得到了持续改进
2. **触发条件描述很重要**：用户需要清晰的触发条件来理解何时使用skill
3. **使用示例很关键**：具体的使用示例帮助用户理解如何使用skill
4. **错误处理指导需要完善**：用户需要知道如何处理使用过程中遇到的问题
5. **自动化检查提高效率**：自动化检查脚本可以快速识别基本问题
6. **人工评审确保质量**：人工评审可以识别自动化检查无法发现的问题
7. **质量基准线很重要**：建立明确的质量基准线有助于持续改进
8. **文档风格需要统一**：统一的文档风格有助于用户理解和使用skills

全量A+级优化的关键经验教训：

1. **全量优化需要系统化方法**：建立统一的优化标准，按优先级批量执行
2. **边界情况处理是A+级的关键**：每个skill必须处理各种边界情况
3. **最佳实践提升内容质量**：提供最佳实践帮助用户更好地使用skill
4. **Agent提示词需要精心设计**：确保角色清晰、流程明确、约束合理
5. **自动化支持提升效率**：提供自动化检查脚本和CI/CD集成
6. **用户体验需要持续优化**：确保学习曲线平缓、使用便捷、错误恢复能力强

详细经验教训见 `docs/lessons-learned/skills-quality-optimization-2026-07-02.md`。

---
最后更新: 2026-07-02（变更：添加全量A+级优化经验）
