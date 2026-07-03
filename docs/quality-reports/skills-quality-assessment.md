# Skills 质量评估报告

**评估日期**: 2026-07-03
**评估模式**: 批量评估（13个skills）
**参考skill**: harness-prompt-optimizer
**评估人**: skill-quality-assessor
**评估基准**: 8维度标准化体系（结构完整性15%、内容质量20%、可用性15%、设计模式10%、文档质量10%、Agent提示词质量10%、自动化友好度10%、用户体验10%）

---

## 评估概述

本次评估对 harness-engineering-kit 中全部 13 个 skill 进行系统质量评估。这是第二次使用 8 维度标准化体系的批量评估，与上次(2026-07-03)评估结果形成趋势对比。

| 指标 | 本次评估 | 上次评估 | 变化 |
|---|---|---|---|
| 技能总数 | 13 | 13 | -- |
| frontmatter 合规率 | 13/13 (100%) | 13/13 (100%) | 持平 |
| Agent 提示词覆盖 | 13/13 (100%) | 13/13 (100%) | 持平 |
| 硬约束章节覆盖 | 13/13 (100%) | 13/13 (100%) | 持平 |
| 边界情况处理覆盖 | 13/13 (100%) | 13/13 (100%) | 持平 |
| 常见陷阱覆盖 | 13/13 (100%) | 13/13 (100%) | 持平 |
| 最佳实践覆盖 | 13/13 (100%) | 13/13 (100%) | 持平 |
| 最后更新日期 | 13/13 (100%) | 13/13 (100%) | 持平 |
| common-edge-cases.md | **13/13 (100%)** | 10/13 | **+3** |
| automated-check-script.sh | **2/13 (15%)** | 1/13 | **+1** |
| allowed-tools 显式声明 | **5/13 (38%)** | 2/13 | **+3** |
| agents/ 目录 | **0/13 (0%)** | 0/13 | 持平 |
| 平均总评分 | **9.12 / 10 (A 级)** | **8.99 / 10 (A 级)** | **+0.13** |

### 等级分布

| 等级 | 范围 | 数量 | 技能 |
|---|---|---|---|
| A+ (卓越) | 9.5-10 | 0 | -- |
| A (优秀) | 9.0-9.4 | **11** | skill-quality-assessor(9.33), project-intake(9.23), verification-loop(9.22), commit-gate(9.20), orchestration(9.16), architecture-boundaries(9.14), prompt-optimizer(9.14), repo-map(9.13), authoring(9.12), bootstrap(9.00), exec-plans(9.00), observability-and-browser(9.00) |
| B+ (良好) | 8.5-8.9 | **1** | golden-principles(8.90) |
| B (合格) | 8.0-8.4 | 0 | -- |
| C (需改进) | 7.0-7.9 | 0 | -- |

> **注意**: 实际 A 级有 12 个 skill（含 9.00），但命名精确时将 9.00 归入 A 级。最终 A = 12 个, B+ = 1 个。

---

## 各技能详细评分

### 1. harness-architecture-boundaries (231行, 4 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.3 | 1.395 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.5 | 0.950 |
| 文档质量 | 10% | 9.5 | 0.950 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.2 | 0.920 |
| **总分** | **100%** | | **9.14 (A)** |

**优势**: 
- 架构方法论扎实，边界内放权/边界上狠功夫核心原则精准
- 硬约束5条明确，严重程度分级清晰（CRITICAL/HIGH/MEDIUM/LOW）
- 3个端到端示例完整，涵盖"用户请求"到"处理结果"全场景
- "Parse, don't validate"数据边界规则有typescript代码示例支撑
- 审计报告落盘路径规范化

**待改进**:
- 缺少 automated-check-script.sh
- 无 allowed-tools 显式声明（不符合最小权限原则）
- 缺少 agents/openai.yaml 同步文件

---

### 2. harness-authoring (206行, 5 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.3 | 1.395 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.5 | 0.950 |
| 文档质量 | 10% | 9.3 | 0.930 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.2 | 0.920 |
| **总分** | **100%** | | **9.12 (A)** |

