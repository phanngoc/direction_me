# Feature Specification: Chatbot Assessment Interface

**Feature Branch**: `003-chatbot-assessment-interface`  
**Created**: 2025-10-25  
**Status**: Draft  
**Input**: User description: "user tương tác theo phương thức chatbot => bài Assessment sẽ hiện ra 1 page riêng để user chọn đáp án (cấu trúc theo @data_question.md ) => hoàn thành thì quay về chatbot , để nhận được result (Frontend hiển thị Radar cho 4 chỉ số và Facet bars; hiển thị "Ikigai map" (vùng giao thoa)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Assessment via Chatbot Interface (Priority: P1)

A user interacts with a chatbot interface to start their career assessment. The chatbot guides them through the process, and when they're ready to take the assessment, they are redirected to a dedicated assessment page where they answer questions structured according to the data_question.md format. After completing the assessment, they return to the chatbot to receive their results with visual representations including radar charts for the four quotients (IQ, EQ, DQ, AQ), facet bars, and an Ikigai map showing intersection areas.

**Why this priority**: This is the core user journey that delivers the primary value proposition. Without this complete flow from chatbot interaction to assessment completion to results visualization, the feature cannot provide meaningful career guidance to users.

**Independent Test**: Can be fully tested by having a user start a conversation with the chatbot, navigate to the assessment page, complete all questions, and return to see their personalized results with all visualizations. This delivers standalone value as a complete assessment experience.

**Acceptance Scenarios**:

1. **Given** a user starts a conversation with the chatbot, **When** they express interest in taking an assessment, **Then** the chatbot provides clear guidance on the assessment process
2. **Given** a user is ready to begin assessment, **When** they click to start, **Then** they are redirected to a dedicated assessment page with questions structured according to the data format
3. **Given** a user is on the assessment page, **When** they answer questions, **Then** their progress is saved and they can navigate between questions
4. **Given** a user completes all assessment questions, **When** they submit their final answers, **Then** they are redirected back to the chatbot interface
5. **Given** a user returns to the chatbot after completing assessment, **When** they request their results, **Then** they see visual representations including radar charts, facet bars, and Ikigai map

---

### User Story 2 - Navigate Assessment Questions with Progress Tracking (Priority: P2)

A user can navigate through the assessment questions with clear progress indicators, save their progress, and return to incomplete assessments later.

**Why this priority**: This enhances the user experience by allowing flexibility in assessment completion and reducing abandonment rates. While valuable, the core assessment functionality can still work without this feature.

**Independent Test**: Can be tested by starting an assessment, answering some questions, leaving the page, and returning later to continue where they left off with progress indicators showing completion status.

**Acceptance Scenarios**:

1. **Given** a user is taking an assessment, **When** they view the question interface, **Then** they see clear progress indicators showing which questions are completed
2. **Given** a user answers a question, **When** they move to the next question, **Then** their answer is automatically saved
3. **Given** a user leaves the assessment page, **When** they return later, **Then** they can continue from where they left off
4. **Given** a user wants to review their answers, **When** they navigate back to previous questions, **Then** they can see and modify their previous responses

---

### User Story 3 - View Detailed Results and Insights (Priority: P3)

A user can explore their assessment results in detail, including breakdowns by quotient and facet, explanations of their scores, and personalized insights about their strengths and areas for development.

**Why this priority**: This adds depth to the results presentation but the core value is delivered with basic result visualization. Users can still benefit from knowing their scores without detailed insights.

**Independent Test**: Can be tested by completing an assessment and then exploring the detailed results section to verify that users receive comprehensive explanations of their scores and personalized insights.

**Acceptance Scenarios**:

1. **Given** a user has completed their assessment, **When** they view their results, **Then** they see detailed breakdowns for each quotient (IQ, EQ, DQ, AQ)
2. **Given** a user explores their results, **When** they click on specific facets, **Then** they see explanations of what each score means
3. **Given** a user reviews their Ikigai map, **When** they hover over intersection areas, **Then** they see explanations of how their quotients align with career paths
4. **Given** a user wants to understand their results better, **When** they request additional insights, **Then** they receive personalized explanations of their strengths and development areas

---

### Edge Cases

- What happens when a user starts an assessment but closes their browser before completing it?
- How does the system handle users who answer questions too quickly (potential rushing)?
- What if a user provides inconsistent answers across similar questions in different modules?
- How does the system respond when a user's assessment results show equal strength across multiple quotients?
- What happens when a user tries to access the assessment page without going through the chatbot interface?
- How does the system handle users who complete the assessment but then try to retake it immediately?
- What if a user's internet connection is lost during the assessment?

## Requirements *(mandatory)*

### Functional Requirements

#### Chatbot Interface Requirements

- **FR-001**: System MUST provide a conversational chatbot interface for user interaction
- **FR-002**: System MUST guide users through the assessment process via chatbot conversation
- **FR-003**: System MUST redirect users from chatbot to dedicated assessment page when ready
- **FR-004**: System MUST maintain conversation context when users return from assessment
- **FR-005**: System MUST provide assessment results through chatbot interface after completion

#### Assessment Page Requirements

