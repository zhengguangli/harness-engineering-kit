# agents/

本 skill 配对 `orchestrator` agent——一个只读的路由顾问,为主对话推荐 skill 组合和执行顺序。

由于编排是"主对话需要持续记住才能推理"的路由知识,主对话也可以直接根据 `SKILL.md` 中的工作流和决策树执行,不一定需要 spawn 独立 agent。

---
最后更新: 2026-06-29
