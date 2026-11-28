import api from './api';
import type {
  CodingProblemResponse,
  CodeSubmissionRequest,
  CodeSubmissionResponse,
} from '@/types';

export const getProblem = async (id: number): Promise<CodingProblemResponse> => {
  const response = await api.get(`/coding/problems/${id}`);
  return response.data.data;
};

export const submitCode = async (
  problemId: number,
  data: CodeSubmissionRequest
): Promise<CodeSubmissionResponse> => {
  const response = await api.post(`/coding/problems/${problemId}/submit`, data);
  return response.data.data;
};

export const codingService = {
  getProblem,
  submitCode,
};
