# Feature Specification: MyWay - Career Assessment Platform

**Feature Branch**: `001-career-assessment-platform`
**Created**: 2025-10-25
**Status**: Draft
**Input**: User description: "MyWay – Tìm đường riêng của bạn - Career assessment platform integrating IQ, EQ, DQ, AQ evaluation and Ikigai philosophy for students"

## Clarifications

### Session 2025-10-25

- Q: What authentication method should the platform use for user accounts? → A: Email/Password - traditional auth with full control, standard for educational platforms
- Q: Should the platform support multiple languages, or only Vietnamese? → A: Vietnamese only - Single language for Vietnamese students, simpler implementation

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Comprehensive Assessment (Priority: P1)

A student visits MyWay to discover their strengths, weaknesses, and potential career paths. They complete a comprehensive assessment covering four key developmental quotients (IQ, EQ, DQ, AQ) and receive personalized career recommendations based on the Ikigai framework.

**Why this priority**: This is the core value proposition of the platform. Without this fundamental journey, the platform cannot deliver any meaningful value to users. It represents the minimum viable product that can be tested and demonstrated independently.

**Independent Test**: Can be fully tested by having a test user create an account, complete all four assessment modules, and receive a comprehensive results dashboard with Ikigai-based career recommendations. This delivers standalone value as a self-discovery tool.

**Acceptance Scenarios**:

1. **Given** a new student visits the platform, **When** they create an account and begin the assessment, **Then** they are presented with a clear assessment structure showing IQ, EQ, DQ, and AQ modules
2. **Given** a student is taking the assessment, **When** they complete each module, **Then** their progress is saved and they can resume later
3. **Given** a student completes all four assessment modules, **When** they submit their final answers, **Then** they receive a comprehensive results dashboard showing:
   - Radar chart visualizing their four quotients
   - Ikigai map showing the intersection of what they love, what they're good at, what the world needs, and what they can be paid for
   - Top 3 recommended career paths with detailed explanations
4. **Given** a student views their results, **When** they explore career recommendations, **Then** each recommendation explains how it aligns with their specific assessment results

---

### User Story 2 - Receive Personalized Learning Roadmap (Priority: P2)

After completing the assessment, a student receives a customized learning roadmap with specific courses, skills to develop, and resources tailored to their assessment results and recommended career paths.

**Why this priority**: This extends the value from awareness (assessment results) to action (personalized development plan). While valuable, users can still benefit from knowing their strengths and career fit without this feature.

**Independent Test**: Can be tested by completing the P1 assessment journey, then verifying that users receive specific, actionable recommendations including online courses, skill development priorities, books, and community resources matched to their profile.

**Acceptance Scenarios**:

1. **Given** a student has completed their assessment, **When** they view their personalized roadmap, **Then** they see recommended online courses from platforms like Coursera and Udemy
2. **Given** a student explores their roadmap, **When** they select a career path, **Then** they see skill development priorities ranked by importance for that career
3. **Given** a student wants to improve a weak quotient, **When** they select that area, **Then** they receive targeted resources (books, projects, communities) to develop that capability
4. **Given** a student views course recommendations, **When** they click on a course, **Then** they are provided with a direct link and explanation of how it supports their development goals

---

### User Story 3 - Track Progress Over Time (Priority: P3)

Students can retake assessments periodically to track their development across the four quotients and see how their Ikigai alignment evolves with skill development and life experience.

**Why this priority**: This adds long-term engagement and shows measurable personal growth, but the platform delivers core value without progress tracking. Users can still discover their current state and get recommendations.

**Independent Test**: Can be tested by having a user complete the initial assessment (P1), wait a period, retake the assessment, and verify they can view comparison charts showing how their quotients have changed and how their career recommendations have evolved.

**Acceptance Scenarios**:

1. **Given** a student completed an assessment 3 months ago, **When** they return to retake it, **Then** the system preserves their historical results while capturing new responses
2. **Given** a student completes a follow-up assessment, **When** they view results, **Then** they see a comparison chart showing how each quotient has changed over time
3. **Given** a student has multiple assessment results, **When** they view their timeline, **Then** they can see how their Ikigai alignment has evolved and which career recommendations have remained consistent
4. **Given** a student shows improvement in a specific quotient, **When** they review progress, **Then** the system highlights which actions or resources from their roadmap may have contributed to growth

---

### User Story 4 - Explore Career Insights and Examples (Priority: P4)

Students can explore detailed information about recommended careers, including real-world examples, required skills, typical career progression, and success stories from people with similar assessment profiles.

**Why this priority**: This enriches career recommendations with context and inspiration but is not essential for the core assessment and recommendation functionality. Users can research careers independently.

**Independent Test**: Can be tested by selecting a recommended career from the results dashboard and verifying that users receive comprehensive career information including skill requirements, career paths, salary ranges, and relevant success stories.

**Acceptance Scenarios**:

