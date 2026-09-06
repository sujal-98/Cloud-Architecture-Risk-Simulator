from config import AVERAGE_REQUESTS_PER_USER, COST_PER_REQUEST


class CloudModel:
    """Simulates cloud resource usage and cost based on user count."""

    def run(self, users: float) -> dict[str, float]:
        total_requests = users * AVERAGE_REQUESTS_PER_USER
        cost = total_requests * COST_PER_REQUEST

        return {
            "users": users,
            "requests": total_requests,
            "cost": cost,
        }
