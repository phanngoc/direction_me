# Tasks: MyWay - Tìm đường riêng của bạn

**Feature Branch**: `001-career-assessment`  
**Created**: 2024-12-19  
**Status**: Ready for Implementation  
**Total Tasks**: 78

## Overview

Hệ thống đánh giá 4 chỉ số IQ, EQ, DQ, AQ và định hướng nghề nghiệp dựa trên triết lý Ikigai cho học sinh-sinh viên. Sử dụng thuật toán toán học để tính điểm, mapping nghề nghiệp rule-based, và tạo lộ trình học tập cá nhân hóa.

**Tech Stack**: Python 3.11, JavaScript (ES2022), FastAPI, Next.js, PostgreSQL, Chart.js, Tailwind CSS  
**Architecture**: Web application với frontend/backend separation, library-first algorithms  
**Testing**: pytest (backend), Jest (frontend), Playwright (E2E)

## Phase 1: Setup (Project Initialization)

**Goal**: Tạo cấu trúc dự án và môi trường phát triển

### Tasks

- [x] T001 Tạo cấu trúc thư mục dự án theo implementation plan trong project root
- [x] T002 [P] Setup Python virtual environment trong backend/venv/
- [x] T003 [P] Setup Node.js project trong frontend/package.json
- [x] T004 [P] Tạo shared/ directory cho types và schemas trong shared/
- [x] T005 [P] Setup PostgreSQL database connection trong backend/src/database.py
- [x] T006 [P] Tạo requirements.txt cho backend dependencies trong backend/requirements.txt
- [x] T007 [P] Tạo package.json cho frontend dependencies trong frontend/package.json
- [x] T008 [P] Setup environment configuration files trong .env

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Tạo các components cơ bản cần thiết cho tất cả user stories

### Tasks

- [x] T009 [P] Tạo database migration scripts trong backend/scripts/
- [x] T010 [P] Implement User model trong backend/src/models/user.py
- [x] T011 [P] Implement Assessment model trong backend/src/models/assessment.py
- [x] T012 [P] Implement AssessmentResult model trong backend/src/models/assessment_result.py
- [x] T013 [P] Implement ProfileVector model trong backend/src/models/profile_vector.py
- [x] T014 [P] Implement CareerSuggestion model trong backend/src/models/career_suggestion.py
- [x] T015 [P] Implement LearningPath model trong backend/src/models/learning_path.py
- [x] T016 [P] Implement ProgressTracking model trong backend/src/models/progress_tracking.py
- [x] T017 [P] Implement CareerRule model trong backend/src/models/career_rule.py
- [x] T018 [P] Implement QuestionBank model trong backend/src/models/question_bank.py
- [x] T019 [P] Tạo database indexes theo data-model.md trong backend/scripts/create_indexes.sql
- [x] T020 [P] Setup FastAPI application structure trong backend/src/main.py
- [x] T021 [P] Setup Next.js application structure trong frontend/src/app/
- [x] T022 [P] Tạo shared TypeScript types trong shared/types/index.ts
- [x] T023 [P] Tạo shared JSON schemas trong shared/schemas/api.json
- [x] T024 [P] Setup authentication middleware trong backend/src/middleware/auth.py
- [x] T025 [P] Setup database connection pool trong backend/src/database.py
- [x] T026 [P] Tạo utility functions trong backend/src/utils/helpers.py
- [x] T027 [P] Tạo utility functions trong frontend/src/utils/helpers.ts

## Phase 3: User Story 1 - Đánh giá 4 chỉ số phát triển (P1)

**Goal**: Học sinh/sinh viên có thể thực hiện bài test đánh giá 4 chỉ số IQ, EQ, DQ, AQ để hiểu rõ năng lực bản thân và nhận được kết quả phân tích chi tiết.

**Independent Test**: Có thể test độc lập bằng cách cho một người dùng mới thực hiện đầy đủ bài test và nhận kết quả 4 chỉ số.

### Tasks

