# Browser Automation Tool Guide

## Tool Selection

| Tool | Use Case | Strengths | Weaknesses |
|---|---|---|---|
| Playwright | E2E testing, cross-browser verification | Multi-browser support, auto-wait, screenshots/DOM snapshots | Steeper learning curve |
| Puppeteer | Chrome-specific testing | Lightweight, native Chrome support | Chrome only |
| Cypress | Component testing, E2E testing | Live debugging, time travel | Chrome/Firefox only |

**Recommendation**: Prefer Playwright, covering Chrome/Firefox/Safari engines.

## Playwright Usage Patterns

### Installation and Configuration

```bash
# Install
npm init playwright@latest

# Or install manually
npm install -D @playwright/test
npx playwright install
```

### Basic Verification Loop

```typescript
import { chromium } from 'playwright';

async function verifyUI(url: string, selector: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Navigate to target page
  await page.goto(url);

  // Wait for key element to load
  await page.waitForSelector(selector);

  // Screenshot (post-action state)
  await page.screenshot({
    path: `verification-${Date.now()}.png`,
    fullPage: true
  });

  // DOM snapshot
  const domSnapshot = await page.content();

  // Console logs
  const logs: string[] = [];
  page.on('console', msg => logs.push(msg.text()));

  // Network requests
  const requests: string[] = [];
  page.on('request', req => requests.push(req.url()));

  await browser.close();

  return { domSnapshot, logs, requests };
}
```

### Screenshot Best Practices

```typescript
// ✅ Good: includes metadata
await page.screenshot({
  path: `verification-${Date.now()}.png`,
  fullPage: true
});
// Filename includes timestamp for traceability

// ❌ Bad: no metadata
await page.screenshot({ path: 'screenshot.png' });
// Cannot trace when and where it was captured
```

### DOM Snapshot Comparison

```typescript
// Pre-action snapshot
const beforeSnapshot = await page.content();

// Execute action
await page.click('#submit-button');

// Wait for state change
await page.waitForTimeout(1000);

// Post-action snapshot
const afterSnapshot = await page.content();

// Compare differences
if (beforeSnapshot !== afterSnapshot) {
  console.log('DOM changed');
}
```

### Mobile Device Emulation

```typescript
// Use Playwright built-in device emulation
const iPhone = devices['iPhone 13'];
const context = await browser.newContext({
  ...iPhone,
});

const page = await context.newPage();
await page.goto(url);
await page.screenshot({ path: 'mobile-verification.png' });
```

### Wait Strategies

```typescript
// ✅ Good: wait for specific conditions
await page.waitForSelector('#loading-spinner', { state: 'hidden' });
await page.waitForLoadState('networkidle');

// ❌ Bad: fixed wait
await page.waitForTimeout(3000); // Unreliable
```

## Common Verification Scenarios

### Scenario 1: Button Click Verification

```typescript
// Verify page response after button click
const button = await page.$('#submit-button');
const isDisabled = await button?.isDisabled();
console.log(`Button initial state: ${isDisabled ? 'disabled' : 'enabled'}`);

await page.click('#submit-button');

// Verify loading state
await page.waitForSelector('#loading-spinner');
await page.waitForSelector('#loading-spinner', { state: 'hidden' });

// Verify result
const result = await page.$eval('#result', el => el.textContent);
console.log(`Operation result: ${result}`);
```

### Scenario 2: Form Validation

```typescript
// Verify form submission
await page.fill('#email', 'test@example.com');
await page.fill('#password', 'password123');
await page.click('#login-button');

// Verify error message
const error = await page.$('.error-message');
if (error) {
  const errorText = await error.textContent();
  console.log(`Error message: ${errorText}`);
}

// Verify redirect
await page.waitForURL('**/dashboard');
console.log('Login successful, redirected to dashboard');
```

### Scenario 3: Visual Regression Verification

```typescript
// Screenshot comparison (requires pixelmatch or similar library)
import { compareScreenshots } from './visual-regression';

const baseline = await page.screenshot({ path: 'baseline.png' });
// Execute changes
const current = await page.screenshot({ path: 'current.png' });

const diff = await compareScreenshots(baseline, current);
if (diff.percentage > 0.01) {
  console.log(`Visual difference: ${(diff.percentage * 100).toFixed(2)}%`);
}
```

## Error Handling

| Error | Cause | Handling |
|---|---|---|
| `TimeoutError` | Element did not appear within timeout | Check selector correctness, increase wait time |
| `Navigation timeout` | Page load timed out | Check network, increase timeout |
| `Element not found` | Selector does not match any element | Check DOM structure, use more stable selectors |
| `Browser not found` | Browser not installed | Run `npx playwright install` |

## Performance Optimization

```typescript
// Reuse browser instance
const browser = await chromium.launch();

// Verify multiple pages in parallel
const pages = await Promise.all([
  browser.newPage().then(async p => { await p.goto(url1); return p; }),
  browser.newPage().then(async p => { await p.goto(url2); return p; }),
]);

// Batch screenshots
await Promise.all(pages.map((p, i) =>
  p.screenshot({ path: `page-${i}.png` })
));

await browser.close();
```

## CI/CD Integration

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