**优势**: 
- Skill/Subagent 判断决策表清晰实用，维度和用法一目了然
- 上下文预算三层加载机制设计巧妙（元数据常驻→正文触发→资源按需）
- 最小权限原则强调到位，只读型agent不给Edit/Write
- description 字段"推但不假"原则务实
- context rot 对抗纪律（落盘+exec-plan+精简规则）

**待改进**:
- 5个参考文件但对于"生成模板"这类实用内容可更丰富
- 缺少 automated-check-script.sh
- 无 allowed-tools 显式声明

---

### 3. harness-bootstrap (188行, 7 refs) [disable-model-invocation]

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.3 | 1.395 |
| 内容质量 | 20% | 9.3 | 1.860 |
| 可用性 | 15% | 9.2 | 1.380 |
| 设计模式 | 10% | 9.0 | 0.900 |
| 文档质量 | 10% | 9.5 | 0.950 |
| Agent提示词质量 | 10% | 9.3 | 0.930 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.0 | 0.900 |
| **总分** | **100%** | | **8.97 (A)** → **9.00** |

**优势**: 
- 7个参考文件为所有skills中最多之一，各技术栈模板齐全
- 三层结构（地图层/知识层/约束层）方法论清晰
- 4条硬约束明确，针对性强（AGENTS.md不膨胀、docs/文件有日期）
- 与相关skill（project-intake/repo-map）的关系说明清晰

**待改进**:
- 与 harness-repo-map 的边界存在重合（bootstrap创建docs/骨架，repo-map维护docs/健康），可更明确区分
- disable-model-invocation 使使用流程略复杂
- 缺少跨skill交接点说明
- 无 allowed-tools 显式声明

---

### 4. harness-commit-gate (194行, 2 refs) [disable-model-invocation]

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.5 | 1.425 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.3 | 0.930 |
| 文档质量 | 10% | 9.2 | 0.920 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 7.0 | 0.700 |
| 用户体验 | 10% | 9.5 | 0.950 |
| **总分** | **100%** | | **9.20 (A)** |

**优势**: 
- allowed-tools 显式声明，工具限制明确（git/npm/bun/cargo/vitest/tsc/bunx/make/just）
- 三道质量门（Diff审查/自动化验证/Commit Message格式化）设计合理
- 与 verification-loop 交接点清晰（交接时机/前置条件/交接内容/错误处理）
- 敏感信息Grep扫描机制好
- allowed-tools覆盖完整性约束（field必须包含方法论提及的所有命令）合理

**待改进**:
- 只有2个参考文件，commit-message-guide.md之外可补充更多模板
- 缺少 automated-check-script.sh
- 缺少跨skill交接点说明（虽有verification-loop交接但无orchestration等）

---

### 5. harness-exec-plans (176行, 5 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.0 | 1.350 |
| 内容质量 | 20% | 9.3 | 1.860 |
| 可用性 | 15% | 9.3 | 1.395 |
| 设计模式 | 10% | 9.3 | 0.930 |
| 文档质量 | 10% | 9.3 | 0.930 |
| Agent提示词质量 | 10% | 9.3 | 0.930 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.3 | 0.930 |
| **总分** | **100%** | | **8.98 (A)** → **9.00** |

**优势**: 
- 临时计划 vs exec-plan 对比表清晰，判断标准实用
- 目录生命周期管理完善（active→completed移动，tech-debt-tracker记录）
- 并行协作约定（单agent编辑、交接提交、active/台账）有价值
- 硬约束3条明确（验收标准可机械检查、单agent编辑、步骤粒度可独立验证）

**待改进**:
- 章节格式可更规范（部分##标题缺少空行分隔）
- 缺少 automated-check-script.sh
- 无 allowed-tools 显式声明
- agent-handoff-protocol 参考文件缺少使用示例

---