- [x] T028 [P] [US1] Implement UserService trong backend/src/services/user_service.py
- [x] T029 [P] [US1] Implement AssessmentService trong backend/src/services/assessment_service.py
- [x] T030 [P] [US1] Implement IQ scoring algorithm trong backend/src/algorithms/iq_scoring.py
- [x] T031 [P] [US1] Implement EQ scoring algorithm trong backend/src/algorithms/eq_scoring.py
- [x] T032 [P] [US1] Implement DQ scoring algorithm trong backend/src/algorithms/dq_scoring.py
- [x] T033 [P] [US1] Implement AQ scoring algorithm trong backend/src/algorithms/aq_scoring.py
- [x] T034 [US1] Implement assessment API endpoints trong backend/src/api/assessment.py
- [x] T035 [US1] Implement user authentication API endpoints trong backend/src/api/auth.py
- [x] T036 [US1] Tạo assessment form component trong frontend/src/components/AssessmentForm.tsx
- [x] T037 [US1] Tạo question display component trong frontend/src/components/QuestionDisplay.tsx
- [x] T038 [US1] Tạo results display component trong frontend/src/components/ResultsDisplay.tsx
- [x] T039 [US1] Tạo radar chart component trong frontend/src/components/RadarChart.tsx
- [x] T040 [US1] Tạo assessment page trong frontend/src/pages/assessment.tsx
- [x] T041 [US1] Tạo results page trong frontend/src/pages/results.tsx
- [x] T042 [US1] Implement API client services trong frontend/src/services/api.ts
- [x] T043 [US1] Tạo sample questions data trong backend/data/sample_questions.json
- [x] T044 [US1] Implement question loading logic trong backend/src/services/question_service.py
- [x] T045 [US1] Tạo assessment progress tracking trong frontend/src/hooks/useAssessment.ts
- [x] T046 [US1] Implement answer validation logic trong backend/src/utils/validation.py
- [x] T047 [US1] Tạo responsive mobile-first design cho assessment interface trong frontend/src/styles/assessment.css
- [x] T048 [US1] Implement error handling cho assessment flow trong frontend/src/components/ErrorBoundary.tsx
- [x] T049 [US1] Tạo unit tests cho scoring algorithms trong backend/tests/unit/test_scoring.py
- [x] T050 [US1] Tạo integration tests cho assessment API trong backend/tests/integration/test_assessment.py
- [x] T051 [US1] Tạo E2E tests cho assessment flow trong frontend/tests/e2e/assessment.spec.ts

## Phase 4: User Story 2 - Phân tích Ikigai và gợi ý nghề nghiệp (P1)

**Goal**: Dựa trên kết quả 4 chỉ số, hệ thống phân tích vùng Ikigai của người dùng và đưa ra gợi ý nghề nghiệp phù hợp.

**Independent Test**: Có thể test độc lập bằng cách nhập kết quả test và kiểm tra gợi ý nghề nghiệp được tạo ra.

### Tasks

- [x] T052 [P] [US2] Implement Ikigai calculation algorithm trong backend/src/algorithms/ikigai_calculation.py
- [x] T053 [P] [US2] Implement career mapping algorithm trong backend/src/algorithms/career_mapping.py
- [x] T054 [P] [US2] Implement CareerService trong backend/src/services/career_service.py
- [x] T055 [US2] Implement Ikigai API endpoints trong backend/src/api/ikigai.py
- [x] T056 [US2] Implement career suggestions API endpoints trong backend/src/api/careers.py
- [x] T057 [US2] Tạo Ikigai chart component trong frontend/src/components/IkigaiChart.tsx
- [x] T058 [US2] Tạo career suggestions component trong frontend/src/components/CareerSuggestions.tsx
- [x] T059 [US2] Tạo Ikigai analysis page trong frontend/src/pages/ikigai.tsx
- [x] T060 [US2] Tạo career suggestions page trong frontend/src/pages/careers.tsx
- [x] T061 [US2] Implement career rules configuration trong backend/data/career_rules.json
- [x] T062 [US2] Tạo career explanation generation logic trong backend/src/utils/explanation_generator.py
- [x] T063 [US2] Implement career fit score calculation trong backend/src/algorithms/career_fit.py
- [x] T064 [US2] Tạo career comparison component trong frontend/src/components/CareerComparison.tsx
- [x] T065 [US2] Implement career rules management trong backend/src/services/career_rule_service.py
- [x] T066 [US2] Tạo unit tests cho Ikigai algorithm trong backend/tests/unit/test_ikigai.py
- [x] T067 [US2] Tạo unit tests cho career mapping trong backend/tests/unit/test_career_mapping.py
- [x] T068 [US2] Tạo integration tests cho career API trong backend/tests/integration/test_careers.py
- [x] T069 [US2] Tạo E2E tests cho Ikigai flow trong frontend/tests/e2e/ikigai.spec.ts

## Phase 5: User Story 3 - Lộ trình học tập cá nhân hóa (P2)

**Goal**: Hệ thống tạo ra lộ trình học tập và phát triển kỹ năng cá nhân hóa dựa trên kết quả đánh giá.

**Independent Test**: Có thể test độc lập bằng cách kiểm tra lộ trình được tạo ra cho các profile khác nhau.

### Tasks

