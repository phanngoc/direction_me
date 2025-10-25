# Research: Assessment Results Visualization and Scoring

**Feature**: 002-results-visualization
**Date**: 2025-10-25
**Purpose**: Resolve technical unknowns from Technical Context

## Research Questions & Decisions

### 1. Language & Runtime Selection

**Question**: What language/version should be used for frontend and backend?

**Decision**:
- **Frontend**: TypeScript 5.x with React 18+
- **Backend**: TypeScript 5.x with Node.js 20 LTS

**Rationale**:
- Unified language across frontend/backend reduces context switching and enables code sharing (e.g., type definitions, validation logic)
- TypeScript provides type safety critical for score calculation accuracy (SC-001: 100% accuracy requirement)
- React ecosystem has mature charting libraries (Recharts, Victory, Nivo) for required visualizations
- Node.js 20 LTS provides stability for production deployment
- Strong ecosystem for testing both calculation logic and UI rendering

**Alternatives Considered**:
- Python backend: Rejected due to type system less strict than TypeScript, would require separate type definitions for frontend
- Separate languages (e.g., Python backend + TS frontend): Rejected to avoid duplication of score calculation types and validation rules

---

### 2. Charting Library Selection

**Question**: Which charting library for radar charts, bar charts, and Ikigai visualization?

**Decision**: Recharts 2.x

**Rationale**:
- Native React integration (no DOM manipulation required)
- Built-in support for radar charts and bar charts
- Accessibility features (ARIA labels, keyboard navigation) aligns with WCAG 2.1 AA requirement
- Responsive by default, works well on small screens (≥320px requirement)
- Customizable for Ikigai Venn diagram (can use composed charts or SVG overlay)
- Performance: Renders 1000+ data points smoothly, well within our 4 domains × ~12 facets scale
- Active maintenance and strong community support

**Alternatives Considered**:
- D3.js: Rejected - too low-level, would require significant custom code for accessibility and responsiveness
- Chart.js: Rejected - canvas-based rendering has accessibility limitations, less React-friendly
- Victory: Considered but Recharts has better radar chart support out-of-box
- Nivo: Considered but documentation less comprehensive than Recharts

---

### 3. Storage & Database Selection

**Question**: What database for assessment responses, scores, career mappings, and analytics?

**Decision**: PostgreSQL 15+

**Rationale**:
- JSONB support ideal for flexible assessment response storage (handles varying question structures across IQ/EQ/DQ/AQ)
- Strong ACID guarantees ensure score calculation data integrity
- Excellent performance for aggregation queries (facet-level, domain-level score calculations)
- Supports complex queries for consistency detection (finding contradictory response pairs)
- JSON functions enable flexible career mapping table queries (score threshold matching)
- Mature ecosystem, proven at scale for 10k+ concurrent users

**Storage Schema Approach**:
- Assessment responses: JSONB column for flexible question/answer pairs + indexed columns for userId, assessmentId, timestamp
- Score results: Structured columns for domain scores, facets stored as JSONB for flexibility
- Career mapping: JSONB rules column for threshold logic, indexed career categories
- Analytics logs: Time-series optimized table with partitioning by date

**Alternatives Considered**:
- MongoDB: Rejected - weaker consistency guarantees unacceptable for score calculation accuracy requirement
- MySQL: Considered but PostgreSQL's JSON support superior for our flexible data needs
- SQLite: Rejected - insufficient for 100 concurrent calculation requirement

---

### 4. Testing Framework Selection

**Question**: What testing frameworks for frontend, backend, and contract testing?

**Decision**:
- **Backend Unit/Integration**: Jest 29+ with ts-jest
- **Frontend Unit/Integration**: Jest 29+ with React Testing Library
- **Contract Testing**: Pact.js for frontend/backend API contracts
- **Accessibility Testing**: jest-axe + @testing-library/jest-dom
- **E2E Visualization**: Playwright for visual regression testing

**Rationale**:
- Jest provides unified testing experience across frontend/backend (TypeScript on both sides)
- React Testing Library enforces accessibility-first testing approach
- Pact.js enables true contract testing - frontend can test against mocked backend contracts, backend validates it implements those contracts
- jest-axe catches WCAG violations during unit tests
- Playwright enables screenshot comparisons for visualization regression (critical for chart rendering accuracy)

**Testing Strategy**:
1. **Score Calculation**: Property-based testing with fast-check for algorithm correctness (generate random assessment data, verify invariants)
2. **Visualizations**: Snapshot testing for chart SVG output + visual regression with Playwright
3. **API Contracts**: Pact consumer/provider tests ensure frontend/backend stay in sync
4. **Accessibility**: Automated axe checks + manual screen reader testing

**Alternatives Considered**:
- Mocha/Chai: Rejected - Jest's ecosystem more mature for React + TypeScript
- Cypress for E2E: Considered but Playwright has better cross-browser support and faster execution
- Manual contract testing: Rejected - error-prone, Pact provides automated verification

---

### 5. Career Mapping Table Structure

**Question**: How to structure the career mapping table for flexible score-to-career matching?

**Decision**: Rule-based JSON configuration with threshold logic

