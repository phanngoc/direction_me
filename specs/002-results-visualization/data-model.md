# Data Model: Assessment Results Visualization and Scoring

**Feature**: 002-results-visualization
**Date**: 2025-10-25
**Database**: PostgreSQL 15+

## Overview

This document defines the data model for storing assessment responses, calculated scores, career mappings, and analytics logs. The model is optimized for:
- Score calculation accuracy (SC-001: 100% accuracy)
- Query performance for visualization data retrieval (SC-002: <2s render time)
- Flexible storage of varying assessment structures (IQ vs Likert)
- Analytics for consistency detection and response time tracking

---

## Core Entities

### 1. AssessmentResponse

**Purpose**: Store individual question responses from assessments

**Table**: `assessment_responses`

```typescript
interface AssessmentResponse {
  id: string;                    // UUID primary key
  userId: string;                // FK to users table
  assessmentId: string;          // Identifies assessment session
  domain: "IQ" | "EQ" | "DQ" | "AQ";
  facet: string;                 // e.g., "Logical", "Self-awareness"
  itemId: string;                // Question identifier
  questionType: "multiple_choice" | "likert";

  // Response data
  selectedAnswer: string;        // User's answer
  correctAnswer?: string;        // For IQ only
  isCorrect?: boolean;           // For IQ only
  difficultyWeight?: number;     // For IQ only (1.0-3.0 range)
  isReverseScored: boolean;      // For Likert only
  rawScore: number;              // 1-5 for Likert, 0/1 for IQ

  // Metadata
  timestamp: Date;               // When answered
  timeSpentMs: number;           // Milliseconds to answer
  sequenceOrder: number;         // Question order in session

  // Indexes
  createdAt: Date;
  updatedAt: Date;
}
```

**Indexes**:
- Primary: `id`
- Composite: `(userId, assessmentId, domain)` for fast session retrieval
- Composite: `(userId, domain, facet)` for facet-level aggregation
- Single: `timestamp` for analytics time-series queries

**Validation Rules**:
- `difficultyWeight`: Must be between 1.0 and 3.0 when present
- `rawScore`: Must be 0 or 1 for IQ, 1-5 for Likert
- `timeSpentMs`: Must be > 0
- `isCorrect` and `correctAnswer`: Required only when `questionType` = "multiple_choice"

---

### 2. ScoreResult

**Purpose**: Store calculated scores at facet and domain levels

**Table**: `score_results`

```typescript
interface ScoreResult {
  id: string;                    // UUID primary key
  userId: string;                // FK to users table
  assessmentId: string;          // Assessment session
  domain: "IQ" | "EQ" | "DQ" | "AQ";

  // Domain-level scores
  rawDomainScore: number;        // Pre-normalization score
  normalizedScore: number;       // 0-100 scale
  percentileRank?: number;       // Compared to all users (optional)

  // Facet-level scores (JSONB for flexibility)
  facetScores: {
    [facetName: string]: {
      rawScore: number;
      normalizedScore: number;
      itemCount: number;         // Number of questions in this facet
    };
  };

  // Calculation metadata
  totalItems: number;            // Total questions answered
  completionPercentage: number;  // % of domain completed
  calculatedAt: Date;            // When score was computed

  // Indexes
  createdAt: Date;
  updatedAt: Date;
}
```

**Indexes**:
- Primary: `id`
- Unique: `(userId, assessmentId, domain)` - one score per domain per session
- Composite: `(userId, domain)` for user profile queries
- Single: `calculatedAt` for cache invalidation

**Validation Rules**:
- `normalizedScore`: Must be 0-100
- `percentileRank`: Must be 0-100 when present
- `completionPercentage`: Must be 0-100
- `facetScores`: Must contain at least one facet entry

**Derived Data**:
- `normalizedScore`: Calculated from `rawDomainScore` using domain-specific normalization formula
- `percentileRank`: Calculated by comparing to all users' scores in same domain (updated periodically)

---

### 3. CareerMapping

**Purpose**: Define rules for mapping score combinations to career recommendations

**Table**: `career_mappings`

