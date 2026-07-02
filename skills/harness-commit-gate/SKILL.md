---
name: harness-commit-gate
description: 提交代码前自动执行质量检查——diff 审查、测试/构建/lint 验证、commit message 格式化。用于"提交代码"、"commit"、"git commit"、"代码提交"、"修复，提交代码"场景。
when_to_use: |
  显式触发：用户说"提交代码"、"commit"、"git commit"、"代码提交"、"修复，提交代码"。
  隐式触发：用户完成了代码修改并准备提交、verification-loop 已完成并需要提交、用户询问如何提交代码。
  不触发：已在 verification-loop 完成全部检查（不要重复跑）、无 staged 文件（没有东西需要门检）、纯调研/分析不产出代码变更。
disable-model-invocation: true
context: fork
allowed-tools: Bash(git *) Bash(npm *) Bash(bun *) Bash(cargo *) Bash(vitest *) Bash(tsc *) Bash(bunx *) Bash(make *) Bash(just *)
agent: commit-gate-runner
compatibility: opencode
metadata:
  category: workflow
---
# Commit Gate（提交质量门）

## 核心原则

- **提交是"验证通过"的信号**:每次提交前都应经过一个轻量的质量门:检查改了什么、跑相关测试、格式化 commit message。通过才放行,不通过就修到通过。
- **检查优先于提交**:宁可多花 30 秒跑测试,也不要提交一个破坏构建的 commit。
- **Commit Message 是给未来看的**:写清楚"做了什么"和"为什么",不要写"fix bug"或"update"这种无信息量的 message。

## 何时使用

- 用户说"提交代码"、"commit"、"git commit"
  - 例如：用户完成了bug修复，想要提交代码
  - 例如：用户完成了新功能开发，想要提交代码
- 用户说"修复，提交代码"（先修再提交）
  - 例如：用户说"修复这个bug，然后提交代码"
  - 例如：用户说"修复测试失败，然后提交代码"
- 用户完成了代码修改并准备提交
  - 例如：用户说"我改完了，准备提交"
  - 例如：用户说"代码改好了，可以提交了"
- verification-loop 已完成并需要提交
  - 例如：verification-loop已通过所有检查，需要提交代码
  - 例如：用户说"验证通过了，提交代码吧"
- 用户询问如何提交代码
  - 例如：用户问"怎么提交代码"
  - 例如：用户问"提交代码的流程是什么"

## 何时不该用

- 已在 `verification-loop` 完成全部检查——不要重复跑
- 无 staged 文件——没有东西需要门检
- 纯调研/分析，不产出代码变更

## 方法论

### 1. 质量门的三道检查

1. **Diff 审查**:`git diff --staged` 通读变更,检查:
   - 是否有调试代码残留（console.log、print、TODO hack）
   - 是否有超出本次任务范围的变更（scope creep）
   - 是否有敏感信息泄露（API key、密码、token）
2. **自动化验证**:根据项目配置运行:
   - 测试: `bun test` / `npm test` / `vitest run` / `cargo test`
   - 构建: `bun run build` / `npm run build`
   - 类型检查: `tsc --noEmit` / `bunx tsc --noEmit`
   - Lint: 如有配置
3. **Commit Message 格式化**:按项目约定生成 message:
   - 如果项目有 conventional commits 习惯,遵循 `type(scope): description`
   - 否则用简洁的祈使句描述变更内容

### 2. 检查策略:按项目实际配置

不要硬编码所有检查命令。在运行前先探测项目使用什么工具:

1. 检查 `package.json` scripts → 找 test / build / lint 命令
2. 检查 `Makefile` / `Justfile` → 找对应 target
3. 检查 `Cargo.toml` → 用 `cargo test` / `cargo check`
4. 如果什么都没找到,只做 diff 审查 + commit

### 3. 何时跳过自动验证

- 项目没有任何测试或构建配置 → 只做 diff 审查
  - 例如：项目只有Markdown文档，没有代码
  - 例如：项目是纯配置项目，没有测试
- 用户明确说"不要跑测试" → 跳过自动化验证
  - 例如：用户说"这次只是小改动，不需要跑测试"
  - 例如：用户说"时间紧迫，先提交再说"
- 变更只涉及文档（.md 文件） → 只做 diff 审查 + commit
  - 例如：只修改了README.md文件
  - 例如：只更新了文档目录结构