- [ ] T070 [P] [US3] Implement LearningPathService trong backend/src/services/learning_path_service.py
- [ ] T071 [P] [US3] Implement roadmap library trong backend/data/roadmap_library.json
- [ ] T072 [US3] Implement learning path generation algorithm trong backend/src/algorithms/learning_path_generator.py
- [ ] T073 [US3] Implement learning path API endpoints trong backend/src/api/learning_path.py
- [ ] T074 [US3] Tạo learning path component trong frontend/src/components/LearningPath.tsx
- [ ] T075 [US3] Tạo skills timeline component trong frontend/src/components/SkillsTimeline.tsx
- [ ] T076 [US3] Tạo learning path page trong frontend/src/pages/learning-path.tsx
- [ ] T077 [US3] Implement skill gap analysis trong backend/src/algorithms/skill_gap_analysis.py
- [ ] T078 [US3] Tạo progress tracking component trong frontend/src/components/ProgressTracker.tsx
- [ ] T079 [US3] Implement learning recommendations engine trong backend/src/algorithms/recommendations.py
- [ ] T080 [US3] Tạo unit tests cho learning path generation trong backend/tests/unit/test_learning_path.py
- [ ] T081 [US3] Tạo integration tests cho learning path API trong backend/tests/integration/test_learning_path.py
- [ ] T082 [US3] Tạo E2E tests cho learning path flow trong frontend/tests/e2e/learning-path.spec.ts

## Phase 6: User Story 4 - Theo dõi tiến trình phát triển (P3)

**Goal**: Người dùng có thể làm lại bài test định kỳ để theo dõi sự phát triển của bản thân theo thời gian.

**Independent Test**: Có thể test độc lập bằng cách so sánh kết quả test của cùng một người ở các thời điểm khác nhau.

### Tasks

- [ ] T083 [P] [US4] Implement ProgressTrackingService trong backend/src/services/progress_tracking_service.py
- [ ] T084 [P] [US4] Implement progress comparison algorithm trong backend/src/algorithms/progress_comparison.py
- [ ] T085 [US4] Implement progress tracking API endpoints trong backend/src/api/progress.py
- [ ] T086 [US4] Tạo progress dashboard component trong frontend/src/components/ProgressDashboard.tsx
- [ ] T087 [US4] Tạo progress chart component trong frontend/src/components/ProgressChart.tsx
- [ ] T088 [US4] Tạo progress comparison component trong frontend/src/components/ProgressComparison.tsx
- [ ] T089 [US4] Tạo progress tracking page trong frontend/src/pages/progress.tsx
- [ ] T090 [US4] Implement progress analytics trong backend/src/algorithms/progress_analytics.py
- [ ] T091 [US4] Tạo achievement system trong backend/src/services/achievement_service.py
- [ ] T092 [US4] Tạo unit tests cho progress tracking trong backend/tests/unit/test_progress.py
- [ ] T093 [US4] Tạo integration tests cho progress API trong backend/tests/integration/test_progress.py
- [ ] T094 [US4] Tạo E2E tests cho progress tracking flow trong frontend/tests/e2e/progress.spec.ts

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Hoàn thiện hệ thống với các tính năng cross-cutting và optimization

### Tasks

- [ ] T095 [P] Implement comprehensive error handling trong backend/src/middleware/error_handler.py
- [ ] T096 [P] Implement logging system trong backend/src/utils/logger.py
- [ ] T097 [P] Implement rate limiting trong backend/src/middleware/rate_limiter.py
- [ ] T098 [P] Implement input validation middleware trong backend/src/middleware/validation.py
- [ ] T099 [P] Tạo responsive design cho tất cả components trong frontend/src/styles/globals.css
- [ ] T100 [P] Implement performance optimization (caching, indexing) trong backend/src/middleware/cache.py
- [ ] T101 [P] Tạo comprehensive API documentation trong docs/api.md
- [ ] T102 [P] Implement security headers và CORS configuration trong backend/src/middleware/security.py
- [ ] T103 [P] Tạo deployment scripts và Docker configuration trong docker-compose.yml
- [ ] T104 [P] Implement monitoring và health checks trong backend/src/middleware/health.py
- [ ] T105 [P] Tạo comprehensive test suite coverage trong tests/coverage/
- [ ] T106 [P] Implement data backup và recovery procedures trong scripts/backup.py
- [ ] T107 [P] Tạo user documentation và help system trong docs/user-guide.md
- [ ] T108 [P] Implement accessibility features (WCAG compliance) trong frontend/src/components/AccessibleWrapper.tsx
- [ ] T109 [P] Tạo performance monitoring và analytics trong backend/src/middleware/analytics.py
- [ ] T110 [P] Implement A/B testing framework cho career rules trong backend/src/services/ab_testing.py
- [ ] T111 [P] Tạo comprehensive error reporting system trong backend/src/middleware/error_reporting.py
- [ ] T112 [P] Implement data export/import functionality trong backend/src/services/data_export.py
- [ ] T113 [P] Tạo comprehensive integration tests trong tests/integration/
- [ ] T114 [P] Implement load testing và performance benchmarks trong tests/load/load_test.py
- [ ] T115 [P] Tạo production deployment checklist trong docs/deployment.md
- [ ] T116 [P] Implement security audit và penetration testing trong scripts/security_audit.py
- [ ] T117 [P] Tạo comprehensive user acceptance testing trong tests/uat/
- [ ] T118 [P] Implement final system integration và validation trong scripts/integration_test.py

