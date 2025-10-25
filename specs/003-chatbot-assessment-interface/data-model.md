# Data Model: Chatbot Assessment Interface

**Date**: 2025-10-25  
**Feature**: 003-chatbot-assessment-interface  
**Database**: PostgreSQL 15+ with Redis for session management

## Entity Definitions

### Chatbot Session

**Table**: `chatbot_sessions`  
**Purpose**: Track ongoing conversations between users and chatbot

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique session identifier |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| session_token | VARCHAR(255) | UNIQUE, NOT NULL | Session token for Redis |
| status | VARCHAR(20) | NOT NULL | active, completed, abandoned |
| current_intent | VARCHAR(50) | NULL | Current conversation intent |
| context_data | JSONB | NULL | Conversation context and state |
| started_at | TIMESTAMP | NOT NULL | Session start time |
| last_activity | TIMESTAMP | NOT NULL | Last interaction time |
| assessment_ready | BOOLEAN | DEFAULT FALSE | Ready to start assessment |
| results_viewed | BOOLEAN | DEFAULT FALSE | User has viewed results |

**Indexes**:
- `idx_chatbot_sessions_user_id` on `user_id`
- `idx_chatbot_sessions_token` on `session_token`
- `idx_chatbot_sessions_status` on `status`

### Chatbot Messages

**Table**: `chatbot_messages`  
**Purpose**: Store conversation history between user and chatbot

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique message identifier |
| session_id | UUID | FOREIGN KEY → chatbot_sessions.id | Associated session |
| sender | VARCHAR(20) | NOT NULL | user, bot, system |
| message_type | VARCHAR(30) | NOT NULL | text, quick_reply, assessment_redirect, results |
| content | TEXT | NOT NULL | Message content in Vietnamese |
| intent | VARCHAR(50) | NULL | Detected user intent |
| entities | JSONB | NULL | Extracted entities |
| confidence | DECIMAL(3,2) | NULL | Intent confidence score |
| created_at | TIMESTAMP | NOT NULL | Message timestamp |

**Indexes**:
- `idx_chatbot_messages_session_id` on `session_id`
- `idx_chatbot_messages_created_at` on `created_at`
- `idx_chatbot_messages_intent` on `intent`

### Assessment Session

**Table**: `assessment_sessions`  
**Purpose**: Track individual assessment attempts

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique session identifier |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| chatbot_session_id | UUID | FOREIGN KEY → chatbot_sessions.id | Associated chatbot session |
| status | VARCHAR(20) | NOT NULL | in_progress, completed, abandoned |
| started_at | TIMESTAMP | NOT NULL | Session start time |
| completed_at | TIMESTAMP | NULL | Session completion time |
| total_time_minutes | INTEGER | NULL | Total assessment time |
| consistency_score | DECIMAL(3,2) | NULL | Response consistency score |
| rushing_detected | BOOLEAN | DEFAULT FALSE | Rushed responses detected |

**Indexes**:
- `idx_assessment_sessions_user_id` on `user_id`
- `idx_assessment_sessions_chatbot_session_id` on `chatbot_session_id`
- `idx_assessment_sessions_status` on `status`

### Assessment Questions

**Table**: `assessment_questions`  
**Purpose**: Store all assessment questions by module

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique question identifier |
| module | VARCHAR(10) | NOT NULL | IQ, EQ, DQ, AQ |
| facet | VARCHAR(50) | NULL | Specific facet within module |
| question_text | TEXT | NOT NULL | Question content in Vietnamese |
| question_type | VARCHAR(20) | NOT NULL | multiple_choice, likert_scale |
| options | JSONB | NULL | Answer options for multiple choice |
| correct_answer | VARCHAR(100) | NULL | Correct answer (IQ only) |
| reverse_scored | BOOLEAN | DEFAULT FALSE | Reverse scoring flag (EQ/DQ/AQ) |
| difficulty | INTEGER | DEFAULT 1 | Difficulty level (1-3) |
| weight | DECIMAL(3,2) | DEFAULT 1.0 | Question weight in scoring |
| is_active | BOOLEAN | DEFAULT TRUE | Question availability |

**Indexes**:
- `idx_assessment_questions_module` on `module`
- `idx_assessment_questions_facet` on `facet`
- `idx_assessment_questions_active` on `is_active`

