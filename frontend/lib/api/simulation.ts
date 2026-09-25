import { fetchApi } from './client';

export interface AllocationMetricsSummary {
  greedy: {
    allocation_rate: number;
    jains_fairness_index: number;
    allocation_disparity: number;
    execution_time_ms: number;
  };
  fairness_aware: {
    allocation_rate: number;
    jains_fairness_index: number;
    allocation_disparity: number;
    execution_time_ms: number;
  };
}

export interface DispatchMetricsSummary {
  nearest: {
    assignment_rate: number;
    total_distance_km: number;
    workload_variance: number;
    execution_time_ms: number;
  };
  scored: {
    assignment_rate: number;
    total_distance_km: number;
    workload_variance: number;
    execution_time_ms: number;
  };
  batch_bipartite: {
    assignment_rate: number;
    total_distance_km: number;
    workload_variance: number;
    execution_time_ms: number;
  };
}

export interface SimulationResult {
  seed: number;
  scenario_summary: {
    num_donations: number;
    num_agencies: number;
    num_rescue_requests: number;
    num_volunteers: number;
  };
  allocation_results: AllocationMetricsSummary;
  dispatch_results: DispatchMetricsSummary;
  execution_time_ms: number;
}

export const simulationApi = {
  quick: (params?: { num_donations?: number; num_agencies?: number; num_volunteers?: number; seed?: number }) => {
    const query = new URLSearchParams();
    if (params?.num_donations) query.append('num_donations', params.num_donations.toString());
    if (params?.num_agencies) query.append('num_agencies', params.num_agencies.toString());
    if (params?.num_volunteers) query.append('num_volunteers', params.num_volunteers.toString());
    if (params?.seed) query.append('seed', params.seed.toString());
    const endpoint = `/api/v1/simulation/quick${query.toString() ? '?' + query.toString() : ''}`;
    return fetchApi<SimulationResult>(endpoint, { method: 'POST' });
  }
};