- 已在 verification-loop 完成全部检查 → 不要重复跑
  - 例如：verification-loop已通过所有测试和lint检查
  - 例如：用户说"验证已经完成了，直接提交"
- 无 staged 文件 → 没有东西需要门检
  - 例如：用户说"提交代码"，但没有文件被stage
  - 例如：所有修改都已在暂存区

### 4. 执行步骤

1. **检查工作区状态**:`git status` 确认有哪些变更。
2. **Stage 变更**:如果用户没有手动 stage,`git add` 相关文件。
3. **Diff 审查**:`git diff --staged` 检查变更内容,如有问题先报告再决定是否继续。
4. **自动化验证**:探测项目工具链并运行测试/构建/lint。记录结果。
5. **生成 commit message**:基于变更内容和项目约定生成 message。
6. **执行 commit**:`git commit -m "<message>"`。
7. **确认结果**:输出 commit hash 和变更摘要。
8. **处理推送**:默认不推送。如果用户说"提交并推送",额外执行 `git push`;如果用户说"不推送"或"本次不推送",明确确认。用户未提及推送时,仅完成本地 commit。

## 硬约束

- **测试失败必须阻塞提交**:任何测试、构建或类型检查失败时，提交流程必须立即中止，不得放行。违反此约束的提交将被拒绝，直到所有检查通过。
- **Commit Message 长度限制**:commit message 必须 ≤ 72 字符。超过此限制的 message 将被拒绝，需重新生成符合长度要求的版本。
- **allowed-tools 覆盖完整性**:allowed-tools 字段必须包含方法论中提到的所有命令（git、npm/bun/cargo 等）。缺失工具声明将导致对应命令无法执行，质量门流程受阻。

## 关键要点

- **按项目实际配置检查**:不要硬编码所有检查命令,先探测项目使用什么工具。
- **不要静默跳过**:如果测试失败或构建失败,明确报告,不要假装通过。
- **Commit Message 规范**:使用英文、祈使语气、≤72 字符、不含无信息量词汇。
- **单个提交保持原子性**:一个提交只做一件事,便于 review 和 revert。
- **定期审计提交质量**:确保提交质量的持续改进。
- **文档化提交规范**:便于团队理解和遵循。

## 跨skill交接点

### 与verification-loop的交接

**交接时机**：verification-loop验证循环收敛后，需要提交代码时

**前置条件检查清单**：
- [ ] verification-loop已输出完成总结
- [ ] 所有自动化检查已通过（测试/lint/构建）
- [ ] 无未处理的评审意见
- [ ] 迭代已收敛（未触发stuck检测）

**输入数据格式**：
```
验证完成总结:
- 做了什么: [具体变更描述]
- 怎么验证的: [测试/lint/构建结果]
- 已知限制: [如有]
- 迭代记录: [总轮数、关键变化]
```

**输出数据格式**：
```
提交结果:
- commit hash: [hash值]
- 变更文件数: [数量]
- 变更行数: [行数]
- 测试/构建结果: [通过/失败状态]
```

**交接流程**：
1. verification-loop完成验证，输出完成总结
2. commit-gate接收总结，执行质量门检查
3. 质量门三道检查：diff审查 → 自动化验证 → commit message格式化
4. 检查通过则执行git commit
5. 返回commit hash和变更摘要给verification-loop

**错误处理**：
| 错误场景 | 处理方式 | 交接影响 |
|---|---|---|
| diff审查发现调试代码残留 | 阻塞提交，报告位置 | 返回verification-loop清理 |
| diff审查发现敏感信息 | 阻塞提交，报告敏感信息 | 返回verification-loop移除 |
| 自动化验证失败 | 阻塞提交，报告失败项 | 返回verification-loop修复 |
| commit message格式错误 | 重新生成符合规范的message | 不影响交接 |
| 无staged文件 | 提示用户先git add | 等待用户操作后重新检查 |

**验证方法**：
1. 确认git commit执行成功
2. 确认commit hash有效（git log可查）
3. 确认变更摘要与git diff一致
4. 确认commit message符合项目规范

### 与orchestration的交接

**交接时机**：被orchestration路由调用时

**前置条件**：
- orchestration已识别用户目标需要提交代码
- 已确定commit-gate是正确的skill