### Assessment Responses

**Table**: `assessment_responses`  
**Purpose**: Store user answers to assessment questions

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique response identifier |
| session_id | UUID | FOREIGN KEY → assessment_sessions.id | Associated session |
| question_id | UUID | FOREIGN KEY → assessment_questions.id | Associated question |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| answer | VARCHAR(500) | NOT NULL | User's answer |
| answer_value | INTEGER | NULL | Numeric value for scoring |
| response_time_seconds | INTEGER | NULL | Time taken to answer |
| score | DECIMAL(5,2) | NULL | Calculated score for this response |
| answered_at | TIMESTAMP | NOT NULL | Response timestamp |

**Indexes**:
- `idx_assessment_responses_session_id` on `session_id`
- `idx_assessment_responses_user_id` on `user_id`
- `idx_assessment_responses_question_id` on `question_id`

### Assessment Results

**Table**: `assessment_results`  
**Purpose**: Store calculated assessment scores and analysis

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique result identifier |
| session_id | UUID | FOREIGN KEY → assessment_sessions.id | Associated session |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| chatbot_session_id | UUID | FOREIGN KEY → chatbot_sessions.id | Associated chatbot session |
| iq_score | DECIMAL(5,2) | NOT NULL | IQ quotient score |
| eq_score | DECIMAL(5,2) | NOT NULL | EQ quotient score |
| dq_score | DECIMAL(5,2) | NOT NULL | DQ quotient score |
| aq_score | DECIMAL(5,2) | NOT NULL | AQ quotient score |
| iq_percentile | DECIMAL(5,2) | NOT NULL | IQ percentile ranking |
| eq_percentile | DECIMAL(5,2) | NOT NULL | EQ percentile ranking |
| dq_percentile | DECIMAL(5,2) | NOT NULL | DQ percentile ranking |
| aq_percentile | DECIMAL(5,2) | NOT NULL | AQ percentile ranking |
| ikigai_love | DECIMAL(5,2) | NOT NULL | What you love score |
| ikigai_good_at | DECIMAL(5,2) | NOT NULL | What you're good at score |
| ikigai_world_needs | DECIMAL(5,2) | NOT NULL | What world needs score |
| ikigai_paid_for | DECIMAL(5,2) | NOT NULL | What you can be paid for score |
| strongest_quotient | VARCHAR(10) | NOT NULL | Highest scoring quotient |
| weakest_quotient | VARCHAR(10) | NOT NULL | Lowest scoring quotient |
| consistency_score | DECIMAL(3,2) | NULL | Overall response consistency |
| quality_flags | JSONB | NULL | Quality assessment flags |
| created_at | TIMESTAMP | NOT NULL | Result calculation time |

**Indexes**:
- `idx_assessment_results_user_id` on `user_id`
- `idx_assessment_results_session_id` on `session_id`
- `idx_assessment_results_chatbot_session_id` on `chatbot_session_id`

### Career Recommendations

**Table**: `career_recommendations`  
**Purpose**: Store career path suggestions for users

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique recommendation identifier |
| result_id | UUID | FOREIGN KEY → assessment_results.id | Associated result |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| career_title | VARCHAR(200) | NOT NULL | Career name in Vietnamese |
| career_description | TEXT | NOT NULL | Career description |
| alignment_score | DECIMAL(5,2) | NOT NULL | How well it matches user profile |
| required_skills | JSONB | NOT NULL | Required skills array |
| market_demand | VARCHAR(50) | NOT NULL | High, medium, low |
| salary_range_min | INTEGER | NULL | Minimum salary in VND |
| salary_range_max | INTEGER | NULL | Maximum salary in VND |
| priority_rank | INTEGER | NOT NULL | Recommendation priority (1-3) |
| explanation | TEXT | NOT NULL | Why this career fits the user |

**Indexes**:
- `idx_career_recommendations_user_id` on `user_id`
- `idx_career_recommendations_result_id` on `result_id`
- `idx_career_recommendations_priority` on `priority_rank`

### Visualization Data

