import numpy as np
from config import (
    AVERAGE_USERS,
    MIN_SERVERS,
    RANDOM_SEED,
    SERVER_FAILURE_PROBABILITY,
    USER_STD_DEV,
)


class RandomNumberGenerator:
    """Helper class for generating random numbers."""

    rng = np.random.default_rng(seed=RANDOM_SEED)

    def __init__(self, rng: np.random.Generator | None = None) -> None:
        self.rng = rng if rng is not None else np.random.default_rng(seed=RANDOM_SEED)

    def generate_poisson(self, lam: float = AVERAGE_USERS) -> int:
        """Generate a random number based on a Poisson distribution."""
        return int(self.rng.poisson(lam=lam))

    def generate_normal(
        self, loc: float = AVERAGE_USERS, scale: float = USER_STD_DEV
    ) -> float:
        """Generate a random number based on a normal distribution."""
        return float(self.rng.normal(loc=loc, scale=scale))

    def generate_users(self) -> float:
        """Generate a random user count based on the user distribution."""
        return max(0.0, self.generate_normal())

    def generate_diurnal_traffic(
        self,
        hour: int,
        base_users: float = AVERAGE_USERS,
        std_dev: float = USER_STD_DEV,
        peak_hour: int = 14,
    ) -> float:
        """Generate hourly user count with a 24-hour diurnal sinusoidal curve and random noise."""
        # Sinusoidal diurnal factor: ranges between ~0.5 (off-peak night) and ~1.5 (mid-day peak)
        diurnal_factor = 1.0 + 0.5 * np.sin((hour - (peak_hour - 6)) * (2 * np.pi / 24))
        hourly_mean = base_users * diurnal_factor
        return max(0.0, float(self.rng.normal(loc=hourly_mean, scale=std_dev)))

    def generate_server_failures(
        self,
        num_servers: int = MIN_SERVERS,
        failure_prob: float = SERVER_FAILURE_PROBABILITY,
    ) -> list[bool]:
        """Generate failure status (True if failed) for N servers."""
        return [bool(self.rng.random() < failure_prob) for _ in range(num_servers)]

    def is_server_failed(self, failure_prob: float = SERVER_FAILURE_PROBABILITY) -> bool:
        """Determine if a single dynamically added server fails."""
        return bool(self.rng.random() < failure_prob)
