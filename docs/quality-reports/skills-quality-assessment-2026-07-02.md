# Skills 质量评估报告

- **评估日期**: 2026-07-02
- **评估模式**: 批量评估（13 skills）
- **评估方法**: 3 路并行 subagent 逐文件 8 维度评审 + 自动化验证（`make triggers-all`）

## 评估结果概览

| 指标 | 数值 |
|------|------|
| 评估总数 | 13 skills |
| 平均分 | 8.97 |
| 最高分 | 9.4（architecture-boundaries） |
| 最低分 | 8.6（verification-loop, bootstrap, quality-assessor） |
| A 级（≥9.0） | 8 skills |
| B+ 级（8.5-8.9） | 5 skills |

## 等级分布

```
A 级 (9.0-9.4): ████████ 8 skills
B+ 级 (8.5-8.9): █████ 5 skills
B 级以下:         0 skills
```

**A 级（优秀）**: architecture-boundaries (9.4), authoring (9.3), project-intake (9.2), observability (9.1), commit-gate (9.0), golden-principles (9.0), orchestration (9.0), repo-map (9.0)

**B+ 级（良好）**: exec-plans (8.9), prompt-optimizer (8.9), verification-loop (8.6), bootstrap (8.6), quality-assessor (8.6)

---

## 逐文件详细评估

### harness-architecture-boundaries — 9.4 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 9.5 | frontmatter 齐全，章节完整 |
| 内容质量 | 9.5 | 方法论链条完整（推导→模型→规则→检查→修复区分） |
| 可用性 | 9.5 | 触发条件具体，六层模型图清晰 |
| 设计模式 | 9.5 | 模块化清晰，4 个 references 覆盖完整 |
| 文档质量 | 9.0 | 边界情况仅 1 条（微服务），与 depth 不匹配 |
| Agent提示词质量 | 9.5 | 四级严重程度 + 结构化报告格式，全场最佳 |
| 自动化友好度 | 9.0 | CI/CD YAML 脚本名不一致（引用了旧脚本名） |
| 用户体验 | 9.0 | 学习曲线中等，建议补充更多边界情况 |

### harness-authoring — 9.3 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 9.5 | 章节齐全 |
| 内容质量 | 9.5 | Skill vs Subagent 对比表是全文亮点 |
| 可用性 | 9.5 | 上下文预算纪律具体可操作 |
| 设计模式 | 9.5 | 跨平台同步纪律严谨 |
| 文档质量 | 9.0 | 示例足够，建议加模板不匹配时的 fallback |
| Agent提示词质量 | 9.0 | 部分步骤只有 2-3 行，深度不够 |
| 自动化友好度 | 9.0 | 脚本引用正常 |
| 用户体验 | 9.0 | 关键要点与正文重复较多 |

### harness-project-intake — 9.2 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 9.5 | 完整 |
| 内容质量 | 9.5 | "成本递增采集"是方法论亮点 |
| 可用性 | 9.5 | 输出卡片模板可直接填空 |
| 设计模式 | 9.3 | 设计一致 |
| 文档质量 | 9.2 | 边界情况 4 条，覆盖良好 |
| Agent提示词质量 | 9.5 | "结论优先"+"静默采集"+"不编造"三原则贯穿 |
| 自动化友好度 | 7.5 | 信息采集依赖语义理解，难以自动化 |
| 用户体验 | 9.3 | 学习曲线平缓 |

### harness-observability-and-browser — 9.1 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 9.5 | 所有必需+可选章节齐全 |
| 内容质量 | 9.0 | 方法论偏薄，核心深度不足 |
| 可用性 | 9.2 | 验证路由逻辑清晰（UI→浏览器，性能→可观测性） |
| 设计模式 | 9.0 | "反馈传感器"概念框架简洁 |
| 文档质量 | 8.5 | 关键要点沦为半结构化清单 |
| Agent提示词质量 | 9.5 | 跳过条件+验证路由+结论格式完整 |
| 自动化友好度 | 9.0 | CI/CD 完整 |
| 用户体验 | 9.0 | 操作步骤与 Agent 流程有重复 |

