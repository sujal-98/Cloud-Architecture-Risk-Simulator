import numpy as np
from config import (
    AUTOSCALE_DOWN_THRESHOLD,
    AUTOSCALE_UP_THRESHOLD,
    AVERAGE_REQUESTS_PER_USER,
    COST_PER_SERVER_HOUR,
    DEFAULT_SERVER_CAPACITY,
    HOURS_PER_SIMULATION,
    MAX_SERVERS,
    MIN_SERVERS,
    SERVER_FAILURE_PROBABILITY,
)


class CloudModel:
    """Simulates a 24-hour time-stepped cloud environment with diurnal traffic and reactive autoscaling."""

    def run_day(
        self,
        rng,
        hours: int = HOURS_PER_SIMULATION,
        min_servers: int = MIN_SERVERS,
        max_servers: int = MAX_SERVERS,
        server_capacity: float = DEFAULT_SERVER_CAPACITY,
        autoscale_up: float = AUTOSCALE_UP_THRESHOLD,
        autoscale_down: float = AUTOSCALE_DOWN_THRESHOLD,
        failure_prob: float = SERVER_FAILURE_PROBABILITY,
        avg_requests_per_user: float = AVERAGE_REQUESTS_PER_USER,
        cost_per_server_hour: float = COST_PER_SERVER_HOUR,
    ) -> dict:
        hourly_logs = []
        current_servers = min_servers

        total_day_requests = 0.0
        total_day_handled = 0.0
        total_day_dropped = 0.0
        total_day_cost = 0.0
        server_counts = []
        utilizations = []

        for hour in range(hours):
            # 1. Generate hourly traffic with diurnal curve
            users = rng.generate_diurnal_traffic(hour=hour)
            requests = users * avg_requests_per_user

            # 2. Evaluate server failure statuses
            server_failures = rng.generate_server_failures(
                num_servers=current_servers, failure_prob=failure_prob
            )
            active_servers = sum(1 for f in server_failures if not f)
            available_capacity = active_servers * server_capacity

            # 3. Calculate utilization
            utilization = (
                requests / available_capacity if available_capacity > 0 else 1.0
            )

            # 4. Make scaling decision (scale up if > 80%, scale down if < 30%)
            scaled_action = "NONE"
            if utilization > autoscale_up and current_servers < max_servers:
                current_servers += 1
                scaled_action = "SCALE_UP"
            elif utilization < autoscale_down and current_servers > min_servers:
                current_servers -= 1
                scaled_action = "SCALE_DOWN"

            # Re-evaluate operational capacity post scaling action
            active_capacities = [
                0.0 if failed else server_capacity
                for failed in server_failures
            ]
            final_available_capacity = sum(active_capacities)

            # 5. Handled vs Dropped requests
            handled = min(requests, final_available_capacity)
            dropped = max(0.0, requests - final_available_capacity)

            # 6. Hourly Cost (server-hour cost for provisioned servers)
            hourly_cost = current_servers * cost_per_server_hour

            # Accumulate day metrics
            total_day_requests += requests
            total_day_handled += handled
            total_day_dropped += dropped
            total_day_cost += hourly_cost
            server_counts.append(current_servers)
            utilizations.append(utilization)

            hourly_logs.append({
                "hour": hour,
                "users": users,
                "requests": requests,
                "servers": current_servers,
                "active_servers": active_servers,
                "available_capacity": final_available_capacity,
                "utilization": utilization,
                "handled": handled,
                "dropped": dropped,
                "action": scaled_action,
                "cost": hourly_cost,
                "server_failures": list(server_failures),
            })

        day_system_failed = bool(total_day_dropped > 0)

        return {
            "hourly_logs": hourly_logs,
            "total_requests": total_day_requests,
            "total_handled": total_day_handled,
            "total_dropped": total_day_dropped,
            "total_cost": total_day_cost,
            "max_servers_needed": max(server_counts),
            "min_servers_used": min(server_counts),
            "avg_servers": float(np.mean(server_counts)),
            "avg_utilization": float(np.mean(utilizations)),
            "system_failed": day_system_failed,
        }

    # Backward compatibility wrapper for single-run invocation
    def run(self, users: float, rng=None, **kwargs) -> dict:
        dummy_day = self.run_day(rng=rng, **kwargs)
        first_hour = dummy_day["hourly_logs"][0]
        return {
            "users": users,
            "requests": first_hour["requests"],
            "handled_requests": first_hour["handled"],
            "dropped_requests": first_hour["dropped"],
            "initial_servers": first_hour["servers"],
            "final_servers": first_hour["servers"],
            "scaled_servers": 0,
            "active_servers": first_hour["active_servers"],
            "failed_servers": sum(1 for f in first_hour["server_failures"] if f),
            "server_failures": first_hour["server_failures"],
            "available_capacity": first_hour["available_capacity"],
            "utilization": first_hour["utilization"],
            "system_failed": dummy_day["system_failed"],
            "cost": dummy_day["total_cost"],
        }
