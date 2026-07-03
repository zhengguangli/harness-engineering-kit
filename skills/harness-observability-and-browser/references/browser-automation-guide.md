# 浏览器自动化工具使用指南

## 工具选型

| 工具 | 适用场景 | 优势 | 劣势 |
|---|---|---|---|
| Playwright | E2E 测试、跨浏览器验证 | 多浏览器支持、自动等待、截图/DOM 快照 | 学习曲线较陡 |
| Puppeteer | Chrome 专项测试 | 轻量、Chrome 原生支持 | 仅支持 Chrome |
| Cypress | 组件测试、E2E 测试 | 实时调试、时间旅行 | 仅支持 Chrome/Firefox |

**推荐**：优先使用 Playwright，覆盖 Chrome/Firefox/Safari 三个引擎。

## Playwright 使用模式

### 安装与配置

```bash
# 安装
npm init playwright@latest

# 或手动安装
npm install -D @playwright/test
npx playwright install
```

### 基础验证循环

```typescript
import { chromium } from 'playwright';

async function verifyUI(url: string, selector: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // 导航到目标页面
  await page.goto(url);

  // 等待关键元素加载
  await page.waitForSelector(selector);

  // 截图（触发后状态）
  await page.screenshot({
    path: `verification-${Date.now()}.png`,
    fullPage: true
  });

  // DOM 快照
  const domSnapshot = await page.content();

  // 控制台日志
  const logs: string[] = [];
  page.on('console', msg => logs.push(msg.text()));

  // 网络请求
  const requests: string[] = [];
  page.on('request', req => requests.push(req.url()));

  await browser.close();

  return { domSnapshot, logs, requests };
}
```

### 截图最佳实践

```typescript
// ✅ 好：包含元数据
await page.screenshot({
  path: `verification-${Date.now()}.png`,
  fullPage: true
});
// 文件名包含时间戳，便于追溯

// ❌ 差：无元数据
await page.screenshot({ path: 'screenshot.png' });
// 无法追溯何时、何地截取
```

### DOM 快照对比

```typescript
// 触发前快照
const beforeSnapshot = await page.content();

// 执行操作
await page.click('#submit-button');

// 等待状态变化
await page.waitForTimeout(1000);

// 触发后快照
const afterSnapshot = await page.content();

// 对比差异
if (beforeSnapshot !== afterSnapshot) {
  console.log('DOM 发生变化');
}
```

### 移动端模拟

```typescript
// 使用 Playwright 内置设备模拟
const iPhone = devices['iPhone 13'];
const context = await browser.newContext({
  ...iPhone,
});

const page = await context.newPage();
await page.goto(url);
await page.screenshot({ path: 'mobile-verification.png' });
```

### 等待策略

```typescript
// ✅ 好：等待具体条件
await page.waitForSelector('#loading-spinner', { state: 'hidden' });
await page.waitForLoadState('networkidle');

// ❌ 差：固定等待
await page.waitForTimeout(3000); // 不可靠
```

## 常见验证场景

### 场景一：按钮点击验证

```typescript
// 验证按钮点击后页面响应
const button = await page.$('#submit-button');
const isDisabled = await button?.isDisabled();
console.log(`按钮初始状态: ${isDisabled ? '禁用' : '启用'}`);

await page.click('#submit-button');

// 验证加载状态
await page.waitForSelector('#loading-spinner');
await page.waitForSelector('#loading-spinner', { state: 'hidden' });

// 验证结果
const result = await page.$eval('#result', el => el.textContent);
console.log(`操作结果: ${result}`);
```

### 场景二：表单验证

```typescript
// 验证表单提交
await page.fill('#email', 'test@example.com');
await page.fill('#password', 'password123');
await page.click('#login-button');

// 验证错误提示
const error = await page.$('.error-message');
if (error) {
  const errorText = await error.textContent();
  console.log(`错误提示: ${errorText}`);
}

// 验证跳转
await page.waitForURL('**/dashboard');
console.log('登录成功，已跳转到 dashboard');
```

### 场景三：视觉回归验证

```typescript
// 截图对比（需要 pixelmatch 等库）
import { compareScreenshots } from './visual-regression';

const baseline = await page.screenshot({ path: 'baseline.png' });
// 执行改动
const current = await page.screenshot({ path: 'current.png' });

const diff = await compareScreenshots(baseline, current);
if (diff.percentage > 0.01) {
  console.log(`视觉差异: ${(diff.percentage * 100).toFixed(2)}%`);
}
```

## 错误处理

| 错误 | 原因 | 处理 |
|---|---|---|
| `TimeoutError` | 元素未在指定时间内出现 | 检查选择器是否正确，增加等待时间 |
| `Navigation timeout` | 页面加载超时 | 检查网络，增加超时时间 |
| `Element not found` | 选择器匹配不到元素 | 检查 DOM 结构，使用更稳定的选择器 |
| `Browser not found` | 浏览器未安装 | 运行 `npx playwright install` |

## 性能优化

```typescript
// 复用浏览器实例
const browser = await chromium.launch();

// 并行验证多个页面
const pages = await Promise.all([
  browser.newPage().then(async p => { await p.goto(url1); return p; }),
  browser.newPage().then(async p => { await p.goto(url2); return p; }),
]);

// 批量截图
await Promise.all(pages.map((p, i) =>
  p.screenshot({ path: `page-${i}.png` })
));

await browser.close();
```

## CI/CD 集成

```yaml
# GitHub Actions
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run browser verification
  run: npx playwright test verification/

- name: Upload screenshots
  if: always()
  uses: actions/upload-artifact@v2
  with:
    name: verification-screenshots
    path: test-results/
```
