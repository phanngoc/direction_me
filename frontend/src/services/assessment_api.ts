import { useState, useCallback } from 'react';
import { AssessmentQuestion, AssessmentResponse } from '../../shared/types';

interface UseAssessmentAPIReturn {
  getAssessmentSequence: (sessionId: string) => Promise<Record<string, AssessmentQuestion[]>>;
  getQuestions: (sessionId: string, module: string, limit?: number) => Promise<AssessmentQuestion[]>;
  submitResponse: (sessionId: string, response: Partial<AssessmentResponse>) => Promise<AssessmentResponse>;
  completeAssessment: (sessionId: string) => Promise<any>;
  getSessionProgress: (sessionId: string) => Promise<any>;
  getSessionResponses: (sessionId: string) => Promise<AssessmentResponse[]>;
  isLoading: boolean;
  error: string | null;
}

export const useAssessmentAPI = (): UseAssessmentAPIReturn => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRequest = async <T>(request: () => Promise<T>): Promise<T> => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await request();
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const getAssessmentSequence = useCallback(async (sessionId: string): Promise<Record<string, AssessmentQuestion[]>> => {
    return handleRequest(async () => {
      const response = await fetch(`/api/assessments/${sessionId}/sequence`);
      if (!response.ok) {
        throw new Error(`Failed to get assessment sequence: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  const getQuestions = useCallback(async (sessionId: string, module: string, limit?: number): Promise<AssessmentQuestion[]> => {
    return handleRequest(async () => {
      const params = new URLSearchParams({ module });
      if (limit) params.append('limit', limit.toString());
      
      const response = await fetch(`/api/assessments/${sessionId}/questions?${params}`);
      if (!response.ok) {
        throw new Error(`Failed to get questions: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  const submitResponse = useCallback(async (sessionId: string, response: Partial<AssessmentResponse>): Promise<AssessmentResponse> => {
    return handleRequest(async () => {
      const responseData = await fetch(`/api/assessments/${sessionId}/responses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question_id: response.question_id,
          answer: response.answer,
          answer_value: response.answer_value,
          response_time_seconds: response.response_time_seconds
        })
      });

      if (!responseData.ok) {
        throw new Error(`Failed to submit response: ${responseData.statusText}`);
      }
      
      const data = await responseData.json();
      return data.data.response;
    });
  }, []);

  const completeAssessment = useCallback(async (sessionId: string): Promise<any> => {
    return handleRequest(async () => {
      const response = await fetch(`/api/assessments/${sessionId}/complete`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error(`Failed to complete assessment: ${response.statusText}`);
      }
      
      const data = await response.json();
      return data.data;
    });
  }, []);

  const getSessionProgress = useCallback(async (sessionId: string): Promise<any> => {
    return handleRequest(async () => {
      const response = await fetch(`/api/assessments/${sessionId}/progress`);
      if (!response.ok) {
        throw new Error(`Failed to get session progress: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  const getSessionResponses = useCallback(async (sessionId: string): Promise<AssessmentResponse[]> => {
    return handleRequest(async () => {
      const response = await fetch(`/api/assessments/${sessionId}/responses`);
      if (!response.ok) {
        throw new Error(`Failed to get session responses: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  return {
    getAssessmentSequence,
    getQuestions,
    submitResponse,
    completeAssessment,
    getSessionProgress,
    getSessionResponses,
    isLoading,
    error
  };
};
