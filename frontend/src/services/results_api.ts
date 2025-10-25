import { useState, useCallback } from 'react';
import { AssessmentResult, CareerRecommendation, VisualizationData } from '../../shared/types';

interface UseResultsAPIReturn {
  getResults: (resultId: string) => Promise<AssessmentResult>;
  calculateResults: (sessionId: string, userId: string, chatbotSessionId: string) => Promise<AssessmentResult>;
  getCareerRecommendations: (resultId: string) => Promise<CareerRecommendation[]>;
  getVisualizationData: (resultId: string, chartType?: string) => Promise<VisualizationData[]>;
  getUserResults: (userId: string) => Promise<AssessmentResult[]>;
  isLoading: boolean;
  error: string | null;
}

export const useResultsAPI = (): UseResultsAPIReturn => {
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

  const getResults = useCallback(async (resultId: string): Promise<AssessmentResult> => {
    return handleRequest(async () => {
      const response = await fetch(`/api/results/${resultId}`);
      if (!response.ok) {
        throw new Error(`Failed to get results: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  const calculateResults = useCallback(async (
    sessionId: string, 
    userId: string, 
    chatbotSessionId: string
  ): Promise<AssessmentResult> => {
    return handleRequest(async () => {
      const response = await fetch('/api/results/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          user_id: userId,
          chatbot_session_id: chatbotSessionId
        })
      });

      if (!response.ok) {
        throw new Error(`Failed to calculate results: ${response.statusText}`);
      }
      
      const data = await response.json();
      return data.data;
    });
  }, []);

  const getCareerRecommendations = useCallback(async (resultId: string): Promise<CareerRecommendation[]> => {
    return handleRequest(async () => {
      const response = await fetch(`/api/results/${resultId}/recommendations`);
      if (!response.ok) {
        throw new Error(`Failed to get career recommendations: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  const getVisualizationData = useCallback(async (
    resultId: string, 
    chartType?: string
  ): Promise<VisualizationData[]> => {
    return handleRequest(async () => {
      const params = new URLSearchParams();
      if (chartType) params.append('chart_type', chartType);
      
      const response = await fetch(`/api/results/${resultId}/visualizations?${params}`);
      if (!response.ok) {
        throw new Error(`Failed to get visualization data: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  const getUserResults = useCallback(async (userId: string): Promise<AssessmentResult[]> => {
    return handleRequest(async () => {
      const response = await fetch(`/api/results/user/${userId}`);
      if (!response.ok) {
        throw new Error(`Failed to get user results: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data;
    });
  }, []);

  return {
    getResults,
    calculateResults,
    getCareerRecommendations,
    getVisualizationData,
    getUserResults,
    isLoading,
    error
  };
};