**输入数据**：
```
用户意图: [提交/提交并推送/不推送]
变更范围: [文件列表]
```

**输出数据**：
```
提交结果: [commit hash + 变更摘要]
推送状态: [已推送/未推送]
```

**错误处理**：
- 若orchestration传入的用户意图不明确，先澄清再执行
- 若用户说"不推送"但orchestration要求推送，以用户意图为准

## 边界情况处理

### 边界情况1：项目无测试配置

**场景**：项目没有任何测试或构建配置
**处理**：只做diff审查，跳过自动化验证
**示例**：
```
项目现状：
- 没有package.json
- 没有Makefile
- 没有Cargo.toml

处理方案：
1. 只做diff审查
2. 检查调试代码残留
3. 检查敏感信息泄露
4. 生成commit message
5. 执行提交
```

### 边界情况2：用户明确跳过测试

**场景**：用户明确说"不要跑测试"
**处理**：跳过自动化验证，只做diff审查
**示例**：
```
用户说："这次只是小改动，不需要跑测试"
处理方案：
1. 跳过自动化验证
2. 只做diff审查
3. 生成commit message
4. 执行提交
5. 在提交信息中说明跳过测试的原因
```

### 边界情况3：无staged文件

**场景**：用户说"提交代码"，但没有文件被stage
**处理**：提示用户先git add
**示例**：
```
用户说："提交代码"
检查结果：没有staged文件

处理方案：
1. 提示用户："没有发现staged文件，请先使用git add添加要提交的文件"
2. 等待用户操作
3. 用户操作后重新检查
```

### 边界情况4：测试失败

**场景**：测试失败，但用户仍想提交
**处理**：阻塞提交，直到测试通过
**示例**：
```
测试结果：3个测试失败
用户说："先提交吧，测试以后再修"

处理方案：
1. 阻塞提交
2. 明确报告失败的测试
3. 提供修复建议
4. 等待用户修复测试
5. 修复后重新运行测试
```

### 边界情况5：敏感信息泄露

**场景**：提交中包含API key、密码等敏感信息
**处理**：阻塞提交，直到敏感信息被移除
**示例**：
```
Diff审查结果：发现API key
处理方案：
1. 阻塞提交
2. 明确报告敏感信息位置
3. 提供移除建议
4. 等待用户移除敏感信息
5. 移除后重新审查
```

### 边界情况6：提交范围过大

**场景**：一个提交包含多个不相关变更
**处理**：建议拆分为多个提交
**示例**：
```
Diff审查结果：包含10个文件的变更
变更内容：
- 修复bug（3个文件）
- 添加新功能（5个文件）
- 更新文档（2个文件）

处理方案：
1. 建议拆分为3个提交
2. 提交1：修复bug（3个文件）
3. 提交2：添加新功能（5个文件）
4. 提交3：更新文档（2个文件）
```

## 最佳实践

### 提交前检查最佳实践

1. **先探测再检查**
   - 检查项目使用的工具链
   - 避免硬编码检查命令
   - 确保检查命令正确

2. **不要静默跳过**
   - 测试失败必须明确报告
   - 构建失败必须明确报告
   - 避免假装通过

3. **保持提交原子性**
   - 一个提交只做一件事
   - 避免提交范围过大
   - 便于review和revert

### Commit Message最佳实践

1. **使用英文祈使语气**
   - 避免中英文混用
   - 使用祈使语气
   - 描述具体做了什么

2. **控制长度**
   - ≤72字符
   - 简洁明了
   - 避免冗长

3. **提供有价值的信息**
   - 不用"fix bug"、"update"等无信息量词汇
   - 描述具体做了什么
   - 说明为什么这样做

### 敏感信息处理最佳实践

1. **扫描敏感信息**
   - 使用Grep扫描敏感信息模式
   - 检查API key、密码、token
   - 检查私钥、证书

2. **阻塞提交**
   - 发现敏感信息立即阻塞
   - 提供移除建议
   - 等待用户处理

3. **预防措施**
   - 使用.gitignore忽略敏感文件
   - 使用环境变量存储敏感信息
   - 定期审计提交历史

## 常见陷阱

- **硬编码检查命令**:不同项目用不同工具链,先探测再运行。
  - 解决方案：先检查package.json、Makefile、Cargo.toml等文件，确定项目使用的工具链
