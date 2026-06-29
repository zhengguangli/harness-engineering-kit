# AGENTS.md

> 这个文件是地图,不是百科全书。如果你在这里没找到答案,去下面对应的 `docs/` 文件里找——不要假设这个文件之外的信息不存在,只是它被放在了别处。

## 这个仓库是什么

<一两句话描述项目;不要展开细节,细节放 docs/product-specs/>

## 硬约束(极少数,违反即阻塞合并)

- 所有外部数据进入系统边界时必须被解析为强类型,不允许校验后继续当弱类型传递(parse, don't validate)。
- 依赖方向和分层规则见 `docs/ARCHITECTURE.md`,由 CI 中的结构化测试机械强制,不接受例外。
- <按项目实际情况补充,每条都应该是可被 lint/测试机械检查的>

## 去哪里找更多

| 我想知道… | 去看这里 |
|---|---|
| 整体架构、分层与依赖方向规则 | `docs/ARCHITECTURE.md` |
| 设计决策的背景和"核心信念" | `docs/design-docs/index.md`, `docs/design-docs/core-beliefs.md` |
| 当前/已完成的执行计划 | `docs/exec-plans/active/`, `docs/exec-plans/completed/` |
| 已知但暂不处理的技术债 | `docs/exec-plans/tech-debt-tracker.md` |
| 产品需求/功能规格 | `docs/product-specs/index.md` |
| 各领域/分层的质量评分 | `docs/QUALITY_SCORE.md` |
| 自动生成的内容(不要手改) | `docs/generated/` |
| 第三方库/工具的精简参考 | `docs/references/` |

## 工作方式提示

- 复杂、可能跨多次会话的任务,先用 `harness-exec-plans` 技能落一份 exec-plan,不要直接动手。
- 改动完成后,跑自验证循环(`harness-verification-loop`)而不是一次性提交了事。
- 涉及 UI/性能验证的改动,用 `harness-observability-and-browser` 技能产出真实证据。
- 不确定某条规则是否仍然有效?去对应的 docs 文件查"最后校验日期",过期的规则应该被标记而不是被信任。

--- 
最后更新: <YYYY-MM-DD> · 如果你修改了这个文件的结构,记得同步更新 `harness-repo-map` 技能里描述的骨架(如果有偏离)。模板文件名: `agents-md-map-template.md`。
