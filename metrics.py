import numpy as np


class MetricsCalculator:
    """Calculates summary metrics across 24-hour time-stepped simulation runs."""

    def calculate(self, results: list[dict]) -> dict:
        costs = [result["total_cost"] for result in results]
        dropped = [result.get("total_dropped", 0.0) for result in results]
        avg_servers = [result.get("avg_servers", 3.0) for result in results]
        max_servers = [result.get("max_servers_needed", 3) for result in results]
        utilizations = [result.get("avg_utilization", 0.0) for result in results]
        system_failures = [1 if result.get("system_failed", False) else 0 for result in results]

        return {
            "average_cost": float(np.mean(costs)),
            "median_cost": float(np.median(costs)),
            "min_cost": float(np.min(costs)),
            "max_cost": float(np.max(costs)),
            "p95_cost": float(np.percentile(costs, 95)),
            "avg_dropped_requests": float(np.mean(dropped)),
            "max_dropped_requests": float(np.max(dropped)),
            "avg_servers_used": float(np.mean(avg_servers)),
            "max_servers_required": int(np.max(max_servers)),
            "avg_utilization": float(np.mean(utilizations)),
            "system_failure_rate": float(np.mean(system_failures)),
        }
