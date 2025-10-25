# Quickstart Guide: Assessment Results Visualization

**Feature**: 002-results-visualization
**Date**: 2025-10-25
**Prerequisites**: Node.js 20 LTS, PostgreSQL 15+, pnpm/npm/yarn

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Node.js | 20 LTS | JavaScript runtime |
| **Language** | TypeScript | 5.x | Type-safe development |
| **Frontend** | React | 18+ | UI framework |
| **Charts** | Recharts | 2.x | Visualization library |
| **Backend** | Express/Fastify | TBD | API server |
| **Database** | PostgreSQL | 15+ | Data persistence |
| **Testing** | Jest | 29+ | Unit/integration testing |
| **E2E Testing** | Playwright | 1.40+ | Browser automation |
| **Contract Testing** | Pact.js | 11+ | API contract validation |

## Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
# Install Node.js 20 LTS (if not already installed)
# macOS
brew install node@20

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should be v20.x.x
npm --version   # Should be v10.x.x
```

### 2. Install PostgreSQL 15+

```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt install postgresql-15 postgresql-contrib-15
sudo systemctl start postgresql

# Verify installation
psql --version  # Should be 15.x
```

### 3. Clone and Setup Project

```bash
# Navigate to project root
cd /path/to/direction_me

# Install dependencies
npm install

# Or with pnpm (recommended for monorepo)
pnpm install
```

### 4. Database Setup

```bash
# Create database
createdb direction_me_dev

# Run migrations (will be created in implementation phase)
npm run db:migrate

# Seed career mapping data (will be created in implementation phase)
npm run db:seed
```

### 5. Environment Configuration

Create `.env` file in project root:

```bash
# Database
DATABASE_URL=postgresql://localhost:5432/direction_me_dev
DATABASE_POOL_SIZE=10

# Server
PORT=3000
NODE_ENV=development

# Visualization Cache
CACHE_TTL_HOURS=24

# Analytics
CONSISTENCY_THRESHOLD=70
RETEST_RECOMMENDATION_ENABLED=true
```

### 6. Start Development Servers

```bash
# Terminal 1: Backend API server
npm run dev:backend

# Terminal 2: Frontend dev server
npm run dev:frontend

# Or run both concurrently
npm run dev
```

### 7. Verify Setup

Open browser to:
- **Frontend**: http://localhost:5173 (Vite default)
- **Backend API**: http://localhost:3000/api
- **API Documentation**: http://localhost:3000/api-docs (Swagger UI)

## Detailed Setup Guide

### Database Schema Creation

```sql
-- Connect to database
psql direction_me_dev

-- Create schema (migrations will handle this, but for reference)
CREATE TABLE assessment_responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  assessment_id UUID NOT NULL,
  domain VARCHAR(2) NOT NULL CHECK (domain IN ('IQ', 'EQ', 'DQ', 'AQ')),
  facet VARCHAR(100) NOT NULL,
  item_id VARCHAR(100) NOT NULL,
  question_type VARCHAR(20) NOT NULL CHECK (question_type IN ('multiple_choice', 'likert')),
  selected_answer TEXT NOT NULL,
  correct_answer TEXT,
  is_correct BOOLEAN,
  difficulty_weight NUMERIC(3,1) CHECK (difficulty_weight BETWEEN 1.0 AND 3.0),
  is_reverse_scored BOOLEAN NOT NULL DEFAULT false,
  raw_score INTEGER NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  time_spent_ms INTEGER NOT NULL,
  sequence_order INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_responses_user_domain ON assessment_responses(user_id, domain);
CREATE INDEX idx_responses_user_facet ON assessment_responses(user_id, domain, facet);
CREATE INDEX idx_responses_timestamp ON assessment_responses(timestamp);

-- See data-model.md for complete schema
```

### Project Structure Setup

```bash
# Create directory structure
mkdir -p backend/src/{models,services/{scoring,analytics,career},api/{routes,middleware}}
mkdir -p backend/tests/{unit/{scoring,analytics,career},integration/api,contract}
mkdir -p frontend/src/{components/{visualizations,results},services/{api,formatters},types}
mkdir -p frontend/tests/{unit/components,integration/visualizations,accessibility}

