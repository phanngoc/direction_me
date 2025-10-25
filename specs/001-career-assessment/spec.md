# Feature Specification: MyWay - Tìm đường riêng của bạn

**Feature Branch**: `001-career-assessment`  
**Created**: 2024-12-19  
**Status**: Draft  
**Input**: User description: "MyWay - Tìm đường riêng của bạn: Hệ thống đánh giá 4 chỉ số IQ, EQ, DQ, AQ và định hướng nghề nghiệp dựa trên triết lý Ikigai"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Đánh giá 4 chỉ số phát triển (Priority: P1)

Học sinh/sinh viên có thể thực hiện bài test đánh giá 4 chỉ số IQ, EQ, DQ, AQ để hiểu rõ năng lực bản thân và nhận được kết quả phân tích chi tiết.

**Why this priority**: Đây là chức năng cốt lõi của hệ thống, cung cấp giá trị chính cho người dùng. Không có đánh giá thì không có định hướng.

**Independent Test**: Có thể test độc lập bằng cách cho một người dùng mới thực hiện đầy đủ bài test và nhận kết quả 4 chỉ số.

**Acceptance Scenarios**:

1. **Given** người dùng mới đăng ký tài khoản, **When** họ truy cập trang test, **Then** hệ thống hiển thị bộ câu hỏi 4 nhóm (IQ, EQ, DQ, AQ)
2. **Given** người dùng đang làm bài test, **When** họ trả lời tất cả câu hỏi, **Then** hệ thống tính toán và hiển thị điểm số 4 chỉ số
3. **Given** người dùng hoàn thành bài test, **When** họ xem kết quả, **Then** hệ thống hiển thị biểu đồ radar chart với 4 trục IQ, EQ, DQ, AQ

---

### User Story 2 - Phân tích Ikigai và gợi ý nghề nghiệp (Priority: P1)

Dựa trên kết quả 4 chỉ số, hệ thống phân tích vùng Ikigai của người dùng và đưa ra gợi ý nghề nghiệp phù hợp.

**Why this priority**: Đây là giá trị độc đáo của hệ thống, kết hợp tâm lý học và triết lý Nhật Bản để đưa ra định hướng nghề nghiệp.

**Independent Test**: Có thể test độc lập bằng cách nhập kết quả test và kiểm tra gợi ý nghề nghiệp được tạo ra.

**Acceptance Scenarios**:

1. **Given** người dùng có kết quả 4 chỉ số, **When** hệ thống phân tích, **Then** hiển thị biểu đồ Ikigai với 4 vòng giao nhau
2. **Given** hệ thống đã phân tích Ikigai, **When** người dùng xem gợi ý, **Then** hiển thị top 3 nghề nghiệp phù hợp với lý do cụ thể
3. **Given** người dùng có kết quả DQ cao, EQ trung bình, **When** xem gợi ý, **Then** hệ thống đề xuất nghề UI/UX Designer, Digital Marketer

---

### User Story 3 - Lộ trình học tập cá nhân hóa (Priority: P2)

Hệ thống tạo ra lộ trình học tập và phát triển kỹ năng cá nhân hóa dựa trên kết quả đánh giá.

**Why this priority**: Cung cấp hướng dẫn cụ thể để người dùng cải thiện và phát triển, tạo giá trị lâu dài.

**Independent Test**: Có thể test độc lập bằng cách kiểm tra lộ trình được tạo ra cho các profile khác nhau.

**Acceptance Scenarios**:

1. **Given** người dùng có kết quả đánh giá, **When** xem lộ trình, **Then** hệ thống hiển thị danh sách khóa học, sách, dự án phù hợp
2. **Given** người dùng có IQ cao, DQ thấp, **When** xem lộ trình, **Then** hệ thống gợi ý khóa học công nghệ, dự án sáng tạo số
3. **Given** người dùng muốn cải thiện kỹ năng, **When** chọn một kỹ năng, **Then** hệ thống hiển thị lộ trình chi tiết với timeline

---

### User Story 4 - Theo dõi tiến trình phát triển (Priority: P3)

Người dùng có thể làm lại bài test định kỳ để theo dõi sự phát triển của bản thân theo thời gian.

**Why this priority**: Tạo engagement lâu dài và cho phép người dùng thấy sự tiến bộ, khuyến khích phát triển liên tục.

**Independent Test**: Có thể test độc lập bằng cách so sánh kết quả test của cùng một người ở các thời điểm khác nhau.

**Acceptance Scenarios**:

1. **Given** người dùng đã có kết quả test trước đó, **When** làm test mới, **Then** hệ thống hiển thị so sánh với kết quả cũ
2. **Given** người dùng xem lịch sử phát triển, **When** chọn khoảng thời gian, **Then** hệ thống hiển thị biểu đồ tiến trình 4 chỉ số
3. **Given** người dùng có sự cải thiện đáng kể, **When** xem báo cáo, **Then** hệ thống ghi nhận và chúc mừng thành tích

---

### Edge Cases

