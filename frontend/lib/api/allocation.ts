import { fetchApi } from './client';

export interface AllocatedAmount {
  agency_id: string;
  quantity_kg: number;
}

export interface AllocationResult {
  donation_id: string;
  algorithm: string;
  allocations: AllocatedAmount[];
  total_donated_kg: number;
  total_allocated_kg: number;
  unmet_demand_kg: number;
  allocation_rate: number;
  jains_fairness_index: number;
  allocation_disparity: number;
  fulfillment_ratios: Record<string, number>;
  execution_time_ms: number;
}

export interface AllocationCompareResult {
  greedy: AllocationResult;
  fairness_aware: AllocationResult;
}

export interface AllocationRecord {
  id: string;
  donation_id: string;
  agency_id: string;
  quantity_kg: number;
  algorithm: string;
  created_at: string;
}

export const allocationApi = {
  greedy: (data: any) => fetchApi<AllocationResult>('/allocation/greedy', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  fair: (data: any) => fetchApi<AllocationResult>('/allocation/fair', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  compare: (data: any) => fetchApi<AllocationCompareResult>('/allocation/compare', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  records: () => fetchApi<AllocationRecord[]>('/api/v1/allocation-records'),
};
