import api from './api';
import type {
  QuestionResponse,
  AssessmentSubmitRequest,
  AssessmentResultResponse,
} from '@/types';

export const getQuestions = async (assessmentId: number): Promise<QuestionResponse[]> => {
  const response = await api.get(`/assessments/${assessmentId}/questions`);
  return response.data.data;
};

export const submitAssessment = async (
  assessmentId: number,
  data: AssessmentSubmitRequest
): Promise<AssessmentResultResponse> => {
  const response = await api.post(`/assessments/${assessmentId}/submit`, data);
  return response.data.data;
};

export const assessmentsService = {
  getQuestions,
  submitAssessment,
};
