# Tasks: MyWay - Tìm đường riêng của bạn

**Feature**: 001-career-assessment  
**Created**: 2024-12-19  
**Status**: Ready for Implementation  
**Total Tasks**: 45 tasks across 6 phases

## Overview

Hệ thống đánh giá 4 chỉ số IQ, EQ, DQ, AQ và định hướng nghề nghiệp dựa trên triết lý Ikigai cho học sinh-sinh viên. Sử dụng thuật toán toán học để tính điểm, mapping nghề nghiệp rule-based, và tạo lộ trình học tập cá nhân hóa.

**Tech Stack**: Python 3.11, FastAPI, Next.js, PostgreSQL, Chart.js, Tailwind CSS  
**Target Platform**: Web application (mobile-first responsive design)  
**Performance Goals**: 1000 concurrent users, <3s page load, <30s test completion

## Phase 1: Setup (Project Initialization)

**Goal**: Thiết lập cấu trúc dự án và môi trường phát triển

### Independent Test Criteria
- [ ] Có thể chạy backend server trên port 8000
- [ ] Có thể chạy frontend server trên port 3000  
- [ ] Database PostgreSQL được tạo và kết nối thành công
- [ ] Tất cả dependencies được cài đặt và import thành công

### Tasks

- [ ] T001 Tạo cấu trúc thư mục dự án theo implementation plan
- [ ] T002 [P] Setup Python virtual environment và requirements.txt trong backend/
- [ ] T003 [P] Setup Node.js project và package.json trong frontend/
- [ ] T004 [P] Tạo shared/ directory với types/ và schemas/ subdirectories
- [ ] T005 [P] Setup PostgreSQL database và connection configuration
- [ ] T006 [P] Tạo .env files cho backend và frontend với environment variables
- [ ] T007 [P] Setup Git repository và .gitignore files
- [ ] T008 Tạo scripts/ directory với database initialization scripts

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Xây dựng các thành phần cơ sở cần thiết cho tất cả user stories

### Independent Test Criteria
- [ ] Database schema được tạo thành công với tất cả tables và indexes
- [ ] Core algorithms có thể được import và test độc lập
- [ ] API authentication middleware hoạt động đúng
- [ ] Shared types và schemas được định nghĩa và export thành công

### Tasks

- [ ] T009 [P] Tạo database migration scripts trong backend/scripts/
- [ ] T010 [P] Implement User model trong backend/src/models/user.py
- [ ] T011 [P] Implement Assessment model trong backend/src/models/assessment.py
- [ ] T012 [P] Implement AssessmentResult model trong backend/src/models/assessment_result.py
- [ ] T013 [P] Implement ProfileVector model trong backend/src/models/profile_vector.py
- [ ] T014 [P] Implement CareerSuggestion model trong backend/src/models/career_suggestion.py
- [ ] T015 [P] Implement LearningPath model trong backend/src/models/learning_path.py
- [ ] T016 [P] Implement ProgressTracking model trong backend/src/models/progress_tracking.py
- [ ] T017 [P] Implement CareerRule model trong backend/src/models/career_rule.py
- [ ] T018 [P] Implement QuestionBank model trong backend/src/models/question_bank.py
- [ ] T019 [P] Tạo shared TypeScript interfaces trong shared/types/
- [ ] T020 [P] Tạo shared JSON schemas trong shared/schemas/
- [ ] T021 [P] Implement IQ scoring algorithm trong backend/src/algorithms/iq_scoring.py
- [ ] T022 [P] Implement EQ/DQ/AQ scoring algorithm trong backend/src/algorithms/emotional_scoring.py
- [ ] T023 [P] Implement Ikigai calculation algorithm trong backend/src/algorithms/ikigai_calculation.py
- [ ] T024 [P] Implement career mapping algorithm trong backend/src/algorithms/career_mapping.py
- [ ] T025 [P] Tạo CLI interface cho algorithms trong backend/src/algorithms/cli.py
- [ ] T026 [P] Implement JWT authentication middleware trong backend/src/middleware/auth.py
- [ ] T027 [P] Setup FastAPI application và basic routing trong backend/src/main.py

