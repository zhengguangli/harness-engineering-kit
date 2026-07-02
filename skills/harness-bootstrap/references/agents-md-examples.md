<!-- 各技术栈 AGENTS.md 示例 — 由 harness-bootstrapper agent 使用 -->
<!-- 根据项目实际情况选用最接近的示例作为起点 -->

## 示例 1：Node.js 全栈项目

```markdown
# AGENTS.md

> 这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找。

## 这个仓库是什么

一个基于 Next.js + Prisma 的 SaaS 管理后台，提供用户管理、数据看板、API 网关功能。

## 硬约束（极少数，违反即阻塞合并）

- `prisma/schema.prisma` 是数据库 schema 的 source of truth，禁止手动改 SQL
- API 路由必须通过 Zod schema 校验，禁止直接信任 req.body
- `docs/` 是源知识目录，`.gitignore` 中禁止忽略整个 `docs/`

## 去哪里找更多

| 我想知道… | 去看这里 |
|---|---|
| 整体架构与 API 设计 | `docs/ARCHITECTURE.md` |
| Prisma schema 与数据模型 | `prisma/schema.prisma` |
| 环境变量配置 | `.env.example` |
| 组件库与样式规范 | `src/components/` |
| 各模块质量评分 | `docs/QUALITY_SCORE.md` |

## 工作方式提示

- 用 TypeScript strict 模式，禁止 `any`
- 提交前跑 `npm run lint && npm run typecheck`
- 组件用函数式写法，不用 class component
- 数据库变更必须走 Prisma migrate

---
最后更新: <YYYY-MM-DD>
```

## 示例 2：Python FastAPI 项目

```markdown
# AGENTS.md

> 这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找。

## 这个仓库是什么

一个基于 FastAPI 的微服务，处理订单和支付流程，使用 PostgreSQL + Redis。

## 硬约束（极少数，违反即阻塞合并）

- 所有 API 端点必须有 Pydantic response model
- 数据库操作必须通过 SQLAlchemy session，禁止裸 SQL
- 环境变量通过 pydantic-settings 管理，禁止硬编码

## 去哪里找更多

| 我想知道… | 去看这里 |
|---|---|
| 整体架构与数据流 | `docs/ARCHITECTURE.md` |
| API 接口文档 | `docs/API_REFERENCE.md` |
| 数据库模型 | `app/models/` |
| 环境变量说明 | `.env.example` |
| 各模块质量评分 | `docs/QUALITY_SCORE.md` |

## 工作方式提示

- Python >=3.11，使用 type hints
- 测试用 pytest，覆盖率要求 >80%
- 提交前跑 `ruff check . && mypy .`
- 异步函数统一用 `async def`

---
最后更新: <YYYY-MM-DD>
```

## 示例 3：Go 微服务项目

```markdown
# AGENTS.md

> 这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找。

## 这个仓库是什么

Go 微服务，提供 gRPC + HTTP 双协议接入，负责用户认证与权限管理。

## 硬约束（极少数，违反即阻塞合并）

- gRPC proto 文件是接口定义的 source of truth，修改接口必须先改 proto
- 所有 error 必须用 `fmt.Errorf` 包装，禁止裸 return
- `internal/` 包对外不可见，`pkg/` 才是公开 API

## 去哪里找更多

| 我想知道… | 去看这里 |
|---|---|
| 包结构与依赖方向 | `docs/ARCHITECTURE.md` |
| Proto 接口定义 | `proto/` |
| 配置与环境变量 | `config/` |
| 各模块质量评分 | `docs/QUALITY_SCORE.md` |

## 工作方式提示

- Go >=1.21，遵循 `go fmt` + `go vet`
- 测试用 `go test -race ./...`
- 提交前跑 `golangci-lint run`
- 错误处理统一用 `errors.Is/As`

---
最后更新: <YYYY-MM-DD>
```

## 示例 4：Rust CLI 工具

```markdown
# AGENTS.md

> 这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找。

## 这个仓库是什么

Rust CLI 工具，用于本地配置管理和部署自动化。

## 硬约束（极少数，违反即阻塞合并）

- `unsafe` 代码必须有 `// SAFETY:` 注释说明安全性论证
- 所有公开 API 必须有文档注释 `///`
- 依赖版本锁定在 `Cargo.lock`，CI 中不允许 `cargo update`

## 去哪里找更多

| 我想知道… | 去看这里 |
|---|---|
| 模块结构与依赖 | `docs/ARCHITECTURE.md` |
| CLI 参数定义 | `src/cli.rs` |
| 配置文件格式 | `docs/CONFIG_FORMAT.md` |
| 各模块质量评分 | `docs/QUALITY_SCORE.md` |

## 工作方式提示

- Rust edition 2021，使用 clippy lint
- 测试用 `cargo test`，覆盖关键路径
- 提交前跑 `cargo clippy -- -D warnings && cargo fmt --check`
- 错误处理用 `anyhow` 或自定义 error type

---
最后更新: <YYYY-MM-DD>
```

## 示例 5：Java Spring Boot 项目

```markdown
# AGENTS.md

> 这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找。

## 这个仓库是什么

Spring Boot 微服务，提供 REST API，集成 RabbitMQ 消息队列和 Elasticsearch 搜索。

## 硬约束（极少数，违反即阻塞合并）

- Controller 层禁止直接访问 Repository，必须通过 Service
- 所有实体必须用 JPA 注解，禁止裸 JDBC
- 配置通过 `application.yml` 管理，敏感信息走 Vault

## 去哪里找更多

| 我想知道… | 去看这里 |
|---|---|
| 分层架构与模块划分 | `docs/ARCHITECTURE.md` |
| API 接口文档 | Swagger UI `/swagger-ui.html` |
| 数据库迁移 | `src/main/resources/db/migration/` |
| 各模块质量评分 | `docs/QUALITY_SCORE.md` |

## 工作方式提示

- Java 17+，Spring Boot 3.x
- 测试用 JUnit 5 + Mockito
- 提交前跑 `./mvnw verify`
- 代码风格用 Google Java Format

---
最后更新: <YYYY-MM-DD>
```

## 选择指南

1. **找到最接近的示例**：根据项目技术栈选择最接近的示例
2. **根据实际情况调整**：修改一句话描述、硬约束、路由表
3. **不要照抄**：示例是起点，不是最终答案
4. **保持精简**：AGENTS.md 只放路由表和硬约束，不要膨胀