**Schema**:
```typescript
interface CareerMappingRule {
  career: {
    id: string;
    name: string;
    category: string;
  };
  thresholds: {
    IQ?: { min?: number; max?: number };
    EQ?: { min?: number; max?: number };
    DQ?: { min?: number; max?: number };
    AQ?: { min?: number; max?: number };
  };
  intersectionZones: string[]; // e.g., ["IQ+EQ", "IQ+EQ+DQ"]
  rationale: string;
  priority: number; // for ranking when multiple careers match
}
```

**Rationale**:
- Flexible threshold ranges (min/max) allow "high IQ" or "moderate EQ" requirements
- Optional thresholds mean careers can require specific domains while ignoring others
- Intersection zones explicitly define Ikigai map placement
- Priority enables ranking when user matches multiple careers
- JSON structure allows easy updates without schema migrations
- Rationale field provides explanation text for "why this career matches" (FR-012)

**Matching Algorithm**:
1. Normalize user scores to 0-100 scale
2. Filter careers where all specified thresholds are satisfied
3. Identify which intersection zones the user's scores qualify for
4. Rank matching careers by priority score
5. Return top N careers per intersection zone

**Alternatives Considered**:
- Machine learning model: Rejected - insufficient training data, rule-based more explainable
- Hard-coded if/else logic: Rejected - inflexible, requires code changes for new careers
- Graph database: Considered but overkill for our scale (50-100 careers)

---

### 6. Consistency Detection Algorithm

**Question**: How to detect contradictory Likert responses?

**Decision**: Semantic pair analysis with configurable threshold

**Algorithm**:
```typescript
interface ConsistencyCheck {
  item1Id: string;
  item2Id: string;
  semanticRelation: "opposite" | "similar";
  expectedPattern: "should_differ" | "should_match";
  threshold: number; // acceptable difference (e.g., ≤1 for similar, ≥3 for opposite)
}
```

**Approach**:
1. **Preprocessing**: Define semantic pairs in assessment configuration (e.g., "I enjoy social gatherings" ↔ "I prefer solitude")
2. **Analysis**: For each pair, compare user responses accounting for reverse scoring
3. **Contradiction Detection**: Flag pairs where:
   - Opposite items: responses differ by <3 points (after reverse-score adjustment)
   - Similar items: responses differ by >1 point
4. **Consistency Score**: `(total_pairs - contradictions) / total_pairs × 100`
5. **Retest Threshold**: Recommend retest if consistency <70%

**Rationale**:
- Configuration-driven allows adding new semantic pairs without code changes
- Threshold-based detection handles minor variation (users can be slightly inconsistent)
- Accounts for reverse scoring (critical - don't flag legitimate disagreements as contradictions)
- Percentage-based score provides clear metric for SC-005 (80% detection accuracy target)

**Alternatives Considered**:
- NLP-based similarity detection: Rejected - overkill, requires training data, less predictable
- Statistical outlier detection: Considered but semantic pairs more explainable to users
- Manual review only: Rejected - doesn't scale, inconsistent

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend** | React | 18+ | UI framework |
| | TypeScript | 5.x | Type safety |
| | Recharts | 2.x | Visualizations |
| | React Testing Library | 14+ | Component testing |
| **Backend** | Node.js | 20 LTS | Runtime |
| | TypeScript | 5.x | Type safety |
| | Express/Fastify | TBD | API framework |
| | Jest | 29+ | Testing |
| **Database** | PostgreSQL | 15+ | Data storage |
| **Testing** | Pact.js | 11+ | Contract testing |
| | Playwright | 1.40+ | E2E & visual regression |
| | jest-axe | 8+ | Accessibility testing |
| **DevOps** | TBD | - | CI/CD, deployment |

---

## Performance Validation Strategy

To meet SC-002 (< 2s visualization render for 95% users):

1. **Backend Optimization**:
   - Cache calculated scores (invalidate on new assessment responses)
   - Database query optimization with proper indexes
   - Response compression (gzip/brotli)

2. **Frontend Optimization**:
   - Code splitting (load visualization components on-demand)
   - Memoization for chart data transformations
   - Lazy loading for Ikigai map (P3 priority, can defer)
   - Recharts built-in performance features

3. **Measurement**:
   - Synthetic monitoring: Lighthouse CI in pipeline
   - Real User Monitoring: Core Web Vitals tracking
   - Load testing: k6 or Artillery for 100 concurrent users

---

## Accessibility Implementation

To meet WCAG 2.1 AA requirement (SC-006):

1. **Recharts Built-in**:
   - ARIA labels on chart elements
   - Keyboard navigation support

2. **Custom Additions**:
   - Data tables as screen-reader alternative to charts
   - Sufficient color contrast (test with axe-core)
   - Focus indicators on interactive elements
   - Descriptive alt text for Ikigai map zones

3. **Testing**:
   - Automated: jest-axe in unit tests
   - Manual: NVDA/JAWS screen reader testing
   - Lighthouse accessibility audit in CI

---

## Next Steps

All "NEEDS CLARIFICATION" items from Technical Context are now resolved. Ready to proceed to:
1. **Phase 1**: Generate data-model.md with concrete entity schemas
2. **Phase 1**: Generate API contracts based on selected tech stack
3. **Phase 1**: Create quickstart.md for local development setup
