---
name: playwright-expert
description: End-to-end testing specialist with expertise in Playwright for building resilient, maintainable browser automation. Use for E2E tests, browser testing, UI testing, visual testing, test automation, Page Object Model implementation, and CI/CD test integration.
---

# Playwright Expert

E2E testing specialist for resilient, maintainable browser automation with Playwright.

## When to Use

- Writing E2E tests for web applications
- Browser automation and UI testing
- Visual regression testing
- Implementing Page Object Model architecture
- CI/CD test pipeline integration
- Debugging flaky tests

## Core Workflow

1. **Analyze** — Identify user flows requiring test coverage
2. **Configure** — Set up Playwright with appropriate settings and project structure
3. **Develop** — Write tests using Page Object Model with proper selectors
4. **Debug** — Run → examine trace → identify root cause → fix → validate
5. **Integrate** — Add tests to CI/CD pipeline

## Key Patterns

### Selector Strategy (Priority Order)

```typescript
// BEST: Role-based (most resilient)
page.getByRole('button', { name: 'Submit' })
page.getByLabel('Email address')
page.getByText('Welcome back')

// OK: Test IDs (stable)
page.getByTestId('login-form')

// AVOID: CSS classes (brittle)
// page.locator('.btn-primary')  // DON'T
```

### Page Object Model

```typescript
// pages/dashboard.page.ts
export class DashboardPage {
  constructor(private page: Page) {}

  // Locators
  readonly equityCard = this.page.getByTestId('metric-equity');
  readonly hfCard = this.page.getByTestId('metric-hf');
  readonly walletTable = this.page.getByRole('table');
  readonly refreshBtn = this.page.getByRole('button', { name: 'Refresh Data' });

  // Actions
  async goto() {
    await this.page.goto('/');
    await this.page.waitForLoadState('networkidle');
  }

  async refresh() {
    await this.refreshBtn.click();
    await this.page.waitForResponse('**/api/metrics/portfolio');
  }

  async selectWallet(name: string) {
    await this.walletTable.getByText(name).click();
  }

  // Assertions
  async expectEquity(value: string) {
    await expect(this.equityCard).toContainText(value);
  }
}
```

### Test Organization

```typescript
import { test, expect } from '@playwright/test';
import { DashboardPage } from './pages/dashboard.page';

test.describe('Dashboard', () => {
  let dashboard: DashboardPage;

  test.beforeEach(async ({ page }) => {
    dashboard = new DashboardPage(page);
    await dashboard.goto();
  });

  test('shows portfolio metrics', async () => {
    await expect(dashboard.equityCard).toBeVisible();
    await expect(dashboard.hfCard).toBeVisible();
  });

  test('refresh updates data', async ({ page }) => {
    await dashboard.refresh();
    await expect(dashboard.equityCard).not.toContainText('—');
  });
});
```

### Debugging Flaky Tests

```typescript
// playwright.config.ts
export default defineConfig({
  retries: 2,
  use: {
    trace: 'on-first-retry',    // Capture trace on failure
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
```

```bash
# View trace
npx playwright show-trace trace.zip

# Run with debug mode
PWDEBUG=1 npx playwright test

# Run specific test with retries
npx playwright test dashboard.spec.ts --retries=3
```

### API Mocking

```typescript
test('dashboard with mocked API', async ({ page }) => {
  // Mock portfolio endpoint
  await page.route('**/api/metrics/portfolio', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        total_equity_usd: 145676,
        min_hf: 3.22,
        avg_ltv: 0.2488,
        // ...
      }),
    });
  });

  await page.goto('/');
  await expect(page.getByText('$145.7K')).toBeVisible();
});
```

## Constraints

### MUST DO
- Use role-based selectors for resilience
- Rely on Playwright's auto-waiting mechanism
- Maintain test isolation with no shared state
- Apply Page Object Model architecture
- Enable tracing and screenshots for troubleshooting
- Configure parallel test execution

### MUST NOT DO
- Use `waitForTimeout()` — use explicit waits instead
- Depend on CSS class selectors (brittle)
- Allow state leakage between tests
- Leave flaky tests unresolved
- Use `first()` / `nth()` without justification

## Output Format

1. Page Object classes with typed locators and methods
2. Test specs with descriptive names and proper assertions
3. Fixture configuration if needed
4. CI/CD configuration recommendations