**Table**: `visualization_data`  
**Purpose**: Store processed data for charts and visualizations

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique visualization identifier |
| result_id | UUID | FOREIGN KEY → assessment_results.id | Associated result |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| chart_type | VARCHAR(30) | NOT NULL | radar, facet_bars, ikigai_map |
| chart_data | JSONB | NOT NULL | Chart configuration and data |
| facet_scores | JSONB | NULL | Detailed facet scores |
| ikigai_intersections | JSONB | NULL | Ikigai intersection data |
| created_at | TIMESTAMP | NOT NULL | Data generation time |

**Indexes**:
- `idx_visualization_data_user_id` on `user_id`
- `idx_visualization_data_result_id` on `result_id`
- `idx_visualization_data_chart_type` on `chart_type`

## Relationships

### Primary Relationships

1. **User → Chatbot Sessions**: One-to-Many
   - A user can have multiple chatbot sessions
   - Each session belongs to one user

2. **Chatbot Session → Assessment Session**: One-to-One
   - A chatbot session can initiate one assessment session
   - Each assessment session belongs to one chatbot session

3. **Assessment Session → Responses**: One-to-Many
   - A session contains multiple responses
   - Each response belongs to one session

4. **Assessment Session → Results**: One-to-One
   - A completed session has one result
   - Each result belongs to one session

5. **Assessment Result → Career Recommendations**: One-to-Many
   - A result generates multiple career recommendations
   - Each recommendation belongs to one result

6. **Assessment Result → Visualization Data**: One-to-Many
   - A result can have multiple visualization data entries
   - Each visualization data belongs to one result

### Data Integrity Rules

1. **Assessment Completion**: Results can only be created when all four modules are completed
2. **Response Validation**: Responses must match the question type and options
3. **Score Calculation**: All scores must be between 0 and 100
4. **Career Alignment**: Career recommendations must have alignment_score > 0
5. **Session Continuity**: Assessment sessions must be linked to chatbot sessions
6. **Consistency Checking**: Response consistency must be calculated and stored

## State Transitions

### Chatbot Session States

```
created → active → assessment_ready → completed
    ↓         ↓           ↓
abandoned  abandoned  abandoned
```

### Assessment Session States

```
created → in_progress → completed
    ↓         ↓
abandoned  abandoned
```

### Message Flow States

```
user_message → intent_detection → bot_response
     ↓              ↓
assessment_redirect → results_display
```

## Performance Considerations

### Query Optimization

1. **Chatbot Dashboard**: Optimized query to fetch user's active sessions and recent messages
2. **Assessment Progress**: Indexed queries for session status and progress
3. **Results Display**: Fast queries for results and visualizations
4. **Conversation History**: Efficient pagination for message history

### Data Archival

1. **Old Sessions**: Archive chatbot sessions older than 6 months
2. **Inactive Users**: Archive users inactive for 1 year
3. **Historical Results**: Keep results for progress tracking
4. **Message History**: Archive messages older than 1 year

## Security Considerations

### Data Protection

1. **Session Security**: Secure session token generation and validation
2. **Conversation Privacy**: Encrypt sensitive conversation data
3. **Assessment Data**: Secure storage of assessment responses
4. **API Security**: Rate limiting and input validation

### Privacy Compliance

1. **Data Retention**: 1-year retention for conversation data
2. **User Rights**: Allow users to delete their data
3. **Anonymization**: Option to anonymize data for research
4. **Consent**: Track user consent for data processing

## Redis Session Management

### Session Data Structure

```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "current_intent": "greeting",
  "context": {
    "last_message": "Hello",
    "assessment_ready": false,
    "current_module": null
  },
  "expires_at": "timestamp"
}
```

### Session Operations

1. **Create Session**: Initialize new chatbot session
2. **Update Context**: Modify conversation context
3. **Get Session**: Retrieve session data
4. **Delete Session**: Clean up expired sessions
5. **Extend Session**: Update expiration time

## Migration Strategy

### Initial Setup

1. Create all tables with proper constraints
2. Set up indexes for performance
3. Insert initial assessment questions
4. Populate career database
5. Configure Redis for session management

### Future Enhancements

1. **Multi-language Support**: Add language fields to questions and conversations
2. **Advanced Analytics**: Add analytics tables for usage tracking
3. **Social Features**: Add user interaction tables
4. **Integration APIs**: Add external service integration tables
