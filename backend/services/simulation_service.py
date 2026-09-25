import os
from typing import List, Optional

from simulation.analysis.aggregate import (
    aggregate_allocation_results,
    aggregate_dispatch_results,
)
from simulation.analysis.plots import generate_all_plots
from simulation.benchmarks.allocation_benchmark import run_allocation_benchmark
from simulation.benchmarks.dispatch_benchmark import run_dispatch_benchmark
from backend.api.schemas.simulation import QuickSimulationResponse


class SimulationService:
    def run_quick_simulation(
        self,
        sizes: Optional[List[int]] = None,
        seed: int = 42,
        repetitions: int = 1,
        output_dir: str = "simulation/results",
    ) -> QuickSimulationResponse:
        if not sizes:
            sizes = [10, 25, 50]

        capped_sizes = [min(n, 100) for n in sizes]
        sizes_alloc = [(n, max(2, n // 2)) for n in capped_sizes]
        sizes_disp = capped_sizes

        alloc_rows = run_allocation_benchmark(
            sizes=sizes_alloc, seeds=[seed], repetitions=repetitions
        )
        disp_rows = run_dispatch_benchmark(
            sizes=sizes_disp, seeds=[seed], repetitions=repetitions
        )

        alloc_dicts = [r.__dict__ for r in alloc_rows]
        disp_dicts = [r.__dict__ for r in disp_rows]

        alloc_agg = aggregate_allocation_results(alloc_dicts)
        disp_agg = aggregate_dispatch_results(disp_dicts)

        plots_dir = os.path.join(output_dir, "plots")
        plots_created = generate_all_plots(alloc_agg, disp_agg, plots_dir)
        plot_names = [os.path.basename(p) for p in plots_created]

        return QuickSimulationResponse(
            status="success",
            allocation_results=alloc_agg,
            dispatch_results=disp_agg,
            plots_generated=plot_names,
        )
