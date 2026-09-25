import { fetchApi } from './client';

export interface Volunteer {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  capacity_kg: number;
  has_refrigeration: boolean;
  available_from?: string;
  available_until?: string;
  current_workload_kg: number;
  max_travel_distance_km: number;
  created_at: string;
}

export interface VolunteerCreate {
  id?: string;
  name: string;
  latitude: number;
  longitude: number;
  capacity_kg: number;
  has_refrigeration?: boolean;
  available_from?: string;
  available_until?: string;
  current_workload_kg?: number;
  max_travel_distance_km?: number;
}

export const volunteersApi = {
  list: () => fetchApi<Volunteer[]>('/api/v1/volunteers'),
  get: (id: string) => fetchApi<Volunteer>(`/api/v1/volunteers/${id}`),
  create: (data: VolunteerCreate) => fetchApi<Volunteer>('/api/v1/volunteers', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};
