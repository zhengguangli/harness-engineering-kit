<!-- 各语言项目结构分析 — 由 project-analyzer agent 使用 -->
<!-- 根据目录布局识别项目类型和架构模式 -->

## 通用目录模式

| 目录/文件 | 含义 | 出现的语言 |
|---|---|---|
| `src/` | 源代码目录 | 通用 |
| `lib/` | 库代码目录 | 通用 |
| `test/` / `tests/` / `__tests__/` | 测试目录 | 通用 |
| `docs/` | 文档目录 | 通用 |
| `scripts/` | 脚本目录 | 通用 |
| `.github/` | GitHub Actions CI | 通用 |
| `Dockerfile` / `docker-compose.yml` | 容器化 | 通用 |
| `Makefile` / `justfile` | 构建脚本 | 通用 |
| `README.md` | 项目说明 | 通用 |

## Node.js / TypeScript

```
node-project/
├── src/                    # 源代码
│   ├── index.ts            # 入口文件
│   ├── routes/             # API 路由（Express/Fastify）
│   ├── controllers/        # 控制器（NestJS）
│   ├── components/         # React 组件
│   ├── pages/              # Next.js 页面
│   └── utils/              # 工具函数
├── public/                 # 静态资源
├── prisma/                 # Prisma schema
├── migrations/             # 数据库迁移
├── package.json            # 包管理
├── tsconfig.json           # TypeScript 配置
├── next.config.js          # Next.js 配置
├── vite.config.ts          # Vite 配置
├── .eslintrc.js            # ESLint 配置
└── jest.config.js          # Jest 配置
```

**入口文件识别**：
- `src/index.ts` — 通用入口
- `src/main.ts` — NestJS 入口
- `src/app.ts` — Express/Fastify 入口
- `pages/_app.tsx` — Next.js App
- `app/layout.tsx` — Next.js App Router

## Python

```
python-project/
├── src/                    # 源代码（或项目名/）
│   ├── __init__.py
│   ├── main.py             # 入口文件
│   ├── models/             # 数据模型
│   ├── routes/             # API 路由
│   ├── services/           # 业务逻辑
│   ├── schemas/            # Pydantic schemas
│   └── utils/              # 工具函数
├── tests/                  # 测试
├── alembic/                # 数据库迁移（SQLAlchemy）
├── migrations/             # 数据库迁移（Django）
├── manage.py               # Django 管理脚本
├── pyproject.toml          # 项目配置
├── setup.py                # 传统配置
├── requirements.txt        # 依赖列表
├── Makefile                # 构建脚本
└── Dockerfile              # 容器配置
```

**入口文件识别**：
- `src/main.py` — FastAPI/Flask 通用入口
- `manage.py` — Django 管理脚本
- `app/main.py` — FastAPI 常见布局
- `wsgi.py` — WSGI 入口（Django/Flask）
- `asgi.py` — ASGI 入口（FastAPI）

## Go

```
go-project/
├── cmd/                    # 命令入口
│   └── server/
│       └── main.go         # 主入口
├── internal/               # 私有包
│   ├── handler/            # HTTP 处理器
│   ├── service/            # 业务逻辑
│   ├── repository/         # 数据访问
│   ├── model/              # 数据模型
│   └── config/             # 配置
├── pkg/                    # 公共包
├── api/                    # API 定义（proto/OpenAPI）
├── proto/                  # gRPC proto 文件
├── migrations/             # 数据库迁移
├── go.mod                  # 模块定义
├── go.sum                  # 依赖校验
├── Makefile                # 构建脚本
├── Dockerfile              # 容器配置
└── .golangci.yml           # lint 配置
```

**入口文件识别**：
- `cmd/server/main.go` — 标准 Go 项目入口
- `main.go` — 简单项目入口
- `internal/handler/*.go` — HTTP 处理器
- `internal/service/*.go` — 业务逻辑

## Rust

```
rust-project/
├── src/
│   ├── main.rs             # 入口文件（binary）
│   ├── lib.rs              # 库入口
│   ├── cli.rs              # CLI 参数定义
│   ├── models/             # 数据模型
│   ├── handlers/           # 请求处理器
│   ├── services/           # 业务逻辑
│   ├── errors.rs           # 错误定义
│   └── config.rs           # 配置
├── tests/                  # 集成测试
├── benches/                # 性能测试
├── examples/               # 示例代码
├── Cargo.toml              # 包管理
├── Cargo.lock              # 依赖锁定
├── clippy.toml             # clippy 配置
├── rustfmt.toml            # 格式化配置
└── Makefile                # 构建脚本
```

