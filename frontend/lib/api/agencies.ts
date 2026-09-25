import { fetchApi } from './client';

export interface Agency {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  demand_kg: number;
  storage_capacity_kg: number;
  requires_refrigeration: boolean;
  priority: number;
  created_at: string;
}

export interface AgencyCreate {
  id?: string;
  name: string;
  latitude: number;
  longitude: number;
  demand_kg: number;
  storage_capacity_kg: number;
  requires_refrigeration?: boolean;
  priority?: number;
}

export const agenciesApi = {
  list: () => fetchApi<Agency[]>('/api/v1/agencies'),
  get: (id: string) => fetchApi<Agency>(`/api/v1/agencies/${id}`),
  create: (data: AgencyCreate) => fetchApi<Agency>('/api/v1/agencies', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};