## Dependencies

### User Story Dependencies
- **US1** (Assessment) → **US2** (Ikigai & Careers): Cần kết quả assessment để tính Ikigai
- **US2** (Ikigai & Careers) → **US3** (Learning Path): Cần career suggestions để tạo learning path
- **US1** (Assessment) → **US4** (Progress Tracking): Cần multiple assessments để track progress
- **US3** (Learning Path) → **US4** (Progress Tracking): Cần learning path để track skill development

### Technical Dependencies
- **Phase 1** (Setup) → **Phase 2** (Foundational): Cần project structure trước khi tạo models
- **Phase 2** (Foundational) → **All User Stories**: Cần database models và basic infrastructure
- **US1** (Assessment) → **US2** (Ikigai): Cần scoring algorithms trước khi tính Ikigai
- **US2** (Ikigai) → **US3** (Learning Path): Cần career mapping trước khi tạo learning path

## Parallel Execution Examples

### Phase 1 Setup (All tasks can run in parallel)
```bash
# Terminal 1: Backend setup
cd backend && python -m venv venv && source venv/bin/activate

# Terminal 2: Frontend setup  
cd frontend && npm init -y && npm install next react react-dom

# Terminal 3: Database setup
createdb myway_assessment && psql myway_assessment < schema.sql

# Terminal 4: Shared types
mkdir -p shared/types && touch shared/types/index.ts
```

### Phase 2 Foundational (Models can be created in parallel)
```bash
# Parallel model creation
touch backend/src/models/user.py
touch backend/src/models/assessment.py
touch backend/src/models/assessment_result.py
# ... all other models
```

### US1 Assessment (Algorithm development in parallel)
```bash
# Terminal 1: IQ Algorithm
python backend/src/algorithms/iq_scoring.py

# Terminal 2: EQ Algorithm
python backend/src/algorithms/eq_scoring.py

# Terminal 3: DQ Algorithm
python backend/src/algorithms/dq_scoring.py

# Terminal 4: AQ Algorithm
python backend/src/algorithms/aq_scoring.py
```

## Implementation Strategy

### MVP First Approach
1. **Phase 1-2**: Setup và foundational components
2. **US1 Only**: Implement assessment functionality (core value)
3. **US2**: Add Ikigai analysis và career suggestions
4. **US3**: Add learning path generation
5. **US4**: Add progress tracking
6. **Phase 7**: Polish và optimization

### Incremental Delivery
- **Week 1**: Setup + US1 (Assessment) - Core functionality
- **Week 2**: US2 (Ikigai & Careers) - Unique value proposition
- **Week 3**: US3 (Learning Path) - Long-term engagement
- **Week 4**: US4 (Progress Tracking) + Polish - Complete system

### Testing Strategy
- **Unit Tests**: Mỗi algorithm và service
- **Integration Tests**: API endpoints và database interactions
- **E2E Tests**: Complete user workflows
- **Contract Tests**: API compatibility
- **Performance Tests**: Load testing cho 1000 concurrent users

## Success Metrics

### Technical Metrics
- **Performance**: <3s page load, <30s test completion
- **Reliability**: 99.9% uptime, <1% error rate
- **Scalability**: 1000 concurrent users
- **Test Coverage**: >90% code coverage

### Business Metrics
- **User Engagement**: 70% return rate within 30 days
- **Assessment Completion**: 90% completion rate
- **Career Relevance**: 80% user satisfaction with suggestions
- **Learning Path Usage**: 60% users follow recommended paths

### Quality Metrics
- **Code Quality**: No critical security vulnerabilities
- **Accessibility**: WCAG 2.1 AA compliance
- **Mobile Performance**: 90+ Lighthouse score
- **API Performance**: <200ms average response time

## Notes

- **Library-First**: Tất cả algorithms được implement như standalone libraries với CLI interface
- **Test-First**: Mỗi feature phải có tests trước khi implement
- **Mobile-First**: UI được design cho mobile trước, sau đó enhance cho desktop
- **Performance**: Database indexing và caching được implement từ đầu
- **Security**: HTTPS required, password validation, input sanitization
- **Scalability**: Architecture hỗ trợ horizontal scaling
- **Maintainability**: Code được organize theo clean architecture principles