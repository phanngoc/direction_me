# Data Model: MyWay Career Assessment System

**Date**: 2024-12-19  
**Feature**: 001-career-assessment  
**Database**: PostgreSQL

## Core Entities

### User
**Purpose**: Store user account information and profile data

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password (min 8 chars) |
| full_name | VARCHAR(255) | NOT NULL | User's full name |
| age | INTEGER | CHECK (age >= 16 AND age <= 25) | User age (16-25) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

### Assessment
**Purpose**: Store assessment sessions and metadata

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique assessment identifier |
| user_id | UUID | FOREIGN KEY → User.id | Owner of this assessment |
| status | VARCHAR(20) | CHECK (status IN ('in_progress', 'completed', 'abandoned')) | Assessment status |
| started_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When assessment started |
| completed_at | TIMESTAMP | NULL | When assessment completed |
| total_questions | INTEGER | NOT NULL, DEFAULT 0 | Total questions in assessment |
| answered_questions | INTEGER | NOT NULL, DEFAULT 0 | Questions answered so far |

### AssessmentResult
**Purpose**: Store calculated scores and analysis results

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique result identifier |
| assessment_id | UUID | FOREIGN KEY → Assessment.id | Associated assessment |
| iq_score | DECIMAL(5,2) | CHECK (iq_score >= 0 AND iq_score <= 100) | IQ score (0-100) |
| eq_score | DECIMAL(5,2) | CHECK (eq_score >= 0 AND eq_score <= 100) | EQ score (0-100) |
| dq_score | DECIMAL(5,2) | CHECK (dq_score >= 0 AND dq_score <= 100) | DQ score (0-100) |
| aq_score | DECIMAL(5,2) | CHECK (aq_score >= 0 AND aq_score <= 100) | AQ score (0-100) |
| ikigai_love | DECIMAL(5,2) | CHECK (ikigai_love >= 0 AND ikigai_love <= 100) | Ikigai Love axis |
| ikigai_good_at | DECIMAL(5,2) | CHECK (ikigai_good_at >= 0 AND ikigai_good_at <= 100) | Ikigai Good at axis |
| ikigai_world_needs | DECIMAL(5,2) | CHECK (ikigai_world_needs >= 0 AND ikigai_world_needs <= 100) | Ikigai World needs axis |
| ikigai_paid_for | DECIMAL(5,2) | CHECK (ikigai_paid_for >= 0 AND ikigai_paid_for <= 100) | Ikigai Paid for axis |
| ikigai_harmonic | DECIMAL(5,2) | CHECK (ikigai_harmonic >= 0 AND ikigai_harmonic <= 100) | Ikigai harmonic mean |
| ikigai_geometric | DECIMAL(5,2) | CHECK (ikigai_geometric >= 0 AND ikigai_geometric <= 100) | Ikigai geometric mean |
| calculated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When scores were calculated |

### ProfileVector
**Purpose**: Store 16-dimensional profile vector for career mapping

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique vector identifier |
| assessment_result_id | UUID | FOREIGN KEY → AssessmentResult.id | Associated result |
| iq_lr | DECIMAL(5,2) | CHECK (iq_lr >= 0 AND iq_lr <= 100) | IQ Logical Reasoning |
| iq_nr | DECIMAL(5,2) | CHECK (iq_nr >= 0 AND iq_nr <= 100) | IQ Numerical Reasoning |
| iq_vr | DECIMAL(5,2) | CHECK (iq_vr >= 0 AND iq_vr <= 100) | IQ Verbal Reasoning |
| iq_sr | DECIMAL(5,2) | CHECK (iq_sr >= 0 AND iq_sr <= 100) | IQ Spatial Reasoning |
| eq_empathy | DECIMAL(5,2) | CHECK (eq_empathy >= 0 AND eq_empathy <= 100) | EQ Empathy |
| eq_social | DECIMAL(5,2) | CHECK (eq_social >= 0 AND eq_social <= 100) | EQ Social Skills |
| eq_self_awareness | DECIMAL(5,2) | CHECK (eq_self_awareness >= 0 AND eq_self_awareness <= 100) | EQ Self-Awareness |
| eq_self_regulation | DECIMAL(5,2) | CHECK (eq_self_regulation >= 0 AND eq_self_regulation <= 100) | EQ Self-Regulation |
| dq_info_literacy | DECIMAL(5,2) | CHECK (dq_info_literacy >= 0 AND dq_info_literacy <= 100) | DQ Information Literacy |
| dq_creativity | DECIMAL(5,2) | CHECK (dq_creativity >= 0 AND dq_creativity <= 100) | DQ Creativity |
| dq_safety | DECIMAL(5,2) | CHECK (dq_safety >= 0 AND dq_safety <= 100) | DQ Safety |
| dq_collaboration | DECIMAL(5,2) | CHECK (dq_collaboration >= 0 AND dq_collaboration <= 100) | DQ Collaboration |
| aq_control | DECIMAL(5,2) | CHECK (aq_control >= 0 AND aq_control <= 100) | AQ Control |
| aq_ownership | DECIMAL(5,2) | CHECK (aq_ownership >= 0 AND aq_ownership <= 100) | AQ Ownership |
| aq_reach | DECIMAL(5,2) | CHECK (aq_reach >= 0 AND aq_reach <= 100) | AQ Reach |
| aq_endurance | DECIMAL(5,2) | CHECK (aq_endurance >= 0 AND aq_endurance <= 100) | AQ Endurance |

