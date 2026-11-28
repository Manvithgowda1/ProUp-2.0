import api from './api';
import type {
  StudentProfileResponse,
  StudentProfileUpdate,
  StudentAchievementsOverviewResponse,
  StudentRegistrationResponse,
  AddSkillRequest,
} from '@/types';

export const getProfile = async (): Promise<StudentProfileResponse> => {
  const response = await api.get('/students/me/profile');
  return response.data.data;
};

export const updateProfile = async (data: StudentProfileUpdate): Promise<StudentProfileResponse> => {
  const response = await api.put('/students/me/profile', data);
  return response.data.data;
};

export const getAchievements = async (): Promise<StudentAchievementsOverviewResponse> => {
  const response = await api.get('/students/me/achievements');
  return response.data.data;
};

export const getRegistrations = async (): Promise<StudentRegistrationResponse[]> => {
  const response = await api.get('/students/me/registrations');
  return response.data.data;
};

export const addSkill = async (data: AddSkillRequest): Promise<any> => {
  const response = await api.post('/students/me/skills/add', data);
  return response.data;
};

export const removeSkill = async (id: number): Promise<void> => {
  await api.delete(`/students/me/skills/${id}`);
};

export const studentsService = {
  getProfile,
  updateProfile,
  getAchievements,
  getRegistrations,
  addSkill,
  removeSkill,
};
