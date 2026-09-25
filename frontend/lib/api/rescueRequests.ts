import { fetchApi } from './client';

export interface RescueRequest {
  id: string;
  donation_id: string;
  agency_id: string;
  requested_quantity_kg: number;
  pickup_deadline?: string;
  status: string;
  created_at: string;
}

export interface RescueRequestCreate {
  id?: string;
  donation_id: string;
  agency_id: string;
  requested_quantity_kg: number;
  pickup_deadline?: string;
  status?: string;
}

export const rescueRequestsApi = {
  list: () => fetchApi<RescueRequest[]>('/api/v1/rescue-requests'),
  get: (id: string) => fetchApi<RescueRequest>(`/api/v1/rescue-requests/${id}`),
  create: (data: RescueRequestCreate) => fetchApi<RescueRequest>('/api/v1/rescue-requests', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};