# Backend structure
backend/
├── src/
│   ├── models/              # Data models
│   │   ├── assessment_response.ts
│   │   ├── score_result.ts
│   │   ├── career_mapping.ts
│   │   └── analytics_log.ts
│   ├── services/            # Business logic
│   │   ├── scoring/
│   │   │   ├── iq_scorer.ts
│   │   │   ├── likert_scorer.ts
│   │   │   ├── facet_aggregator.ts
│   │   │   └── normalizer.ts
│   │   ├── analytics/
│   │   │   ├── consistency_checker.ts
│   │   │   ├── response_timer.ts
│   │   │   └── retest_recommender.ts
│   │   └── career/
│   │       └── career_matcher.ts
│   └── api/                 # API layer
│       ├── routes/
│       │   ├── results.ts
│       │   └── analytics.ts
│       └── middleware/
└── tests/                   # Test files

# Frontend structure
frontend/
├── src/
│   ├── components/
│   │   ├── visualizations/
│   │   │   ├── RadarChart.tsx
│   │   │   ├── FacetBarChart.tsx
│   │   │   ├── IkigaiMap.tsx
│   │   │   └── ResponseAnalytics.tsx
│   │   └── results/
│   │       ├── ResultsContainer.tsx
│   │       └── PartialResults.tsx
│   ├── services/
│   │   └── api/
│   │       └── results_api.ts
│   └── types/
│       ├── score_types.ts
│       └── visualization_types.ts
└── tests/
```

## Development Workflow

### Test-Driven Development (TDD)

**1. Write Test First**

```typescript
// backend/tests/unit/scoring/iq_scorer.test.ts
describe('IQ Scorer', () => {
  it('should calculate weighted IQ score correctly', () => {
    const responses = [
      { isCorrect: true, difficultyWeight: 1.0 },  // 1 point
      { isCorrect: true, difficultyWeight: 2.0 },  // 2 points
      { isCorrect: false, difficultyWeight: 3.0 }, // 0 points
      { isCorrect: true, difficultyWeight: 1.5 },  // 1.5 points
    ];

    const score = calculateIQScore(responses);
    expect(score).toBe(4.5); // 1 + 2 + 0 + 1.5
  });
});
```

**2. Implement Minimal Code**

```typescript
// backend/src/services/scoring/iq_scorer.ts
export function calculateIQScore(responses: AssessmentResponse[]): number {
  return responses.reduce((sum, response) => {
    const score = response.isCorrect ? response.difficultyWeight : 0;
    return sum + score;
  }, 0);
}
```

**3. Run Tests**

```bash
# Run all tests
npm test

# Run specific test file
npm test iq_scorer.test.ts

# Run with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Contract Testing Workflow

**Frontend Consumer Test**:

```typescript
// frontend/tests/contract/results_api.pact.test.ts
import { pactWith } from 'jest-pact';

pactWith({ consumer: 'Frontend', provider: 'Backend API' }, (interaction) => {
  interaction('get radar chart data for user', ({ provider, execute }) => {
    provider
      .given('user has completed all 4 assessments')
      .uponReceiving('request for radar data')
      .withRequest({
        method: 'GET',
        path: '/api/results/123/radar',
      })
      .willRespondWith({
        status: 200,
        body: {
          IQ: 75,
          EQ: 82,
          DQ: 68,
          AQ: 79,
        },
      });

    return execute(async () => {
      const data = await getRadarData('123');
      expect(data.IQ).toBe(75);
    });
  });
});
```

**Backend Provider Test**:

```typescript
// backend/tests/contract/api.pact.test.ts
import { Verifier } from '@pact-foundation/pact';

describe('Pact Verification', () => {
  it('should validate the expectations of Frontend', () => {
    return new Verifier({
      provider: 'Backend API',
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: ['./pacts/frontend-backend_api.json'],
    }).verifyProvider();
  });
});
```

