/**
 * API client services for MyWay Career Assessment Frontend
 */
import { API_BASE_URL, getAuthHeaders, handleApiError } from '@/utils/helpers';
import {
  User,
  CreateUserRequest,
  LoginRequest,
  AuthResponse,
  Assessment,
  CreateAssessmentRequest,
  Question,
  Answer,
  SubmitAnswersRequest,
  AssessmentResult,
  CareerSuggestion,
  LearningPath,
  ProgressTracking,
  ApiResponse,
  PaginatedResponse
} from '@/shared/types';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  // Authentication API
  async register(userData: CreateUserRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(loginData: LoginRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(loginData),
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/auth/me');
  }

  // Assessment API
  async createAssessment(assessmentData: CreateAssessmentRequest): Promise<Assessment> {
    return this.request<Assessment>('/assessments', {
      method: 'POST',
      body: JSON.stringify(assessmentData),
    });
  }

  async getAssessment(assessmentId: string): Promise<Assessment> {
    return this.request<Assessment>(`/assessments/${assessmentId}`);
  }

  async getUserAssessments(userId: string): Promise<Assessment[]> {
    return this.request<Assessment[]>(`/assessments/user/${userId}`);
  }

  async getAssessmentQuestions(assessmentId: string, category?: string): Promise<Question[]> {
    const params = category ? `?category=${category}` : '';
    return this.request<Question[]>(`/assessments/${assessmentId}/questions${params}`);
  }

  async submitAnswers(assessmentId: string, answers: SubmitAnswersRequest): Promise<void> {
    return this.request<void>(`/assessments/${assessmentId}/answers`, {
      method: 'POST',
      body: JSON.stringify(answers),
    });
  }

  async completeAssessment(assessmentId: string): Promise<void> {
    return this.request<void>(`/assessments/${assessmentId}/complete`, {
      method: 'POST',
    });
  }

  // Results API
  async getAssessmentResult(assessmentId: string): Promise<AssessmentResult> {
    return this.request<AssessmentResult>(`/results/${assessmentId}`);
  }

  async getUserResults(userId: string): Promise<AssessmentResult[]> {
    return this.request<AssessmentResult[]>(`/results/user/${userId}`);
  }

  // Career API
  async getCareerSuggestions(assessmentId: string): Promise<CareerSuggestion[]> {
    return this.request<CareerSuggestion[]>(`/careers/suggestions/${assessmentId}`);
  }

  async getCareerDetails(careerName: string): Promise<CareerSuggestion> {
    return this.request<CareerSuggestion>(`/careers/${encodeURIComponent(careerName)}`);
  }

  // Learning Path API
  async getLearningPaths(assessmentId: string): Promise<LearningPath[]> {
    return this.request<LearningPath[]>(`/learning-paths/${assessmentId}`);
  }

  async createLearningPath(assessmentId: string, careerName: string): Promise<LearningPath> {
    return this.request<LearningPath>('/learning-paths', {
      method: 'POST',
      body: JSON.stringify({ assessment_id: assessmentId, career_name: careerName }),
    });
  }

  // Progress API
  async getProgressTracking(userId: string): Promise<ProgressTracking[]> {
    return this.request<ProgressTracking[]>(`/progress/${userId}`);
  }

  async getProgressComparison(userId: string, assessmentId1: string, assessmentId2: string): Promise<{
    improvement: {
      iq: number;
      eq: number;
      dq: number;
      aq: number;
    };
    timeSpan: string;
  }> {
    return this.request(`/progress/${userId}/compare`, {
      method: 'POST',
      body: JSON.stringify({
        assessment_id_1: assessmentId1,
        assessment_id_2: assessmentId2,
      }),
    });
  }

  // Health check
  async healthCheck(): Promise<{ status: string; database: string; version: string }> {
    return this.request('/health');
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

// Export individual service functions for convenience
export const authApi = {
  register: (userData: CreateUserRequest) => apiClient.register(userData),
  login: (loginData: LoginRequest) => apiClient.login(loginData),
  getCurrentUser: () => apiClient.getCurrentUser(),
};

export const assessmentApi = {
  create: (assessmentData: CreateAssessmentRequest) => apiClient.createAssessment(assessmentData),
  get: (assessmentId: string) => apiClient.getAssessment(assessmentId),
  getByUser: (userId: string) => apiClient.getUserAssessments(userId),
  getQuestions: (assessmentId: string, category?: string) => apiClient.getAssessmentQuestions(assessmentId, category),
  submitAnswers: (assessmentId: string, answers: SubmitAnswersRequest) => apiClient.submitAnswers(assessmentId, answers),
  complete: (assessmentId: string) => apiClient.completeAssessment(assessmentId),
};

export const resultsApi = {
  get: (assessmentId: string) => apiClient.getAssessmentResult(assessmentId),
  getByUser: (userId: string) => apiClient.getUserResults(userId),
};

export const careerApi = {
  getSuggestions: (assessmentId: string) => apiClient.getCareerSuggestions(assessmentId),
  getDetails: (careerName: string) => apiClient.getCareerDetails(careerName),
};

export const learningPathApi = {
  get: (assessmentId: string) => apiClient.getLearningPaths(assessmentId),
  create: (assessmentId: string, careerName: string) => apiClient.createLearningPath(assessmentId, careerName),
};

export const progressApi = {
  get: (userId: string) => apiClient.getProgressTracking(userId),
  compare: (userId: string, assessmentId1: string, assessmentId2: string) => 
    apiClient.getProgressComparison(userId, assessmentId1, assessmentId2),
};

export default apiClient;