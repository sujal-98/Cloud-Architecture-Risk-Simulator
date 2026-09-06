from typing import Callable, Optional
from config import ITERATIONS


class MonteCarloEngine:
    """Orchestrates Monte Carlo simulations using a generator and a model."""

    def __init__(self, generator, model) -> None:
        self.generator = generator
        self.model = model

    def run(
        self,
        iterations: int = ITERATIONS,
        callback: Optional[Callable[[dict, int, int], None]] = None,
    ) -> list[dict]:
        results = []

        for i in range(1, iterations + 1):
            # Generate random inputs: user count and server failure status list
            users = self.generator.generate_users()
            server_failures = self.generator.generate_server_failures()

            # Run the model
            result = self.model.run(users, server_failures=server_failures)

            # Store result
            results.append(result)

            # Trigger live update callback if provided
            if callback:
                callback(result, i, iterations)

        return results
