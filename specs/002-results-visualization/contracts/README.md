# API Contracts: Assessment Results Visualization

**Feature**: 002-results-visualization
**Date**: 2025-10-25
**Contract Format**: OpenAPI 3.0.3

## Overview

This directory contains API contracts for the assessment results visualization and scoring system. The contracts define the interface between frontend visualization components and backend scoring/analytics services.

## Files

- **`openapi.yaml`**: Complete OpenAPI specification for all endpoints
- **`README.md`**: This file - contract design rationale and usage guide

## API Design Principles

### 1. Resource-Oriented Design

Endpoints organized around four primary resources:
- **Results**: Visualization data aggregation (`/results`)
- **Scores**: Score calculation and retrieval (`/scores`)
- **Analytics**: Response timing and consistency analysis (`/analytics`)
- **Careers**: Career recommendations based on scores (`/careers`)

### 2. Performance Optimization

**Granular Data Retrieval**:
- `GET /results/{userId}` - Full visualization data (radar + facets + careers)
- `GET /results/{userId}/radar` - Radar chart only (fastest)
- `GET /results/{userId}/facets` - Facet bars only (filtered by domain)
- `GET /results/{userId}/careers` - Career recommendations only

**Rationale**: Enables frontend to request only needed data, supports progressive rendering to meet <2s performance target.

### 3. Separation of Concerns

**Calculation vs Retrieval**:
- `POST /scores/calculate` - Trigger score calculation (write operation)
- `GET /results/{userId}` - Retrieve cached results (read operation)

**Rationale**: Allows asynchronous score calculation, caching strategies, and independent scaling of read/write workloads.

### 4. Analytics Independence

**Dedicated Analytics Endpoints**:
- `GET /analytics/{assessmentId}` - Retrieve full analytics report
- `POST /analytics/consistency` - Run consistency check independently

**Rationale**: Analytics can be calculated asynchronously or on-demand without blocking visualization rendering.

## Endpoint Mapping to Functional Requirements

| Endpoint | Functional Requirements | Purpose |
|----------|------------------------|---------|
| `GET /results/{userId}/radar` | FR-003, FR-010 | Radar chart visualization data |
| `GET /results/{userId}/facets` | FR-004, FR-005, FR-011 | Facet bar chart data |
| `GET /results/{userId}/careers` | FR-012, FR-013, FR-014 | Ikigai career map data |
| `POST /scores/calculate` | FR-001, FR-002, FR-006, FR-007 | IQ & Likert scoring algorithms |
| `GET /analytics/{assessmentId}` | FR-015, FR-016, FR-017, FR-018 | Response analytics & consistency |
| `POST /analytics/consistency` | FR-016, FR-017 | Contradiction detection |
| `POST /careers/match` | FR-012, FR-013 | Career threshold matching |

## Data Flow Examples

### User Completes Assessment → View Results

```
1. Frontend: POST /scores/calculate
   Body: { userId, assessmentId, domain: "IQ" }
   → Backend calculates IQ scores with difficulty weighting

2. Frontend: GET /results/{userId}/radar
   → Backend returns { IQ: 75, EQ: null, DQ: null, AQ: null }
   → Frontend renders partial radar chart

3. User completes all 4 domains...

4. Frontend: GET /results/{userId}
   → Backend returns full visualization data
   → Frontend renders complete radar + facets + careers
```

### Retest Recommendation Workflow

```
1. Backend: Automatically runs consistency check after Likert completion
   → Creates ResponseAnalytics record

2. Frontend: GET /analytics/{assessmentId}
   → Returns { consistencyScore: 65, retestRecommended: true, retestReason: "..." }

3. Frontend displays warning banner with retest option

4. User clicks "Retest" → Frontend initiates new assessment session
```

### Career Recommendation Workflow

```
1. Frontend: GET /results/{userId}/careers
   → Backend queries CareerMapping table with user scores
   → Returns careers grouped by intersection zones

2. Response format:
   {
     recommendedCareers: [
       {
         zone: "IQ+EQ",
         careers: [
           { name: "Clinical Psychologist", rationale: "..." },
           { name: "UX Researcher", rationale: "..." }
         ]
       },
       {
         zone: "IQ+EQ+DQ",
         careers: [...]
       }
     ]
   }

3. Frontend renders Ikigai Venn diagram with careers in appropriate zones
```

## Request/Response Formats

### Score Calculation Request

```json
POST /scores/calculate
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "assessmentId": "987fcdeb-51a2-43d7-8f9e-123456789abc",
  "domain": "IQ"
}
```

### Visualization Data Response