1. **Given** a student receives career recommendations, **When** they select a specific career, **Then** they see detailed information including required skills, typical progression, and market demand
2. **Given** a student explores a career, **When** they view success stories, **Then** they see profiles of professionals with similar assessment patterns who succeeded in that field
3. **Given** a student is uncertain about a career path, **When** they compare multiple recommendations, **Then** they can view side-by-side comparisons of skill requirements, growth potential, and alignment with their assessment
4. **Given** a student wants to understand market context, **When** they view career details, **Then** they see current job market information including demand trends and salary ranges

---

### Edge Cases

- What happens when a student provides inconsistent answers across similar questions in different modules?
- How does the system handle partially completed assessments that are abandoned for extended periods?
- What if a student's assessment results show equal strength across multiple quotients with no clear dominant area?
- How does the system respond when a student's interests (what they love) don't align with market demand (what they can be paid for)?
- What happens when a student completes the assessment but all four quotient scores are below average thresholds?
- How does the system handle students who rush through questions, completing the entire assessment in an unrealistically short time?
- What if a student's assessment suggests careers that conflict with their stated educational background or current field of study?

## Requirements *(mandatory)*

### Functional Requirements

#### Assessment Module Requirements

- **FR-001**: System MUST provide separate assessment modules for each of the four quotients (IQ, EQ, DQ, AQ)
- **FR-002**: System MUST deliver IQ assessment through logic puzzles, pattern recognition, mathematical problems, and analytical reasoning questions
- **FR-003**: System MUST evaluate EQ through situational scenarios requiring emotional awareness, empathy assessment, and social interaction judgment questions
- **FR-004**: System MUST measure DQ through questions about digital tool usage, online learning behaviors, content creation capabilities, and technology adoption patterns
- **FR-005**: System MUST assess AQ through hypothetical challenge scenarios, failure response situations, and adaptability questions
- **FR-006**: System MUST save user progress automatically during assessment to allow resumption at any point
- **FR-007**: System MUST validate assessment completion by ensuring all required questions in each module are answered
- **FR-008**: System MUST prevent assessment result generation until all four quotient modules are completed

#### Results and Analysis Requirements

- **FR-009**: System MUST generate a four-axis radar chart visualizing the user's scores across IQ, EQ, DQ, and AQ
- **FR-010**: System MUST create an interactive Ikigai map showing the intersection of: what the user loves, what they're good at, what the world needs, and what they can be paid for
- **FR-011**: System MUST provide at least three career path recommendations ranked by alignment with the user's assessment profile
- **FR-012**: System MUST explain each career recommendation by mapping it to specific assessment results and Ikigai components
- **FR-013**: System MUST identify the user's strongest and weakest quotients with contextual interpretation
- **FR-014**: System MUST preserve historical assessment results when users retake evaluations

#### Personalized Roadmap Requirements

- **FR-015**: System MUST generate customized skill development priorities based on recommended career paths
- **FR-016**: System MUST recommend specific online courses from major platforms matched to the user's development needs
- **FR-017**: System MUST suggest relevant books, projects, and experiential learning opportunities aligned with career goals
- **FR-018**: System MUST provide mentor suggestions and community recommendations relevant to target career paths
- **FR-019**: System MUST identify skill gaps between current assessment results and requirements for recommended careers

#### User Account and Data Requirements

- **FR-020**: System MUST allow users to create and authenticate accounts using email/password authentication
- **FR-020a**: System MUST validate email format and enforce password complexity requirements (minimum 8 characters)
- **FR-020b**: System MUST provide password reset functionality via email verification
- **FR-021**: System MUST persist user profile information, assessment responses, and results across sessions
- **FR-022**: System MUST allow users to update their profile information after account creation
- **FR-023**: System MUST associate all assessment data with individual user accounts for personalized tracking
- **FR-024**: System MUST allow users to retake assessments and view historical comparison data

#### Progress Tracking Requirements

- **FR-025**: System MUST enable users to retake assessments at defined intervals for progress measurement
- **FR-026**: System MUST generate comparison visualizations showing quotient changes over time
- **FR-027**: System MUST track which recommended resources users have engaged with
- **FR-028**: System MUST display timeline views of assessment history and personal development trends

#### Career Exploration Requirements

- **FR-029**: System MUST provide detailed career information for each recommended path including required skills, market demand, and typical progression
- **FR-030**: System MUST include success stories or case studies of professionals with similar assessment profiles
- **FR-031**: System MUST allow side-by-side comparison of multiple recommended career paths
- **FR-032**: System MUST display current market context including demand trends and salary information for recommended careers

### Non-Functional Requirements

- **NFR-001**: Assessment completion time should not exceed 45 minutes for the full four-module evaluation
- **NFR-002**: Results dashboard and visualizations must load within 3 seconds of assessment completion
- **NFR-003**: Platform must be accessible via web browsers without requiring software installation
- **NFR-004**: Assessment questions and career recommendations must be culturally appropriate and relevant for Vietnamese students, presented in Vietnamese language only
- **NFR-005**: User interface must be intuitive enough for students aged 15-25 to navigate without training
- **NFR-006**: System must handle at least 500 concurrent users during peak usage periods