```typescript
interface CareerMapping {
  id: string;                    // UUID primary key

  // Career information
  career: {
    id: string;
    name: string;                // e.g., "Clinical Psychologist"
    category: string;            // e.g., "Healthcare", "Technology"
    description: string;
  };

  // Score thresholds (JSONB for flexibility)
  thresholds: {
    IQ?: { min?: number; max?: number };
    EQ?: { min?: number; max?: number };
    DQ?: { min?: number; max?: number };
    AQ?: { min?: number; max?: number };
  };

  // Ikigai map placement
  intersectionZones: string[];   // e.g., ["IQ+EQ", "IQ+EQ+DQ"]

  // Recommendation details
  rationale: string;             // Why this career matches (FR-012)
  priority: number;              // Ranking when multiple matches (1-100)

  // Metadata
  isActive: boolean;             // Enable/disable without deletion
  createdAt: Date;
  updatedAt: Date;
}
```

**Indexes**:
- Primary: `id`
- GIN: `thresholds` JSONB for efficient threshold queries
- Single: `priority` for ranking
- Single: `isActive` for filtering active careers

**Validation Rules**:
- `thresholds`: At least one domain threshold must be specified
- Threshold values: 0-100 range
- `priority`: 1-100 range
- `intersectionZones`: Must contain valid zone identifiers

**Query Pattern**:
```sql
-- Find careers matching user scores
SELECT * FROM career_mappings
WHERE isActive = true
  AND (thresholds->'IQ'->>'min' IS NULL OR (thresholds->'IQ'->>'min')::int <= user_iq_score)
  AND (thresholds->'IQ'->>'max' IS NULL OR (thresholds->'IQ'->>'max')::int >= user_iq_score)
  -- Repeat for EQ, DQ, AQ
ORDER BY priority DESC;
```

---

### 4. ResponseAnalytics

**Purpose**: Store response timing and consistency metrics for quality assurance

**Table**: `response_analytics`

```typescript
interface ResponseAnalytics {
  id: string;                    // UUID primary key
  userId: string;                // FK to users table
  assessmentId: string;          // Assessment session
  domain: "IQ" | "EQ" | "DQ" | "AQ";

  // Timing analytics
  averageResponseTimeMs: number;
  fastestResponseMs: number;
  slowestResponseMs: number;
  totalTimeMs: number;

  // Consistency analysis (for Likert only)
  consistencyScore?: number;     // 0-100, higher = more consistent
  contradictionCount?: number;   // Number of contradictory pairs
  totalPairsChecked?: number;    // Denominator for consistency %
  contradictoryPairs?: {         // JSONB array of flagged pairs
    item1Id: string;
    item2Id: string;
    item1Response: number;
    item2Response: number;
    expectedPattern: string;
    reason: string;
  }[];

  // Retest recommendation
  retestRecommended: boolean;
  retestReason?: string;         // Why retest is recommended

  // Metadata
  analyzedAt: Date;
  createdAt: Date;
  updatedAt: Date;
}
```

**Indexes**:
- Primary: `id`
- Unique: `(userId, assessmentId, domain)`
- Composite: `(userId, domain)` for user history
- Single: `retestRecommended` for filtering flagged assessments

**Validation Rules**:
- Time fields: Must be > 0
- `consistencyScore`: 0-100 when present
- `contradictionCount` ≤ `totalPairsChecked`
- `retestRecommended` = true requires `retestReason`

**Derived Logic**:
```typescript
// Consistency score calculation
consistencyScore = ((totalPairsChecked - contradictionCount) / totalPairsChecked) * 100;

// Retest recommendation logic (FR-017)
retestRecommended = consistencyScore < 70 || averageResponseTimeMs < 1000; // Too fast = not reading
```

---

### 5. VisualizationCache (Optional - Performance Optimization)

**Purpose**: Cache rendered visualization data to meet <2s performance target

**Table**: `visualization_cache`

```typescript
interface VisualizationCache {
  id: string;
  userId: string;

  // Cached data
  radarChartData: {
    IQ: number;
    EQ: number;
    DQ: number;
    AQ: number;
  };

  facetChartData: {
    [domain: string]: {
      facetName: string;
      score: number;
      normalizedScore: number;
    }[];
  };

  ikigaiMapData: {
    recommendedCareers: {
      zone: string;
      careers: {
        name: string;
        rationale: string;
      }[];
    }[];
  };

  // Cache metadata
  calculatedFrom: string[];      // Array of score_result IDs used
  expiresAt: Date;               // TTL for cache invalidation
  createdAt: Date;
}
```

