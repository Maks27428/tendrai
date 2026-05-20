import api from './client';

export interface AuthResponse {
  token: string;
  nickname: string;
}

export interface UserInfo {
  id: number;
  nickname: string;
}

export async function register(nickname: string, password: string): Promise<AuthResponse> {
  const { data } = await api.post<AuthResponse>('/auth/register/', { nickname, password });
  return data;
}

export async function login(nickname: string, password: string): Promise<AuthResponse> {
  const { data } = await api.post<AuthResponse>('/auth/login/', { nickname, password });
  return data;
}

export async function getMe(): Promise<UserInfo> {
  const { data } = await api.get<UserInfo>('/auth/me/');
  return data;
}
