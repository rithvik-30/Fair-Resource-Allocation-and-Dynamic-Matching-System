import { fetchApi } from './client';

export interface HealthCheck {
  status: string;
  database?: string;
}

export const healthApi = {
  appHealth: () => fetchApi<HealthCheck>('/health'),
  dbHealth: () => fetchApi<HealthCheck>('/api/v1/database/health'),
};