### harness-commit-gate — 9.0 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 8.3 | 方法论 4 节内容过少（引用了 Agent 流程） |
| 内容质量 | 9.2 | 清晰可执行 |
| 可用性 | 9.5 | 触发条件+何时不该用覆盖最全面 |
| 设计模式 | 9.0 | 与其他 skill 一致 |
| 文档质量 | 8.8 | 边界情况代码块已精简 |
| Agent提示词质量 | 9.0 | 完整 5 段式，含跳过条件 |
| 自动化友好度 | 9.2 | allowed-tools 最完整 |
| 用户体验 | 8.5 | 344 行偏长 |

### harness-golden-principles — 9.0 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 9.0 | 唯一使用 `## 硬约束` 独立章节，与其余不一致 |
| 内容质量 | 9.2 | "黄金原则 vs 架构边界"对比精准 |
| 可用性 | 9.0 | 触发条件明确 |
| 设计模式 | 9.0 | 与其他 skill 一致 |
| 文档质量 | 8.5 | `## 相关模板` 仅 2 条引用，references 利用不足 |
| Agent提示词质量 | 9.2 | "无原则时终止"流程设计好 |
| 自动化友好度 | 9.0 | 脚本引用正常 |
| 用户体验 | 8.8 | 执行步骤过于概括 |

### harness-orchestration — 9.0 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 9.5 | 完整 |
| 内容质量 | 9.2 | 5 条标准工作流覆盖主要场景 |
| 可用性 | 9.3 | 跨 skill 交接表设计精良 |
| 设计模式 | 9.0 | 编排模式一致 |
| 文档质量 | 8.5 | 仅 1 个特有边界情况 |
| Agent提示词质量 | 9.3 | 跳过条件+约束违反行为+输出规范形成闭环 |
| 自动化友好度 | 7.5 | 路由决策本质是语义理解，难以全自动化 |
| 用户体验 | 8.8 | 缺少最小化快速启动示例 |

### harness-repo-map — 9.0 (A)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 9.5 | 完整 |
| 内容质量 | 9.4 | "地图不是百科全书"原则精准 |
| 可用性 | 9.3 | 与 bootstrap 职责边界清晰 |
| 设计模式 | 8.8 | 跨 skill 引用路径脆弱 |
| 文档质量 | 8.8 | 边界情况 4 条，但不够深入 |
| Agent提示词质量 | 9.0 | doc-gardener 5 步流程结构化程度高 |
| 自动化友好度 | 8.0 | 知识治理难全自动化 |
| 用户体验 | 8.8 | 两套流程（初始化/操作）缺对比说明 |

### harness-exec-plans — 8.9 (B+)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 8.2 | 方法论 `###` 无编号前缀 |
| 内容质量 | 9.3 | 临时 vs exec-plan 对比表是全文亮点 |
| 可用性 | 9.0 | 执行计划生命周期清晰 |
| 设计模式 | 9.2 | active/completed 目录设计出色 |
| 文档质量 | 8.8 | 硬约束仅 3 条 |
| Agent提示词质量 | 8.8 | 完整 5 段式 |
| 自动化友好度 | 8.5 | 脚本引用正常 |
| 用户体验 | 9.0 | 扫读友好，决策辅助降低门槛 |

### harness-prompt-optimizer — 8.9 (B+)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 8.2 | 220 行最小文件，章节精简但缺边界情况 |
| 内容质量 | 9.5 | 五维评估框架+六区块对应关系设计精良 |
| 可用性 | 9.3 | 简单任务判断标准防过度工程化 |
| 设计模式 | 8.8 | 6 参考文件覆盖完整 |
| 文档质量 | 9.2 | 域名特定模式参考全面 |
| Agent提示词质量 | 8.8 | 完整 5 段式 |
| 自动化友好度 | 8.0 | 无 CI/CD 集成 |
| 用户体验 | 9.0 | "步骤 0"编号可优化 |