### CareerSuggestion
**Purpose**: Store career recommendations and fit scores

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique suggestion identifier |
| assessment_result_id | UUID | FOREIGN KEY → AssessmentResult.id | Associated result |
| career_name | VARCHAR(100) | NOT NULL | Career name (e.g., "Software Engineer") |
| fit_score | DECIMAL(5,2) | CHECK (fit_score >= 0 AND fit_score <= 100) | Career fit score (0-100) |
| rank | INTEGER | CHECK (rank >= 1 AND rank <= 8) | Ranking position (1-8) |
| explanation | TEXT | NULL | AI explanation for recommendation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When suggestion was generated |

### LearningPath
**Purpose**: Store personalized learning recommendations

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique path identifier |
| assessment_result_id | UUID | FOREIGN KEY → AssessmentResult.id | Associated result |
| career_name | VARCHAR(100) | NOT NULL | Target career for this path |
| skills | JSONB | NOT NULL | Array of recommended skills |
| projects | JSONB | NOT NULL | Array of recommended projects |
| habits | JSONB | NOT NULL | Array of recommended habits |
| timeline_weeks | INTEGER | CHECK (timeline_weeks > 0) | Recommended timeline in weeks |
| priority | VARCHAR(20) | CHECK (priority IN ('high', 'medium', 'low')) | Learning priority |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When path was generated |

### ProgressTracking
**Purpose**: Track user progress over time

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique tracking identifier |
| user_id | UUID | FOREIGN KEY → User.id | User being tracked |
| assessment_id | UUID | FOREIGN KEY → Assessment.id | Latest assessment |
| previous_assessment_id | UUID | FOREIGN KEY → Assessment.id | Previous assessment for comparison |
| improvement_iq | DECIMAL(5,2) | NULL | IQ improvement from previous |
| improvement_eq | DECIMAL(5,2) | NULL | EQ improvement from previous |
| improvement_dq | DECIMAL(5,2) | NULL | DQ improvement from previous |
| improvement_aq | DECIMAL(5,2) | NULL | AQ improvement from previous |
| tracked_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When tracking was recorded |

## Configuration Tables

### CareerRule
**Purpose**: Store career mapping rules and weights

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique rule identifier |
| career_name | VARCHAR(100) | UNIQUE, NOT NULL | Career name |
| weights | JSONB | NOT NULL | Career weights for each facet |
| thresholds | JSONB | NOT NULL | Minimum thresholds for each facet |
| bonus_keys | JSONB | NULL | Facets that get bonus points |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether rule is active |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When rule was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When rule was last updated |

### QuestionBank
**Purpose**: Store assessment questions and metadata

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique question identifier |
| category | VARCHAR(10) | CHECK (category IN ('IQ', 'EQ', 'DQ', 'AQ')) | Question category |
| facet | VARCHAR(50) | NOT NULL | Specific facet (e.g., 'LR', 'Empathy') |
| question_text | TEXT | NOT NULL | Question text |
| question_type | VARCHAR(20) | CHECK (question_type IN ('MCQ', 'Likert')) | Question type |
| difficulty_weight | DECIMAL(3,2) | CHECK (difficulty_weight > 0) | Difficulty weight for IQ questions |
| reverse_score | BOOLEAN | NOT NULL, DEFAULT FALSE | Whether to reverse score for Likert |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether question is active |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When question was created |

## Relationships

### Primary Relationships
- User → Assessment (1:N)
- Assessment → AssessmentResult (1:1)
- AssessmentResult → ProfileVector (1:1)
- AssessmentResult → CareerSuggestion (1:N)
- AssessmentResult → LearningPath (1:N)
- User → ProgressTracking (1:N)

### Foreign Key Constraints
- All foreign keys have CASCADE DELETE
- AssessmentResult requires completed Assessment
- ProfileVector requires AssessmentResult
- CareerSuggestion requires AssessmentResult
- LearningPath requires AssessmentResult

## Indexes

### Performance Indexes
```sql
-- User lookups
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_created_at ON users(created_at);

-- Assessment queries
CREATE INDEX idx_assessment_user_id ON assessments(user_id);
CREATE INDEX idx_assessment_status ON assessments(status);
CREATE INDEX idx_assessment_completed_at ON assessments(completed_at);

-- Result queries
CREATE INDEX idx_assessment_result_assessment_id ON assessment_results(assessment_id);
CREATE INDEX idx_assessment_result_calculated_at ON assessment_results(calculated_at);

-- Career suggestions
CREATE INDEX idx_career_suggestion_result_id ON career_suggestions(assessment_result_id);
CREATE INDEX idx_career_suggestion_rank ON career_suggestions(rank);

-- Progress tracking
CREATE INDEX idx_progress_tracking_user_id ON progress_tracking(user_id);
CREATE INDEX idx_progress_tracking_tracked_at ON progress_tracking(tracked_at);
```

## Data Retention Policy

### Automatic Cleanup
- Assessment data older than 2 years: Soft delete (mark as archived)
- User accounts inactive for 1 year: Send retention email
- Backup data: Daily backups retained for 30 days

### GDPR Compliance
- User data export: JSON format with all user data
- User data deletion: Cascade delete all associated data
- Data anonymization: Remove PII while keeping aggregate statistics