### Visualization Development

**Component Development with Recharts**:

```tsx
// frontend/src/components/visualizations/RadarChart.tsx
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';

interface RadarChartProps {
  data: {
    IQ: number;
    EQ: number;
    DQ: number;
    AQ: number;
  };
}

export function AssessmentRadarChart({ data }: RadarChartProps) {
  const chartData = [
    { domain: 'IQ', score: data.IQ },
    { domain: 'EQ', score: data.EQ },
    { domain: 'DQ', score: data.DQ },
    { domain: 'AQ', score: data.AQ },
  ];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <RadarChart data={chartData}>
        <PolarGrid />
        <PolarAngleAxis dataKey="domain" />
        <Radar
          name="Assessment Scores"
          dataKey="score"
          stroke="#8884d8"
          fill="#8884d8"
          fillOpacity={0.6}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
```

**Testing Visualization Components**:

```typescript
// frontend/tests/unit/components/RadarChart.test.tsx
import { render, screen } from '@testing-library/react';
import { AssessmentRadarChart } from '@/components/visualizations/RadarChart';

describe('RadarChart', () => {
  it('should render all four domains', () => {
    const data = { IQ: 75, EQ: 82, DQ: 68, AQ: 79 };
    render(<AssessmentRadarChart data={data} />);

    expect(screen.getByText('IQ')).toBeInTheDocument();
    expect(screen.getByText('EQ')).toBeInTheDocument();
    expect(screen.getByText('DQ')).toBeInTheDocument();
    expect(screen.getByText('AQ')).toBeInTheDocument();
  });

  it('should meet accessibility standards', async () => {
    const { container } = render(<AssessmentRadarChart data={...} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Common Development Tasks

### Running Score Calculations Locally

```bash
# Start backend with database connection
npm run dev:backend

# In another terminal, use curl to test
curl -X POST http://localhost:3000/api/scores/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "assessmentId": "987fcdeb-51a2-43d7-8f9e-123456789abc",
    "domain": "IQ"
  }'
```

### Testing Visualizations

```bash
# Run Playwright E2E tests
npm run test:e2e

# Run in headed mode (see browser)
npm run test:e2e -- --headed

# Run specific test
npm run test:e2e -- radar-chart.spec.ts

# Generate test report
npm run test:e2e -- --reporter=html
```

### Accessibility Testing

```bash
# Run jest-axe tests
npm test -- accessibility

# Manual screen reader testing (macOS)
# 1. Enable VoiceOver: Cmd + F5
# 2. Navigate to http://localhost:5173
# 3. Test chart navigation with VoiceOver

# Run Lighthouse audit
npx lighthouse http://localhost:5173 --only-categories=accessibility --view
```

### Database Operations

```bash
# Reset database (drop all tables and re-migrate)
npm run db:reset

# Create new migration
npm run db:migrate:create add_percentile_rank

# Run migrations
npm run db:migrate

# Rollback last migration
npm run db:migrate:down

# Seed career mapping data
npm run db:seed

# Open PostgreSQL console
psql direction_me_dev
```

### Performance Profiling

```bash
# Backend performance profiling
npm run dev:backend -- --inspect

# Open Chrome DevTools
# Navigate to chrome://inspect
# Click "inspect" on the Node.js process

# Frontend performance profiling
npm run build
npm run preview
# Open Chrome DevTools > Performance tab
# Record user interaction with visualizations
```

## Environment-Specific Configuration

### Development (.env.development)

```bash
DATABASE_URL=postgresql://localhost:5432/direction_me_dev
NODE_ENV=development
LOG_LEVEL=debug
CACHE_TTL_HOURS=1
ENABLE_PROFILING=true
```

### Testing (.env.test)

```bash
DATABASE_URL=postgresql://localhost:5432/direction_me_test
NODE_ENV=test
LOG_LEVEL=error
CACHE_TTL_HOURS=0
MOCK_EXTERNAL_SERVICES=true
```

### Production (.env.production)

```bash
DATABASE_URL=${DATABASE_URL}  # From environment
NODE_ENV=production
LOG_LEVEL=info
CACHE_TTL_HOURS=24
ENABLE_PROFILING=false
```

## Troubleshooting

### PostgreSQL Connection Issues

```bash
# Check PostgreSQL is running
pg_isready

