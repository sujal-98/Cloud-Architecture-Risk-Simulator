import numpy as np


class MetricsCalculator:
    """Calculates performance, latency percentiles, throughput, and utilization for discrete-event simulations."""

    def calculate(self, simulation_result: dict) -> dict:
        completed = simulation_result["completed_requests"]
        dropped = simulation_result["dropped_requests"]
        servers = simulation_result["servers"]
        queue = simulation_result["queue"]
        total_time = simulation_result["total_simulation_time"]

        latencies = [r.latency for r in completed]
        waiting_times = [r.waiting_time for r in completed]
        service_times = [r.service_time for r in completed]

        num_servers = len(servers)
        total_busy_time = sum(s.total_busy_time for s in servers)
        overall_utilization = (
            total_busy_time / (total_time * num_servers) if total_time > 0 and num_servers > 0 else 0.0
        )
        throughput = len(completed) / total_time if total_time > 0 else 0.0

        per_server_stats = {
            f"Server {s.id}": {
                "processed": s.total_processed,
                "busy_time": s.total_busy_time,
                "utilization": (s.total_busy_time / total_time * 100) if total_time > 0 else 0.0,
            }
            for s in servers
        }

        if not latencies:
            return {
                "total_completed": 0,
                "total_dropped": len(dropped),
                "throughput_req_per_sec": 0.0,
                "overall_utilization_pct": 0.0,
                "per_server_stats": per_server_stats,
            }

        return {
            "total_completed": len(completed),
            "total_dropped": len(dropped),
            "throughput_req_per_sec": float(throughput),
            "overall_utilization_pct": float(overall_utilization * 100),
            # Latency Metrics
            "avg_latency": float(np.mean(latencies)),
            "p50_latency": float(np.median(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "p99_latency": float(np.percentile(latencies, 99)),
            "max_latency": float(np.max(latencies)),
            # Waiting Time Metrics
            "avg_waiting_time": float(np.mean(waiting_times)),
            "p95_waiting_time": float(np.percentile(waiting_times, 95)),
            # Service Processing Metrics
            "avg_service_time": float(np.mean(service_times)),
            # Queue Metrics
            "max_queue_depth": queue.max_depth,
            "total_enqueued": queue.total_enqueued,
            "per_server_stats": per_server_stats,
        }