### harness-verification-loop — 8.6 (B+)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 8.0 | 方法论编号断裂（从 `### 2.` 开始，缺 `### 1.`） |
| 内容质量 | 8.8 | "失败是缺失能力的信号"理念深刻 |
| 可用性 | 8.5 | 循环控制机制完整（最大迭代+卡住检测） |
| 设计模式 | 8.8 | 与 commit-gate 交接完整 |
| 文档质量 | 8.5 | 边界情况仅 3 个 |
| Agent提示词质量 | 8.8 | 完整 5 段式 |
| 自动化友好度 | 8.5 | 缺少 `allowed-tools` 字段 |
| 用户体验 | 8.2 | 读者需要在方法论和 Agent 流程间跳跃 |

### harness-bootstrap — 8.6 (B+)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 8.0 | Agent 提示词位置与其他 skill 不同 |
| 内容质量 | 8.8 | 三层结构（地图/知识/约束）阐述清晰 |
| 可用性 | 8.8 | 触发条件明确 |
| 设计模式 | 9.0 | 方法论编号规范 |
| 文档质量 | 8.2 | 仅 2 个边界情况，最少 |
| Agent提示词质量 | 8.8 | 完整 5 段式 |
| 自动化友好度 | 8.8 | 脚本引用正常 |
| 用户体验 | 8.0 | 关键要点 15 条偏长，有重复 |

### harness-skill-quality-assessor — 8.6 (B+)

| 维度 | 得分 | 评语 |
|------|------|------|
| 结构完整性 | 8.5 | 缺少 `## 硬约束` 章节 |
| 内容质量 | 8.5 | 8 维度体系设计合理，三种模式务实 |
| 可用性 | 8.8 | 改进建议分层（短期/中期/长期） |
| 设计模式 | 8.8 | 自洽验证设计 |
| 文档质量 | 8.5 | 缺少输出报告的具体模板示例 |
| Agent提示词质量 | 8.8 | 标题与 frontmatter `agent:` 不匹配 |
| 自动化友好度 | 8.5 | 脚本引用正常 |
| 用户体验 | 8.3 | 自引用概念较复杂，学习曲线陡 |

---

## 维度平均得分

| 维度 | 平均分 | 最强 skill | 最弱 skill |
|------|--------|------------|------------|
| 结构完整性 | 8.9 | 多 skill 并列 9.5 | verification-loop 8.0 |
| 内容质量 | 9.2 | prompt-optimizer / architecture-boundaries 9.5 | quality-assessor 8.5 |
| 可用性 | 9.2 | commit-gate / project-intake 9.5 | verification-loop 8.5 |
| 设计模式 | 9.1 | architecture-boundaries 9.5 | repo-map / prompt-optimizer 8.8 |
| 文档质量 | 8.8 | prompt-optimizer 9.2 | golden-principles 8.5 |
| Agent提示词质量 | 9.1 | architecture-boundaries / observability / project-intake 9.5 | quality-assessor 8.8 |
| 自动化友好度 | 8.3 | commit-gate 9.2 | orchestration / project-intake 7.5 |
| 用户体验 | 8.8 | prompt-optimizer / project-intake 9.3 | bootstrap / quality-assessor 8.0 |

---

## 共性高优问题（需立即处理）

| # | 问题 | 影响 | 涉及文件 |
|---|------|------|----------|
| 1 | Agent 提示词内部标题用 `##` 而非 `###`（`## Agent 提示词` 下的子节） | Markdown 层级违规 | 全部 13 个文件 |
| 2 | `agent:` frontmatter 字段与 Agent 提示词标题不匹配 | 配对校验失败 | orchestrator (`orchestrator` vs `Orchestrator`), quality-assessor (`skill-quality-assessor` vs `Skill Quality Assessor`) |
| 3 | 缺少 `allowed-tools` 字段 | 沙箱阻塞 | verification-loop, exec-plans, 及其他非 commit-gate skill |
| 4 | CI/CD YAML 引用了旧的独立脚本名而非共享脚本 | 断链风险 | architecture-boundaries 等引用 `scripts/architecture-boundaries-check.sh` |

