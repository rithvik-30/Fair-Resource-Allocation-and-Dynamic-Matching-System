import { fetchApi } from './client';

export interface DispatchAssignment {
  rescue_request_id: string;
  volunteer_id: string;
  distance_km: number;
  is_feasible: boolean;
  explanation: string;
}

export interface DispatchResult {
  algorithm: string;
  assignments: DispatchAssignment[];
  unassigned_request_ids: string[];
  total_requests: number;
  assigned_requests: number;
  assignment_rate: number;
  total_distance_km: number;
  mean_distance_km: number;
  max_distance_km: number;
  workload_variance: number;
  execution_time_ms: number;
}

export interface DispatchCompareResult {
  nearest: DispatchResult;
  scored: DispatchResult;
  batch_bipartite: DispatchResult;
}

export interface DispatchRecord {
  id: string;
  rescue_request_id: string;
  volunteer_id: string;
  algorithm: string;
  distance_km: number;
  created_at: string;
}

export const dispatchApi = {
  nearest: (data: any) => fetchApi<DispatchResult>('/dispatch/nearest', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  scored: (data: any) => fetchApi<DispatchResult>('/dispatch/scored', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  batch: (data: any) => fetchApi<DispatchResult>('/dispatch/batch-matching', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  compare: (data: any) => fetchApi<DispatchCompareResult>('/dispatch/compare', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  records: () => fetchApi<DispatchRecord[]>('/api/v1/dispatch-records'),
};