## Phase 3: User Story 1 - Đánh giá 4 chỉ số phát triển (P1)

**Goal**: Học sinh/sinh viên có thể thực hiện bài test đánh giá 4 chỉ số IQ, EQ, DQ, AQ để hiểu rõ năng lực bản thân và nhận được kết quả phân tích chi tiết.

**Independent Test**: Có thể test độc lập bằng cách cho một người dùng mới thực hiện đầy đủ bài test và nhận kết quả 4 chỉ số.

### Independent Test Criteria
- [ ] Người dùng có thể đăng ký tài khoản và đăng nhập
- [ ] Hệ thống hiển thị bộ câu hỏi 4 nhóm (IQ, EQ, DQ, AQ) với giao diện thân thiện
- [ ] Hệ thống tính toán và hiển thị điểm số 4 chỉ số sau khi hoàn thành test
- [ ] Biểu đồ radar chart hiển thị 4 trục IQ, EQ, DQ, AQ

### Tasks

- [ ] T028 [P] [US1] Implement UserService trong backend/src/services/user_service.py
- [ ] T029 [P] [US1] Implement AssessmentService trong backend/src/services/assessment_service.py
- [ ] T030 [P] [US1] Implement QuestionService trong backend/src/services/question_service.py
- [ ] T031 [P] [US1] Implement ScoringService trong backend/src/services/scoring_service.py
- [ ] T032 [P] [US1] Tạo API endpoints cho authentication trong backend/src/api/auth.py
- [ ] T033 [P] [US1] Tạo API endpoints cho assessment trong backend/src/api/assessment.py
- [ ] T034 [P] [US1] Tạo API endpoints cho questions trong backend/src/api/questions.py
- [ ] T035 [P] [US1] Tạo API endpoints cho results trong backend/src/api/results.py
- [ ] T036 [P] [US1] Implement TestForm component trong frontend/src/components/TestForm.tsx
- [ ] T037 [P] [US1] Implement QuestionCard component trong frontend/src/components/QuestionCard.tsx
- [ ] T038 [P] [US1] Implement ResultsChart component trong frontend/src/components/ResultsChart.tsx
- [ ] T039 [P] [US1] Tạo assessment page trong frontend/src/pages/assessment.tsx
- [ ] T040 [P] [US1] Tạo results page trong frontend/src/pages/results.tsx
- [ ] T041 [P] [US1] Implement API client services trong frontend/src/services/api.ts
- [ ] T042 [P] [US1] Tạo sample questions data trong backend/scripts/load_sample_questions.py
- [ ] T043 [US1] Implement assessment completion logic trong backend/src/services/assessment_service.py
- [ ] T044 [US1] Implement results calculation logic trong backend/src/services/scoring_service.py

## Phase 4: User Story 2 - Phân tích Ikigai và gợi ý nghề nghiệp (P1)

**Goal**: Dựa trên kết quả 4 chỉ số, hệ thống phân tích vùng Ikigai của người dùng và đưa ra gợi ý nghề nghiệp phù hợp.

**Independent Test**: Có thể test độc lập bằng cách nhập kết quả test và kiểm tra gợi ý nghề nghiệp được tạo ra.

### Independent Test Criteria
- [ ] Hệ thống hiển thị biểu đồ Ikigai với 4 vòng giao nhau
- [ ] Hệ thống hiển thị top 3 nghề nghiệp phù hợp với lý do cụ thể
- [ ] Gợi ý nghề nghiệp phù hợp với profile người dùng (VD: DQ cao, EQ trung bình → UI/UX Designer)

### Tasks

- [ ] T045 [P] [US2] Implement CareerService trong backend/src/services/career_service.py
- [ ] T046 [P] [US2] Implement IkigaiService trong backend/src/services/ikigai_service.py
- [ ] T047 [P] [US2] Tạo API endpoints cho career suggestions trong backend/src/api/careers.py
- [ ] T048 [P] [US2] Implement IkigaiChart component trong frontend/src/components/IkigaiChart.tsx
- [ ] T049 [P] [US2] Implement CareerSuggestions component trong frontend/src/components/CareerSuggestions.tsx
- [ ] T050 [P] [US2] Tạo career results page trong frontend/src/pages/career-results.tsx
- [ ] T051 [P] [US2] Tạo career rules data trong backend/scripts/load_career_rules.py
- [ ] T052 [US2] Implement career mapping logic trong backend/src/services/career_service.py
- [ ] T053 [US2] Implement Ikigai calculation logic trong backend/src/services/ikigai_service.py