```json
GET /results/{userId}
{
  "radarChartData": {
    "IQ": 75,
    "EQ": 82,
    "DQ": 68,
    "AQ": 79
  },
  "facetChartData": {
    "IQ": [
      { "facetName": "Logical", "score": 12, "normalizedScore": 80 },
      { "facetName": "Spatial", "score": 10, "normalizedScore": 70 }
    ],
    "EQ": [...]
  },
  "ikigaiMapData": {
    "recommendedCareers": [
      {
        "zone": "IQ+EQ",
        "careers": [
          {
            "name": "Clinical Psychologist",
            "rationale": "High EQ (82) and strong IQ (75) align with therapeutic work requiring analytical skills and emotional intelligence"
          }
        ]
      }
    ]
  },
  "calculatedAt": "2025-10-25T10:30:00Z"
}
```

### Analytics Response

```json
GET /analytics/{assessmentId}
{
  "assessmentId": "987fcdeb-51a2-43d7-8f9e-123456789abc",
  "domain": "EQ",
  "averageResponseTimeMs": 3500,
  "fastestResponseMs": 1200,
  "slowestResponseMs": 8500,
  "totalTimeMs": 105000,
  "consistencyScore": 85,
  "contradictionCount": 2,
  "totalPairsChecked": 45,
  "contradictoryPairs": [
    {
      "item1Id": "EQ_Q12",
      "item2Id": "EQ_Q24",
      "item1Response": 5,
      "item2Response": 2,
      "expectedPattern": "should_match",
      "reason": "Both measure self-awareness; responses differ by >1 point"
    }
  ],
  "retestRecommended": false,
  "retestReason": null
}
```

## Validation Rules

### Path Parameters
- `userId`: Must be valid UUID
- `assessmentId`: Must be valid UUID
- `domain`: Must be one of [IQ, EQ, DQ, AQ]
- `careerId`: String identifier

### Request Body Validation
- **Score Calculation**: Requires userId, assessmentId, domain (all mandatory)
- **Consistency Check**: Requires assessmentId, domain must be Likert (EQ/DQ/AQ, not IQ)
- **Career Match**: Scores object must contain valid 0-100 values for all domains

### Response Validation
- Normalized scores: 0-100 range
- Percentile ranks: 0-100 range
- Timestamps: ISO 8601 format
- Consistency scores: 0-100 range

## Error Handling

### Standard Error Response
```json
{
  "code": "CALCULATION_ERROR",
  "message": "Unable to calculate scores: incomplete assessment data",
  "details": {
    "domain": "IQ",
    "missingQuestions": 5,
    "totalRequired": 30
  }
}
```

### Common Error Codes
- `USER_NOT_FOUND`: User ID doesn't exist
- `ASSESSMENT_NOT_FOUND`: Assessment ID invalid
- `INCOMPLETE_ASSESSMENT`: Not all questions answered
- `CALCULATION_ERROR`: Score calculation failed
- `INVALID_DOMAIN`: Domain parameter invalid
- `CONSISTENCY_CHECK_NOT_APPLICABLE`: Attempted consistency check on IQ (multiple choice)

## Performance Considerations

### Caching Strategy
- `GET /results/{userId}`: Cache entire response for 24 hours
- Invalidate cache when new assessment responses added
- `VisualizationCache` table stores pre-calculated data

### Query Optimization
- Composite indexes on `(userId, domain)` for fast score retrieval
- JSONB GIN indexes for career threshold queries
- Connection pooling for 100 concurrent requests

### Response Compression
- Enable gzip/brotli compression for all JSON responses
- Typical response sizes:
  - Radar data: ~200 bytes
  - Full visualization data: ~2-5 KB
  - Analytics data: ~1-3 KB

## Contract Testing

### Recommended Testing Strategy
- **Consumer Tests** (Frontend): Use Pact.js to define expected API contracts
- **Provider Tests** (Backend): Validate implementation against Pact contracts
- **Contract Validation**: Run automated tests on every API change

### Example Pact Test (Frontend)
```javascript
describe('Results API Contract', () => {
  it('should return radar chart data for valid user', async () => {
    const interaction = {
      state: 'user 123 has completed all 4 assessments',
      uponReceiving: 'a request for radar chart data',
      withRequest: {
        method: 'GET',
        path: '/results/123/radar'
      },
      willRespondWith: {
        status: 200,
        body: {
          IQ: Matchers.number(75),
          EQ: Matchers.number(82),
          DQ: Matchers.number(68),
          AQ: Matchers.number(79)
        }
      }
    };
    // Test implementation...
  });
});
```

## Versioning Strategy

### Current Version: v1.0.0

**Versioning Approach**: URL path versioning for breaking changes
- Current: `/api/results/{userId}`
- Future v2: `/api/v2/results/{userId}`

**Breaking Changes** (require new version):
- Removing fields from responses
- Changing required request parameters
- Changing data types or formats

**Non-Breaking Changes** (backward compatible):
- Adding new optional fields
- Adding new endpoints
- Adding new query parameters (optional)

## Next Steps

Contracts complete. Ready to:
1. Generate `quickstart.md` for local development setup
2. Update agent context with `.specify/scripts/bash/update-agent-context.sh`
3. Begin implementation with contract-first TDD approach
