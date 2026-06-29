# Golden Principles（黄金原则）

把人类的经验和品味编码为可机械化检查的规则。由 `entropy-collector` agent 在周期性清扫时对照执行。

黄金原则 ≠ 架构边界。架构边界是结构性不变量（阻塞合并），黄金原则是品味一致性（周期性清扫修复）。详见 `harness-golden-principles` 技能。

## 原则列表

### GP-01: 禁止跨 skill 直接引用

- **规则**: `skills/harness-X/` 内的任何文件不得包含对 `skills/harness-Y/`（X ≠ Y）的路径引用。跨 skill 引用只通过 `docs/` 做单向指向。
- **检查**:
  - 路径引用: `rg 'skills/harness-(?!${CURRENT_SKILL})' skills/harness-*/` 在每个 skill 目录内执行
  - 间接引用: `for skill_dir in skills/harness-*/; do name=$(basename "$skill_dir"); rg -o 'references/[a-zA-Z0-9_-]+\.md' "$skill_dir/SKILL.md" --no-filename 2>/dev/null | while read ref; do [ ! -f "$skill_dir$ref" ] && echo "FAIL: $name -> $ref (文件不在本 skill 的 references/ 中)"; done; done`
- **修复**: 将跨 skill 引用改为指向 `docs/` 中对应的索引/地图条目
- **违反后果**: 进入清扫队列，低风险自动合并修复

### GP-02: agent 提示词必须声明权限边界

- **规则**: 每个 `references/*-prompt.md` 必须包含工具风险声明段落，明确说明该 agent 是只读型还是执行型，以及哪些工具可用、哪些被禁止。
- **检查**: `for f in skills/*/references/*-prompt.md; do grep -qE '工具风险声明|只读|执行型|read.only|禁止|授权的写' "$f" \|\| echo "FAIL: $f"; done`
- **修复**: 在提示词文件开头附近添加"## 工具风险声明"段落
- **违反后果**: 进入清扫队列，低风险自动合并修复

### GP-03: openai.yaml 必须包含完整三区块

- **规则**: 每个 `agents/openai.yaml` 必须包含 `metadata`、`tools`、`system_prompt` 三个区块，且 `system_prompt` 行数 ≥ 10。
- **检查**: `for f in skills/*/agents/openai.yaml; do blocks=$(grep -cE '^(metadata|tools|system_prompt):' "$f"); [ "$blocks" -lt 3 ] && echo "FAIL: $f (只有 $blocks 个区块)"; lines=$(sed -n '/^system_prompt:/,$ p' "$f" | sed '/^[[:space:]]*$/d' | wc -l); [ "$lines" -lt 10 ] && echo "FAIL: $f system_prompt 行数不足 ($lines 行)"; done`
- **修复**: 参考 `skills/harness-repo-map/agents/openai.yaml` 的格式补齐
- **违反后果**: 进入清扫队列，低风险自动合并修复

### GP-04: 模板文件必须包含占位符和使用说明

- **规则**: `references/*-template.md` 不得为空骨架，必须包含至少一个 `<placeholder>` 标记和填写指引说明。
- **检查**: `for f in skills/*/references/*-template.md; do [ ! -s "$f" ] && echo "FAIL: $f 为空文件"; grep -q '<' "$f" \|\| echo "WARN: $f 可能缺少占位符标记"; done`
- **修复**: 参考 `skills/harness-repo-map/references/agents-md-map-template.md` 的格式补充内容
- **违反后果**: 进入清扫队列，低风险自动合并修复

### GP-05: 单个 SKILL.md 不超过 200 行

- **规则**: SKILL.md 是方法论正文，被注入主对话上下文。超过 200 行说明在写百科全书而非方法论，应将细节拆分到 `references/` 下的独立参考文件。
- **检查**: `for f in skills/*/SKILL.md; do lines=$(wc -l < "$f"); [ "$lines" -gt 200 ] && echo "FAIL: $f ($lines 行，上限 200)"; done`
- **修复**: 将超出部分提取到 `references/` 下的独立文件，SKILL.md 中保留摘要和指向链接
- **违反后果**: 进入清扫队列，需人工判断哪些内容可以拆分

## 扫描节奏

- **触发时机**: `commit-gate` 提交前或 `verification-loop` 自验证循环中按需触发
- **执行者**: `entropy-collector` agent
- **扫描范围**: 全部 11 个 skill + `docs/` 结构
- **修复粒度**: 每个偏差生成独立的小颗粒度修复（一个 PR 只修一处偏差）
- **偏差记录**: 未处理/暂缓处理的偏差记录进 `docs/exec-plans/tech-debt-tracker.md`

---
最后更新: 2026-06-29
