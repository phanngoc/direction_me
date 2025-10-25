import React, { useState, useEffect, useCallback } from 'react';
import { AssessmentQuestion, AssessmentResponse } from '../../shared/types';
import AssessmentHeader from './AssessmentHeader';
import QuestionDisplay from './QuestionDisplay';
import QuestionNavigation from './QuestionNavigation';
import ProgressTracker from './ProgressTracker';
import ResponseSubmitter from './ResponseSubmitter';
import { useAssessmentAPI } from '../services/assessment_api';

interface AssessmentPageProps {
  sessionId: string;
  userId: string;
  onComplete?: (results: any) => void;
  onExit?: () => void;
}

interface AssessmentState {
  currentModule: string;
  currentQuestionIndex: number;
  questions: AssessmentQuestion[];
  responses: AssessmentResponse[];
  isSubmitting: boolean;
  isCompleted: boolean;
  progress: {
    total: number;
    completed: number;
    current: number;
  };
}

const AssessmentPage: React.FC<AssessmentPageProps> = ({
  sessionId,
  userId,
  onComplete,
  onExit
}) => {
  const [state, setState] = useState<AssessmentState>({
    currentModule: 'IQ',
    currentQuestionIndex: 0,
    questions: [],
    responses: [],
    isSubmitting: false,
    isCompleted: false,
    progress: { total: 0, completed: 0, current: 0 }
  });

  const { 
    getAssessmentSequence,
    submitResponse,
    completeAssessment,
    getSessionProgress
  } = useAssessmentAPI();

  // Load assessment sequence on mount
  useEffect(() => {
    loadAssessmentSequence();
  }, [sessionId]);

  const loadAssessmentSequence = async () => {
    try {
      const sequence = await getAssessmentSequence(sessionId);
      
      // Calculate total questions across all modules
      const totalQuestions = Object.values(sequence).reduce(
        (sum, questions) => sum + questions.length, 0
      );
      
      setState(prev => ({
        ...prev,
        questions: sequence.IQ || [],
        progress: {
          ...prev.progress,
          total: totalQuestions
        }
      }));
    } catch (error) {
      console.error('Failed to load assessment sequence:', error);
    }
  };

  const handleResponseSubmit = useCallback(async (response: Partial<AssessmentResponse>) => {
    if (state.isSubmitting) return;

    setState(prev => ({ ...prev, isSubmitting: true }));

    try {
      const currentQuestion = state.questions[state.currentQuestionIndex];
      if (!currentQuestion) return;

      const submittedResponse = await submitResponse(sessionId, {
        question_id: currentQuestion.id,
        answer: response.answer || '',
        answer_value: response.answer_value,
        response_time_seconds: response.response_time_seconds
      });

      // Add response to state
      setState(prev => ({
        ...prev,
        responses: [...prev.responses, submittedResponse],
        progress: {
          ...prev.progress,
          completed: prev.progress.completed + 1
        }
      }));

      // Move to next question or complete assessment
      moveToNextQuestion();

    } catch (error) {
      console.error('Failed to submit response:', error);
    } finally {
      setState(prev => ({ ...prev, isSubmitting: false }));
    }
  }, [state.questions, state.currentQuestionIndex, sessionId, submitResponse]);

  const moveToNextQuestion = () => {
    setState(prev => {
      const nextIndex = prev.currentQuestionIndex + 1;
      
      // Check if we've completed all questions
      if (nextIndex >= prev.questions.length) {
        // Move to next module or complete assessment
        const nextModule = getNextModule(prev.currentModule);
        if (nextModule) {
          return {
            ...prev,
            currentModule: nextModule,
            currentQuestionIndex: 0,
            questions: getQuestionsForModule(nextModule)
          };
        } else {
          // All modules completed
          completeAssessment();
          return { ...prev, isCompleted: true };
        }
      }
      
      return {
        ...prev,
        currentQuestionIndex: nextIndex,
        progress: {
          ...prev.progress,
          current: nextIndex + 1
        }
      };
    });
  };

  const getNextModule = (currentModule: string): string | null => {
    const moduleOrder = ['IQ', 'EQ', 'DQ', 'AQ'];
    const currentIndex = moduleOrder.indexOf(currentModule);
    return currentIndex < moduleOrder.length - 1 ? moduleOrder[currentIndex + 1] : null;
  };

  const getQuestionsForModule = (module: string): AssessmentQuestion[] => {
    // This would typically load questions for the specific module
    // For now, return empty array as placeholder
    return [];
  };

  const completeAssessment = async () => {
    try {
      const results = await completeAssessment(sessionId);
      if (onComplete) {
        onComplete(results);
      }
    } catch (error) {
      console.error('Failed to complete assessment:', error);
    }
  };

  const handleExit = () => {
    if (onExit) {
      onExit();
    }
  };

  const currentQuestion = state.questions[state.currentQuestionIndex];

  if (state.isCompleted) {
    return (
      <div className="assessment-completed">
        <h2>Đánh giá hoàn thành!</h2>
        <p>Cảm ơn bạn đã hoàn thành bài đánh giá. Kết quả sẽ được hiển thị trong giây lát.</p>
      </div>
    );
  }

  return (
    <div className="assessment-page">
      <AssessmentHeader 
        module={state.currentModule}
        onExit={handleExit}
      />
      
      <ProgressTracker 
        progress={state.progress}
        module={state.currentModule}
      />
      
      {currentQuestion && (
        <QuestionDisplay 
          question={currentQuestion}
          questionNumber={state.currentQuestionIndex + 1}
          totalQuestions={state.questions.length}
        />
      )}
      
      <ResponseSubmitter 
        question={currentQuestion}
        onSubmit={handleResponseSubmit}
        isSubmitting={state.isSubmitting}
      />
      
      <QuestionNavigation 
        currentIndex={state.currentQuestionIndex}
        totalQuestions={state.questions.length}
        onPrevious={() => setState(prev => ({
          ...prev,
          currentQuestionIndex: Math.max(0, prev.currentQuestionIndex - 1)
        }))}
        onNext={() => moveToNextQuestion()}
        canGoNext={!state.isSubmitting}
      />
    </div>
  );
};

export default AssessmentPage;