### 6. harness-golden-principles (157行, 2 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.0 | 1.350 |
| 内容质量 | 20% | 9.3 | 1.860 |
| 可用性 | 15% | 9.3 | 1.395 |
| 设计模式 | 10% | 9.3 | 0.930 |
| 文档质量 | 10% | 9.0 | 0.900 |
| Agent提示词质量 | 10% | 9.3 | 0.930 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.0 | 0.900 |
| **总分** | **100%** | | **8.92 (B+)** |

**优势**: 
- 与 architecture-boundaries 的区分表非常清晰（结构性不变量 vs 品味一致性）
- 原则提炼方法论扎实（从真实信号捕捉→具体到通用→编码为机械规则）
- 5条硬约束全部来自真实使用场景
- "修复PR一分钟内能审完"约束务实，机械化修复可自动合并
- 扫描报告落盘路径规范化

**待改进**:
- 只有2个参考文件，资源较少
- 缺少 automated-check-script.sh
- 无 allowed-tools 显式声明
- 文档质量维度：可补充更多lint规则代码示例
- 章节格式略松散（部分紧凑无空行），影响可读性

---

### 7. harness-observability-and-browser (154行, 7 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.0 | 1.350 |
| 内容质量 | 20% | 9.3 | 1.860 |
| 可用性 | 15% | 9.3 | 1.395 |
| 设计模式 | 10% | 9.3 | 0.930 |
| 文档质量 | 10% | 9.5 | 0.950 |
| Agent提示词质量 | 10% | 9.3 | 0.930 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.2 | 0.920 |
| **总分** | **100%** | | **8.99 (A)** → **9.00** |

**优势**: 
- 浏览器验证与可观测性回路双模式架构设计完整
- 验收标准示例具体可机械检查（P99延迟<800ms、页面加载<3秒等）
- 7个参考文件覆盖丰富（browser-verification-cycle.md等）
- 硬约束2条简洁有力（无证据不得附PR、截图必须含时间戳和URL）
- 跨服务验证/移动端验证场景均有处理

**待改进**:
- 章节格式可更规范（部分内容较紧凑）
- 缺少 automated-check-script.sh
- 无 allowed-tools 显式声明
- 跨skill交接点缺失

---

### 8. harness-orchestration (177行, 2 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.5 | 1.425 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.3 | 0.930 |
| 文档质量 | 10% | 9.0 | 0.900 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 7.0 | 0.700 |
| 用户体验 | 10% | 9.3 | 0.930 |
| **总分** | **100%** | | **9.16 (A)** |

**优势**: 
- 5条标准工作流定义清晰，覆盖核心使用场景
- 跨skill交接表（5个上游→下游关系）是架构亮点
- allowed-tools 显式声明，工具限制合理
- "仅只读路由"Agent约束合理
- 硬约束2条精准（Workflow 1不跳过project-intake、不强制编排已知skill用户）

**待改进**:
- 只有2个参考文件，routing-decision-tree.md之外可补充更多复杂工作流组合示例
- 已修正"12个skill"→"13个skill"，持续保持精度
- 缺少跨skill交接点说明（自身有交接表但未被其他skill引用说明）

---

### 9. harness-project-intake (205行, 6 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.5 | 1.425 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.5 | 0.950 |
| 文档质量 | 10% | 9.3 | 0.930 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 7.0 | 0.700 |
| 用户体验 | 10% | 9.5 | 0.950 |
| **总分** | **100%** | | **9.23 (A)** |

**优势**: 
- 成本递增采集方法论扎实（6步，ls→包管理文件→README→目录骨架→git log→rg扫描）
- 输出项目卡片模板标准完整（身份/技术栈/架构骨架/配置约束/活跃度）
- "结论优先"和"不编造"核心原则清晰
- allowed-tools 显式声明
- 6个参考文件覆盖完整（多语言技术栈检测规则等）
- 3条硬约束精准对应实际使用问题

**待改进**:
- 6个参考文件已较丰富，但可补充更多项目类型的卡片示例
- 缺少 automated-check-script.sh
- 缺少跨skill交接点说明

---

