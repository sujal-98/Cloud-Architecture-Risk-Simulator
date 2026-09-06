import numpy as np
from config import AVERAGE_USERS, RANDOM_SEED, USER_STD_DEV


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