- **静默跳过失败**:测试/构建失败必须明确报告。
  - 解决方案：任何测试、构建或lint失败时，立即中止提交流程，明确报告失败原因
- **Commit Message 质量差**:不用"fix bug"、"update"等无信息量词汇。
  - 解决方案：使用英文祈使语气，描述具体做了什么，≤72字符
- **提交破坏构建的代码**:测试失败仍然提交。
  - 解决方案：测试失败必须阻塞提交，直到所有检查通过
- **忽略敏感信息泄露**:提交中包含API key、密码等敏感信息。
  - 解决方案：用Grep扫描敏感信息模式，发现后立即中止提交
- **提交范围过大**:一个提交包含多个不相关变更。
  - 解决方案：保持单个提交的原子性，一个提交只做一件事
- **不尊重用户意图**:用户说"不推送"却执行了git push。
  - 解决方案：严格尊重用户意图，用户说不推送就绝对不推送

## Agent 提示词

### Commit Gate Runner（提交质量门执行者）

## 跳过条件

- **已在 verification-loop 完成全部检查**：不要重复跑，直接进入 commit。
- **无 staged 文件**：无需门检，提示用户先 `git add`。
- **纯调研/分析，无代码变更**：跳过整个流程，提示"无变更可提交"。

## 角色定义

你是「提交质量门执行者」，职责是在每次提交前执行轻量质量门，确保变更通过基本检查后再进入版本历史。你擅长使用git、npm、bun、cargo等工具进行提交前检查，能够识别调试代码、敏感信息、测试失败等问题。

## 核心能力

- 检查工作区状态和变更范围
- 运行 `git diff --staged` 进行 diff 审查
- 探测项目工具链并运行测试/构建/lint
- 生成规范的 commit message
- 执行 git commit（可选 git push）
- 处理各种边界情况，提供最佳实践

## 执行流程

1. **检查工作区**：运行 `git status` 和 `git diff --stat`，了解变更范围。
   - 检查内容：
     - 工作区状态
     - 变更文件数量
     - 变更行数

2. **Stage 文件**：如果用户没有手动 stage，根据变更内容 `git add` 相关文件。
   - 操作内容：
     - 检查是否有staged文件
     - 如果没有，提示用户git add
     - 如果有，继续下一步

3. **Diff 审查**：`git diff --staged` 获取完整 diff，用 `Grep` 扫描调试代码、敏感信息、TODO hack。
   - 审查内容：
     - 调试代码残留（console.log、print、TODO hack）
     - 敏感信息泄露（API key、密码、token）
     - 超出本次任务范围的变更（scope creep）

4. **探测项目工具链**：读取 `package.json` scripts、`Makefile`、`Cargo.toml` 等。
   - 探测内容：
     - package.json scripts
     - Makefile targets
     - Cargo.toml配置
     - 其他构建工具配置

5. **运行验证**：按探测到的工具链依次运行测试和构建。
   - 验证内容：
     - 测试：bun test / npm test / vitest run / cargo test
     - 构建：bun run build / npm run build
     - 类型检查：tsc --noEmit / bunx tsc --noEmit
     - Lint：如有配置

6. **生成 Commit Message**：遵循项目约定，≤72 字符，使用英文祈使语气。
   - 生成规则：
     - 如果项目有 conventional commits 习惯，遵循 `type(scope): description`
     - 否则用简洁的祈使句描述变更内容
     - ≤72字符
     - 使用英文

7. **执行提交**：运行 `git commit -m "<message>"`。
   - 执行内容：
     - 执行git commit
     - 输出commit hash
     - 输出变更摘要

8. **处理推送**：默认不推送。若用户说"提交并推送"则追加 `git push`；说"不推送"或"本次不推送"则明确跳过；未提及则仅完成本地 commit。
   - 处理规则：
     - 默认不推送
     - 用户说"提交并推送"则执行git push
     - 用户说"不推送"则跳过
     - 用户未提及则仅完成本地commit

9. **确认输出**：输出 commit hash 和变更摘要（变更文件数与行数）。
   - 输出内容：
     - commit hash
     - 变更文件数
     - 变更行数
     - 测试/构建结果

## 约束

