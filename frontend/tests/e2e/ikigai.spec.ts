/**
 * End-to-end tests for Ikigai analysis flow.
 */
import { test, expect } from '@playwright/test';

test.describe('Ikigai Analysis Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock API responses for Ikigai analysis
    await page.route('**/api/v1/ikigai/analysis/*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          message: 'Ikigai analysis retrieved successfully',
          data: {
            ikigai_scores: {
              ikigai_love: 75.0,
              ikigai_good_at: 80.0,
              ikigai_world_needs: 70.0,
              ikigai_paid_for: 85.0,
              ikigai_harmonic: 77.5,
              ikigai_geometric: 77.2
            },
            interpretation: {
              quadrant: 'Balanced',
              description: 'Bạn có sự cân bằng tốt giữa các yếu tố Ikigai',
              recommendations: [
                'Tiếp tục phát triển kỹ năng hiện có',
                'Tìm kiếm cơ hội để kết hợp đam mê với nghề nghiệp',
                'Tham gia các hoạt động cộng đồng để phát triển yếu tố "World Needs"'
              ]
            },
            development_recommendations: [
              'Phát triển kỹ năng giao tiếp để tăng EQ',
              'Học thêm về công nghệ để cải thiện DQ',
              'Tham gia các dự án thực tế để phát triển AQ'
            ]
          }
        })
      });
    });

    // Mock career suggestions API
    await page.route('**/api/v1/careers/suggestions/*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          message: 'Career suggestions retrieved successfully',
          data: [
            {
              career_name: 'Software Engineer',
              fit_score: 85.0,
              rank: 1,
              explanation: 'Bạn có tiềm năng rất cao để thành công trong Software Engineer'
            },
            {
              career_name: 'Data Scientist',
              fit_score: 80.0,
              rank: 2,
              explanation: 'Bạn có tiềm năng tốt để phát triển trong Data Scientist'
            },
            {
              career_name: 'UX Designer',
              fit_score: 75.0,
              rank: 3,
              explanation: 'Bạn có thể phát triển để phù hợp với UX Designer'
            }
          ]
        })
      });
    });

    // Mock career details API
    await page.route('**/api/v1/careers/details/*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          message: 'Career details retrieved successfully',
          data: {
            career_name: 'Software Engineer',
            description: 'Phát triển và duy trì phần mềm ứng dụng',
            key_skills: ['Programming', 'Problem Solving', 'Teamwork'],
            education_requirements: 'Bachelor in Computer Science or related field',
            experience_level: 'Entry to Senior level',
            salary_range: '15-50 triệu VND/tháng',
            growth_outlook: 'Tăng trưởng mạnh trong 5-10 năm tới'
          }
        })
      });
    });
  });

  test('should display Ikigai analysis page', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Check page title
    await expect(page.locator('h1')).toContainText('Phân tích Ikigai');
    
    // Check Ikigai quadrant display
    await expect(page.locator('.ikigai-quadrant')).toBeVisible();
    
    // Check chart container
    await expect(page.locator('.ikigai-chart-container')).toBeVisible();
  });

  test('should display Ikigai scores correctly', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Wait for data to load
    await page.waitForSelector('.ikigai-scores');
    
    // Check individual scores
    await expect(page.locator('[data-testid="ikigai-love"]')).toContainText('75.0');
    await expect(page.locator('[data-testid="ikigai-good-at"]')).toContainText('80.0');
    await expect(page.locator('[data-testid="ikigai-world-needs"]')).toContainText('70.0');
    await expect(page.locator('[data-testid="ikigai-paid-for"]')).toContainText('85.0');
    
    // Check harmonic and geometric means
    await expect(page.locator('[data-testid="ikigai-harmonic"]')).toContainText('77.5');
    await expect(page.locator('[data-testid="ikigai-geometric"]')).toContainText('77.2');
  });

  test('should display Ikigai chart', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Wait for chart to load
    await page.waitForSelector('canvas');
    
    // Check that chart canvas is visible
    const chartCanvas = page.locator('canvas');
    await expect(chartCanvas).toBeVisible();
    
    // Check chart dimensions
    const canvasBox = await chartCanvas.boundingBox();
    expect(canvasBox?.width).toBeGreaterThan(0);
    expect(canvasBox?.height).toBeGreaterThan(0);
  });

  test('should display interpretation and recommendations', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Wait for content to load
    await page.waitForSelector('.ikigai-interpretation');
    
    // Check quadrant
    await expect(page.locator('.ikigai-quadrant')).toContainText('Balanced');
    
    // Check description
    await expect(page.locator('.ikigai-description')).toContainText('Bạn có sự cân bằng tốt giữa các yếu tố Ikigai');
    
    // Check recommendations
    const recommendations = page.locator('.ikigai-recommendations li');
    await expect(recommendations).toHaveCount(3);
    await expect(recommendations.nth(0)).toContainText('Tiếp tục phát triển kỹ năng hiện có');
  });

  test('should navigate to career suggestions', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Click on careers tab
    await page.click('[data-testid="careers-tab"]');
    
    // Wait for career suggestions to load
    await page.waitForSelector('.career-suggestions');
    
    // Check that career suggestions are displayed
    await expect(page.locator('.career-suggestion')).toHaveCount(3);
    
    // Check first career suggestion
    const firstSuggestion = page.locator('.career-suggestion').first();
    await expect(firstSuggestion).toContainText('Software Engineer');
    await expect(firstSuggestion).toContainText('85.0');
    await expect(firstSuggestion).toContainText('Rank #1');
  });

  test('should display career details when clicked', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Navigate to careers tab
    await page.click('[data-testid="careers-tab"]');
    await page.waitForSelector('.career-suggestions');
    
    // Click on first career suggestion
    await page.click('.career-suggestion:first-child .view-details-btn');
    
    // Wait for career details modal or page
    await page.waitForSelector('.career-details');
    
    // Check career details
    await expect(page.locator('.career-details h3')).toContainText('Software Engineer');
    await expect(page.locator('.career-description')).toContainText('Phát triển và duy trì phần mềm ứng dụng');
    await expect(page.locator('.key-skills')).toContainText('Programming');
  });

  test('should navigate to learning path', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Click on learning path button
    await page.click('[data-testid="learning-path-btn"]');
    
    // Should navigate to learning path page
    await expect(page).toHaveURL(/.*learning-path.*/);
  });

  test('should handle loading states', async ({ page }) => {
    // Mock slow API response
    await page.route('**/api/v1/ikigai/analysis/*', async route => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: { ikigai_scores: {}, interpretation: {}, development_recommendations: [] }
        })
      });
    });

    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Check loading state
    await expect(page.locator('.loading-spinner')).toBeVisible();
    
    // Wait for loading to complete
    await page.waitForSelector('.ikigai-scores', { timeout: 5000 });
    
    // Loading spinner should be hidden
    await expect(page.locator('.loading-spinner')).not.toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API error
    await page.route('**/api/v1/ikigai/analysis/*', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          success: false,
          message: 'Internal server error'
        })
      });
    });

    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Check error message
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText('Có lỗi xảy ra khi tải phân tích Ikigai');
    
    // Check retry button
    await expect(page.locator('.retry-btn')).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Check that content is visible on mobile
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('.ikigai-chart-container')).toBeVisible();
    
    // Check that tabs are accessible on mobile
    await expect(page.locator('[data-testid="overview-tab"]')).toBeVisible();
    await expect(page.locator('[data-testid="careers-tab"]')).toBeVisible();
    await expect(page.locator('[data-testid="recommendations-tab"]')).toBeVisible();
  });

  test('should allow retaking assessment', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Click retake assessment button
    await page.click('[data-testid="retake-assessment-btn"]');
    
    // Should navigate to assessment page
    await expect(page).toHaveURL(/.*assessment.*/);
  });

  test('should display development recommendations', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Click on recommendations tab
    await page.click('[data-testid="recommendations-tab"]');
    
    // Wait for recommendations to load
    await page.waitForSelector('.development-recommendations');
    
    // Check recommendations
    const recommendations = page.locator('.development-recommendations li');
    await expect(recommendations).toHaveCount(3);
    await expect(recommendations.nth(0)).toContainText('Phát triển kỹ năng giao tiếp để tăng EQ');
  });

  test('should allow sharing results', async ({ page }) => {
    await page.goto('/ikigai?assessment_result_id=test-123');
    
    // Click share button
    await page.click('[data-testid="share-btn"]');
    
    // Check that share modal appears
    await expect(page.locator('.share-modal')).toBeVisible();
    
    // Check share options
    await expect(page.locator('.share-option')).toHaveCount(3); // Facebook, Twitter, Copy Link
  });

  test('should validate assessment result ID', async ({ page }) => {
    // Test with invalid ID
    await page.goto('/ikigai?assessment_result_id=invalid-id');
    
    // Should show error for invalid ID
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText('ID không hợp lệ');
  });

  test('should handle missing assessment result ID', async ({ page }) => {
    // Test without ID
    await page.goto('/ikigai');
    
    // Should redirect to assessment or show error
    await expect(page).toHaveURL(/.*assessment.*|.*error.*/);
  });
});