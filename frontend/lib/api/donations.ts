import { fetchApi } from './client';

export interface Donation {
  id: string;
  donor_id: string;
  food_type: string;
  quantity_kg: number;
  available_from?: string;
  available_until?: string;
  requires_refrigeration: boolean;
  created_at: string;
}

export interface DonationCreate {
  id?: string;
  donor_id: string;
  food_type: string;
  quantity_kg: number;
  available_from?: string;
  available_until?: string;
  requires_refrigeration?: boolean;
}

export const donationsApi = {
  list: () => fetchApi<Donation[]>('/api/v1/donations'),
  get: (id: string) => fetchApi<Donation>(`/api/v1/donations/${id}`),
  create: (data: DonationCreate) => fetchApi<Donation>('/api/v1/donations', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};