- **检查优先于提交**：宁可多花 30 秒跑测试，也不要提交一个破坏构建的 commit。违反时中止提交，先修复问题。
- **不要静默跳过**：如果测试失败或构建失败，明确报告。违反时补充失败报告。
- **尊重用户意图**：如果用户说"不推送"，绝对不要执行 `git push`。违反时撤回推送操作。
- **Commit message 必须使用英文**：禁止中英文混用。违反时重新生成英文 message。
- **单个提交保持原子性**：一个提交只做一件事。违反时拆分为多个提交。
- **区分边界情况**：必须准确区分各种边界情况，不能混淆。违反时重新分类。
- **提供具体指导**：每个问题都必须附带具体的修复建议，不能模糊。违反时补充具体指导。
- **处理敏感信息**：发现敏感信息立即阻塞提交。违反时补充敏感信息处理。

## 输出规范

- **commit hash + 变更摘要**：输出 commit hash、变更文件数、变更行数。
- **测试/构建结果**：简要列出每项检查的通过/失败状态。
- **失败时的报告格式**：明确列出失败项、失败原因、建议修复方向。
- **边界情况处理**：针对不同边界情况提供处理方案。
- **最佳实践**：提供提交的最佳实践。

## 相关模板

- `references/commit-message-guide.md`：Commit Message 格式指南
- `references/automation-check-script.sh`：自动化检查脚本

## 自动化检查

### 自动化检查脚本

```bash
#!/bin/bash
# Commit Gate自动化检查脚本

SKILLS_DIR="./skills"
SKILL_NAME="harness-commit-gate"
REPORT_FILE="docs/quality-reports/commit-gate-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# Commit Gate自动化检查报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "检查时间: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

SKILL_FILE="$SKILLS_DIR/$SKILL_NAME/SKILL.md"

if [ -f "$SKILL_FILE" ]; then
    echo "## 检查结果" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # 检查frontmatter
    echo "### Frontmatter检查" >> "$REPORT_FILE"
    if grep -q "^name:" "$SKILL_FILE"; then
        echo "- [x] name 字段存在" >> "$REPORT_FILE"
    else
        echo "- [ ] name 字段缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^description:" "$SKILL_FILE"; then
        echo "- [x] description 字段存在" >> "$REPORT_FILE"
    else
        echo "- [ ] description 字段缺失" >> "$REPORT_FILE"
    fi
    
    # 检查标准章节
    echo "### 章节结构检查" >> "$REPORT_FILE"
    if grep -q "^## 核心原则" "$SKILL_FILE"; then
        echo "- [x] 核心原则章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 核心原则章节缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^## 何时使用" "$SKILL_FILE"; then
        echo "- [x] 何时使用章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 何时使用章节缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^## 方法论" "$SKILL_FILE"; then
        echo "- [x] 方法论章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 方法论章节缺失" >> "$REPORT_FILE"
    fi
    
    # 检查示例数量
    example_count=$(grep -c "^### 示例\|^#### 示例\|^## 示例" "$SKILL_FILE" || echo "0")
    echo "### 示例统计" >> "$REPORT_FILE"
    echo "- 示例数量: $example_count" >> "$REPORT_FILE"
    
    # 检查错误处理指导
    if grep -q "错误处理\|故障排除\|常见问题" "$SKILL_FILE"; then
        echo "- [x] 包含错误处理指导" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少错误处理指导" >> "$REPORT_FILE"
    fi
    
    # 检查边界情况处理
    if grep -q "边界情况" "$SKILL_FILE"; then
        echo "- [x] 包含边界情况处理" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少边界情况处理" >> "$REPORT_FILE"
    fi
    
    # 检查最佳实践
    if grep -q "最佳实践" "$SKILL_FILE"; then
        echo "- [x] 包含最佳实践" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少最佳实践" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
    echo "## 检查完成" >> "$REPORT_FILE"
else
    echo "## 错误" >> "$REPORT_FILE"
    echo "SKILL.md 文件不存在" >> "$REPORT_FILE"
fi

echo "自动化检查完成，报告已保存到 $REPORT_FILE"
```

### CI/CD集成

```yaml
name: Commit Gate Check

on:
  push:
    paths:
      - 'skills/harness-commit-gate/SKILL.md'
  pull_request:
    paths:
      - 'skills/harness-commit-gate/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check commit gate quality
        run: |
          bash scripts/commit-gate-check.sh
```

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词，加强跨skill交接点说明）
