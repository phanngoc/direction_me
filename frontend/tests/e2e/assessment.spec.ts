/**
 * End-to-end tests for assessment flow
 */
import { test, expect } from '@playwright/test';

test.describe('Assessment Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock API responses
    await page.route('**/api/v1/auth/login', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          access_token: 'mock-token',
          user: {
            id: 'user-123',
            email: 'test@example.com',
            full_name: 'Test User',
            age: 20
          }
        })
      });
    });

    await page.route('**/api/v1/assessments', async route => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            id: 'assessment-123',
            user_id: 'user-123',
            status: 'in_progress',
            started_at: new Date().toISOString(),
            total_questions: 0,
            answered_questions: 0
          })
        });
      }
    });

    await page.route('**/api/v1/assessments/assessment-123/questions', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: 'q1',
            category: 'IQ',
            facet: 'LR',
            question_text: 'What is 2 + 2?',
            question_type: 'MCQ',
            options: ['3', '4', '5', '6'],
            difficulty_weight: 1.0,
            reverse_score: false
          },
          {
            id: 'q2',
            category: 'EQ',
            facet: 'Empathy',
            question_text: 'I can easily understand other people\'s emotions',
            question_type: 'Likert',
            difficulty_weight: 1.0,
            reverse_score: false
          },
          {
            id: 'q3',
            category: 'DQ',
            facet: 'InfoLiteracy',
            question_text: 'I know how to evaluate information reliability online',
            question_type: 'Likert',
            difficulty_weight: 1.0,
            reverse_score: false
          },
          {
            id: 'q4',
            category: 'AQ',
            facet: 'Control',
            question_text: 'I believe I can control difficult situations',
            question_type: 'Likert',
            difficulty_weight: 1.0,
            reverse_score: false
          }
        ])
      });
    });

    await page.route('**/api/v1/assessments/assessment-123/answers', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'Answers submitted successfully' })
      });
    });

    await page.route('**/api/v1/assessments/assessment-123/complete', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'Assessment completed successfully' })
      });
    });

    await page.route('**/api/v1/results/assessment-123', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 'result-123',
          assessment_id: 'assessment-123',
          iq_score: 85.5,
          eq_score: 78.2,
          dq_score: 92.1,
          aq_score: 73.8,
          calculated_at: new Date().toISOString()
        })
      });
    });
  });

  test('should complete full assessment flow', async ({ page }) => {
    // Navigate to assessment page
    await page.goto('/assessment');

    // Wait for questions to load
    await expect(page.locator('h1')).toContainText('Đánh giá 4 chỉ số phát triển');
    await expect(page.locator('.question-card')).toBeVisible();

    // Check progress bar
    await expect(page.locator('.progress-info')).toContainText('Câu hỏi 1 / 4');
    await expect(page.locator('.progress-fill')).toHaveCSS('width', '25%');

    // Answer first question (IQ MCQ)
    await page.locator('input[value="2"]').check(); // Select "4" as answer
    await expect(page.locator('input[value="2"]')).toBeChecked();

    // Navigate to next question
    await page.click('button:has-text("Câu tiếp theo")');
    await expect(page.locator('.progress-info')).toContainText('Câu hỏi 2 / 4');
    await expect(page.locator('.progress-fill')).toHaveCSS('width', '50%');

    // Answer second question (EQ Likert)
    await page.locator('input[value="4"]').check(); // Select "Đồng ý"
    await expect(page.locator('input[value="4"]')).toBeChecked();

    // Navigate to next question
    await page.click('button:has-text("Câu tiếp theo")');
    await expect(page.locator('.progress-info')).toContainText('Câu hỏi 3 / 4');
    await expect(page.locator('.progress-fill')).toHaveCSS('width', '75%');

    // Answer third question (DQ Likert)
    await page.locator('input[value="5"]').check(); // Select "Hoàn toàn đồng ý"
    await expect(page.locator('input[value="5"]')).toBeChecked();

    // Navigate to next question
    await page.click('button:has-text("Câu tiếp theo")');
    await expect(page.locator('.progress-info')).toContainText('Câu hỏi 4 / 4');
    await expect(page.locator('.progress-fill')).toHaveCSS('width', '100%');

    // Answer fourth question (AQ Likert)
    await page.locator('input[value="3"]').check(); // Select "Trung lập"
    await expect(page.locator('input[value="3"]')).toBeChecked();

    // Complete assessment
    await page.click('button:has-text("Hoàn thành đánh giá")');

    // Should redirect to results page
    await expect(page).toHaveURL(/\/results\/assessment-123/);
    await expect(page.locator('h1')).toContainText('Kết quả đánh giá của bạn');
  });

  test('should handle navigation between questions', async ({ page }) => {
    await page.goto('/assessment');
    await expect(page.locator('.question-card')).toBeVisible();

    // Answer first question
    await page.locator('input[value="2"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    // Answer second question
    await page.locator('input[value="4"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    // Answer third question
    await page.locator('input[value="5"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    // Answer fourth question
    await page.locator('input[value="3"]').check();

    // Go back to previous question
    await page.click('button:has-text("Câu trước")');
    await expect(page.locator('.progress-info')).toContainText('Câu hỏi 3 / 4');

    // Verify answer is still selected
    await expect(page.locator('input[value="5"]')).toBeChecked();

    // Go forward again
    await page.click('button:has-text("Câu tiếp theo")');
    await expect(page.locator('.progress-info')).toContainText('Câu hỏi 4 / 4');

    // Verify answer is still selected
    await expect(page.locator('input[value="3"]')).toBeChecked();
  });

  test('should show answer summary', async ({ page }) => {
    await page.goto('/assessment');
    await expect(page.locator('.question-card')).toBeVisible();

    // Answer first question
    await page.locator('input[value="2"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    // Check answer summary
    await expect(page.locator('.answer-summary')).toContainText('Đã trả lời: 1 / 4 câu hỏi');

    // Answer second question
    await page.locator('input[value="4"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    // Check updated summary
    await expect(page.locator('.answer-summary')).toContainText('Đã trả lời: 2 / 4 câu hỏi');
  });

  test('should handle loading states', async ({ page }) => {
    // Mock slow API response
    await page.route('**/api/v1/assessments/assessment-123/questions', async route => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([])
      });
    });

    await page.goto('/assessment');

    // Should show loading state
    await expect(page.locator('.loading-spinner')).toBeVisible();
    await expect(page.locator('.loading-text')).toContainText('Đang tải câu hỏi...');
  });

  test('should handle errors gracefully', async ({ page }) => {
    // Mock error response
    await page.route('**/api/v1/assessments/assessment-123/questions', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' })
      });
    });

    await page.goto('/assessment');

    // Should show error state
    await expect(page.locator('.error-icon')).toBeVisible();
    await expect(page.locator('.error-title')).toContainText('Có lỗi xảy ra');
    await expect(page.locator('button:has-text("Thử lại")')).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.goto('/assessment');
    await expect(page.locator('.question-card')).toBeVisible();

    // Check that mobile styles are applied
    const questionCard = page.locator('.question-card');
    await expect(questionCard).toHaveCSS('padding', '16px'); // Mobile padding

    // Answer questions
    await page.locator('input[value="2"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    await page.locator('input[value="4"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    await page.locator('input[value="5"]').check();
    await page.click('button:has-text("Câu tiếp theo")');

    await page.locator('input[value="3"]').check();
    await page.click('button:has-text("Hoàn thành đánh giá")');

    // Should redirect to results
    await expect(page).toHaveURL(/\/results\/assessment-123/);
  });

  test('should validate required answers', async ({ page }) => {
    await page.goto('/assessment');
    await expect(page.locator('.question-card')).toBeVisible();

    // Try to go to next question without answering
    const nextButton = page.locator('button:has-text("Câu tiếp theo")');
    await expect(nextButton).toBeDisabled();

    // Answer the question
    await page.locator('input[value="2"]').check();
    await expect(nextButton).toBeEnabled();

    // Continue with rest of assessment
    await page.click('button:has-text("Câu tiếp theo")');
    await page.locator('input[value="4"]').check();
    await page.click('button:has-text("Câu tiếp theo")');
    await page.locator('input[value="5"]').check();
    await page.click('button:has-text("Câu tiếp theo")');
    await page.locator('input[value="3"]').check();

    // Complete assessment
    await page.click('button:has-text("Hoàn thành đánh giá")');
    await expect(page).toHaveURL(/\/results\/assessment-123/);
  });
});