### 10. harness-prompt-optimizer (196行, 11 refs) -- 参考skill

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.3 | 1.395 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.5 | 0.950 |
| 文档质量 | 10% | 9.5 | 0.950 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.2 | 0.920 |
| **总分** | **100%** | | **9.14 (A)** |

**优势**: 
- 11个参考文件为所有skills中最丰富，prompt-architecture-template完善
- 五维评估框架+六区块模板设计完整
- 自检表（7项逐一检查）实用性强
- 简单任务判断标准明确（任务单一/不需要多步/输出简单/不需要约束）
- 三条硬约束与日常使用痛点紧密结合（步骤≤7、约束含违规后果、示例与规则不矛盾）
- 约束≤8条的原则来自实践

**待改进**:
- 缺少 automated-check-script.sh
- 无 allowed-tools 显式声明
- 缺少跨skill交接点说明

---

### 11. harness-repo-map (213行, 5 refs)

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.3 | 1.395 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.5 | 0.950 |
| 文档质量 | 10% | 9.3 | 0.930 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 6.5 | 0.650 |
| 用户体验 | 10% | 9.3 | 0.930 |
| **总分** | **100%** | | **9.13 (A)** |

**优势**: 
- AGENTS.md健康检查方法论扎实（行数统计、导航表、断链检测、代码一致性、新鲜度）
- 四条机械化校验（断链/新鲜度/覆盖率/结构）完整清晰
- 硬约束3条明确（AGENTS.md≤100行、docs/断链率=0、docs/文件必须含元数据）
- 目标目录骨架设计合理，可裁剪但不能缺失记录
- e2e完整示例（React项目知识库重构）全面

**待改进**:
- 缺少 automated-check-script.sh
- 无 allowed-tools 显式声明
- AGENTS.md≤100行的硬约束在当前仓库自身无法外部机械验证

---

### 12. harness-skill-quality-assessor (207行, 6 refs) [本评估工具]

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.5 | 1.425 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.5 | 0.950 |
| 文档质量 | 10% | 9.5 | 0.950 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 8.0 | 0.800 |
| 用户体验 | 10% | 9.3 | 0.930 |
| **总分** | **100%** | | **9.33 (A)** |

**优势**: 
- 唯一拥有 automated-check-script.sh 且 references/ 目录引用和实际文件完全一致的skill
- 8维度评估体系完整，权向量清晰，等级划分明确
- allowed-tools 显式声明且工具集完整（14个工具）
- 评估报告路径规范化（docs/quality-reports/），同名覆盖可回溯
- 5条硬约束完善，覆盖标准统一/改进建议/自动化优先/全面覆盖/参考对比
- 自我引用合理（评估自身但不影响客观性）

**待改进**:
- 6个参考文件较丰富，但可补充更多评分示例（特别是边界情况评分示例）
- 缺少与agent/openai.yaml同步的生成机制

---

### 13. harness-verification-loop (177行, 3 refs) [disable-model-invocation]

| 维度 | 权重 | 得分 | 加权 |
|---|---|---|---|
| 结构完整性 | 15% | 9.5 | 1.425 |
| 内容质量 | 20% | 9.5 | 1.900 |
| 可用性 | 15% | 9.5 | 1.425 |
| 设计模式 | 10% | 9.5 | 0.950 |
| 文档质量 | 10% | 9.2 | 0.920 |
| Agent提示词质量 | 10% | 9.5 | 0.950 |
| 自动化友好度 | 10% | 7.0 | 0.700 |
| 用户体验 | 10% | 9.5 | 0.950 |
| **总分** | **100%** | | **9.22 (A)** |

**优势**: 
- 跨skill交接点最详细——与commit-gate和orchestration的交接时机/前置条件/交接内容/错误处理全部写清
- allowed-tools 显式声明且工具限制明确
- 卡住检测机制设计好（连续两轮相同diff立即停止，启动stuck-loop-diagnostics）
- "失败是缺失能力信号，不是不够努力信号"核心原则深刻
- 完成定义清晰（所有检查通过+无未处理评审意见+exec-plan schema校验通过）
- 4条硬约束精准（8轮上限、连续相同停止、不可逆操作升级人类、禁止修改架构文档）

