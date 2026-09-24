# Changelog

本文件只记录**架构级变更**：新的契约/不变量、CI 行为变更、验证方法论变更、
核心依赖变更。逐 commit 的流水账看 `git log`。

格式遵循 `AGENTS.md` §6：Context & Trade-offs / Impact Radius。

---

## [2026-09-24] depends_on 契约与依赖机械强制

- **Context & Trade-offs**: TD-001（skill 间循环依赖仅靠人工 review）在 13 个 skill 的规模下已不可靠。
  在"新增 frontmatter 字段"与"改写 Related Skills 标注体系"之间选择了前者——后者需要把 13 个
  SKILL.md 的相关章节全部重写，且 `Upstream`/`Downstream` 在现有内容里有两种相反语义
  （"我消费它的产出" vs "它调用我"），无法无歧义地机械解析。代价是每个 SKILL.md 多一个字段。
- **Impact Radius**:
  - 全部 13 个 `skills/*/SKILL.md` — 新增 `depends_on` frontmatter（14 条依赖边，零循环，全部向下）
  - `scripts/validate_skill_dependencies.py` — 新增，5 类校验：环检测 / 向下流动 / Meta 层隔离 /
    引用有效性 / 跨 skill `../harness-*/references/*` 路径存在性
  - `scripts/run-all.py` — 新增第四阶段 `deps`，CI 自动继承（**deps 失败即阻断 PR**）
  - `tests/dependencies/test_dependency_validation.py` — 新增，18 个标准库 unittest 用例
  - `docs/ARCHITECTURE.md` — 新增 "Declaring a dependency" 契约说明

## [2026-09-24] 质量评估方法论由主观加权分改为机械检查点审计

- **Context & Trade-offs**: 第 1-33 轮的 9.xx 分依赖评估者对 clarity / executability / UX 等维度的
  主观判断，且 13 个 skill 已密集分布在 9.42-9.50——分差落入评估噪声，继续加权打分只会产生分数通胀。
  改为对 rubric 中可客观判定的检查点做全量机械审计。代价是失去单一可比较的总分。
- **Impact Radius**:
  - `docs/QUALITY_SCORE.md`、`docs/quality-reports/skills-quality-assessment.md` — 记录第 34 次审计
  - 第 33 次的 5 A+ / 8 A、平均 9.46 保留为**最后一次主观评估结果**，未被覆盖
  - 若需新的 A+ 判定，必须由 `harness-skill-quality-assessor` 按 rubric 人工执行

## [2026-09-24] SKILL.md 规范章节顺序确立

- **Context & Trade-offs**: 13 个 skill 的章节顺序分裂为多个变体（5 个把 `Related Skills` 放在
  `Best Practices` 之前，8 个放在之后；3 个把 `Key Points` 放在 `Examples` 之前）。
  顺序取全库**众数位置**而非个人偏好，使其可被无争议地收敛。8 个 skill 被重排，
  安全性校验：标题集合与总行数均未变化。
- **Impact Radius**:
  - `docs/ARCHITECTURE.md` — 新增 "Canonical section order" 章节，列出 13 个章节的规定顺序
  - 8 个 `skills/*/SKILL.md` — 章节重排（内容零变更）
  - `harness-orchestration` 的 `Routing Recommendation` 移至 `Methodology` 之后

## [2026-09-24] CI 分支门禁规则修正

- **Context & Trade-offs**: 原规则要求 `head_ref == "developer"`，但仓库在 `aee5cec` 已把该分支
  改名为 `develop`，导致**所有** PR 都被阻断，且错误信息指向一个不存在的分支名，极难排查。
  改为集合匹配 `develop|main|release/*`，符合 gitflow。
- **Impact Radius**:
  - `.github/workflows/skill-triggers.yml` — job 改名 `enforce-developer-flow` → `enforce-branch-flow`，
    规则由全等比较改为集合匹配（**行为变更**）
  - `.github/pull_request_template.md` — 修正分支名，并将死命令 `make triggers-all`
    （Makefile 不存在）替换为 `python3 scripts/run-all.py`

## [2026-09-24] 质量报告纳入版本控制

- **Context & Trade-offs**: `.gitignore` 忽略 `docs/quality-reports/*.md`，但
  `skills-quality-assessment.md` 实际被 git 跟踪——同一目录两种状态，导致新的质量报告**无法提交**。
  删除该忽略规则。副作用：此前被忽略的 `harness-commit-gate-check.md`（2026-07-06 一次性输出，
  无任何引用）变为可提交，已删除。
- **Impact Radius**:
  - `.gitignore` — 删除质量报告忽略规则
  - `docs/quality-reports/harness-commit-gate-check.md` — 删除

---

最后更新: 2026-09-24
