<!-- 各技术栈 docs/ 骨架模板 — 由 harness-bootstrapper agent 使用 -->
<!-- 根据项目技术栈选用对应的 docs/ 补充文件 -->

## 通用骨架（所有项目必须包含）

参见 `references/docs-skeleton-template.md`。

以下为各技术栈**额外推荐**的 docs/ 文件。

## Node.js / TypeScript 项目

```
docs/
├── ARCHITECTURE.md          # 项目架构
├── QUALITY_SCORE.md         # 质量评分
├── API_REFERENCE.md         # API 接口文档（如项目对外暴露 API）
├── DEPLOYMENT.md            # 部署指南
├── MIGRATION_GUIDE.md       # 数据库迁移指南（如有 ORM）
├── design-docs/
│   └── index.md             # 设计决策索引
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md 骨架示例**：

```markdown
# 架构

## 概览

项目基于 [Express/Fastify/NestJS] 构建，[一句话描述整体架构]。

## 领域划分

| 领域 | 职责 | 入口文件 |
|---|---|---|
| <领域1> | <职责> | `<路径>` |
| <领域2> | <职责> | `<路径>` |

## 依赖方向

[描述模块间的依赖关系和约束]

## 数据流

[描述请求处理流程]

---
最后更新: <YYYY-MM-DD>
```

## Python 项目

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md         # FastAPI/Flask API 文档
├── DEPLOYMENT.md
├── ENVIRONMENT_SETUP.md     # Python 环境配置指南
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md 骨架示例**：

```markdown
# 架构

## 概览

项目基于 [Django/FastAPI/Flask] 构建，[一句话描述]。

## 领域划分

| 领域 | 职责 | 包/模块 |
|---|---|---|
| <领域1> | <职责> | `<包路径>` |
| <领域2> | <职责> | `<包路径>` |

## 依赖方向

[描述包之间的依赖关系]

## 数据库设计

[描述 ORM 模型关系，如有]

---
最后更新: <YYYY-MM-DD>
```

## Go 项目

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md         # HTTP/gRPC 接口文档
├── DEPLOYMENT.md
├── PROTOBUF_GUIDE.md        # Proto 文件管理（如使用 gRPC）
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md 骨架示例**：

```markdown
# 架构

## 概览

项目基于 [Gin/Echo/标准库] 构建，[一句话描述]。

## 包结构

| 包 | 职责 | 依赖 |
|---|---|---|
| `cmd/` | 入口 | 内部包 |
| `internal/` | 业务逻辑 | `pkg/` |
| `pkg/` | 公共工具 | 无外部依赖 |

## 依赖方向

`cmd/` → `internal/` → `pkg/`

## 并发模型

[描述 goroutine/channel 使用模式]

---
最后更新: <YYYY-MM-DD>
```

## Rust 项目

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── SAFETY_NOTES.md          # unsafe 使用记录
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md 骨架示例**：

```markdown
# 架构

## 概览

项目基于 [Actix/Axum/Tokio] 构建，[一句话描述]。

## Crate 结构

| Crate | 职责 | 可见性 |
|---|---|---|
| `src/main.rs` | 入口 | binary |
| `src/lib.rs` | 核心库 | public |
| `src/models/` | 数据模型 | pub(crate) |

## 依赖方向

[描述 crate 间的依赖]

## 内存安全

[描述 unsafe 代码使用约束]

---
最后更新: <YYYY-MM-DD>
```

## Java / Kotlin 项目

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── DATABASE_MIGRATION.md     # Flyway/Liquibase 迁移指南
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md 骨架示例**：

```markdown
# 架构

## 概览

项目基于 [Spring Boot/Quarkus/Ktor] 构建，[一句话描述]。

## 模块划分

| 模块 | 职责 | 技术 |
|---|---|---|
| `api/` | 接口层 | REST/gRPC |
| `service/` | 业务层 | Spring Service |
| `repository/` | 数据层 | JPA/MyBatis |

## 依赖方向

`api/` → `service/` → `repository/`

## 分层约束

[描述层间通信规则]

---
最后更新: <YYYY-MM-DD>
```

## PHP 项目

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── ARTISAN_COMMANDS.md       # Artisan 命令参考（Laravel）
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

## Ruby 项目

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── RAKE_TASKS.md             # Rake 任务参考
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

## 选择指南

1. **先用通用骨架**：所有项目必须包含 ARCHITECTURE.md 和 QUALITY_SCORE.md
2. **按技术栈追加**：根据项目实际使用的技术栈追加对应文件
3. **不确定就跳过**：如果某个文件不确定是否需要，先不创建，在 AGENTS.md 路由表留占位条目
4. **骨架要精简**：每个文件只写骨架和"最后更新"日期，不要写大量空内容
