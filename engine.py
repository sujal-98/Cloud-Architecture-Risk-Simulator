from typing import Callable, Optional
from config import SIMULATIONS


class MonteCarloEngine:
    """Orchestrates time-stepped Monte Carlo simulations using a generator and a model."""

    def __init__(self, generator, model) -> None:
        self.generator = generator
        self.model = model

    def run(
        self,
        simulations: int = SIMULATIONS,
        callback: Optional[Callable[[dict, int, int], None]] = None,
    ) -> list[dict]:
        results = []

        for sim_idx in range(1, simulations + 1):
            # Run a full 24-hour time-stepped simulation day
            result = self.model.run_day(rng=self.generator)

            # Store simulation day result
            results.append(result)

            # Trigger live update callback if provided
            if callback:
                callback(result, sim_idx, simulations)

        return results
