<!-- 各语言技术栈检测 — 由 project-analyzer agent 使用 -->
<!-- 从配置文件中提取框架、运行时、部署目标等信息 -->

## 检测维度

技术栈信息从以下维度提取：

| 维度 | 数据来源 | 提取方式 |
|---|---|---|
| 语言 | 包管理文件 + 文件后缀 | 模式匹配 |
| 版本 | 包管理文件 + CLI 命令 | 正则提取 |
| 框架 | dependencies 列表 | 关键词匹配 |
| 运行时 | 配置文件 + engines 字段 | 正则提取 |
| 包管理器 | lock 文件 | 文件存在性 |
| 部署目标 | 配置文件 + CI 配置 | 关键词匹配 |

## 框架检测规则

### Node.js / TypeScript 框架

| 框架 | 检测关键词 | 来源文件 |
|---|---|---|
| Next.js | `"next"` | `package.json` dependencies |
| Nuxt | `"nuxt"` | `package.json` dependencies |
| React | `"react"` | `package.json` dependencies |
| Vue | `"vue"` | `package.json` dependencies |
| Angular | `"@angular/core"` | `package.json` dependencies |
| Express | `"express"` | `package.json` dependencies |
| Fastify | `"fastify"` | `package.json` dependencies |
| NestJS | `"@nestjs/core"` | `package.json` dependencies |
| Hono | `"hono"` | `package.json` dependencies |
| Astro | `"astro"` | `package.json` dependencies |
| Remix | `"@remix-run/react"` | `package.json` dependencies |
| SvelteKit | `"@sveltejs/kit"` | `package.json` dependencies |

### Python 框架

| 框架 | 检测关键词 | 来源文件 |
|---|---|---|
| Django | `django` | `pyproject.toml` / `requirements.txt` |
| FastAPI | `fastapi` | `pyproject.toml` / `requirements.txt` |
| Flask | `flask` | `pyproject.toml` / `requirements.txt` |
| SQLAlchemy | `sqlalchemy` | `pyproject.toml` / `requirements.txt` |
| Celery | `celery` | `pyproject.toml` / `requirements.txt` |
| Tornado | `tornado` | `pyproject.toml` / `requirements.txt` |
| Starlette | `starlette` | `pyproject.toml` / `requirements.txt` |

### Go 框架

| 框架 | 检测关键词 | 来源文件 |
|---|---|---|
| Gin | `github.com/gin-gonic/gin` | `go.mod` |
| Echo | `github.com/labstack/echo` | `go.mod` |
| Fiber | `github.com/gofiber/fiber` | `go.mod` |
| Chi | `github.com/go-chi/chi` | `go.mod` |
| gRPC | `google.golang.org/grpc` | `go.mod` |
| GORM | `gorm.io/gorm` | `go.mod` |
| Ent | `entgo.io/ent` | `go.mod` |

### Rust 框架

| 框架 | 检测关键词 | 来源文件 |
|---|---|---|
| Actix | `actix-web` | `Cargo.toml` |
| Axum | `axum` | `Cargo.toml` |
| Tokio | `tokio` | `Cargo.toml` |
| Rocket | `rocket` | `Cargo.toml` |
| Warp | `warp` | `Cargo.toml` |
| Serde | `serde` | `Cargo.toml` |
| Clap | `clap` | `Cargo.toml` |

### Java 框架

| 框架 | 检测关键词 | 来源文件 |
|---|---|---|
| Spring Boot | `org.springframework.boot` | `pom.xml` / `build.gradle` |
| Quarkus | `io.quarkus` | `pom.xml` / `build.gradle` |
| Micronaut | `io.micronaut` | `pom.xml` / `build.gradle` |
| MyBatis | `org.mybatis` | `pom.xml` / `build.gradle` |
| Hibernate | `org.hibernate` | `pom.xml` / `build.gradle` |

### PHP 框架

| 框架 | 检测关键词 | 来源文件 |
|---|---|---|
| Laravel | `laravel/framework` | `composer.json` |
| Symfony | `symfony/framework-bundle` | `composer.json` |
| Slim | `slim/slim` | `composer.json` |
| Lumen | `laravel/lumen` | `composer.json` |

### Ruby 框架

| 框架 | 检测关键词 | 来源文件 |
|---|---|---|
| Rails | `rails` | `Gemfile` |
| Sinatra | `sinatra` | `Gemfile` |
| Hanami | `hanami` | `Gemfile` |

## 运行时检测

| 运行时 | 检测方式 | 说明 |
|---|---|---|
| Node.js | `package.json` 中 `engines.node` | 服务端/全栈 |
| Bun | `package.json` 中 `engines.bun` 或 `bun.lockb` 存在 | 替代运行时 |
| Deno | `deno.json` 存在 | 替代运行时 |
| 浏览器 | `package.json` 中 `browserslist` | 前端 |
| Python | `pyproject.toml` 中 `requires-python` | 服务端 |
| JVM | `pom.xml` 中 `java.version` | Java/Kotlin |
| Go runtime | `go.mod` 中 `go` 指令 | 编译型 |
| Rust native | `Cargo.toml` 中 `edition` | 编译型 |

## 部署目标检测

| 部署目标 | 检测关键词 | 来源文件 |
|---|---|---|
| Docker | `Dockerfile` / `docker-compose.yml` 存在 | 根目录 |
| Vercel | `vercel.json` 或 `next.config.js` | 根目录 |
| Netlify | `netlify.toml` | 根目录 |
| Cloudflare Workers | `wrangler.toml` | 根目录 |
| AWS Lambda | `serverless.yml` / `sam` 配置 | 根目录 |
| Kubernetes | `k8s/` / `kubernetes/` 目录或 Helm chart | 根目录 |
| Fly.io | `fly.toml` | 根目录 |
| Railway | `railway.toml` | 根目录 |
| Render | `render.yaml` | 根目录 |
| Heroku | `Procfile` | 根目录 |
| GitHub Pages | `.github/workflows/` 中 `pages` 关键词 | CI 配置 |
| Static | `static/` / `build/` 输出 | 构建配置 |

## CI/CD 检测

| CI/CD | 检测关键词 | 来源文件 |
|---|---|---|
| GitHub Actions | `.github/workflows/` 目录 | 根目录 |
| GitLab CI | `.gitlab-ci.yml` | 根目录 |
| CircleCI | `.circleci/config.yml` | 根目录 |
| Travis CI | `.travis.yml` | 根目录 |
| Jenkins | `Jenkinsfile` | 根目录 |
| Azure Pipelines | `azure-pipelines.yml` | 根目录 |

## 数据库检测

| 数据库 | 检测关键词 | 来源文件 |
|---|---|---|
| PostgreSQL | `postgresql` / `postgres` | 配置文件 / docker-compose |
| MySQL | `mysql` | 配置文件 / docker-compose |
| SQLite | `sqlite` / `.db` 文件 | 配置文件 |
| MongoDB | `mongodb` / `mongo` | 配置文件 / docker-compose |
| Redis | `redis` | 配置文件 / docker-compose |
| Elasticsearch | `elasticsearch` | 配置文件 / docker-compose |

## 输出格式

技术栈信息按以下格式输出到项目卡片：

```markdown
### 技术栈

| 维度 | 值 |
|---|---|
| 语言 | TypeScript 5.3 |
| 框架 | Next.js 14 (React 18) |
| 运行时 | Node.js 20 |
| 包管理 | pnpm |
| 部署目标 | Vercel |
| 数据库 | PostgreSQL 16 |
| CI/CD | GitHub Actions |
```
