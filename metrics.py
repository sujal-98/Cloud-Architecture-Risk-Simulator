import numpy as np


class MetricsCalculator:
    """Calculates summary metrics across simulation results."""

    def calculate(self, results: list[dict]) -> dict:
        costs = [result["cost"] for result in results]
        dropped = [result.get("dropped_requests", 0.0) for result in results]
        failed_servers = [result.get("failed_servers", 0) for result in results]
        system_failures = [1 if result.get("system_failed", False) else 0 for result in results]

        num_servers = (
            len(results[0]["server_failures"])
            if results and "server_failures" in results[0]
            else 0
        )
        per_server_failures = {}
        for s_idx in range(num_servers):
            failures_cnt = sum(1 for r in results if r["server_failures"][s_idx])
            per_server_failures[f"Server {s_idx + 1}"] = failures_cnt

        return {
            "average": float(np.mean(costs)),
            "median": float(np.median(costs)),
            "minimum": float(np.min(costs)),
            "maximum": float(np.max(costs)),
            "p95": float(np.percentile(costs, 95)),
            "avg_dropped_requests": float(np.mean(dropped)),
            "max_dropped_requests": float(np.max(dropped)),
            "avg_failed_servers": float(np.mean(failed_servers)),
            "system_failure_rate": float(np.mean(system_failures)),
            "per_server_failures": per_server_failures,
        }
