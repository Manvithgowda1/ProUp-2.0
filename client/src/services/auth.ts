import api from './api';
import type {
  LoginRequest,
  StudentRegisterRequest,
  OrganizerRegisterRequest,
  Token,
  UserSummary,
} from '@/types';

export const login = async (data: LoginRequest): Promise<Token> => {
  const response = await api.post('/auth/login', data);
  return response.data;
};

export const registerStudent = async (data: StudentRegisterRequest): Promise<Token> => {
  const response = await api.post('/auth/register/student', data);
  return response.data;
};

export const registerOrganizer = async (data: OrganizerRegisterRequest): Promise<Token> => {
  const response = await api.post('/auth/register/organizer', data);
  return response.data;
};

export const getMe = async (): Promise<UserSummary> => {
  const response = await api.get('/auth/me');
  return response.data.data;
};

export const refreshToken = async (token: string): Promise<Token> => {
  const response = await api.post('/auth/refresh', { token });
  return response.data;
};

export const authService = {
  login,
  registerStudent,
  registerOrganizer,
  getMe,
  refreshToken,
};