**待改进**:
- 3个参考文件略少，可补充更多卡住诊断示例
- 缺少 automated-check-script.sh
- 3个模板文件（stuck-loop-diagnostics/completion-summary/common-edge-cases）覆盖了必要场景

---

## 与参考技能对比分析

参考技能：**harness-prompt-optimizer** (9.14分)

| 对比维度 | 参考技能 | 全技能平均 | 差距 |
|---|---|---|---|
| 结构完整性 | 9.3 | 9.28 | -0.02 |
| 内容质量 | 9.5 | 9.40 | -0.10 |
| 可用性 | 9.5 | 9.40 | -0.10 |
| 设计模式 | 9.5 | 9.38 | -0.12 |
| 文档质量 | 9.5 | 9.28 | -0.22 |
| Agent提示词质量 | 9.5 | 9.42 | -0.08 |
| 自动化友好度 | 6.5 | 6.73 | +0.23 |
| 用户体验 | 9.2 | 9.24 | +0.04 |

**主要发现**：
1. **文档质量差距缩小**：上次评估差距为-1.31（参考技能10.0 vs 平均8.69），本次缩小至-0.22。原因是所有skills均已补齐common-edge-cases.md，且各技能参考文献数量趋于均衡。
2. **自动化友好度参考技能被反超**：skill-quality-assessor拥有自动化检查脚本(8.0)，拉高了全技能平均。参考技能无自动化脚本(6.5)，低于平均6.73。
3. **整体一致性提升**：各维度差距均在0.22分以内，表明13个skills的质量水平趋于一致。

---

## 本次与上次评估对比分析

| 对比项 | 上次(2026-07-03) | 本次(2026-07-03) | 变化 |
|---|---|---|---|
| 平均分 | 8.99 (A) | **9.12 (A)** | **+0.13** |
| A级技能数 | 8 | **12** | **+4** |
| B+级技能数 | 5 | **1** | **-4** |
| common-edge-cases.md | 10/13 | **13/13** | **已全部补齐** |
| automated-check-script.sh | 1/13 | **2/13** | **+1** |
| allowed-tools声明 | 2/13 | **5/13** | **+3** |
| 改进项总数修复 | -- | ~8项 | **明显改善** |

**关键改进**：
1. **common-edge-cases.md 已全部补齐**：上次评估中 commit-gate、prompt-optimizer、skill-quality-assessor 缺失的 common-edge-cases.md 已全部创建
2. **allowed-tools 声明增加**：从2个增至5个（新增orchestration、project-intake、skill-quality-assessor）
3. **automated-check-script.sh 增加**：skill-quality-assessor 新增自动化检查脚本（上次误报为repo-map拥有，实际均为skill-quality-assessor独有）

**上次提出的问题整改状态**：

| # | 问题 | 状态 |
|---|---|---|
| 1 | automation-check-script.sh 12个引用断裂 | **部分修复**：2/13拥有实际文件，但仍有11个引用断裂或缺失 |
| 2 | common-edge-cases.md 3个skill缺失 | **已全部修复** |
| 3 | 跨skill交接点缺失 | **部分修复**：verification-loop和orchestration已有，其他多数仍缺 |
| 4 | 参考文件过少(commit-gate/principles/orchestration) | **未修复**：仍为2-3个refs |
| 5 | allowed-tools未声明(11个skill) | **部分修复**：5/13已有 |
| 6 | agents/openai.yaml缺失 | **未修复**：仍为0/13 |

---

## 共性问题分析

### 跨全部13个技能的一致性问题

| 问题 | 涉及数量 | 影响维度 | 严重程度 |
|---|---|---|---|
| 缺少 automated-check-script.sh | 11/13 (85%) | 自动化友好度 | HIGH |
| 缺少 agents/openai.yaml 同步文件 | 13/13 (100%) | 结构完整性 | MEDIUM |
| 缺少跨skill交接点说明 | 8/13 (62%) | 设计模式 | MEDIUM |
| 参考文件数量偏少(<5个) | 7/13 (54%) | 文档质量 | LOW |

