import numpy as np


class MetricsCalculator:

    def calculate(self, results):

        costs = [
            result["cost"]
            for result in results
        ]

        return {
            "average": np.mean(costs),

            "median": np.median(costs),

            "minimum": np.min(costs),

            "maximum": np.max(costs),

            "p95": np.percentile(
                costs,
                95
            )
        }