- What happens when người dùng bỏ dở bài test giữa chừng?
- How does system handle khi người dùng trả lời tất cả câu hỏi với cùng một đáp án?
- What happens when kết quả 4 chỉ số đều bằng nhau?
- How does system handle khi không có nghề nghiệp nào phù hợp với profile người dùng?
- What happens when người dùng muốn xóa kết quả test cũ?
- What happens when hệ thống gặp lỗi trong quá trình tính toán?
- How does system handle khi database connection bị mất?
- What happens when người dùng nhập dữ liệu không hợp lệ?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST cho phép người dùng tạo tài khoản và đăng nhập
- **FR-002**: System MUST hiển thị bộ câu hỏi 4 nhóm (IQ, EQ, DQ, AQ) với giao diện thân thiện
- **FR-003**: System MUST tính toán điểm số cho từng chỉ số dựa trên câu trả lời
- **FR-004**: System MUST hiển thị biểu đồ radar chart với 4 trục IQ, EQ, DQ, AQ
- **FR-005**: System MUST phân tích và hiển thị biểu đồ Ikigai tương tác
- **FR-006**: System MUST đưa ra gợi ý top 3 nghề nghiệp phù hợp với lý do cụ thể
- **FR-007**: System MUST tạo lộ trình học tập cá nhân hóa với khóa học, sách, dự án
- **FR-008**: System MUST lưu trữ kết quả test và lịch sử phát triển của người dùng
- **FR-009**: System MUST cho phép người dùng làm lại test và so sánh kết quả
- **FR-010**: System MUST hiển thị báo cáo tiến trình phát triển theo thời gian
- **FR-023**: System MUST yêu cầu password tối thiểu 8 ký tự cho tài khoản người dùng
- **FR-024**: System MUST sử dụng relational database (PostgreSQL/MySQL) để lưu trữ dữ liệu
- **FR-027**: System MUST hiển thị giao diện responsive trên mobile và desktop
- **FR-028**: System MUST ưu tiên mobile-first design cho trải nghiệm người dùng
- **FR-012**: System MUST hoạt động ổn định với ít nhất 1000 người dùng đồng thời
- **FR-013**: System MUST tính toán điểm số IQ với trọng số độ khó cho từng câu hỏi
- **FR-014**: System MUST chuẩn hóa điểm Likert scale từ 1-5 thành thang 0-100
- **FR-015**: System MUST tính toán 4 trục Ikigai (Love, Good at, World needs, Paid for) theo công thức toán học
- **FR-016**: System MUST sử dụng harmonic mean để tính điểm Ikigai tổng hợp
- **FR-017**: System MUST đánh giá độ phù hợp nghề nghiệp dựa trên vector profile 16 chiều
- **FR-018**: System MUST áp dụng ngưỡng tối thiểu và trọng số cho từng nghề nghiệp
- **FR-019**: System MUST cung cấp giải thích AI về lý do gợi ý nghề nghiệp
- **FR-020**: System MUST tạo lộ trình học tập dựa trên thư viện roadmap có sẵn
- **FR-021**: System MUST cho phép cấu hình trọng số và ngưỡng nghề nghiệp qua JSON
- **FR-022**: System MUST phát hiện và cảnh báo mất cân bằng trong 4 trục Ikigai

### Key Entities *(include if feature involves data)*

- **User Profile**: Thông tin cá nhân, kết quả test, lịch sử phát triển, lộ trình học tập
- **Assessment Result**: Điểm số 4 chỉ số IQ, EQ, DQ, AQ, thời gian test, phân tích Ikigai
- **Profile Vector**: Vector 16 chiều chứa điểm số tất cả facets (IQ_LR, IQ_NR, IQ_VR, IQ_SR, EQ_Emp, EQ_Soc, EQ_SAw, EQ_SReg, DQ_IL, DQ_Cr, DQ_Sf, DQ_Co, AQ_C, AQ_O, AQ_R, AQ_E)
- **Ikigai Scores**: 4 trục Love, Good at, World needs, Paid for và điểm tổng hợp harmonic/geometric
- **Career Rules**: Trọng số, ngưỡng tối thiểu, bonus keys cho từng nghề nghiệp
- **Career Suggestion**: Nghề nghiệp gợi ý, điểm phù hợp, lý do cụ thể, giải thích AI
- **Learning Path**: Khóa học, sách, dự án, timeline, mức độ ưu tiên
- **Roadmap Library**: Thư viện kỹ năng, dự án, thói quen cho từng nghề nghiệp
- **Progress Tracking**: Lịch sử test, so sánh kết quả, biểu đồ tiến trình
- **Algorithm Config**: Cấu hình JSON cho trọng số nghề nghiệp, A/B testing

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Người dùng có thể hoàn thành bài test đánh giá trong vòng 15 phút
- **SC-002**: Hệ thống xử lý và hiển thị kết quả trong vòng 30 giây sau khi hoàn thành test
- **SC-003**: 90% người dùng hiểu được kết quả đánh giá và gợi ý nghề nghiệp
- **SC-004**: 80% người dùng thấy gợi ý nghề nghiệp phù hợp với mong muốn của họ
- **SC-005**: Hệ thống hỗ trợ ít nhất 1000 người dùng đồng thời mà không giảm hiệu suất
- **SC-006**: 70% người dùng quay lại sử dụng hệ thống trong vòng 30 ngày
- **SC-007**: Người dùng có thể truy cập lộ trình học tập và theo dõi tiến trình mọi lúc
- **SC-008**: Giảm 50% thời gian người dùng cần để tìm hiểu về nghề nghiệp phù hợp
- **SC-009**: Thuật toán tính điểm có độ chính xác >95% so với đánh giá thủ công
- **SC-010**: Hệ thống mapping nghề nghiệp có thể xử lý 8+ nghề với độ phù hợp >70%
- **SC-011**: Giải thích AI cho gợi ý nghề nghiệp được 85% người dùng hiểu và chấp nhận
- **SC-012**: Lộ trình học tập được cá nhân hóa dựa trên top-1 nghề nghiệp phù hợp
- **SC-013**: Hệ thống phát hiện mất cân bằng Ikigai với độ chính xác >90%
- **SC-014**: Hệ thống đáp ứng yêu cầu cơ bản về performance cho 1000 người dùng đồng thời
- **SC-015**: Thời gian tải trang không vượt quá 3 giây trên kết nối internet thông thường

