# Implementation Plan: MyWay - Tìm đường riêng của bạn

**Branch**: `001-career-assessment` | **Date**: 2024-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-career-assessment/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Hệ thống đánh giá 4 chỉ số IQ, EQ, DQ, AQ và định hướng nghề nghiệp dựa trên triết lý Ikigai cho học sinh-sinh viên. Sử dụng thuật toán toán học để tính điểm, mapping nghề nghiệp rule-based, và tạo lộ trình học tập cá nhân hóa.

## Technical Context

**Language/Version**: Python 3.11, JavaScript (ES2022), HTML5/CSS3  
**Primary Dependencies**: FastAPI, Next.js, PostgreSQL, Chart.js, Tailwind CSS  
**Storage**: PostgreSQL với backup hàng ngày và data retention 2 năm  
**Testing**: pytest (backend), Jest (frontend), Playwright (E2E)  
**Target Platform**: Web application (mobile-first responsive design)  
**Project Type**: Web application (frontend + backend)  
**Performance Goals**: 1000 concurrent users, <3s page load, <30s test completion  
**Constraints**: HTTPS required, mobile-first design, basic error handling  
**Scale/Scope**: 1000+ users, 8 career mappings, 16-dimensional profile vectors

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ PASSED**: Constitution file exists but is template-based. No specific constraints identified that would block implementation.

**Key Considerations**:
- Test-First approach: All features must have tests before implementation
- Library-First: Core assessment algorithms should be standalone libraries
- CLI Interface: Assessment algorithms should be callable via CLI for testing
- Integration Testing: Focus on API contracts and data model validation

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
│   ├── models/           # Data models (User, Assessment, Career, etc.)
│   ├── services/         # Business logic (AssessmentService, CareerService)
│   ├── algorithms/       # Core assessment algorithms (IQ, EQ, DQ, AQ, Ikigai)
│   ├── api/             # FastAPI routes and endpoints
│   └── utils/           # Utility functions and helpers
├── tests/
│   ├── unit/            # Unit tests for algorithms and services
│   ├── integration/     # API integration tests
│   └── contract/        # API contract tests
└── requirements.txt

frontend/
├── src/
│   ├── components/      # React components (TestForm, ResultsChart, etc.)
│   ├── pages/          # Next.js pages (assessment, results, dashboard)
│   ├── services/       # API client services
│   ├── utils/          # Frontend utilities
│   └── styles/         # Tailwind CSS styles
├── tests/
│   ├── unit/           # Component unit tests
│   └── e2e/            # End-to-end tests with Playwright
└── package.json

shared/
├── types/              # TypeScript interfaces shared between frontend/backend
├── schemas/            # JSON schemas for API validation
└── constants/          # Shared constants and configurations
```

**Structure Decision**: Web application với frontend/backend separation. Backend sử dụng FastAPI với modular structure cho algorithms. Frontend sử dụng Next.js với component-based architecture. Shared folder cho types và schemas.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