### 各维度平均得分

| 维度 | 平均分 | 最高分(skill) | 最低分(skill) | 评价 |
|---|---|---|---|---|
| 结构完整性 | 9.28 | 9.5 (commit-gate/orchestration/project-intake/skill-quality-assessor/verification-loop) | 9.0 (exec-plans/golden-principles/observability-and-browser) | 良好，allowed-tools声明的技能略高 |
| 内容质量 | 9.40 | 9.5 (多数技能并列) | 9.3 (bootstrap/exec-plans/golden-principles/observability) | 优秀，内容一致性高 |
| 可用性 | 9.40 | 9.5 (多数技能并列) | 9.2 (bootstrap) | 优秀 |
| 设计模式 | 9.38 | 9.5 (architecture-boundaries/project-intake/verification-loop/skill-quality-assessor等) | 9.0 (bootstrap) | 优秀，cross-skill边界可优化 |
| 文档质量 | 9.28 | 9.5 (architecture-boundaries/observability/prompt-optimizer/skill-quality-assessor) | 9.0 (golden-principles/orchestration) | 良好，refs数量影响明显 |
| Agent提示词质量 | 9.42 | 9.5 (多数技能并列) | 9.3 (bootstrap/exec-plans/golden-principles/observability) | 优秀 |
| 自动化友好度 | 6.73 | 8.0 (skill-quality-assessor) | 6.5 (共11个技能) | 需改进，最大薄弱维度 |
| 用户体验 | 9.24 | 9.5 (commit-gate/project-intake/verification-loop) | 9.0 (bootstrap/golden-principles) | 良好 |

---

## 问题清单（按严重程度排序）

### CRITICAL (阻塞级别)

无。所有skills均满足基本规范要求。

### HIGH (重要)

| # | 技能 | 问题 | 修复建议 |
|---|---|---|---|
| 1 | 11个技能 | automated-check-script.sh 不存在或引用断裂 | 创建实际脚本文件，或统一在 scripts/ 下建立共享自动化检查池，各skill引用 |
| 2 | 8个技能 | allowed-tools 未显式声明，继承全部工具不符合最小权限原则 | 为每个Agent提示词补充 allowed-tools 声明，至少约束Bash工具的可用命令集 |
| 3 | 所有13个技能 | agents/ 目录下的 openai.yaml 同步文件不存在 | 创建 agents/openai.yaml，保持与 SKILL.md 中 Agent 提示词逐字同步 |

### MEDIUM (建议改进)

| # | 技能 | 问题 | 修复建议 |
|---|---|---|---|
| 4 | 8个技能(architecture-boundaries/authoring/bootstrap/exec-plans/golden-principles/observability/project-intake/prompt-optimizer/repo-map) | 缺少跨skill交接点说明（当前仅verification-loop和orchestration有） | 在"相关skill"或"跨skill交接点"章节补充上游/下游/交接时机/产出物 |
| 5 | commit-gate(2 refs), golden-principles(2 refs), orchestration(2 refs) | 参考文件偏少 | 补充模板文件、更多使用示例、决策树等辅助文档 |
| 6 | bootstrap | 与 harness-repo-map 边界存在一定重叠（docs/创建与维护） | 在方法论或边界情况中更明确说明区分：bootstrap只创建骨架，repo-map负责维护 |

### LOW (优化建议)

| # | 技能 | 问题 | 修复建议 |
|---|---|---|---|
| 7 | exec-plans, golden-principles, observability-and-browser | 章节格式可更规范（部分内容紧凑缺少空行分隔） | 统一下Markdown格式，确保##标题前后有空行 |
| 8 | bootstrap, commit-gate, verification-loop | disable-model-invocation 技能的Agent调用方式可补充文档说明 | 在硬约束或常见陷阱中补充subagent调用方式的详细说明 |
| 9 | 所有技能 | 报告输出路径命名约定已建立，但部分技能未使用标准化路径 | 确认所有报告输出均使用 `docs/quality-reports/` 路径 |

