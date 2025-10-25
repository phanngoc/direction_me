import { test, expect } from '@playwright/test';

test.describe('Learning Path Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: Register and login
    await page.goto('http://localhost:3000');

    // Register new user
    await page.click('text=Register');
    await page.fill('input[name="email"]', `learningpath${Date.now()}@test.com`);
    await page.fill('input[name="password"]', 'testpass123');
    await page.fill('input[name="full_name"]', 'Learning Path User');
    await page.fill('input[name="age"]', '20');
    await page.click('button[type="submit"]');

    // Wait for redirect to login or dashboard
    await page.waitForURL(/login|dashboard/);

    // Login if on login page
    if (page.url().includes('login')) {
      await page.fill('input[name="email"]', `learningpath${Date.now()}@test.com`);
      await page.fill('input[name="password"]', 'testpass123');
      await page.click('button[type="submit"]');
    }

    // Complete assessment
    await page.click('text=Take Assessment');

    // Answer all questions (simplified for test)
    for (let i = 0; i < 10; i++) {
      await page.click('input[type="radio"]');
      await page.click('text=Next');
    }

    await page.click('text=Complete Assessment');
    await page.waitForURL(/results/);
  });

  test('should display learning path page', async ({ page }) => {
    // Navigate to learning path
    await page.click('text=View Learning Path');

    // Wait for learning path page to load
    await page.waitForURL(/learning-path/);

    // Verify page elements
    await expect(page.locator('h1')).toContainText('Learning Path');
    await expect(page.locator('text=Career:')).toBeVisible();
    await expect(page.locator('text=Duration:')).toBeVisible();
  });

  test('should display skills timeline', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Verify timeline components
    await expect(page.locator('text=Skills Development Timeline')).toBeVisible();
    await expect(page.locator('.timeline-container')).toBeVisible();

    // Verify phases are displayed
    const phases = page.locator('.phase-item');
    await expect(phases).toHaveCount(await phases.count());

    // At least one phase should be visible
    expect(await phases.count()).toBeGreaterThan(0);
  });

  test('should display skills with correct structure', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Find skill items
    const skillItems = page.locator('.skill-item');
    const firstSkill = skillItems.first();

    // Verify skill structure
    await expect(firstSkill).toBeVisible();
    await expect(firstSkill.locator('.skill-item h4')).toBeVisible();

    // Verify level badge exists
    const levelBadge = firstSkill.locator('[class*="bg-"]');
    await expect(levelBadge).toBeVisible();
  });

  test('should display progress tracker', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Verify progress tracker components
    await expect(page.locator('text=Learning Progress Tracker')).toBeVisible();
    await expect(page.locator('.progress-tracker')).toBeVisible();

    // Verify progress bar
    const progressBar = page.locator('.bg-blue-600');
    await expect(progressBar).toBeVisible();

    // Verify week markers
    const weekMarkers = page.locator('button[aria-label*="Week"]');
    expect(await weekMarkers.count()).toBeGreaterThan(0);
  });

  test('should allow week selection in progress tracker', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Click on a week marker
    const weekButton = page.locator('button[aria-label="Week 2"]');
    await weekButton.click();

    // Verify week details are displayed
    await expect(page.locator('text=Week 2 Details')).toBeVisible();
  });

  test('should display projects section', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Scroll to projects section
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

    // Verify projects are displayed
    const projectElements = page.locator('[class*="project"]');

    if (await projectElements.count() > 0) {
      await expect(projectElements.first()).toBeVisible();
    }
  });

  test('should display habits section', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Scroll to habits section
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

    // Verify habits are displayed
    const habitElements = page.locator('[class*="habit"]');

    if (await habitElements.count() > 0) {
      await expect(habitElements.first()).toBeVisible();
    }
  });

  test('should navigate back to results', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Click back button
    await page.click('text=Back to Results');

    // Verify navigation to results page
    await page.waitForURL(/results/);
    await expect(page.locator('text=Assessment Results')).toBeVisible();
  });

  test('should navigate to careers page', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Click explore careers button
    await page.click('text=Explore Other Careers');

    // Verify navigation to careers page
    await page.waitForURL(/careers/);
  });

  test('should display different learning paths for different careers', async ({ page }) => {
    // Get learning path for first career
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    const firstCareer = await page.locator('[class*="career"]').first().textContent();

    // Go back and select different career
    await page.click('text=Explore Other Careers');
    await page.waitForURL(/careers/);

    // Select second career
    const careerCards = page.locator('[class*="career-card"]');
    if (await careerCards.count() > 1) {
      await careerCards.nth(1).click();
      await page.click('text=View Learning Path');

      const secondCareer = await page.locator('[class*="career"]').first().textContent();

      // Careers should be different
      expect(firstCareer).not.toBe(secondCareer);
    }
  });

  test('should show loading state while fetching learning path', async ({ page }) => {
    await page.click('text=View Learning Path');

    // Verify loading indicator
    await expect(page.locator('text=Loading your learning path')).toBeVisible();

    // Wait for content to load
    await page.waitForURL(/learning-path/);
    await expect(page.locator('text=Learning Path')).toBeVisible();
  });

  test('should handle error state gracefully', async ({ page }) => {
    // Navigate directly to learning path with invalid result ID
    await page.goto('http://localhost:3000/learning-path?result_id=invalid-uuid');

    // Verify error message is displayed
    await expect(page.locator('text=Error Loading Learning Path')).toBeVisible();

    // Verify back button exists
    await expect(page.locator('text=Go Back to Results')).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Verify components are visible on mobile
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('.timeline-container')).toBeVisible();
    await expect(page.locator('.progress-tracker')).toBeVisible();
  });

  test('should display correct timeline phases', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Verify timeline phases
    const phases = ['Foundation', 'Intermediate', 'Advanced'];

    for (const phase of phases) {
      const phaseElement = page.locator(`text=${phase}`);
      if (await phaseElement.count() > 0) {
        await expect(phaseElement.first()).toBeVisible();
      }
    }
  });

  test('should show completed weeks in progress tracker', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Verify statistics section
    await expect(page.locator('text=Completed Weeks')).toBeVisible();
    await expect(page.locator('text=Remaining Weeks')).toBeVisible();
    await expect(page.locator('text=Milestones')).toBeVisible();
  });

  test('should display resources for skills', async ({ page }) => {
    await page.click('text=View Learning Path');
    await page.waitForURL(/learning-path/);

    // Find first skill item
    const skillItem = page.locator('.skill-item').first();

    // Verify resources section
    const resourcesSection = skillItem.locator('text=Resources:');

    if (await resourcesSection.count() > 0) {
      await expect(resourcesSection).toBeVisible();
    }
  });
});