**Indexes**:
- Primary: `id`
- Unique: `userId`
- Single: `expiresAt` for cleanup job

**Cache Invalidation**:
- Invalidate when new assessment responses added for user
- TTL: 24 hours
- Background job to cleanup expired entries

---

## Entity Relationships

```
User (external)
  │
  ├─── 1:N ──→ AssessmentResponse (one user, many responses)
  │
  ├─── 1:N ──→ ScoreResult (one user, many domain scores)
  │
  ├─── 1:N ──→ ResponseAnalytics (one user, many analytics records)
  │
  └─── 1:1 ──→ VisualizationCache (one user, one cache entry)

CareerMapping (independent, queried based on scores)
```

---

## Data Flow

### Score Calculation Flow

1. **Input**: User completes assessment → `AssessmentResponse` records created
2. **Aggregation**: System reads all responses for a domain/session
3. **Calculation**:
   - IQ: Sum (isCorrect × difficultyWeight) for all items
   - Likert: Sum reverse-adjusted rawScores, group by facet
4. **Normalization**: Convert raw scores to 0-100 scale
5. **Storage**: Write to `ScoreResult` table
6. **Cache**: Update `VisualizationCache` if enabled

### Visualization Data Retrieval Flow

1. **Request**: Frontend requests `/api/results/:userId`
2. **Cache Check**: Look for valid `VisualizationCache` entry
3. **Cache Hit**: Return cached data (fast path)
4. **Cache Miss**:
   - Query `ScoreResult` for all domains
   - Query `CareerMapping` with score filters
   - Transform to visualization format
   - Cache result
   - Return data

### Analytics Flow

1. **Response Logging**: Each answer creates `AssessmentResponse` with timing
2. **Consistency Check**: After domain completion, analyze Likert pairs
3. **Analytics Calculation**:
   - Aggregate timing statistics
   - Run contradiction detection algorithm
   - Calculate consistency score
4. **Storage**: Write to `ResponseAnalytics`
5. **Recommendation**: Flag for retest if consistency <70%

---

## Migration Strategy

### Initial Schema

```sql
-- Core tables created in priority order
CREATE TABLE assessment_responses (...);
CREATE TABLE score_results (...);
CREATE TABLE career_mappings (...);
CREATE TABLE response_analytics (...);

-- Optional performance table
CREATE TABLE visualization_cache (...);
```

### Seed Data

- **CareerMapping**: Pre-populate with 50-100 careers and threshold rules
- **Consistency Pairs**: Configuration table for semantic pairs (separate from main schema)

### Indexes

Create indexes after initial data load for performance:
```sql
CREATE INDEX CONCURRENTLY idx_responses_user_domain ON assessment_responses(userId, domain);
CREATE INDEX CONCURRENTLY idx_scores_user_domain ON score_results(userId, domain);
-- etc.
```

---

## Data Integrity Constraints

### Foreign Keys
- `assessment_responses.userId` → `users.id` (ON DELETE CASCADE)
- `score_results.userId` → `users.id` (ON DELETE CASCADE)
- `response_analytics.userId` → `users.id` (ON DELETE CASCADE)

### Check Constraints
```sql
ALTER TABLE assessment_responses
  ADD CONSTRAINT check_difficulty_weight
  CHECK (difficultyWeight IS NULL OR (difficultyWeight >= 1.0 AND difficultyWeight <= 3.0));

ALTER TABLE score_results
  ADD CONSTRAINT check_normalized_score
  CHECK (normalizedScore >= 0 AND normalizedScore <= 100);
```

---

## Performance Considerations

### Query Optimization
- Composite indexes on common query patterns (userId + domain)
- JSONB GIN indexes for flexible queries on facetScores and thresholds
- Partitioning for `assessment_responses` if scale exceeds 10M records (by userId or timestamp)

### Caching Strategy
- Application-level caching with Redis for hot user data
- Database-level `VisualizationCache` table for persistence
- TTL-based invalidation to prevent stale data

### Scalability
- Read replicas for visualization queries (can tolerate slight lag)
- Write master for score calculations and response logging
- Connection pooling sized for 100 concurrent requests

---

## Next Steps

Data model complete. Ready to:
1. Generate API contracts (`/contracts/*`)
2. Create quickstart guide for local development
3. Begin implementation with TDD approach (tests first)
