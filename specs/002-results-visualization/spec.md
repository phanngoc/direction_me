# Feature Specification: Assessment Results Visualization and Scoring

**Feature Branch**: `002-results-visualization`
**Created**: 2025-10-25
**Status**: Draft
**Input**: User description: "Frontend hiển thị Radar cho 4 chỉ số và Facet bars; hiển thị Ikigai map (vùng giao thoa). Backend chấm điểm: IQ: tính đúng/sai + trọng số difficulty. Likert: xử lý reverse_scored, tính facet → tính chỉ số → gợi ý nghề theo bảng mapping. Log thêm: thời gian trả lời, độ nhất quán (e.g., kiểm tra mâu thuẫn nội bộ), đề xuất retest."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - View Four-Domain Radar Chart (Priority: P1)

A student completes all four assessments (IQ, EQ, DQ, AQ) and views a radar chart visualizing their scores across all domains. The system calculates scores using weighted difficulty for IQ and reverse-scored handling for Likert items, then displays the results in an intuitive radar visualization showing relative strengths and weaknesses.

**Why this priority**: The radar chart is the primary visual summary that students need to understand their overall profile at a glance. It's the foundational visualization that enables self-awareness and career exploration, making it the highest priority deliverable.

**Independent Test**: Can be fully tested by completing all four assessments with known scores, verifying correct score calculations (IQ with difficulty weighting, Likert with reverse scoring), and confirming the radar chart accurately plots all four domain scores with proper scaling. Delivers immediate value as a comprehensive profile visualization.

**Acceptance Scenarios**:

1. **Given** a student has completed all four assessment domains, **When** they view their results, **Then** the system displays a radar chart with four axes (IQ, EQ, DQ, AQ) showing their normalized scores on each dimension
2. **Given** the system calculates IQ scores, **When** processing correct/incorrect answers, **Then** the system applies difficulty weighting to each question before calculating the total IQ score
3. **Given** the system calculates Likert scores (EQ, DQ, AQ), **When** processing responses, **Then** the system reverses scores for items flagged as reverse-scored before aggregating facet and domain scores
4. **Given** a student views the radar chart, **When** they interact with it, **Then** the system displays exact numerical scores and percentile rankings when hovering over each axis point

---

###User Story 2 - View Facet Bar Charts (Priority: P2)

A student views detailed facet-level breakdowns for each assessment domain displayed as bar charts. For IQ, the system shows performance across Logical, Numeric, Verbal, and Spatial reasoning. For EQ/DQ/AQ, the system shows scores for domain-specific facets, enabling students to identify specific strengths and development areas within each domain.

**Why this priority**: Facet-level insights provide actionable detail beyond domain scores, helping students understand which specific skills drive their overall performance. This is essential for personalized development planning but builds on the P1 overview visualization.

**Independent Test**: Can be tested by completing assessments and verifying facet scores are correctly calculated and displayed as horizontal bar charts for each domain, with facet names, scores, and visual bars proportional to performance levels. Delivers value as a diagnostic tool for targeted skill development.

**Acceptance Scenarios**:

1. **Given** a student views their IQ results, **When** they expand the facet details, **Then** the system displays four horizontal bars showing scores for Logical, Numeric, Verbal, and Spatial reasoning facets
2. **Given** a student views their EQ/DQ/AQ results, **When** they expand facet details, **Then** the system displays bar charts for each domain-specific facet (e.g., Self-awareness, Self-regulation, Empathy, Social skills for EQ)
3. **Given** facet scores are calculated, **When** the system processes IQ facets, **Then** each facet score reflects only the questions tagged to that facet with appropriate difficulty weighting
4. **Given** facet scores are calculated, **When** the system processes Likert facets, **Then** each facet score aggregates only the reverse-scored items belonging to that facet

---

### User Story 3 - View Ikigai Career Map (Priority: P3)