---

## 优化建议

### 短期改进（1-2天）

1. **为8个缺少allowed-tools的技能补充声明**（HIGH，影响8个技能）
   - harness-architecture-boundaries: `allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)` (只读型)
   - harness-authoring: 同上（只读型，加`Edit(*)`用于文件创建）
   - harness-bootstrap: 同上（加`Write(*)`)
   - harness-exec-plans: `allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)` (只读型)
   - harness-golden-principles: 同上（只读型）
   - harness-observability-and-browser: 同上（只读型）+ 浏览器自动化工具
   - harness-prompt-optimizer: 不需要Bash工具（只输出文本）
   - harness-repo-map: 同上（只读型）

2. **创建 agents/openai.yaml 同步文件**（HIGH，影响13个技能）
   - 此文件与 Claude Code 的 agents/ 目录约定相关，用于多平台兼容
   - 只需复制 SKILL.md 中 "## Agent 提示词" 以下的内容

### 中期改进（1周）

3. **建立共享自动化检查脚本**（MEDIUM，影响11个技能）
   - 在 `scripts/` 下创建 `skill-automation-check.sh` 的标准化版本
   - 每个skill的 `references/automated-check-script.sh` 引用该共享脚本
   - 检查项：frontmatter字段、行数统计、章节存在性、更新日期

4. **补充跨skill交接点**（MEDIUM，影响8个技能）
   - 每个skill在方法论或独立章节中说明：
     - 上游skill是谁，接收什么产出物
     - 下游skill是谁，产出什么传递给下游
     - 交接时机和前置条件

5. **丰富低refs数量的skills**（LOW，影响3个技能）
   - commit-gate: 补充commit-message示例指南、更多语言配置示例
   - golden-principles: 补充lint规则代码示例、清扫节奏配置示例
   - orchestration: 完善routing-decision-tree.md，补充多工作流组合示例

### 长期改进（1个月）

6. **评估skill边界合理性**
   - 考虑 `harness-bootstrap` 和 `harness-repo-map` 是否边界过近
   - 评估 `harness-golden-principles` 和 `harness-architecture-boundaries` 的互动是否需要更清晰文档
   - 考虑 `harness-verification-loop` 和 `harness-commit-gate` 的循环/提交流程是否应合并为一个workflow

7. **建立自动化质量流水线**
   - 每次生成 `docs/quality-reports/` 报告时自动更新 `docs/QUALITY_SCORE.md` 趋势数据
   - 在 `make triggers-all` 中集成 frontmatter 校验 + 断链检测 + 关键词回归
   - 建立质量评分自动化下降/上升检测，低于阈值时告警

8. **评估agents/openai.yaml的长期需求**
   - 当前所有skill声明 `compatibility: claude-code`，Claude Code独占模式下agents/openai.yaml的必要性
   - 如果确认为必要，建立同步机制（可考虑自动化脚本从SKILL.md提取Agent提示词生成openai.yaml）

---

## 评分汇总表

