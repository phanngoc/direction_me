# Data Model: MyWay Career Assessment Platform

**Date**: 2025-10-25  
**Feature**: 001-career-assessment-platform  
**Database**: PostgreSQL 15+

## Entity Definitions

### User Profile

**Table**: `users`  
**Purpose**: Store user account information and preferences

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| first_name | VARCHAR(100) | NOT NULL | User's first name |
| last_name | VARCHAR(100) | NOT NULL | User's last name |
| age | INTEGER | CHECK (age >= 15 AND age <= 25) | User age |
| education_level | VARCHAR(50) | NOT NULL | High school, university, etc. |
| field_of_study | VARCHAR(100) | NULL | Current field of study |
| created_at | TIMESTAMP | NOT NULL | Account creation time |
| updated_at | TIMESTAMP | NOT NULL | Last profile update |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |

**Indexes**:
- `idx_users_email` on `email`
- `idx_users_created_at` on `created_at`

### Assessment Session

**Table**: `assessment_sessions`  
**Purpose**: Track individual assessment attempts

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique session identifier |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| status | VARCHAR(20) | NOT NULL | in_progress, completed, abandoned |
| started_at | TIMESTAMP | NOT NULL | Session start time |
| completed_at | TIMESTAMP | NULL | Session completion time |
| total_time_minutes | INTEGER | NULL | Total assessment time |

**Indexes**:
- `idx_assessment_sessions_user_id` on `user_id`
- `idx_assessment_sessions_status` on `status`

### Assessment Questions

**Table**: `assessment_questions`  
**Purpose**: Store all assessment questions by module

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique question identifier |
| module | VARCHAR(10) | NOT NULL | IQ, EQ, DQ, AQ |
| question_text | TEXT | NOT NULL | Question content in Vietnamese |
| question_type | VARCHAR(20) | NOT NULL | multiple_choice, scale, scenario |
| options | JSONB | NULL | Answer options for multiple choice |
| correct_answer | VARCHAR(100) | NULL | Correct answer (if applicable) |
| weight | DECIMAL(3,2) | DEFAULT 1.0 | Question weight in scoring |
| is_active | BOOLEAN | DEFAULT TRUE | Question availability |

**Indexes**:
- `idx_assessment_questions_module` on `module`
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
| created_at | TIMESTAMP | NOT NULL | Result calculation time |

**Indexes**:
- `idx_assessment_results_user_id` on `user_id`
- `idx_assessment_results_session_id` on `session_id`

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

### Learning Resources

**Table**: `learning_resources`  
**Purpose**: Store recommended learning materials

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique resource identifier |
| title | VARCHAR(300) | NOT NULL | Resource title |
| description | TEXT | NOT NULL | Resource description |
| resource_type | VARCHAR(50) | NOT NULL | course, book, project, community |
| platform | VARCHAR(100) | NULL | Coursera, Udemy, etc. |
| url | VARCHAR(500) | NULL | Resource URL |
| target_quotient | VARCHAR(10) | NULL | IQ, EQ, DQ, AQ |
| skill_tags | JSONB | NULL | Associated skills array |
| difficulty_level | VARCHAR(20) | NOT NULL | beginner, intermediate, advanced |
| cost | DECIMAL(10,2) | NULL | Resource cost in VND |
| is_free | BOOLEAN | DEFAULT FALSE | Free resource flag |
| is_active | BOOLEAN | DEFAULT TRUE | Resource availability |

**Indexes**:
- `idx_learning_resources_type` on `resource_type`
- `idx_learning_resources_target_quotient` on `target_quotient`
- `idx_learning_resources_active` on `is_active`

### User Learning Roadmap

**Table**: `user_learning_roadmaps`  
**Purpose**: Personalized learning paths for users

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique roadmap identifier |
| user_id | UUID | FOREIGN KEY → users.id | Associated user |
| result_id | UUID | FOREIGN KEY → assessment_results.id | Associated result |
| resource_id | UUID | FOREIGN KEY → learning_resources.id | Associated resource |
| priority_rank | INTEGER | NOT NULL | Learning priority (1-10) |
| skill_gap | DECIMAL(5,2) | NOT NULL | Current vs target skill level |
| estimated_hours | INTEGER | NULL | Estimated completion time |
| is_completed | BOOLEAN | DEFAULT FALSE | Completion status |
| started_at | TIMESTAMP | NULL | When user started this resource |
| completed_at | TIMESTAMP | NULL | When user completed this resource |

**Indexes**:
- `idx_user_learning_roadmaps_user_id` on `user_id`
- `idx_user_learning_roadmaps_priority` on `priority_rank`

## Relationships

### Primary Relationships

1. **User → Assessment Sessions**: One-to-Many
   - A user can have multiple assessment sessions
   - Each session belongs to one user

2. **Assessment Session → Responses**: One-to-Many
   - A session contains multiple responses
   - Each response belongs to one session

3. **Assessment Session → Results**: One-to-One
   - A completed session has one result
   - Each result belongs to one session

4. **Assessment Result → Career Recommendations**: One-to-Many
   - A result generates multiple career recommendations
   - Each recommendation belongs to one result

5. **User → Learning Roadmap**: One-to-Many
   - A user has multiple learning resources in their roadmap
   - Each roadmap item belongs to one user

### Data Integrity Rules

1. **Assessment Completion**: Results can only be created when all four modules are completed
2. **Response Validation**: Responses must match the question type and options
3. **Score Calculation**: All scores must be between 0 and 100
4. **Career Alignment**: Career recommendations must have alignment_score > 0
5. **Resource Availability**: Only active resources can be added to roadmaps

## State Transitions

### Assessment Session States

```
created → in_progress → completed
    ↓         ↓
abandoned  abandoned
```

### User Learning Roadmap States

```
recommended → started → completed
     ↓           ↓
  skipped    abandoned
```

## Performance Considerations

### Query Optimization

1. **User Dashboard**: Optimized query to fetch user's latest results and recommendations
2. **Assessment Progress**: Indexed queries for session status and progress
3. **Career Search**: Full-text search on career titles and descriptions
4. **Resource Filtering**: Efficient filtering by type, difficulty, and target quotient

### Data Archival

1. **Old Sessions**: Archive sessions older than 2 years
2. **Inactive Users**: Archive users inactive for 1 year
3. **Historical Results**: Keep results for progress tracking

## Security Considerations

### Data Protection

1. **Password Security**: Bcrypt hashing with salt rounds = 12
2. **Personal Data**: Encrypt sensitive personal information
3. **Assessment Data**: Secure storage of assessment responses
4. **API Security**: Rate limiting and input validation

### Privacy Compliance

1. **Data Retention**: 2-year retention for assessment data
2. **User Rights**: Allow users to delete their data
3. **Anonymization**: Option to anonymize data for research
4. **Consent**: Track user consent for data processing

## Migration Strategy

### Initial Setup

1. Create all tables with proper constraints
2. Set up indexes for performance
3. Insert initial assessment questions
4. Populate career database
5. Add learning resources

### Future Enhancements

1. **Multi-language Support**: Add language fields to questions and careers
2. **Advanced Analytics**: Add analytics tables for usage tracking
3. **Social Features**: Add user interaction tables
4. **Integration APIs**: Add external service integration tables
