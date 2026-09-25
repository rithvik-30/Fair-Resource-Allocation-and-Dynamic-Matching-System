import os
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = {
    "Greedy Allocation": "#3B82F6",
    "Fairness-Aware Allocation": "#10B981",
    "Nearest Volunteer Greedy": "#8B5CF6",
    "Score-Based Dispatch": "#F59E0B",
    "Batch Bipartite Matching": "#EF4444",
}

LINE_STYLES = {
    "Greedy Allocation": "o-",
    "Fairness-Aware Allocation": "s-",
    "Nearest Volunteer Greedy": "o-",
    "Score-Based Dispatch": "s-",
    "Batch Bipartite Matching": "^-",
}


def generate_all_plots(
    allocation_agg: List[Dict[str, Any]],
    dispatch_agg: List[Dict[str, Any]],
    output_dir: str,
) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    plot_files = []

    def _group_by_algo(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        algos: Dict[str, List[Dict[str, Any]]] = {}
        for r in data:
            a = str(r["algorithm"])
            if a not in algos:
                algos[a] = []
            algos[a].append(r)
        for a in algos:
            algos[a].sort(key=lambda x: int(x["problem_size"]))
        return algos

    alloc_groups = _group_by_algo(allocation_agg)
    disp_groups = _group_by_algo(dispatch_agg)

    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["axes.edgecolor"] = "#CCCCCC"
    plt.rcParams["axes.linewidth"] = 0.8

    # 1. Allocation: Runtime vs Problem Size
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for algo, rows in alloc_groups.items():
        x = [int(r["problem_size"]) for r in rows]
        y = [float(r["mean_runtime_ms"]) for r in rows]
        color = COLORS.get(algo, "#555555")
        marker = LINE_STYLES.get(algo, "o-")
        ax.plot(x, y, marker, label=algo, color=color, linewidth=2, markersize=6)
    ax.set_title("Allocation Engine: Runtime vs Problem Size", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Problem Size (Number of Donations)", fontsize=10)
    ax.set_ylabel("Mean Execution Time (ms)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#EEEEEE")
    fig.tight_layout()
    p1 = os.path.join(output_dir, "allocation_runtime_vs_size.png")
    fig.savefig(p1)
    plt.close(fig)
    plot_files.append(p1)

    # 2. Allocation: Allocation Rate vs Problem Size
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for algo, rows in alloc_groups.items():
        x = [int(r["problem_size"]) for r in rows]
        y = [float(r["mean_allocation_rate"]) for r in rows]
        color = COLORS.get(algo, "#555555")
        marker = LINE_STYLES.get(algo, "o-")
        ax.plot(x, y, marker, label=algo, color=color, linewidth=2, markersize=6)
    ax.set_title("Allocation Engine: Allocation Rate vs Problem Size", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Problem Size (Number of Donations)", fontsize=10)
    ax.set_ylabel("Mean Allocation Rate (Allocated / Supply)", fontsize=10)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#EEEEEE")
    fig.tight_layout()
    p2 = os.path.join(output_dir, "allocation_rate_vs_size.png")
    fig.savefig(p2)
    plt.close(fig)
    plot_files.append(p2)

    # 3. Allocation: Jain Fairness vs Problem Size
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for algo, rows in alloc_groups.items():
        x = [int(r["problem_size"]) for r in rows]
        y = [float(r["mean_jain_fairness"]) for r in rows]
        color = COLORS.get(algo, "#555555")
        marker = LINE_STYLES.get(algo, "o-")
        ax.plot(x, y, marker, label=algo, color=color, linewidth=2, markersize=6)
    ax.set_title("Allocation Engine: Jain Fairness Index vs Problem Size", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Problem Size (Number of Donations)", fontsize=10)
    ax.set_ylabel("Jain Fairness Index (0 to 1)", fontsize=10)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#EEEEEE")
    fig.tight_layout()
    p3 = os.path.join(output_dir, "allocation_fairness_vs_size.png")
    fig.savefig(p3)
    plt.close(fig)
    plot_files.append(p3)

    # 4. Dispatch: Runtime vs Problem Size
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for algo, rows in disp_groups.items():
        x = [int(r["problem_size"]) for r in rows]
        y = [float(r["mean_runtime_ms"]) for r in rows]
        color = COLORS.get(algo, "#555555")
        marker = LINE_STYLES.get(algo, "o-")
        ax.plot(x, y, marker, label=algo, color=color, linewidth=2, markersize=6)
    ax.set_title("Dispatch Engine: Runtime vs Problem Size", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Problem Size (Number of Requests / Volunteers)", fontsize=10)
    ax.set_ylabel("Mean Execution Time (ms)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#EEEEEE")
    fig.tight_layout()
    p4 = os.path.join(output_dir, "dispatch_runtime_vs_size.png")
    fig.savefig(p4)
    plt.close(fig)
    plot_files.append(p4)

    # 5. Dispatch: Assignment Rate vs Problem Size
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for algo, rows in disp_groups.items():
        x = [int(r["problem_size"]) for r in rows]
        y = [float(r["mean_assignment_rate"]) for r in rows]
        color = COLORS.get(algo, "#555555")
        marker = LINE_STYLES.get(algo, "o-")
        ax.plot(x, y, marker, label=algo, color=color, linewidth=2, markersize=6)
    ax.set_title("Dispatch Engine: Assignment Rate vs Problem Size", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Problem Size (Number of Requests / Volunteers)", fontsize=10)
    ax.set_ylabel("Mean Assignment Rate (Assigned / Total)", fontsize=10)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#EEEEEE")
    fig.tight_layout()
    p5 = os.path.join(output_dir, "dispatch_assignment_rate_vs_size.png")
    fig.savefig(p5)
    plt.close(fig)
    plot_files.append(p5)

    # 6. Dispatch: Total Distance vs Problem Size
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for algo, rows in disp_groups.items():
        x = [int(r["problem_size"]) for r in rows]
        y = [float(r["mean_total_distance_km"]) for r in rows]
        color = COLORS.get(algo, "#555555")
        marker = LINE_STYLES.get(algo, "o-")
        ax.plot(x, y, marker, label=algo, color=color, linewidth=2, markersize=6)
    ax.set_title("Dispatch Engine: Total Distance vs Problem Size", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Problem Size (Number of Requests / Volunteers)", fontsize=10)
    ax.set_ylabel("Mean Total Travel Distance (km)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#EEEEEE")
    fig.tight_layout()
    p6 = os.path.join(output_dir, "dispatch_total_distance_vs_size.png")
    fig.savefig(p6)
    plt.close(fig)
    plot_files.append(p6)

    # 7. Dispatch: Workload Variance vs Problem Size
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for algo, rows in disp_groups.items():
        x = [int(r["problem_size"]) for r in rows]
        y = [float(r["mean_workload_variance"]) for r in rows]
        color = COLORS.get(algo, "#555555")
        marker = LINE_STYLES.get(algo, "o-")
        ax.plot(x, y, marker, label=algo, color=color, linewidth=2, markersize=6)
    ax.set_title("Dispatch Engine: Workload Variance vs Problem Size", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Problem Size (Number of Requests / Volunteers)", fontsize=10)
    ax.set_ylabel("Mean Workload Variance", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#EEEEEE")
    fig.tight_layout()
    p7 = os.path.join(output_dir, "dispatch_workload_variance_vs_size.png")
    fig.savefig(p7)
    plt.close(fig)
    plot_files.append(p7)

    return plot_files
