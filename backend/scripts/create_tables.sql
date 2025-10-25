-- MyWay Career Assessment Database Schema
-- Created: 2024-12-19
-- Database: PostgreSQL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    age INTEGER CHECK (age >= 16 AND age <= 25),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Assessments table
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) CHECK (status IN ('in_progress', 'completed', 'abandoned')) NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    total_questions INTEGER NOT NULL DEFAULT 0,
    answered_questions INTEGER NOT NULL DEFAULT 0
);

-- Assessment Results table
CREATE TABLE assessment_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    iq_score DECIMAL(5,2) CHECK (iq_score >= 0 AND iq_score <= 100),
    eq_score DECIMAL(5,2) CHECK (eq_score >= 0 AND eq_score <= 100),
    dq_score DECIMAL(5,2) CHECK (dq_score >= 0 AND dq_score <= 100),
    aq_score DECIMAL(5,2) CHECK (aq_score >= 0 AND aq_score <= 100),
    ikigai_love DECIMAL(5,2) CHECK (ikigai_love >= 0 AND ikigai_love <= 100),
    ikigai_good_at DECIMAL(5,2) CHECK (ikigai_good_at >= 0 AND ikigai_good_at <= 100),
    ikigai_world_needs DECIMAL(5,2) CHECK (ikigai_world_needs >= 0 AND ikigai_world_needs <= 100),
    ikigai_paid_for DECIMAL(5,2) CHECK (ikigai_paid_for >= 0 AND ikigai_paid_for <= 100),
    ikigai_harmonic DECIMAL(5,2) CHECK (ikigai_harmonic >= 0 AND ikigai_harmonic <= 100),
    ikigai_geometric DECIMAL(5,2) CHECK (ikigai_geometric >= 0 AND ikigai_geometric <= 100),
    calculated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Profile Vectors table
CREATE TABLE profile_vectors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_result_id UUID NOT NULL REFERENCES assessment_results(id) ON DELETE CASCADE,
    iq_lr DECIMAL(5,2) CHECK (iq_lr >= 0 AND iq_lr <= 100),
    iq_nr DECIMAL(5,2) CHECK (iq_nr >= 0 AND iq_nr <= 100),
    iq_vr DECIMAL(5,2) CHECK (iq_vr >= 0 AND iq_vr <= 100),
    iq_sr DECIMAL(5,2) CHECK (iq_sr >= 0 AND iq_sr <= 100),
    eq_empathy DECIMAL(5,2) CHECK (eq_empathy >= 0 AND eq_empathy <= 100),
    eq_social DECIMAL(5,2) CHECK (eq_social >= 0 AND eq_social <= 100),
    eq_self_awareness DECIMAL(5,2) CHECK (eq_self_awareness >= 0 AND eq_self_awareness <= 100),
    eq_self_regulation DECIMAL(5,2) CHECK (eq_self_regulation >= 0 AND eq_self_regulation <= 100),
    dq_info_literacy DECIMAL(5,2) CHECK (dq_info_literacy >= 0 AND dq_info_literacy <= 100),
    dq_creativity DECIMAL(5,2) CHECK (dq_creativity >= 0 AND dq_creativity <= 100),
    dq_safety DECIMAL(5,2) CHECK (dq_safety >= 0 AND dq_safety <= 100),
    dq_collaboration DECIMAL(5,2) CHECK (dq_collaboration >= 0 AND dq_collaboration <= 100),
    aq_control DECIMAL(5,2) CHECK (aq_control >= 0 AND aq_control <= 100),
    aq_ownership DECIMAL(5,2) CHECK (aq_ownership >= 0 AND aq_ownership <= 100),
    aq_reach DECIMAL(5,2) CHECK (aq_reach >= 0 AND aq_reach <= 100),
    aq_endurance DECIMAL(5,2) CHECK (aq_endurance >= 0 AND aq_endurance <= 100)
);

-- Career Suggestions table
CREATE TABLE career_suggestions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_result_id UUID NOT NULL REFERENCES assessment_results(id) ON DELETE CASCADE,
    career_name VARCHAR(100) NOT NULL,
    fit_score DECIMAL(5,2) CHECK (fit_score >= 0 AND fit_score <= 100),
    rank INTEGER CHECK (rank >= 1 AND rank <= 8),
    explanation TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Learning Paths table
CREATE TABLE learning_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_result_id UUID NOT NULL REFERENCES assessment_results(id) ON DELETE CASCADE,
    career_name VARCHAR(100) NOT NULL,
    skills JSONB NOT NULL,
    projects JSONB NOT NULL,
    habits JSONB NOT NULL,
    timeline_weeks INTEGER CHECK (timeline_weeks > 0),
    priority VARCHAR(20) CHECK (priority IN ('high', 'medium', 'low')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Progress Tracking table
CREATE TABLE progress_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    previous_assessment_id UUID REFERENCES assessments(id) ON DELETE SET NULL,
    improvement_iq DECIMAL(5,2),
    improvement_eq DECIMAL(5,2),
    improvement_dq DECIMAL(5,2),
    improvement_aq DECIMAL(5,2),
    tracked_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Career Rules table
CREATE TABLE career_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    career_name VARCHAR(100) UNIQUE NOT NULL,
    weights JSONB NOT NULL,
    thresholds JSONB NOT NULL,
    bonus_keys JSONB,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Question Bank table
CREATE TABLE question_bank (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(10) CHECK (category IN ('IQ', 'EQ', 'DQ', 'AQ')),
    facet VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(20) CHECK (question_type IN ('MCQ', 'Likert')),
    difficulty_weight DECIMAL(3,2) CHECK (difficulty_weight > 0),
    reverse_score BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);