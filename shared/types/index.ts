/**
 * Shared TypeScript types for MyWay Career Assessment System
 */

// User types
export interface User {
  id: string;
  email: string;
  full_name: string;
  age: number;
  created_at: string;
  updated_at: string;
}

export interface CreateUserRequest {
  email: string;
  password: string;
  full_name: string;
  age: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

// Assessment types
export interface Assessment {
  id: string;
  user_id: string;
  status: 'in_progress' | 'completed' | 'abandoned';
  started_at: string;
  completed_at?: string;
  total_questions: number;
  answered_questions: number;
}

export interface CreateAssessmentRequest {
  user_id: string;
}

// Question types
export interface Question {
  id: string;
  category: 'IQ' | 'EQ' | 'DQ' | 'AQ';
  facet: string;
  question_text: string;
  question_type: 'MCQ' | 'Likert';
  options?: string[];
  difficulty_weight?: number;
  reverse_score: boolean;
}

export interface Answer {
  question_id: string;
  answer_value: number;
  answer_text?: string;
}

export interface SubmitAnswersRequest {
  answers: Answer[];
}

// Assessment Result types
export interface AssessmentResult {
  id: string;
  assessment_id: string;
  iq_score: number;
  eq_score: number;
  dq_score: number;
  aq_score: number;
  ikigai_love: number;
  ikigai_good_at: number;
  ikigai_world_needs: number;
  ikigai_paid_for: number;
  ikigai_harmonic: number;
  ikigai_geometric: number;
  calculated_at: string;
}

// Profile Vector types
export interface ProfileVector {
  id: string;
  assessment_result_id: string;
  iq_lr: number;
  iq_nr: number;
  iq_vr: number;
  iq_sr: number;
  eq_empathy: number;
  eq_social: number;
  eq_self_awareness: number;
  eq_self_regulation: number;
  dq_info_literacy: number;
  dq_creativity: number;
  dq_safety: number;
  dq_collaboration: number;
  aq_control: number;
  aq_ownership: number;
  aq_reach: number;
  aq_endurance: number;
}

// Career types
export interface CareerSuggestion {
  id: string;
  career_name: string;
  fit_score: number;
  rank: number;
  explanation?: string;
}

export interface CareerRule {
  id: string;
  career_name: string;
  weights: Record<string, number>;
  thresholds: Record<string, number>;
  bonus_keys?: string[];
  is_active: boolean;
}

// Learning Path types
export interface LearningPath {
  id: string;
  career_name: string;
  skills: string[];
  projects: string[];
  habits: string[];
  timeline_weeks: number;
  priority: 'high' | 'medium' | 'low';
}

// Progress Tracking types
export interface ProgressTracking {
  id: string;
  user_id: string;
  assessment_id: string;
  previous_assessment_id?: string;
  improvement_iq?: number;
  improvement_eq?: number;
  improvement_dq?: number;
  improvement_aq?: number;
  tracked_at: string;
}

// API Response types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Error types
export interface ApiError {
  error: string;
  message: string;
  details?: string;
}

// Chart data types
export interface RadarChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: string;
    borderColor: string;
    borderWidth: number;
  }[];
}

export interface IkigaiChartData {
  love: number;
  good_at: number;
  world_needs: number;
  paid_for: number;
}

// Constants
export const ASSESSMENT_CATEGORIES = ['IQ', 'EQ', 'DQ', 'AQ'] as const;
export const QUESTION_TYPES = ['MCQ', 'Likert'] as const;
export const ASSESSMENT_STATUS = ['in_progress', 'completed', 'abandoned'] as const;
export const LEARNING_PRIORITIES = ['high', 'medium', 'low'] as const;

// Facet mappings
export const IQ_FACETS = ['iq_lr', 'iq_nr', 'iq_vr', 'iq_sr'] as const;
export const EQ_FACETS = ['eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation'] as const;
export const DQ_FACETS = ['dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration'] as const;
export const AQ_FACETS = ['aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'] as const;

export const ALL_FACETS = [
  ...IQ_FACETS,
  ...EQ_FACETS,
  ...DQ_FACETS,
  ...AQ_FACETS
] as const;