## Phase 5: User Story 3 - Lộ trình học tập cá nhân hóa (P2)

**Goal**: Hệ thống tạo ra lộ trình học tập và phát triển kỹ năng cá nhân hóa dựa trên kết quả đánh giá.

**Independent Test**: Có thể test độc lập bằng cách kiểm tra lộ trình được tạo ra cho các profile khác nhau.

### Independent Test Criteria
- [ ] Hệ thống hiển thị danh sách khóa học, sách, dự án phù hợp
- [ ] Lộ trình được cá nhân hóa dựa trên profile người dùng (VD: IQ cao, DQ thấp → khóa học công nghệ)
- [ ] Hệ thống hiển thị lộ trình chi tiết với timeline khi chọn kỹ năng

### Tasks

- [ ] T054 [P] [US3] Implement LearningPathService trong backend/src/services/learning_path_service.py
- [ ] T055 [P] [US3] Tạo API endpoints cho learning paths trong backend/src/api/learning_paths.py
- [ ] T056 [P] [US3] Implement LearningPath component trong frontend/src/components/LearningPath.tsx
- [ ] T057 [P] [US3] Implement SkillCard component trong frontend/src/components/SkillCard.tsx
- [ ] T058 [P] [US3] Tạo learning path page trong frontend/src/pages/learning-path.tsx
- [ ] T059 [P] [US3] Tạo roadmap library data trong backend/scripts/load_roadmap_library.py
- [ ] T060 [US3] Implement learning path generation logic trong backend/src/services/learning_path_service.py

## Phase 6: User Story 4 - Theo dõi tiến trình phát triển (P3)

**Goal**: Người dùng có thể làm lại bài test định kỳ để theo dõi sự phát triển của bản thân theo thời gian.

**Independent Test**: Có thể test độc lập bằng cách so sánh kết quả test của cùng một người ở các thời điểm khác nhau.

### Independent Test Criteria
- [ ] Hệ thống hiển thị so sánh với kết quả test cũ khi làm test mới
- [ ] Hệ thống hiển thị biểu đồ tiến trình 4 chỉ số theo thời gian
- [ ] Hệ thống ghi nhận và chúc mừng thành tích khi có sự cải thiện đáng kể

### Tasks

- [ ] T061 [P] [US4] Implement ProgressTrackingService trong backend/src/services/progress_tracking_service.py
- [ ] T062 [P] [US4] Tạo API endpoints cho progress tracking trong backend/src/api/progress.py
- [ ] T063 [P] [US4] Implement ProgressChart component trong frontend/src/components/ProgressChart.tsx
- [ ] T064 [P] [US4] Implement ComparisonView component trong frontend/src/components/ComparisonView.tsx
- [ ] T065 [P] [US4] Tạo progress tracking page trong frontend/src/pages/progress.tsx
- [ ] T066 [US4] Implement progress comparison logic trong backend/src/services/progress_tracking_service.py

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Hoàn thiện hệ thống với các tính năng cross-cutting và tối ưu hóa

### Independent Test Criteria
- [ ] Hệ thống hoạt động ổn định với 1000 người dùng đồng thời
- [ ] Thời gian tải trang không vượt quá 3 giây
- [ ] Tất cả tests pass (unit, integration, E2E)
- [ ] Mobile-first responsive design hoạt động đúng trên các thiết bị

### Tasks