**入口文件识别**：
- `src/main.rs` — binary 入口
- `src/lib.rs` — 库入口
- `src/cli.rs` — CLI 定义（clap）
- `src/handlers/*.rs` — HTTP 处理器

## Java / Kotlin

```
java-project/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── Application.java    # 主入口
│   │   │       ├── controller/         # 控制器
│   │   │       ├── service/            # 业务逻辑
│   │   │       ├── repository/         # 数据访问
│   │   │       ├── model/              # 数据模型
│   │   │       └── config/             # 配置
│   │   └── resources/
│   │       ├── application.yml         # 配置文件
│   │       ├── db/migration/           # 数据库迁移
│   │       └── static/                 # 静态资源
│   └── test/
│       └── java/
├── pom.xml                  # Maven 配置
├── build.gradle             # Gradle 配置
└── gradle/                  # Gradle wrapper
```

**入口文件识别**：
- `Application.java` — Spring Boot 主类
- `*Controller.java` — REST 控制器
- `*Service.java` — 业务逻辑
- `*Repository.java` — 数据访问

## PHP

```
php-project/
├── app/                    # Laravel 应用代码
│   ├── Http/
│   │   └── Controllers/    # 控制器
│   ├── Models/             # 数据模型
│   └── Services/           # 业务逻辑
├── routes/                 # 路由定义
├── database/
│   ├── migrations/         # 数据库迁移
│   └── seeders/            # 数据填充
├── public/                 # 公共入口
│   └── index.php           # 入口文件
├── config/                 # 配置文件
├── storage/                # 存储目录
├── tests/                  # 测试
├── composer.json           # 包管理
├── artisan                 # Laravel CLI
├── .env.example            # 环境变量模板
└── phpunit.xml             # 测试配置
```

**入口文件识别**：
- `public/index.php` — Web 入口
- `artisan` — CLI 入口
- `routes/api.php` — API 路由
- `app/Http/Controllers/*.php` — 控制器

## Ruby

```
ruby-project/
├── app/                    # Rails 应用代码
│   ├── controllers/        # 控制器
│   ├── models/             # 数据模型
│   ├── views/              # 视图
│   ├── services/           # 业务逻辑
│   └── jobs/               # 后台任务
├── config/                 # 配置文件
├── db/
│   ├── migrate/            # 数据库迁移
│   └── seeds.rb            # 数据填充
├── lib/                    # 库代码
├── spec/                   # RSpec 测试
├── test/                   # Minitest 测试
├── Gemfile                 # 依赖
├── Rakefile                # Rake 任务
├── bin/rails               # Rails 入口
└── config.ru               # Rack 配置
```

**入口文件识别**：
- `bin/rails` — Rails CLI 入口
- `config/routes.rb` — 路由定义
- `app/controllers/*.rb` — 控制器

## Dart / Flutter

```
dart-project/
├── lib/                    # 源代码
│   ├── main.dart           # 入口文件
│   ├── models/             # 数据模型
│   ├── screens/            # 页面
│   ├── widgets/            # 组件
│   └── services/           # 业务逻辑
├── test/                   # 测试
├── web/                    # Web 平台
├── android/                # Android 平台
├── ios/                    # iOS 平台
├── pubspec.yaml            # 依赖
└── analysis_options.yaml   # lint 配置
```

## 项目类型识别

| 类型 | 特征 | 常见技术栈 |
|---|---|---|
| Web API | routes/ 或 controllers/ 目录 | Express, FastAPI, Gin, Spring |
| Web 全栈 | pages/ 或 views/ + 前端框架 | Next.js, Nuxt, Rails, Laravel |
| CLI 工具 | cli.rs 或 argparse 或 cobra | Rust clap, Python click, Go cobra |
| Library | lib/ 目录为主，无 main 入口 | 各语言库项目 |
| Microservice | 独立部署配置 + API 定义 | gRPC, REST, 消息队列 |
| Monorepo | 多个 package/module 目录 | Turborepo, Nx, Go workspace |
