import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    """Visualizes Monte Carlo simulation results with cost, server failures, system reliability, and capacity boundary plots."""

    def __init__(self) -> None:
        self.fig = None
        self.axes = None
        self.results_history = []

    def setup_live_plot(self) -> None:
        """Setup matplotlib interactive mode with 4 live visualization subplots."""
        plt.ion()
        self.fig, self.axes = plt.subplots(2, 2, figsize=(14, 10))
        self.fig.subplots_adjust(wspace=0.3, hspace=0.35, top=0.9, bottom=0.08)

    def update_live_plot(
        self, result: dict, iteration: int, total_iterations: int
    ) -> None:
        """Update live subplots for cost, server failures, system reliability, and requests vs capacity boundary."""
        if self.fig is None or self.axes is None:
            self.setup_live_plot()

        self.results_history.append(result)

        # Refresh plot periodically (every 1% of total iterations) for smooth animation
        update_interval = max(1, total_iterations // 100)
        if iteration % update_interval == 0 or iteration == total_iterations:
            (ax1, ax2), (ax3, ax4) = self.axes

            costs = [r["cost"] for r in self.results_history]
            requests = [r["requests"] for r in self.results_history]
            capacities = [r["available_capacity"] for r in self.results_history]
            system_failed = [r.get("system_failed", False) for r in self.results_history]

            # Subplot 1: Infrastructure Cost Distribution
            ax1.clear()
            ax1.hist(costs, bins=35, color="skyblue", edgecolor="black", alpha=0.7)
            ax1.set_xlabel("Cost ($)")
            ax1.set_ylabel("Frequency")
            ax1.set_title("Infrastructure Cost Distribution")
            ax1.grid(True, linestyle="--", alpha=0.5)

            # Subplot 2: Per-Server Failure Count
            ax2.clear()
            num_servers = (
                len(self.results_history[0]["server_failures"])
                if self.results_history and "server_failures" in self.results_history[0]
                else 0
            )
            server_labels = [f"Server {idx + 1}" for idx in range(num_servers)]
            server_counts = [
                sum(1 for r in self.results_history if r["server_failures"][idx])
                for idx in range(num_servers)
            ]
            bars2 = ax2.bar(
                server_labels, server_counts, color="salmon", edgecolor="black", alpha=0.8
            )
            ax2.set_xlabel("Server")
            ax2.set_ylabel("Failure Count")
            ax2.set_title("Server Failure Counts")
            ax2.grid(True, linestyle="--", alpha=0.5)

            for bar in bars2:
                yval = bar.get_height()
                if yval > 0:
                    ax2.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        yval + 0.5,
                        f"{int(yval)}",
                        ha="center",
                        va="bottom",
                        fontsize=9,
                    )

            # Subplot 3: System Reliability (Healthy vs Failed)
            ax3.clear()
            failed_cnt = sum(1 for f in system_failed if f)
            healthy_cnt = len(system_failed) - failed_cnt
            fail_pct = (failed_cnt / len(system_failed)) * 100
            healthy_pct = 100.0 - fail_pct

            bars3 = ax3.bar(
                ["Healthy", "Failed"],
                [healthy_cnt, failed_cnt],
                color=["lightgreen", "crimson"],
                edgecolor="black",
                alpha=0.8,
            )
            ax3.set_ylabel("Simulation Count")
            ax3.set_title(f"System Reliability (Fail Rate: {fail_pct:.1f}%)")
            ax3.grid(True, linestyle="--", alpha=0.5)

            if len(bars3) >= 2:
                ax3.text(
                    bars3[0].get_x() + bars3[0].get_width() / 2.0,
                    healthy_cnt + 0.5,
                    f"{healthy_pct:.1f}%",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )
                ax3.text(
                    bars3[1].get_x() + bars3[1].get_width() / 2.0,
                    failed_cnt + 0.5,
                    f"{fail_pct:.1f}%",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

            # Subplot 4: Capacity vs Requests (Scatter plot boundary)
            ax4.clear()
            req_arr = np.array(requests)
            cap_arr = np.array(capacities)
            fail_arr = np.array(system_failed)

            # Plot healthy (green) and failed (red)
            if np.any(~fail_arr):
                ax4.scatter(
                    req_arr[~fail_arr],
                    cap_arr[~fail_arr],
                    color="green",
                    alpha=0.4,
                    label="Healthy",
                    s=12,
                )
            if np.any(fail_arr):
                ax4.scatter(
                    req_arr[fail_arr],
                    cap_arr[fail_arr],
                    color="red",
                    alpha=0.7,
                    label="System Failed",
                    s=16,
                )

            # 1:1 Reference Line (Capacity == Requests)
            max_val = max(max(requests, default=100), max(capacities, default=100))
            ax4.plot(
                [0, max_val],
                [0, max_val],
                "k--",
                linewidth=1.2,
                label="Capacity Boundary",
            )

            ax4.set_xlabel("Requests")
            ax4.set_ylabel("Available Capacity")
            ax4.set_title("Requests vs Capacity Boundary")
            ax4.legend(loc="upper left", fontsize=9)
            ax4.grid(True, linestyle="--", alpha=0.5)

            self.fig.suptitle(
                f"Live Monte Carlo Simulation (Iteration {iteration:,}/{total_iterations:,})",
                fontsize=14,
                fontweight="bold",
            )
            plt.draw()
            plt.pause(0.001)

    def finish_live_plot(self) -> None:
        """Turn off interactive mode and hold the final plot open."""
        plt.ioff()
        plt.show()

    def plot_cost_distribution(self, results: list[dict]) -> None:
        """Plot cost distribution histogram."""
        costs = [r["cost"] for r in results]
        plt.figure(figsize=(8, 5))
        plt.hist(costs, bins=40, color="skyblue", edgecolor="black", alpha=0.7)
        plt.xlabel("Infrastructure Cost ($)")
        plt.ylabel("Frequency")
        plt.title("Cloud Infrastructure Cost Distribution")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.show()

    def plot_server_failures(self, results: list[dict]) -> None:
        """Plot failure count per individual server."""
        if not results or "server_failures" not in results[0]:
            return

        num_servers = len(results[0]["server_failures"])
        server_labels = [f"Server {idx + 1}" for idx in range(num_servers)]
        server_counts = [
            sum(1 for r in results if r["server_failures"][idx])
            for idx in range(num_servers)
        ]

        plt.figure(figsize=(8, 5))
        bars = plt.bar(
            server_labels, server_counts, color="salmon", edgecolor="black", alpha=0.8
        )
        plt.xlabel("Server")
        plt.ylabel("Total Failures")
        plt.title(f"Server Failure Counts ({len(results):,} Iterations)")
        plt.grid(True, linestyle="--", alpha=0.5)

        for bar in bars:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                yval + 1,
                f"{int(yval)}",
                ha="center",
                va="bottom",
            )

        plt.show()

    def plot_system_failures(self, results: list[dict]) -> None:
        """Plot system failure probability (Healthy vs Failed)."""
        system_failed = [r.get("system_failed", False) for r in results]
        failed_cnt = sum(1 for f in system_failed if f)
        healthy_cnt = len(system_failed) - failed_cnt
        fail_pct = (failed_cnt / len(system_failed)) * 100

        plt.figure(figsize=(7, 5))
        bars = plt.bar(
            ["Healthy", "System Failed"],
            [healthy_cnt, failed_cnt],
            color=["lightgreen", "crimson"],
            edgecolor="black",
            alpha=0.8,
        )
        plt.ylabel("Simulation Count")
        plt.title(f"System Reliability Breakdown (Failure Rate: {fail_pct:.2f}%)")
        plt.grid(True, linestyle="--", alpha=0.5)

        for bar in bars:
            yval = bar.get_height()
            pct = (yval / len(system_failed)) * 100
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                yval + 1,
                f"{int(yval):,} ({pct:.1f}%)",
                ha="center",
                va="bottom",
            )

        plt.show()

    def plot_capacity_vs_requests(self, results: list[dict]) -> None:
        """Plot Requests vs Available Capacity boundary scatter plot."""
        requests = np.array([r["requests"] for r in results])
        capacities = np.array([r["available_capacity"] for r in results])
        system_failed = np.array([r.get("system_failed", False) for r in results])

        plt.figure(figsize=(9, 6))

        if np.any(~system_failed):
            plt.scatter(
                requests[~system_failed],
                capacities[~system_failed],
                color="green",
                alpha=0.4,
                label="Healthy",
                s=15,
            )
        if np.any(system_failed):
            plt.scatter(
                requests[system_failed],
                capacities[system_failed],
                color="red",
                alpha=0.7,
                label="System Failed",
                s=20,
            )

        max_val = max(np.max(requests), np.max(capacities))
        plt.plot(
            [0, max_val],
            [0, max_val],
            "k--",
            linewidth=1.5,
            label="Capacity Boundary (Requests = Capacity)",
        )

        plt.xlabel("Number of Requests")
        plt.ylabel("Available Capacity")
        plt.title("Simulation Capacity vs Requests Boundary Analysis")
        plt.legend(loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.show()
