/**
 * Custom hook for assessment progress tracking
 */
import { useState, useEffect, useCallback } from 'react';
import { Assessment, Question, Answer } from '@/shared/types';
import { getFromStorage, setToStorage, STORAGE_KEYS } from '@/utils/helpers';
import { assessmentApi } from '@/services/api';

interface UseAssessmentOptions {
  assessmentId?: string;
  autoSave?: boolean;
  saveInterval?: number; // in milliseconds
}

interface UseAssessmentReturn {
  // State
  assessment: Assessment | null;
  questions: Question[];
  answers: Answer[];
  currentQuestionIndex: number;
  loading: boolean;
  error: string | null;
  progress: {
    current: number;
    total: number;
    percentage: number;
  };

  // Actions
  setCurrentQuestion: (index: number) => void;
  setAnswer: (questionId: string, answerValue: number, answerText?: string) => void;
  nextQuestion: () => void;
  previousQuestion: () => void;
  submitAnswers: () => Promise<void>;
  completeAssessment: () => Promise<void>;
  resetAssessment: () => void;
  loadAssessment: (id: string) => Promise<void>;
  loadQuestions: (category?: string) => Promise<void>;
}

export function useAssessment(options: UseAssessmentOptions = {}): UseAssessmentReturn {
  const { assessmentId, autoSave = true, saveInterval = 30000 } = options;

  // State
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Progress calculation
  const progress = {
    current: currentQuestionIndex + 1,
    total: questions.length,
    percentage: questions.length > 0 ? Math.round(((currentQuestionIndex + 1) / questions.length) * 100) : 0,
  };

  // Load assessment from storage on mount
  useEffect(() => {
    if (assessmentId) {
      loadAssessment(assessmentId);
    } else {
      // Try to load from storage
      const storedAssessment = getFromStorage(STORAGE_KEYS.CURRENT_ASSESSMENT);
      if (storedAssessment) {
        setAssessment(storedAssessment);
        loadQuestions();
      }
    }
  }, [assessmentId]);

  // Auto-save answers
  useEffect(() => {
    if (autoSave && answers.length > 0) {
      const timer = setTimeout(() => {
        setToStorage(STORAGE_KEYS.ASSESSMENT_PROGRESS, {
          assessmentId: assessment?.id,
          answers,
          currentQuestionIndex,
        });
      }, saveInterval);

      return () => clearTimeout(timer);
    }
  }, [answers, currentQuestionIndex, assessment?.id, autoSave, saveInterval]);

  // Load assessment
  const loadAssessment = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);

      const assessmentData = await assessmentApi.get(id);
      setAssessment(assessmentData);
      setToStorage(STORAGE_KEYS.CURRENT_ASSESSMENT, assessmentData);

      // Load questions
      await loadQuestions();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load assessment');
    } finally {
      setLoading(false);
    }
  }, []);

  // Load questions
  const loadQuestions = useCallback(async (category?: string) => {
    if (!assessment) return;

    try {
      setLoading(true);
      setError(null);

      const questionsData = await assessmentApi.getQuestions(assessment.id, category);
      setQuestions(questionsData);

      // Load saved progress if available
      const savedProgress = getFromStorage(STORAGE_KEYS.ASSESSMENT_PROGRESS);
      if (savedProgress && savedProgress.assessmentId === assessment.id) {
        setAnswers(savedProgress.answers || []);
        setCurrentQuestionIndex(savedProgress.currentQuestionIndex || 0);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load questions');
    } finally {
      setLoading(false);
    }
  }, [assessment]);

  // Set current question
  const setCurrentQuestion = useCallback((index: number) => {
    if (index >= 0 && index < questions.length) {
      setCurrentQuestionIndex(index);
    }
  }, [questions.length]);

  // Set answer
  const setAnswer = useCallback((questionId: string, answerValue: number, answerText?: string) => {
    setAnswers(prev => {
      const existingIndex = prev.findIndex(a => a.question_id === questionId);
      const newAnswer: Answer = {
        question_id: questionId,
        answer_value: answerValue,
        answer_text: answerText,
      };

      if (existingIndex >= 0) {
        // Update existing answer
        const updated = [...prev];
        updated[existingIndex] = newAnswer;
        return updated;
      } else {
        // Add new answer
        return [...prev, newAnswer];
      }
    });
  }, []);

  // Navigation
  const nextQuestion = useCallback(() => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  }, [currentQuestionIndex, questions.length]);

  const previousQuestion = useCallback(() => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  }, [currentQuestionIndex]);

  // Submit answers
  const submitAnswers = useCallback(async () => {
    if (!assessment) {
      throw new Error('No active assessment');
    }

    try {
      setLoading(true);
      setError(null);

      await assessmentApi.submitAnswers(assessment.id, { answers });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit answers');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [assessment, answers]);

  // Complete assessment
  const completeAssessment = useCallback(async () => {
    if (!assessment) {
      throw new Error('No active assessment');
    }

    try {
      setLoading(true);
      setError(null);

      // Submit answers first
      await submitAnswers();

      // Complete assessment
      await assessmentApi.complete(assessment.id);

      // Clear saved progress
      removeFromStorage(STORAGE_KEYS.ASSESSMENT_PROGRESS);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to complete assessment');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [assessment, submitAnswers]);

  // Reset assessment
  const resetAssessment = useCallback(() => {
    setAnswers([]);
    setCurrentQuestionIndex(0);
    setError(null);
    removeFromStorage(STORAGE_KEYS.ASSESSMENT_PROGRESS);
  }, []);

  return {
    // State
    assessment,
    questions,
    answers,
    currentQuestionIndex,
    loading,
    error,
    progress,

    // Actions
    setCurrentQuestion,
    setAnswer,
    nextQuestion,
    previousQuestion,
    submitAnswers,
    completeAssessment,
    resetAssessment,
    loadAssessment,
    loadQuestions,
  };
}

// Helper function to remove from storage
function removeFromStorage(key: string): void {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error('Error removing from localStorage:', error);
  }
}