A student views an Ikigai-inspired career map showing the intersection of their four assessment domains with recommended career paths. The system maps assessment scores to career categories using a predefined mapping table, highlighting careers that align with the student's strengths across multiple domains (intersection zones).

**Why this priority**: The Ikigai map provides career guidance value but requires all domain scores to be calculated first. It's an enhancement that translates assessment data into actionable career recommendations, making it valuable but dependent on P1 and P2.

**Independent Test**: Can be tested by providing known assessment scores, verifying the system correctly identifies intersection zones (e.g., high IQ + high EQ = counseling/teaching careers), and confirming recommended careers appear in the appropriate Ikigai quadrants. Delivers value as a career exploration and decision-support tool.

**Acceptance Scenarios**:

1. **Given** a student has completed all four assessments, **When** they view the Ikigai map, **Then** the system displays a Venn diagram-style visualization with four overlapping circles representing IQ, EQ, DQ, and AQ
2. **Given** the system determines career recommendations, **When** analyzing assessment scores, **Then** the system uses a predefined mapping table to match score combinations to relevant career categories
3. **Given** a student views intersection zones on the Ikigai map, **When** they click on a specific zone (e.g., IQ + EQ intersection), **Then** the system displays a list of recommended careers that require strengths in both domains
4. **Given** career recommendations are displayed, **When** the student explores them, **Then** each career shows why it matches their assessment profile (e.g., "High logical reasoning + strong empathy = ideal for clinical psychology")

---

### User Story 4 - Review Response Analytics and Retest Recommendations (Priority: P4)

A student views analytics about their assessment-taking behavior, including response times per question, consistency metrics (detecting contradictory answers), and receives recommendations to retake assessments if inconsistencies are detected. This helps ensure result validity and identifies potential engagement issues.

**Why this priority**: Response analytics provide quality assurance and engagement insights but are secondary to core visualization features. They enhance result trustworthiness and user experience but don't directly contribute to career guidance, making them a lower priority enhancement.

**Independent Test**: Can be tested by completing assessments with deliberately inconsistent or rushed answers, verifying the system logs response times, detects contradictions (e.g., answering opposite on logically related Likert items), and displays appropriate retest warnings. Delivers value as a data quality and user engagement tool.

**Acceptance Scenarios**:

1. **Given** a student completes an assessment, **When** the system logs their responses, **Then** it records the timestamp and time spent for each question answered
2. **Given** the system analyzes Likert responses, **When** checking for consistency, **Then** it identifies logically contradictory answers (e.g., agreeing with both "I enjoy working with people" and its semantic opposite)
3. **Given** consistency issues are detected, **When** results are displayed, **Then** the system shows a warning message suggesting the student retake the affected assessment for more accurate results
4. **Given** a student views response analytics, **When** they explore their data, **Then** the system displays average response time per question type, fastest/slowest questions, and a consistency score percentage

---

### Edge Cases

- What happens when a student has only completed some domains but not all four?
- How does the system handle extreme outlier scores (e.g., perfect score on all IQ questions or all 1s on Likert scales)?
- What happens if the career mapping table doesn't contain any careers matching a student's unique score combination?
- How does the system visualize results for students with incomplete facet data (skipped questions)?
- What happens when response time logging fails due to client-side time drift or network issues?
- How does the consistency check handle assessments with insufficient data points to detect contradictions?
- What happens if a student's normalized scores result in a degenerate radar chart (all scores at min or max)?
- How does the system handle visualization rendering on very small screens or accessibility devices?

## Requirements *(mandatory)*

### Functional Requirements

**Score Calculation**:
- **FR-001**: System MUST calculate IQ scores by validating each answer against the correct answer, applying difficulty weighting to each question, and summing weighted scores for the total IQ score
- **FR-002**: System MUST identify and reverse-score Likert items flagged as reverse-scored before aggregating facet and domain scores
- **FR-003**: System MUST calculate facet-level scores by aggregating only the items tagged to each specific facet within a domain
- **FR-004**: System MUST calculate domain-level scores by aggregating all facet scores within that domain using equal or specified weighting
- **FR-005**: System MUST normalize scores to a common scale (e.g., 0-100) to enable cross-domain comparison on visualizations

