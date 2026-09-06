import matplotlib.pyplot as plt


class Visualizer:
    """Visualizes simulation results with static and live plotting."""

    def __init__(self) -> None:
        self.fig, self.ax = None, None
        self.costs = []

    def setup_live_plot(self) -> None:
        """Setup matplotlib interactive mode for live plotting."""
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

    def update_live_plot(
        self, current_cost: float, iteration: int, total_iterations: int
    ) -> None:
        """Update live cost histogram during simulation."""
        if self.fig is None or self.ax is None:
            self.setup_live_plot()

        self.costs.append(current_cost)

        # Refresh plot periodically (e.g. every 1% of total iterations) for smooth animation
        update_interval = max(1, total_iterations // 100)
        if iteration % update_interval == 0 or iteration == total_iterations:
            self.ax.clear()
            self.ax.hist(
                self.costs, bins=50, color="skyblue", edgecolor="black", alpha=0.7
            )
            self.ax.set_xlabel("Infrastructure Cost ($)")
            self.ax.set_ylabel("Number of Simulations")
            self.ax.set_title(
                f"Live Cloud Infrastructure Cost Distribution (Iteration {iteration:,}/{total_iterations:,})"
            )
            self.ax.grid(True, linestyle="--", alpha=0.5)
            plt.draw()
            plt.pause(0.001)

    def finish_live_plot(self) -> None:
        """Turn off interactive mode and hold the final plot open."""
        plt.ioff()
        plt.show()

    def plot_cost_distribution(self, results: list[dict]) -> None:
        """Plot static cost histogram after simulation completes."""
        costs = [result["cost"] for result in results]

        plt.figure(figsize=(10, 6))
        plt.hist(costs, bins=50, color="skyblue", edgecolor="black", alpha=0.7)
        plt.xlabel("Infrastructure Cost ($)")
        plt.ylabel("Number of Simulations")
        plt.title("Cloud Infrastructure Cost Distribution")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.show()
