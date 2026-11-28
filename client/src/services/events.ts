import api from './api';
import type {
  EventResponse,
  EventCreate,
  EventUpdate,
  RoundResponse,
  PaginatedResponse,
} from '@/types';

export const getEvents = async (params?: {
  search?: string;
  status?: string;
  event_type?: string;
  page?: number;
  limit?: number;
}): Promise<PaginatedResponse<EventResponse>> => {
  const response = await api.get('/events', { params });
  return response.data;
};

export const getEvent = async (id: number): Promise<EventResponse> => {
  const response = await api.get(`/events/${id}`);
  return response.data.data;
};

export const registerForEvent = async (id: number): Promise<any> => {
  const response = await api.post(`/events/${id}/register`);
  return response.data;
};

export const getEventRounds = async (id: number): Promise<RoundResponse[]> => {
  const response = await api.get(`/events/${id}/rounds`);
  return response.data.data;
};

export const createEvent = async (data: EventCreate): Promise<EventResponse> => {
  const response = await api.post('/events', data);
  return response.data;
};

export const updateEvent = async (id: number, data: EventUpdate): Promise<EventResponse> => {
  const response = await api.put(`/events/${id}`, data);
  return response.data;
};

export const getRecommendations = async (): Promise<EventResponse[]> => {
  const response = await api.get('/events/recommendations');
  return response.data.data;
};

export const eventsService = {
  getEvents,
  getEvent,
  registerForEvent,
  getEventRounds,
  createEvent,
  updateEvent,
  getRecommendations,
};
