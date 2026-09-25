import { fetchApi } from './client';

export interface Donor {
  id: string;
  name: string;
  organization_type?: string;
  latitude: number;
  longitude: number;
  created_at: string;
}

export interface DonorCreate {
  id?: string;
  name: string;
  organization_type?: string;
  latitude: number;
  longitude: number;
}

export const donorsApi = {
  list: () => fetchApi<Donor[]>('/api/v1/donors'),
  get: (id: string) => fetchApi<Donor>(`/api/v1/donors/${id}`),
  create: (data: DonorCreate) => fetchApi<Donor>('/api/v1/donors', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};