- **FR-006**: System MUST display assessment questions in a dedicated page separate from chatbot
- **FR-007**: System MUST structure questions according to the data_question.md format with IQ, EQ, DQ, AQ modules
- **FR-008**: System MUST present IQ questions as multiple-choice with correct answers and rationales
- **FR-009**: System MUST present EQ, DQ, AQ questions as Likert-scale statements with reverse scoring
- **FR-010**: System MUST save user responses automatically during assessment
- **FR-011**: System MUST allow users to navigate between questions and review previous answers
- **FR-012**: System MUST track assessment progress and completion status
- **FR-013**: System MUST redirect users back to chatbot after assessment completion

#### Results Visualization Requirements

- **FR-014**: System MUST display radar charts showing scores for all four quotients (IQ, EQ, DQ, AQ)
- **FR-015**: System MUST display facet bars showing detailed breakdowns within each quotient
- **FR-016**: System MUST display Ikigai map showing intersection areas of user's strengths
- **FR-017**: System MUST calculate and display scores based on correct answers and difficulty weights for IQ
- **FR-018**: System MUST calculate and display scores based on Likert responses with reverse scoring for EQ, DQ, AQ
- **FR-019**: System MUST provide career recommendations based on assessment results
- **FR-020**: System MUST log assessment timing and consistency metrics for analysis

#### Data Processing Requirements

- **FR-021**: System MUST process IQ responses using correct/incorrect scoring with difficulty weights
- **FR-022**: System MUST process Likert responses with reverse scoring flags for EQ, DQ, AQ
- **FR-023**: System MUST calculate facet scores within each quotient domain
- **FR-024**: System MUST generate overall quotient scores from facet calculations
- **FR-025**: System MUST detect and flag inconsistent responses for quality control
- **FR-026**: System MUST track response timing to identify rushed or thoughtful answers
- **FR-027**: System MUST suggest retesting when inconsistency or rushing is detected

### Key Entities

- **Chatbot Session**: Represents an ongoing conversation between user and chatbot, including context, assessment status, and results access
- **Assessment Response**: Captures user answers to assessment questions with timestamps, question metadata, and scoring information
- **Assessment Result**: Aggregated scores and analysis including quotient scores, facet breakdowns, Ikigai components, and career recommendations
- **Visualization Data**: Structured data for rendering radar charts, facet bars, and Ikigai map with user-specific values and configurations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete the full assessment journey from chatbot interaction to results viewing in under 60 minutes
- **SC-002**: 90% of users who start the assessment complete it successfully without technical issues
- **SC-003**: Assessment results load and display within 5 seconds of completion
- **SC-004**: Users can navigate between chatbot and assessment page seamlessly without losing progress
- **SC-005**: 85% of users report that the chatbot interface feels natural and helpful for assessment guidance
- **SC-006**: All visualizations (radar charts, facet bars, Ikigai map) render correctly across different devices and browsers
- **SC-007**: System accurately processes and scores all question types according to their respective algorithms
- **SC-008**: Users can save and resume incomplete assessments with 100% data preservation
- **SC-009**: Assessment completion rate exceeds 80% of users who start the process
- **SC-010**: Results visualization provides clear, actionable insights that 90% of users find valuable
- **SC-011**: System detects and flags inconsistent responses in at least 95% of cases where inconsistency exists
- **SC-012**: Career recommendations are generated and displayed within 3 seconds of assessment completion

### Assumptions

1. **User Base**: Primary users are Vietnamese students aged 15-25 seeking career guidance
2. **Assessment Data**: Questions and scoring algorithms are based on validated psychological research
3. **Chatbot Capability**: Chatbot can handle natural language interactions and guide users effectively
4. **Device Compatibility**: Users primarily access via desktop/laptop browsers with mobile support
5. **Internet Connectivity**: Users have reliable internet access for seamless chatbot and assessment interaction
6. **Data Privacy**: User assessment data is treated confidentially and stored securely
7. **Visualization Performance**: Charts and maps render efficiently without causing browser slowdowns
8. **Question Format**: Assessment questions follow the exact structure defined in data_question.md
9. **Scoring Accuracy**: Backend scoring algorithms correctly process all question types and difficulty levels
10. **User Intent**: Users are motivated to complete assessments honestly for meaningful results

### Dependencies

1. **Assessment Data**: Complete question bank with IQ, EQ, DQ, AQ items and scoring keys
2. **Chatbot Engine**: Conversational AI system capable of natural language processing
3. **Visualization Library**: Charting solution for radar charts, bar charts, and custom Ikigai maps
4. **User Authentication**: System to identify and track users across chatbot and assessment sessions
5. **Data Storage**: Persistent storage for user responses, results, and conversation history
6. **Scoring Engine**: Backend system for processing responses and calculating scores
7. **Career Database**: Repository of career recommendations mapped to assessment results

### Out of Scope

- Voice-based chatbot interaction (text-only interface)
- Offline assessment capability
- Real-time collaboration or group assessments
- Integration with external career databases beyond basic recommendations
- Advanced AI-powered career counseling beyond basic recommendations
- Social sharing of results or comparison with other users
- Parent or teacher access to student results
- Mobile native applications (web-responsive interface only)
- Multi-language support beyond Vietnamese
- Advanced analytics or reporting for administrators