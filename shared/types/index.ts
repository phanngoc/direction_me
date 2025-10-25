// User types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  age: number;
  education_level: string;
  field_of_study?: string;
  created_at: string;
  updated_at: string;
}

// Chatbot types
export interface ChatbotSession {
  id: string;
  user_id: string;
  session_token: string;
  status: 'active' | 'completed' | 'abandoned';
  current_intent?: string;
  context_data?: Record<string, any>;
  started_at: string;
  last_activity: string;
  assessment_ready: boolean;
  results_viewed: boolean;
}

export interface ChatbotMessage {
  id: string;
  session_id: string;
  sender: 'user' | 'bot' | 'system';
  message_type: 'text' | 'quick_reply' | 'assessment_redirect' | 'results';
  content: string;
  intent?: string;
  entities?: Record<string, any>;
  confidence?: number;
  created_at: string;
}

export interface ChatbotResponse {
  message: string;
  message_type: 'text' | 'quick_reply' | 'assessment_redirect' | 'results';
  quick_replies?: string[];
  intent?: string;
  entities?: Record<string, any>;
  confidence?: number;
}

// Assessment types
export interface AssessmentSession {
  id: string;
  user_id: string;
  chatbot_session_id: string;
  status: 'in_progress' | 'completed' | 'abandoned';
  started_at: string;
  completed_at?: string;
  total_time_minutes?: number;
  consistency_score?: number;
  rushing_detected: boolean;
}

export interface AssessmentQuestion {
  id: string;
  module: 'IQ' | 'EQ' | 'DQ' | 'AQ';
  facet?: string;
  question_text: string;
  question_type: 'multiple_choice' | 'likert_scale';
  options?: string[];
  correct_answer?: string;
  reverse_scored: boolean;
  difficulty: number;
  weight: number;
  is_active: boolean;
}

export interface AssessmentResponse {
  id: string;
  session_id: string;
  question_id: string;
  user_id: string;
  answer: string;
  answer_value?: number;
  response_time_seconds?: number;
  score?: number;
  answered_at: string;
}

// Results types
export interface AssessmentResult {
  id: string;
  session_id: string;
  user_id: string;
  chatbot_session_id: string;
  iq_score: number;
  eq_score: number;
  dq_score: number;
  aq_score: number;
  iq_percentile: number;
  eq_percentile: number;
  dq_percentile: number;
  aq_percentile: number;
  ikigai_love: number;
  ikigai_good_at: number;
  ikigai_world_needs: number;
  ikigai_paid_for: number;
  strongest_quotient: string;
  weakest_quotient: string;
  consistency_score?: number;
  quality_flags?: Record<string, any>;
  created_at: string;
}

export interface CareerRecommendation {
  id: string;
  result_id: string;
  user_id: string;
  career_title: string;
  career_description: string;
  alignment_score: number;
  required_skills: string[];
  market_demand: 'high' | 'medium' | 'low';
  salary_range_min?: number;
  salary_range_max?: number;
  priority_rank: number;
  explanation: string;
}

export interface VisualizationData {
  id: string;
  result_id: string;
  user_id: string;
  chart_type: 'radar' | 'facet_bars' | 'ikigai_map';
  chart_data: Record<string, any>;
  facet_scores?: Record<string, any>;
  ikigai_intersections?: Record<string, any>;
  created_at: string;
}

// API types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
  has_prev: boolean;
}

// WebSocket types
export interface WebSocketMessage {
  type: string;
  data: Record<string, any>;
  session_id: string;
}

export interface WebSocketResponse {
  type: string;
  data: Record<string, any>;
  timestamp: string;
}
