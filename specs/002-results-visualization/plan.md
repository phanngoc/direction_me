# Implementation Plan: Assessment Results Visualization and Scoring

**Branch**: `002-results-visualization` | **Date**: 2025-10-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-results-visualization/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a comprehensive assessment results visualization and scoring system that calculates student performance across four domains (IQ, EQ, DQ, AQ) and presents results through three interactive visualizations: a radar chart showing overall profile, facet-level bar charts showing detailed breakdowns, and an Ikigai career map recommending careers based on score intersections. The system must implement sophisticated scoring algorithms including difficulty-weighted IQ calculations and reverse-scored Likert processing, while logging response analytics to detect inconsistencies and recommend retests when needed.

## Technical Context

**Language/Version**: NEEDS CLARIFICATION (likely TypeScript for frontend, Python/TypeScript for backend based on assessment platform context)
**Primary Dependencies**: NEEDS CLARIFICATION (charting library for radar/bar visualizations, likely Recharts/D3.js/Chart.js)
**Storage**: NEEDS CLARIFICATION (database for assessment responses, score calculations, career mapping table, analytics logs)
**Testing**: NEEDS CLARIFICATION (frontend testing framework, backend API testing, visualization rendering tests)
**Target Platform**: Web application (responsive design for desktop/mobile browsers, accessibility compliance required)
**Project Type**: Web (frontend visualization components + backend scoring API)
**Performance Goals**: Render visualizations within 2 seconds for 95% of users, handle 100 concurrent result calculations
**Constraints**: <2s p95 visualization render time, accessibility WCAG 2.1 AA compliance, responsive design for screens ≥320px width
**Scale/Scope**: Support visualization for 4 assessment domains × multiple facets, career mapping table with 50-100 careers, analytics logging for all assessment responses

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Since the project constitution is still in template form, applying standard best practices gates:

### Architecture Principles
- ✅ **Separation of Concerns**: Scoring logic (backend) separated from visualization logic (frontend)
- ✅ **Library-First Approach**: Scoring algorithms can be extracted as standalone, testable libraries
- ✅ **API-Driven**: Visualization consumes scoring results via well-defined API contracts

### Quality Gates
- ✅ **Test-First Required**: All scoring algorithms must have tests before implementation (critical for accuracy requirement SC-001: 100% calculation accuracy)
- ✅ **Contract Testing**: API contracts between frontend/backend must be tested independently
- ✅ **Performance Testing**: Visualization render time (<2s) must be validated under load

### Complexity Justification
- ✅ **Acceptable Complexity**: Three visualization types justified by distinct user needs (overview → detail → career guidance)
- ✅ **Data Model Clarity**: Clear entities defined in spec (Radar Chart Data, Facet Bar Chart Data, Career Mapping, etc.)

**Status**: ✅ PASS - No constitutional violations detected. Feature aligns with modular, testable, API-driven architecture.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── assessment_response.ts     # Assessment answer data
│   │   ├── score_result.ts            # Calculated scores
│   │   ├── career_mapping.ts          # Career recommendation rules
│   │   └── analytics_log.ts           # Response time & consistency data
│   ├── services/
│   │   ├── scoring/
│   │   │   ├── iq_scorer.ts           # IQ difficulty-weighted scoring
│   │   │   ├── likert_scorer.ts       # Likert reverse-score handling
│   │   │   ├── facet_aggregator.ts    # Facet-level score calculation
│   │   │   └── normalizer.ts          # Score normalization (0-100)
│   │   ├── analytics/
│   │   │   ├── consistency_checker.ts # Contradiction detection
│   │   │   ├── response_timer.ts      # Time analytics
│   │   │   └── retest_recommender.ts  # Retest logic
│   │   └── career/
│   │       └── career_matcher.ts      # Career mapping & intersection logic
│   └── api/
│       ├── routes/
│       │   ├── results.ts             # GET /results/:userId
│       │   └── analytics.ts           # GET /analytics/:assessmentId
│       └── middleware/
└── tests/
    ├── unit/
    │   ├── scoring/                   # Scoring algorithm tests
    │   ├── analytics/                 # Analytics tests
    │   └── career/                    # Career matching tests
    ├── integration/
    │   └── api/                       # API endpoint tests
    └── contract/
        └── api-contracts.test.ts      # Contract validation

frontend/
├── src/
│   ├── components/
│   │   ├── visualizations/
│   │   │   ├── RadarChart.tsx         # Four-domain radar visualization
│   │   │   ├── FacetBarChart.tsx      # Facet-level horizontal bars
│   │   │   ├── IkigaiMap.tsx          # Venn diagram career map
│   │   │   └── ResponseAnalytics.tsx  # Analytics dashboard
│   │   └── results/
│   │       ├── ResultsContainer.tsx   # Results page wrapper
│   │       └── PartialResults.tsx     # Incomplete assessment handling
│   ├── services/
│   │   ├── api/
│   │   │   └── results_api.ts         # API client for results endpoints
│   │   └── formatters/
│   │       └── score_formatter.ts     # Score display formatting
│   └── types/
│       ├── score_types.ts             # Score data interfaces
│       └── visualization_types.ts     # Chart data interfaces
└── tests/
    ├── unit/
    │   └── components/                # Component unit tests
    ├── integration/
    │   └── visualizations/            # Visualization integration tests
    └── accessibility/
        └── a11y.test.ts               # WCAG compliance tests
```

**Structure Decision**: Web application structure selected. Frontend handles all visualizations (radar, bars, Ikigai map) while backend provides scoring APIs and career matching logic. This separation enables independent testing of calculation accuracy (backend) and visualization rendering (frontend).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
