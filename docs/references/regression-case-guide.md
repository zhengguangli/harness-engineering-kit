# 回归用例维护规范（Case Guide）

新增或修改回归用例时，请遵循：

- 用例文件：`tests/triggers/cases.json`
- 每条 case 至少包含：
  - `id`：唯一 ID，建议格式 `skill-topic-NN`
  - `input`：自然语言输入（尽量贴近用户原话）
  - `expected_primary_skill`：首选命中 skill
  - `expected_candidates`：可接受候选列表（用于歧义场景）
  - `tags`：分类标签（如 `commit`、`plan`、`ambiguous`）

#### 判定规则

- `PASS`：主 skill 命中且为最强信号
- `WARN`：主 skill 命中但不是最强信号（候选歧义仍存在）
- `FAIL`：主 skill 未命中

#### 关键词一致性要求

回归脚本依赖静态关键词映射（`scripts/run_trigger_regression.py` 中的 `SKILL_KW`）。  
当你新增 case 时，务必保证：

1. 所有用于匹配的关键词在对应 `SKILL.md` 中真实存在
2. 避免“只改用例、不改关键词”导致结果漂移

#### 报告与产物

- 回归报告：`tests/triggers/report.json`（`python3 scripts/run-all.py --run-type regression --json` 生成）
- 推荐更新节奏：每次修改触发词/用例后都跑一次 `python3 scripts/run-all.py`
