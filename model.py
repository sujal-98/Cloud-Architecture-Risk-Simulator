from config import (
    AVERAGE_REQUESTS_PER_USER,
    COST_PER_REQUEST,
    SERVER_CAPACITIES,
)


class CloudModel:
    """Simulates cloud resource usage, server capacities, and cost based on user count and server failures."""

    def run(
        self,
        users: float,
        server_failures: list[bool] | None = None,
        server_capacities: list[float] = SERVER_CAPACITIES,
        avg_requests_per_user: float = AVERAGE_REQUESTS_PER_USER,
        cost_per_request: float = COST_PER_REQUEST,
    ) -> dict[str, float | list | bool]:
        total_requests = users * avg_requests_per_user

        if server_failures is None:
            server_failures = [False] * len(server_capacities)

        # Calculate active capacity for each server
        active_capacities = [
            0.0 if failed else capacity
            for failed, capacity in zip(server_failures, server_capacities)
        ]
        total_available_capacity = sum(active_capacities)

        # Calculate handled vs dropped requests
        handled_requests = min(total_requests, total_available_capacity)
        dropped_requests = max(0.0, total_requests - total_available_capacity)
        system_failed = bool(dropped_requests > 0)

        cost = total_requests * cost_per_request

        return {
            "users": users,
            "requests": total_requests,
            "handled_requests": handled_requests,
            "dropped_requests": dropped_requests,
            "available_capacity": total_available_capacity,
            "active_servers": sum(1 for f in server_failures if not f),
            "failed_servers": sum(1 for f in server_failures if f),
            "server_failures": list(server_failures),
            "system_failed": system_failed,
            "cost": cost,
        }
