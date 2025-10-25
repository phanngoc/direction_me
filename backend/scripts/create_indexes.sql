-- Performance indexes for MyWay Career Assessment System
-- Created: 2024-12-19

-- User lookups
CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_created_at ON users(created_at);

-- Assessment queries
CREATE INDEX IF NOT EXISTS idx_assessment_user_id ON assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_assessment_status ON assessments(status);
CREATE INDEX IF NOT EXISTS idx_assessment_completed_at ON assessments(completed_at);

-- Result queries
CREATE INDEX IF NOT EXISTS idx_assessment_result_assessment_id ON assessment_results(assessment_id);
CREATE INDEX IF NOT EXISTS idx_assessment_result_calculated_at ON assessment_results(calculated_at);

-- Career suggestions
CREATE INDEX IF NOT EXISTS idx_career_suggestion_result_id ON career_suggestions(assessment_result_id);
CREATE INDEX IF NOT EXISTS idx_career_suggestion_rank ON career_suggestions(rank);

-- Progress tracking
CREATE INDEX IF NOT EXISTS idx_progress_tracking_user_id ON progress_tracking(user_id);
CREATE INDEX IF NOT EXISTS idx_progress_tracking_tracked_at ON progress_tracking(tracked_at);

-- Question bank
CREATE INDEX IF NOT EXISTS idx_question_bank_category ON question_bank(category);
CREATE INDEX IF NOT EXISTS idx_question_bank_active ON question_bank(is_active);

-- Career rules
CREATE INDEX IF NOT EXISTS idx_career_rule_active ON career_rules(is_active);