### Key Entities

- **User Profile**: Represents a student using the platform, including account credentials (email and hashed password), demographic information (age, education level, field of study), and preferences. Linked to all assessment results and roadmap data.

- **Assessment Response**: Captures user answers for each question within the four quotient modules. Associated with a specific user and assessment session. Includes question ID, selected answer, timestamp, and module type (IQ/EQ/DQ/AQ).

- **Assessment Result**: Aggregated scores and analysis for a complete assessment session. Contains calculated quotient scores, percentile rankings, Ikigai component ratings, timestamp of completion, and links to the user profile.

- **Career Recommendation**: Represents a suggested career path generated from assessment results. Includes career title, alignment score, explanation of fit based on quotients and Ikigai, required skills, market information, and priority ranking.

- **Learning Resource**: Represents recommended courses, books, projects, or communities. Contains resource type, title, provider/platform, description, target quotient or skill, difficulty level, and relevance score to user's goals.

- **Skill Development Priority**: Identifies capabilities the user should develop for their recommended career paths. Contains skill name, importance ranking, current proficiency estimate, target proficiency, and associated learning resources.

- **Progress Snapshot**: Historical record of a user's assessment results at a specific point in time. Enables comparison and tracking of development over multiple assessment sessions.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can complete the full four-quotient assessment in 45 minutes or less
- **SC-002**: 85% of users successfully complete the entire assessment journey from account creation to viewing results in a single session
- **SC-003**: Students receive their personalized results dashboard within 5 seconds of completing the final assessment question
- **SC-004**: Each user receives at least 3 distinct career recommendations with detailed explanations
- **SC-005**: 90% of students report that career recommendations feel relevant and aligned with their self-perception
- **SC-006**: Users can view their complete learning roadmap with at least 5 specific resource recommendations within 10 seconds of viewing results
- **SC-007**: Platform successfully handles 500 concurrent users without performance degradation
- **SC-008**: Students who retake assessments after 90 days can view comparison data showing changes in all four quotients
- **SC-009**: 70% of users who complete the assessment return to explore their personalized roadmap and resources within 7 days
- **SC-010**: Assessment completion rate (users who finish all four modules) exceeds 75% of those who start the first module
- **SC-011**: Students can navigate from account creation to assessment completion without external assistance or documentation
- **SC-012**: Career exploration features provide sufficient detail that 80% of users feel they understand the recommended paths without additional research

### Assumptions

1. **User Base**: Primary users are Vietnamese high school and university students aged 15-25 seeking career guidance
2. **Assessment Methodology**: Questions and scoring algorithms for IQ, EQ, DQ, and AQ are based on validated psychological research and industry best practices
3. **Ikigai Interpretation**: The platform uses a simplified, career-focused interpretation of Ikigai suitable for student audiences rather than the complete philosophical framework
4. **Career Database**: Career recommendations are drawn from a curated database of professions relevant to Vietnamese job market and educational system
5. **Resource Availability**: Recommended courses and resources are accessible to Vietnamese students (Vietnamese language content, cost, platform availability)
6. **Data Privacy**: User assessment data and personal information are treated as confidential and stored securely according to standard privacy practices
7. **Assessment Validity**: The four-quotient assessment provides meaningful career guidance when completed honestly and thoughtfully
8. **Internet Access**: Students have reliable internet access to complete the web-based assessment and explore results
9. **Device Compatibility**: Students primarily access the platform via laptop or desktop browsers, with mobile support as secondary
10. **Update Frequency**: Career market data and resource recommendations are updated quarterly to maintain relevance

### Dependencies

1. **Content Development**: Assessment questions must be developed and validated by educational psychologists or career counselors
2. **Career Database**: Comprehensive career information database must be curated with Vietnamese market context
3. **Learning Resource Partnerships**: Relationships or data feeds from online learning platforms (Coursera, Udemy, etc.) for course recommendations
4. **Chart Visualization Library**: Charting solution for rendering radar charts and Ikigai maps (e.g., Chart.js, D3.js)
5. **Authentication System**: User account management and secure authentication infrastructure
6. **Database Infrastructure**: Persistent storage for user profiles, assessment responses, and historical results
7. **Hosting Environment**: Web hosting platform capable of serving the application to target user volume

### Out of Scope

- Integration with school systems or learning management platforms
- Mobile native applications (iOS/Android apps) - web-responsive interface only
- AI-powered chatbot or virtual career counselor
- Direct job board or employment matching functionality
- Paid certification or credential issuance for completed assessments
- Social features (peer comparison, sharing results, community forums)
- Parent or teacher dashboards for monitoring student progress
- Integration with third-party career assessment tools or standardized tests
- Real-time collaboration or group assessment sessions
- Gamification elements (badges, points, leaderboards)
- Video content or interactive multimedia beyond charts and text