- [ ] T067 [P] Implement error handling middleware trong backend/src/middleware/error_handler.py
- [ ] T068 [P] Implement rate limiting middleware trong backend/src/middleware/rate_limiter.py
- [ ] T069 [P] Implement database backup scripts trong backend/scripts/backup.py
- [ ] T070 [P] Implement data retention scripts trong backend/scripts/retention.py
- [ ] T071 [P] Tạo responsive CSS styles trong frontend/src/styles/
- [ ] T072 [P] Implement mobile navigation component trong frontend/src/components/MobileNav.tsx
- [ ] T073 [P] Tạo unit tests cho algorithms trong backend/tests/unit/
- [ ] T074 [P] Tạo integration tests cho API trong backend/tests/integration/
- [ ] T075 [P] Tạo E2E tests cho user workflows trong frontend/tests/e2e/
- [ ] T076 [P] Implement performance monitoring trong backend/src/monitoring/
- [ ] T077 [P] Tạo deployment scripts trong scripts/deploy/
- [ ] T078 [P] Tạo documentation trong docs/

## Dependencies

### User Story Completion Order
1. **User Story 1** (P1) - Đánh giá 4 chỉ số phát triển
2. **User Story 2** (P1) - Phân tích Ikigai và gợi ý nghề nghiệp  
3. **User Story 3** (P2) - Lộ trình học tập cá nhân hóa
4. **User Story 4** (P3) - Theo dõi tiến trình phát triển

### Story Dependencies
- **User Story 2** phụ thuộc vào **User Story 1** (cần kết quả 4 chỉ số)
- **User Story 3** phụ thuộc vào **User Story 2** (cần gợi ý nghề nghiệp)
- **User Story 4** phụ thuộc vào **User Story 1** (cần lịch sử test)

## Parallel Execution Examples

### Phase 3 (User Story 1) - Parallel Opportunities
```bash
# Backend services (có thể chạy song song)
T028, T029, T030, T031  # Services
T032, T033, T034, T035  # API endpoints

# Frontend components (có thể chạy song song)  
T036, T037, T038        # Components
T039, T040              # Pages
T041                    # API client
```

### Phase 4 (User Story 2) - Parallel Opportunities
```bash
# Backend services (có thể chạy song song)
T045, T046              # Services
T047                    # API endpoints

# Frontend components (có thể chạy song song)
T048, T049              # Components
T050                    # Page
```

## Implementation Strategy

### MVP Scope (Phase 1-4)
- **Phase 1-2**: Setup và foundational components
- **Phase 3**: User Story 1 (Đánh giá 4 chỉ số) - Core functionality
- **Phase 4**: User Story 2 (Ikigai và gợi ý nghề nghiệp) - Unique value proposition

### Incremental Delivery
1. **Sprint 1**: Setup + Foundational (T001-T027)
2. **Sprint 2**: User Story 1 - Backend (T028-T044)  
3. **Sprint 3**: User Story 1 - Frontend (T036-T044)
4. **Sprint 4**: User Story 2 - Complete (T045-T053)
5. **Sprint 5**: User Story 3 (T054-T060)
6. **Sprint 6**: User Story 4 (T061-T066)
7. **Sprint 7**: Polish & Cross-cutting (T067-T078)

### Testing Strategy
- **Unit Tests**: Algorithms và business logic (T073)
- **Integration Tests**: API endpoints và database (T074)
- **E2E Tests**: Complete user workflows (T075)
- **Performance Tests**: Load testing với 1000 concurrent users

## Success Metrics

- **SC-001**: Người dùng hoàn thành bài test trong vòng 15 phút
- **SC-002**: Hệ thống xử lý và hiển thị kết quả trong vòng 30 giây
- **SC-003**: 90% người dùng hiểu được kết quả đánh giá
- **SC-004**: 80% người dùng thấy gợi ý nghề nghiệp phù hợp
- **SC-005**: Hệ thống hỗ trợ 1000 người dùng đồng thời
- **SC-006**: 70% người dùng quay lại sử dụng trong 30 ngày
- **SC-007**: Thời gian tải trang <3 giây
- **SC-008**: Thuật toán có độ chính xác >95%

## Notes

- Tất cả tasks phải tuân thủ format checklist nghiêm ngặt
- Mỗi task phải có file path cụ thể
- Tasks có [P] có thể chạy song song
- Tasks có [US1-4] thuộc về user story tương ứng
- Setup và Foundational phases không có story labels
- Polish phase không có story labels