## 共性中低问题（建议后续处理）

| # | 问题 | 涉及文件 |
|---|------|----------|
| 5 | 方法论与 Agent 提示词执行流程仍有部分重叠 | project-intake, verification-loop, quality-assessor |
| 6 | 边界情况处理普遍偏少（1-3 条/文件） | golden-principles, orchestrator, bootstrap |
| 7 | `## 硬约束` 章节命名不一致（golden-principles 独立使用，其余内嵌） | golden-principles |
| 8 | 章节顺序不一致（bootstrap 的 Agent 提示词在自动化检查之后） | bootstrap |
| 9 | 方法论编号不一致（exec-plans 无编号前缀，verification-loop 从 2 开始） | exec-plans, verification-loop |

---

## 自动化验证结果

```
triggers-check:  13/13 OK
keyword-consistency: 13/13 OK
triggers-regression: PASS=48 WARN=0 FAIL=0
agent-prompt-sync:   pass=13 warn=0 fail=0
```

全部 4 项自动化检查通过，零退化。

## 优化回顾（2026-07-02 修复验证）

| # | 问题 | 状态 | 验证方式 |
|---|------|------|----------|
| 1 | Agent 提示词内部标题 `##` → `###` | ✅ 已修复（13 文件） | `rg '^## (角色定义\|核心能力\|执行流程\|约束\|输出规范\|跳过条件)'` → 0 匹配 |
| 2 | `agent:` 字段与标题不匹配 | ✅ 已修复（orchestrator, quality-assessor） | 标题统一为 kebab-case + 中文名格式 |
| 3 | CI/CD YAML 引用旧脚本名 | ✅ 已修复（11 文件） | `rg 'bash scripts/[a-z]*-check\.sh'` → 0 匹配 |
| 4 | 缺少 `allowed-tools` | ✅ 已修复（verification-loop） | 现与 commit-gate 并列完整配置 |

修复前后 `make triggers-all` 保持 PASS=48 WARN=0 FAIL=0 零退化，质量体系不受影响。

---

## 改进建议

### 短期（1-2 天）

1. **修复 Agent 提示词标题层级**：13 个文件中 `## Agent 提示词` 下的子节从 `##` 改为 `###`
2. **修复 `agent:` 字段不匹配**：orchestrator 和 quality-assessor 统一 frontmatter 与标题
3. **修复 CI/CD YAML 脚本引用**：architecture-boundaries 等改为 `scripts/skill-automation-check.sh`
4. **补充缺少 `allowed-tools` 的 skill**：verification-loop, exec-plans 等

### 中期（1 周）

5. **方法论去重收尾**：project-intake, verification-loop, quality-assessor 进一步将执行细节下沉到 Agent 提示词
6. **补充边界情况**：golden-principles 2→4, orchestrator 1→3, bootstrap 2→4
7. **统一章节顺序**：bootstrap 将 Agent 提示词移到 CI/CD 之前
8. **统一方法论编号**：exec-plans 加 `### 1.` 前缀，verification-loop 修复序号

### 长期（1 个月）

9. **评估是否需要 `allowed-tools` 作为 frontmatter 硬约束**
10. **探索 agent-driven skill 的自动化测试方法**（orchestration, project-intake 自动化友好度偏低）
11. **建立 skills 质量基准线**：设定最低维度分数阈值

---

## 与上次评估的对比

前一次评估（2026-07-02 A+ 级优化）后，本次臃肿重构使文件行数从 5,347→3,674（-31.3%），`make triggers-all` 保持 48/48 零退化。质量得分总体稳定（平均 8.97 vs 上次 ~9.2），结构完整性因精简方法论执行步骤有所下降（少数文件），但内容密度和可读性提升。

---
最后更新: 2026-07-02