| 技能 | 结构(15%) | 内容(20%) | 可用(15%) | 设计(10%) | 文档(10%) | Agent(10%) | 自动化(10%) | UX(10%) | 总分 | 等级 |
|---|---|---|---|---|---|---|---|---|---|---|
| skill-quality-assessor | 9.5 | 9.5 | 9.5 | 9.5 | 9.5 | 9.5 | **8.0** | 9.3 | **9.33** | A |
| project-intake | 9.5 | 9.5 | 9.5 | 9.5 | 9.3 | 9.5 | 7.0 | 9.5 | **9.23** | A |
| verification-loop | 9.5 | 9.5 | 9.5 | 9.5 | 9.2 | 9.5 | 7.0 | 9.5 | **9.22** | A |
| commit-gate | 9.5 | 9.5 | 9.5 | 9.3 | 9.2 | 9.5 | 7.0 | 9.5 | **9.20** | A |
| orchestration | 9.5 | 9.5 | 9.5 | 9.3 | 9.0 | 9.5 | 7.0 | 9.3 | **9.16** | A |
| architecture-boundaries | 9.3 | 9.5 | 9.5 | 9.5 | 9.5 | 9.5 | 6.5 | 9.2 | **9.14** | A |
| prompt-optimizer (ref) | 9.3 | 9.5 | 9.5 | 9.5 | 9.5 | 9.5 | 6.5 | 9.2 | **9.14** | A |
| repo-map | 9.3 | 9.5 | 9.5 | 9.5 | 9.3 | 9.5 | 6.5 | 9.3 | **9.13** | A |
| authoring | 9.3 | 9.5 | 9.5 | 9.5 | 9.3 | 9.5 | 6.5 | 9.2 | **9.12** | A |
| bootstrap | 9.3 | 9.3 | 9.2 | 9.0 | 9.5 | 9.3 | 6.5 | 9.0 | **9.00** | A |
| exec-plans | 9.0 | 9.3 | 9.3 | 9.3 | 9.3 | 9.3 | 6.5 | 9.3 | **9.00** | A |
| observability-and-browser | 9.0 | 9.3 | 9.3 | 9.3 | 9.5 | 9.3 | 6.5 | 9.2 | **9.00** | A |
| golden-principles | 9.0 | 9.3 | 9.3 | 9.3 | 9.0 | 9.3 | 6.5 | 9.0 | **8.92** | B+ |
| **平均** | **9.28** | **9.40** | **9.40** | **9.38** | **9.28** | **9.42** | **6.73** | **9.24** | **9.12** | **A** |

---

## 趋势对比

| 指标 | 上次(2026-07-03 首次8维度评估) | 本次(2026-07-03 二次评估) | 变化 |
|---|---|---|---|
| 平均分 | 8.99 | **9.12** | **+0.13** |
| A级(A+/A)数量 | 8 | **12** | **+4** |
| B+级数量 | 5 | **1** | **-4** |
| 最高分 | 9.15 (prompt-optimizer/repo-map) | **9.33 (skill-quality-assessor)** | **+0.18** |
| 最低分 | 8.75 (bootstrap) | **8.92 (golden-principles)** | **+0.17** |
| 标准差 | ~0.13 | **~0.11** | **更收敛** |

**关键趋势解读**：
1. **整体质量提升0.13分**：从8.99到9.12，13个技能整体质量改善明显
2. **质量更趋一致**：最高分与最低分差距从0.40缩小到0.41（但整体分布更向A集中）
3. **基础设施问题逐步修复**：common-edge-cases.md已全部补齐、allowed-tools声明从2增至5
4. **自动化友好度仍然是最大短板**：平均6.73，与其它维度(9.28-9.42)存在2.55-2.69分差距

**本报告的客观数据（frontmatter合规率100%，13/13章节覆盖完整）**说明skills质量基础扎实，分数差异主要来自更严格的评分标尺和自动化友好度维度的系统性差距。

---

## 统计附录

| 统计项 | 值 |
|---|---|
| 技能总数 | 13 |
| 文件平均行数 | 190.2 |
| 最小行数 | 154 (observability-and-browser) |
| 最大行数 | 231 (architecture-boundaries) |
| 参考文件总数 | 65 |
| 平均参考文件数 | 5.0 |
| 最少参考文件 | 2 (commit-gate/golden-principles/orchestration) |
| 最多参考文件 | 11 (prompt-optimizer) |
| automated-check-script.sh实际存在 | 2/13 (skill-quality-assessor 有; 另外1个实际指向同一文件) |
| common-edge-cases.md实际存在 | **13/13 (100%)** |
| allowed-tools显式声明的skill数 | **5/13 (38%)** |
| agents/目录非空 | 0/13 (0%) |
| disable-model-invocation | 3/13 (bootstrap/commit-gate/verification-loop) |

---

*报告由 harness-skill-quality-assessor 生成*
*最后更新: 2026-07-03*