## Mathematical Assessment Algorithm *(technical)*

### Scoring Methodology

**IQ Assessment (MCQ with weighted difficulty)**:
- Formula: `S_IQ = 100 * (Σ(d_i * r_i)) / Σ(d_i)`
- Where: `d_i` = difficulty weight, `r_i` = correct/incorrect (0/1)
- Facets: Logical Reasoning (LR), Numerical Reasoning (NR), Verbal Reasoning (VR), Spatial Reasoning (SR)

**EQ/DQ/AQ Assessment (Likert scale)**:
- Normalization: `t_j = (6-x_j) if reverse else x_j`, then `t̂_j = 25*(t_j-1)`
- Domain score: `S_D = (1/|G_D|) * Σ(S_D,facet)`
- EQ facets: Empathy, Social Skills, Self-Awareness, Self-Regulation
- DQ facets: Information Literacy, Creativity, Safety, Collaboration
- AQ facets: Control, Ownership, Reach, Endurance

### Ikigai Calculation

**Four Axes (0-100 scale)**:
- **Love (L)**: `mean(S_EQ,Empathy, S_EQ,Social, S_DQ,Creativity, S_INT)`
- **Good at (G)**: `0.6*S_IQ + 0.4*mean(S_DQ,IL, S_DQ,Cr, S_DQ,Co)`
- **World needs (W)**: `mean(S_EQ,Empathy, S_EQ,Social, S_DQ,Collaboration)`
- **Paid for (P)**: `max(φ_c(profile))` across all careers

**Ikigai Score**:
- Harmonic mean: `I_harm = 4 / (1/L + 1/G + 1/W + 1/P)`
- Geometric mean: `I_geo = (L*G*W*P)^0.25`

### Career Mapping Algorithm

**Profile Vector**: 16-dimensional vector `z` containing all facet scores

**Career Fit Score**: `φ_c(z) = (Σ w_c,k * z_k) * Π 1[z_m ≥ T_c,m]`
- Where: `w_c` = career weights, `T_c` = minimum thresholds
- Bonus: `+2%` per bonus axis exceeding 80 points

**Career Rules Database**:
- 8 predefined careers with weights, thresholds, and bonus keys
- JSON-configurable for A/B testing and market adaptation
- Explainable AI: Shows which facets contributed to high scores

### Learning Path Generation

**Roadmap Library**: Pre-defined skill sets, projects, and habits for each career
- **Skills**: Technical competencies to develop
- **Projects**: Hands-on practice opportunities  
- **Habits**: Daily/weekly routines for skill building

**Personalization Logic**:
- Based on top career match
- Considers current skill gaps
- Provides 2-week starter roadmap
- Includes progress tracking milestones

## Clarifications

### Session 2024-12-19

- Q: Security & Privacy Requirements → A: Basic security - chỉ cần HTTPS và password protection
- Q: Error Handling & Recovery → A: Basic error handling - chỉ hiển thị generic error messages
- Q: Data Persistence & Storage → A: Standard database - PostgreSQL/MySQL với backup và data retention
- Q: User Interface & Accessibility → A: Basic responsive design - mobile-first, desktop support
- Q: Performance & Scalability → A: Basic performance - chỉ đảm bảo hoạt động cơ bản

## Assumptions

- Người dùng chủ yếu là học sinh, sinh viên trong độ tuổi 16-25
- Người dùng có khả năng sử dụng internet và thiết bị di động cơ bản
- Người dùng sẵn sàng dành 15-20 phút để hoàn thành bài test
- Dữ liệu nghề nghiệp và khóa học được cập nhật định kỳ
- Người dùng muốn nhận được gợi ý cụ thể và có thể thực hiện được
- Thuật toán đánh giá dựa trên nghiên cứu tâm lý học và thống kê
- Hệ thống mapping nghề nghiệp có thể điều chỉnh theo thị trường Việt Nam