**Visualization**:
- **FR-006**: System MUST display a radar chart with four axes (IQ, EQ, DQ, AQ) showing normalized scores for students who have completed all four assessments
- **FR-007**: System MUST display horizontal bar charts showing facet-level scores for each assessment domain with facet names and proportional visual bars
- **FR-008**: System MUST display an Ikigai-inspired career map showing intersection zones between the four domains with recommended careers in each zone
- **FR-009**: System MUST make visualizations interactive, allowing users to hover or click for detailed numerical scores and percentile rankings

**Career Recommendations**:
- **FR-010**: System MUST use a predefined career mapping table to match score combinations to relevant career categories
- **FR-011**: System MUST identify intersection zones on the Ikigai map based on which domains have above-threshold scores
- **FR-012**: System MUST display career recommendations with explanations of why each career matches the student's assessment profile

**Response Analytics**:
- **FR-013**: System MUST log the timestamp and time spent for each question answered during assessments
- **FR-014**: System MUST calculate average response time per question type and identify fastest/slowest questions
- **FR-015**: System MUST detect logically contradictory Likert responses by identifying semantically opposite items answered inconsistently
- **FR-016**: System MUST calculate a consistency score percentage based on detected contradictions relative to total comparable item pairs
- **FR-017**: System MUST display warnings and retest recommendations when consistency scores fall below acceptable thresholds

**Data Display**:
- **FR-018**: System MUST display partial results for students who have completed fewer than four domains, clearly indicating which domains are missing
- **FR-019**: System MUST handle extreme outlier scores gracefully in visualizations without distorting scales or hiding data
- **FR-020**: System MUST provide fallback career recommendations when the mapping table lacks entries for unusual score combinations

### Key Entities

- **Radar Chart Data**: Four-axis visualization data containing normalized domain scores (IQ, EQ, DQ, AQ), percentile rankings, and interaction state
- **Facet Bar Chart Data**: Domain-specific horizontal bar visualization containing facet names, raw scores, normalized scores, and visual bar lengths
- **Ikigai Career Map**: Venn diagram-style visualization with four overlapping circles, intersection zones, and career recommendations per zone
- **Score Calculation Result**: Computed scores including raw responses, difficulty weights (for IQ), reverse-scoring flags (for Likert), facet aggregations, domain aggregations, and normalized values
- **Career Mapping Entry**: Predefined mapping rule containing score thresholds for each domain, intersection zone identifier, career category, and recommendation rationale
- **Response Analytics Log**: Timestamped response data including question ID, answer selected, time spent, submission timestamp, and sequence order
- **Consistency Analysis**: Contradiction detection results including item pairs checked, contradictions found, consistency score percentage, and retest recommendation flag

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System calculates all scores (IQ with difficulty weighting, Likert with reverse scoring) with 100% accuracy verified against manual calculations
- **SC-002**: Radar chart, facet bar charts, and Ikigai map render within 2 seconds of data availability for 95% of users
- **SC-003**: 90% of students can correctly interpret their relative strengths and weaknesses after viewing the radar chart without additional guidance
- **SC-004**: Career recommendations match student expectations or interests in at least 70% of cases based on user feedback surveys
- **SC-005**: Consistency detection identifies at least 80% of deliberately contradictory responses in validation testing
- **SC-006**: Visualizations display correctly across all screen sizes and accessibility tools without data loss or distortion
- **SC-007**: Students with partial assessment completion (1-3 domains) receive meaningful partial results within the same timeframe as complete results
- **SC-008**: 85% of students find facet-level insights actionable for personal development planning based on exit surveys
