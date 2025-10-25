"""Create all tables

Revision ID: 001
Revises: 
Create Date: 2025-10-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('education_level', sa.String(length=50), nullable=False),
        sa.Column('field_of_study', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create chatbot_sessions table
    op.create_table('chatbot_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_token', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('current_intent', sa.String(length=50), nullable=True),
        sa.Column('context_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('last_activity', sa.DateTime(), nullable=False),
        sa.Column('assessment_ready', sa.Boolean(), nullable=False),
        sa.Column('results_viewed', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chatbot_sessions_user_id'), 'chatbot_sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_chatbot_sessions_session_token'), 'chatbot_sessions', ['session_token'], unique=True)
    op.create_index(op.f('ix_chatbot_sessions_status'), 'chatbot_sessions', ['status'], unique=False)
    
    # Create chatbot_messages table
    op.create_table('chatbot_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sender', sa.String(length=20), nullable=False),
        sa.Column('message_type', sa.String(length=30), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('intent', sa.String(length=50), nullable=True),
        sa.Column('entities', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['chatbot_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chatbot_messages_session_id'), 'chatbot_messages', ['session_id'], unique=False)
    op.create_index(op.f('ix_chatbot_messages_created_at'), 'chatbot_messages', ['created_at'], unique=False)
    op.create_index(op.f('ix_chatbot_messages_intent'), 'chatbot_messages', ['intent'], unique=False)
    
    # Create assessment_sessions table
    op.create_table('assessment_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chatbot_session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('total_time_minutes', sa.Integer(), nullable=True),
        sa.Column('consistency_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('rushing_detected', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['chatbot_session_id'], ['chatbot_sessions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessment_sessions_user_id'), 'assessment_sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_assessment_sessions_chatbot_session_id'), 'assessment_sessions', ['chatbot_session_id'], unique=False)
    op.create_index(op.f('ix_assessment_sessions_status'), 'assessment_sessions', ['status'], unique=False)
    
    # Create assessment_questions table
    op.create_table('assessment_questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('module', sa.String(length=10), nullable=False),
        sa.Column('facet', sa.String(length=50), nullable=True),
        sa.Column('question_text', sa.String(), nullable=False),
        sa.Column('question_type', sa.String(length=20), nullable=False),
        sa.Column('options', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('correct_answer', sa.String(length=100), nullable=True),
        sa.Column('reverse_scored', sa.Boolean(), nullable=False),
        sa.Column('difficulty', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessment_questions_module'), 'assessment_questions', ['module'], unique=False)
    op.create_index(op.f('ix_assessment_questions_facet'), 'assessment_questions', ['facet'], unique=False)
    op.create_index(op.f('ix_assessment_questions_is_active'), 'assessment_questions', ['is_active'], unique=False)
    
    # Create assessment_responses table
    op.create_table('assessment_responses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('question_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('answer', sa.String(length=500), nullable=False),
        sa.Column('answer_value', sa.Integer(), nullable=True),
        sa.Column('response_time_seconds', sa.Integer(), nullable=True),
        sa.Column('score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('answered_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['assessment_questions.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['assessment_sessions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessment_responses_session_id'), 'assessment_responses', ['session_id'], unique=False)
    op.create_index(op.f('ix_assessment_responses_user_id'), 'assessment_responses', ['user_id'], unique=False)
    op.create_index(op.f('ix_assessment_responses_question_id'), 'assessment_responses', ['question_id'], unique=False)
    
    # Create assessment_results table
    op.create_table('assessment_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chatbot_session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('iq_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('eq_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('dq_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('aq_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('iq_percentile', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('eq_percentile', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('dq_percentile', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('aq_percentile', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('ikigai_love', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('ikigai_good_at', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('ikigai_world_needs', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('ikigai_paid_for', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('strongest_quotient', sa.String(length=10), nullable=False),
        sa.Column('weakest_quotient', sa.String(length=10), nullable=False),
        sa.Column('consistency_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('quality_flags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['chatbot_session_id'], ['chatbot_sessions.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['assessment_sessions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessment_results_user_id'), 'assessment_results', ['user_id'], unique=False)
    op.create_index(op.f('ix_assessment_results_session_id'), 'assessment_results', ['session_id'], unique=False)
    op.create_index(op.f('ix_assessment_results_chatbot_session_id'), 'assessment_results', ['chatbot_session_id'], unique=False)
    
    # Create career_recommendations table
    op.create_table('career_recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('result_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('career_title', sa.String(length=200), nullable=False),
        sa.Column('career_description', sa.String(), nullable=False),
        sa.Column('alignment_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('required_skills', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('market_demand', sa.String(length=50), nullable=False),
        sa.Column('salary_range_min', sa.Integer(), nullable=True),
        sa.Column('salary_range_max', sa.Integer(), nullable=True),
        sa.Column('priority_rank', sa.Integer(), nullable=False),
        sa.Column('explanation', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['result_id'], ['assessment_results.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_career_recommendations_user_id'), 'career_recommendations', ['user_id'], unique=False)
    op.create_index(op.f('ix_career_recommendations_result_id'), 'career_recommendations', ['result_id'], unique=False)
    op.create_index(op.f('ix_career_recommendations_priority_rank'), 'career_recommendations', ['priority_rank'], unique=False)
    
    # Create visualization_data table
    op.create_table('visualization_data',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('result_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chart_type', sa.String(length=30), nullable=False),
        sa.Column('chart_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('facet_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ikigai_intersections', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['result_id'], ['assessment_results.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_visualization_data_user_id'), 'visualization_data', ['user_id'], unique=False)
    op.create_index(op.f('ix_visualization_data_result_id'), 'visualization_data', ['result_id'], unique=False)
    op.create_index(op.f('ix_visualization_data_chart_type'), 'visualization_data', ['chart_type'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_visualization_data_chart_type'), table_name='visualization_data')
    op.drop_index(op.f('ix_visualization_data_result_id'), table_name='visualization_data')
    op.drop_index(op.f('ix_visualization_data_user_id'), table_name='visualization_data')
    op.drop_table('visualization_data')
    op.drop_index(op.f('ix_career_recommendations_priority_rank'), table_name='career_recommendations')
    op.drop_index(op.f('ix_career_recommendations_result_id'), table_name='career_recommendations')
    op.drop_index(op.f('ix_career_recommendations_user_id'), table_name='career_recommendations')
    op.drop_table('career_recommendations')
    op.drop_index(op.f('ix_assessment_results_chatbot_session_id'), table_name='assessment_results')
    op.drop_index(op.f('ix_assessment_results_session_id'), table_name='assessment_results')
    op.drop_index(op.f('ix_assessment_results_user_id'), table_name='assessment_results')
    op.drop_table('assessment_results')
    op.drop_index(op.f('ix_assessment_responses_question_id'), table_name='assessment_responses')
    op.drop_index(op.f('ix_assessment_responses_user_id'), table_name='assessment_responses')
    op.drop_index(op.f('ix_assessment_responses_session_id'), table_name='assessment_responses')
    op.drop_table('assessment_responses')
    op.drop_index(op.f('ix_assessment_questions_is_active'), table_name='assessment_questions')
    op.drop_index(op.f('ix_assessment_questions_facet'), table_name='assessment_questions')
    op.drop_index(op.f('ix_assessment_questions_module'), table_name='assessment_questions')
    op.drop_table('assessment_questions')
    op.drop_index(op.f('ix_assessment_sessions_status'), table_name='assessment_sessions')
    op.drop_index(op.f('ix_assessment_sessions_chatbot_session_id'), table_name='assessment_sessions')
    op.drop_index(op.f('ix_assessment_sessions_user_id'), table_name='assessment_sessions')
    op.drop_table('assessment_sessions')
    op.drop_index(op.f('ix_chatbot_messages_intent'), table_name='chatbot_messages')
    op.drop_index(op.f('ix_chatbot_messages_created_at'), table_name='chatbot_messages')
    op.drop_index(op.f('ix_chatbot_messages_session_id'), table_name='chatbot_messages')
    op.drop_table('chatbot_messages')
    op.drop_index(op.f('ix_chatbot_sessions_status'), table_name='chatbot_sessions')
    op.drop_index(op.f('ix_chatbot_sessions_session_token'), table_name='chatbot_sessions')
    op.drop_index(op.f('ix_chatbot_sessions_user_id'), table_name='chatbot_sessions')
    op.drop_table('chatbot_sessions')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
