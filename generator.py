import numpy as np
from config import ARRIVAL_RATE, AVG_SERVICE_TIME, RANDOM_SEED
from request import Request


class RequestGenerator:
    """Generates stochastic request arrival streams and processing service times."""

    def __init__(
        self,
        arrival_rate: float = ARRIVAL_RATE,
        avg_service_time: float = AVG_SERVICE_TIME,
        seed: int = RANDOM_SEED,
    ) -> None:
        self.arrival_rate = arrival_rate
        self.avg_service_time = avg_service_time
        self.rng = np.random.default_rng(seed=seed)
        self.request_counter = 0

    def generate_next_arrival_delta(self) -> float:
        """Generate inter-arrival time interval via Exponential distribution (Poisson arrival process)."""
        return float(self.rng.exponential(scale=1.0 / self.arrival_rate))

    def generate_service_time(self) -> float:
        """Generate request service processing duration."""
        return max(0.001, float(self.rng.exponential(scale=self.avg_service_time)))

    def generate_request(self, arrival_time: float) -> Request:
        """Generate a new Request object at a given arrival timestamp."""
        self.request_counter += 1
        service_time = self.generate_service_time()
        return Request(
            id=self.request_counter,
            arrival_time=arrival_time,
            service_time=service_time,
        )