# Check if database exists
psql -l | grep direction_me

# Check connection string
psql $DATABASE_URL

# Reset PostgreSQL permissions
sudo -u postgres psql -c "ALTER USER $USER WITH SUPERUSER;"
```

### TypeScript Compilation Errors

```bash
# Clear TypeScript cache
rm -rf node_modules/.cache

# Regenerate types
npm run typecheck

# Check tsconfig.json
cat tsconfig.json
```

### Test Failures

```bash
# Run tests in verbose mode
npm test -- --verbose

# Run single test file
npm test -- path/to/test.ts

# Clear Jest cache
npm test -- --clearCache

# Debug test with Node inspector
node --inspect-brk node_modules/.bin/jest --runInBand path/to/test.ts
```

### Visualization Not Rendering

```bash
# Check Recharts version
npm list recharts

# Verify React version compatibility
npm list react

# Clear frontend cache
rm -rf frontend/.vite

# Check browser console for errors
# Open DevTools > Console
```

## Performance Benchmarks

### Target Metrics (from Success Criteria)

| Metric | Target | Verification Method |
|--------|--------|---------------------|
| Visualization render time | <2s (p95) | Lighthouse, Real User Monitoring |
| Score calculation time | <500ms | Backend profiling |
| API response time | <1s (p95) | Load testing with k6 |
| Concurrent calculations | 100 users | k6 load test script |
| Accessibility score | WCAG 2.1 AA | Lighthouse, axe-core |

### Running Performance Tests

```bash
# Install k6 (load testing)
brew install k6  # macOS
# or download from https://k6.io

# Run load test
k6 run performance/load-test.js

# Generate performance report
npm run perf:report
```

### Example k6 Load Test

```javascript
// performance/load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp up to 50 users
    { duration: '1m', target: 100 },   // Hold at 100 users
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests < 2s
  },
};

export default function () {
  const res = http.get('http://localhost:3000/api/results/123');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 2s': (r) => r.timings.duration < 2000,
  });
  sleep(1);
}
```

## Next Steps

1. **Implement Core Scoring Logic** (TDD approach):
   - Start with `iq_scorer.test.ts` → implement `iq_scorer.ts`
   - Continue with `likert_scorer.test.ts` → implement `likert_scorer.ts`
   - Build up to full calculation pipeline

2. **Create Database Migrations**:
   - Generate migration files for all tables in `data-model.md`
   - Create seed data for `career_mappings` table

3. **Build API Endpoints**:
   - Implement routes from `contracts/openapi.yaml`
   - Use contract tests to validate implementation

4. **Develop Visualization Components**:
   - Start with `RadarChart.tsx` (P1 priority)
   - Add accessibility features (ARIA labels, keyboard navigation)
   - Test with Playwright for visual regression

5. **Integration Testing**:
   - End-to-end flow: assessment completion → score calculation → visualization render
   - Performance validation against <2s target
   - Accessibility audit with screen readers

## Additional Resources

- **TypeScript**: https://www.typescriptlang.org/docs/
- **React 18**: https://react.dev/
- **Recharts**: https://recharts.org/en-US/
- **PostgreSQL 15**: https://www.postgresql.org/docs/15/
- **Jest**: https://jestjs.io/docs/getting-started
- **Playwright**: https://playwright.dev/docs/intro
- **Pact.js**: https://docs.pact.io/implementation_guides/javascript
- **OpenAPI**: https://swagger.io/specification/

## Getting Help

- Check `data-model.md` for database schema reference
- Check `contracts/openapi.yaml` for API specification
- Check `research.md` for technology stack decisions and rationale
- Check `spec.md` for functional requirements and acceptance criteria
