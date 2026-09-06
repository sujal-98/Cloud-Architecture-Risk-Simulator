import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    """Visualizes 24-hour time-stepped Monte Carlo simulation results."""

    def __init__(self) -> None:
        self.fig = None
        self.axes = None
        self.results_history = []

    def setup_live_plot(self) -> None:
        """Setup matplotlib interactive mode with 4 subplots for 24-hour simulation metrics."""
        plt.ion()
        self.fig, self.axes = plt.subplots(2, 2, figsize=(15, 10))
        self.fig.subplots_adjust(wspace=0.3, hspace=0.35, top=0.9, bottom=0.08)

    def update_live_plot(
        self, result: dict, iteration: int, total_iterations: int
    ) -> None:
        """Update live subplots for diurnal timeline, cost distribution, outage reliability, and max server capacity."""
        if self.fig is None or self.axes is None:
            self.setup_live_plot()

        self.results_history.append(result)

        # Refresh plot periodically (every 1% of total iterations) for smooth rendering
        update_interval = max(1, total_iterations // 100)
        if iteration % update_interval == 0 or iteration == total_iterations:
            (ax1, ax2), (ax3, ax4) = self.axes

            costs = [r["total_cost"] for r in self.results_history]
            max_servers = [r["max_servers_needed"] for r in self.results_history]
            system_failed = [r["system_failed"] for r in self.results_history]

            # Aggregate 24-hour diurnal profile across recorded days
            hours = list(range(24))
            avg_hourly_req = [
                np.mean([day["hourly_logs"][h]["requests"] for day in self.results_history])
                for h in hours
            ]
            avg_hourly_cap = [
                np.mean([day["hourly_logs"][h]["available_capacity"] for day in self.results_history])
                for h in hours
            ]
            avg_hourly_srv = [
                np.mean([day["hourly_logs"][h]["servers"] for day in self.results_history])
                for h in hours
            ]

            # Subplot 1: 24-Hour Diurnal Traffic & Capacity Profile
            ax1.clear()
            ax1.plot(hours, avg_hourly_req, "b-o", label="Traffic (Requests)", linewidth=2, markersize=4)
            ax1.plot(hours, avg_hourly_cap, "g--", label="Capacity", linewidth=2)
            ax1.set_xlabel("Hour of Day (0..23)")
            ax1.set_ylabel("Requests / Capacity")
            ax1.set_title("Average 24-Hour Diurnal Traffic & Capacity")
            ax1.set_xticks(range(0, 24, 2))
            ax1.legend(loc="upper left", fontsize=9)
            ax1.grid(True, linestyle="--", alpha=0.5)

            # Subplot 2: Daily Infrastructure Cost Distribution
            ax2.clear()
            ax2.hist(costs, bins=35, color="skyblue", edgecolor="black", alpha=0.7)
            ax2.set_xlabel("Daily Cost ($)")
            ax2.set_ylabel("Frequency")
            ax2.set_title("24-Hour Infrastructure Cost Distribution")
            ax2.grid(True, linestyle="--", alpha=0.5)

            # Subplot 3: System Reliability (Healthy vs Outage Days)
            ax3.clear()
            failed_cnt = sum(1 for f in system_failed if f)
            healthy_cnt = len(system_failed) - failed_cnt
            fail_pct = (failed_cnt / len(system_failed)) * 100
            healthy_pct = 100.0 - fail_pct

            bars3 = ax3.bar(
                ["Healthy Day", "Outage Day"],
                [healthy_cnt, failed_cnt],
                color=["lightgreen", "crimson"],
                edgecolor="black",
                alpha=0.8,
            )
            ax3.set_ylabel("Simulated Days")
            ax3.set_title(f"System Reliability (Outage Rate: {fail_pct:.1f}%)")
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

            # Subplot 4: Max Servers Required Distribution (Capacity Planning)
            ax4.clear()
            max_s_val = max(max_servers, default=3)
            min_s_val = min(max_servers, default=3)
            bins4 = range(min_s_val, max_s_val + 2)
            ax4.hist(
                max_servers,
                bins=bins4,
                color="plum",
                edgecolor="black",
                alpha=0.8,
                align="left",
                rwidth=0.8,
            )
            ax4.set_xlabel("Max Servers Required per Day")
            ax4.set_ylabel("Frequency")
            ax4.set_title("Peak Server Capacity Demand")
            ax4.grid(True, linestyle="--", alpha=0.5)

            self.fig.suptitle(
                f"Live 24-Hour Time-Stepped Monte Carlo Simulation (Day {iteration:,}/{total_iterations:,})",
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
        """Plot daily cost distribution."""
        costs = [r["total_cost"] for r in results]
        plt.figure(figsize=(8, 5))
        plt.hist(costs, bins=40, color="skyblue", edgecolor="black", alpha=0.7)
        plt.xlabel("Daily Cost ($)")
        plt.ylabel("Frequency")
        plt.title("24-Hour Infrastructure Cost Distribution")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.show()

    def plot_system_failures(self, results: list[dict]) -> None:
        """Plot system outage reliability breakdown."""
        system_failed = [r["system_failed"] for r in results]
        failed_cnt = sum(1 for f in system_failed if f)
        healthy_cnt = len(system_failed) - failed_cnt
        fail_pct = (failed_cnt / len(system_failed)) * 100

        plt.figure(figsize=(7, 5))
        bars = plt.bar(
            ["Healthy Day", "Outage Day"],
            [healthy_cnt, failed_cnt],
            color=["lightgreen", "crimson"],
            edgecolor="black",
            alpha=0.8,
        )
        plt.ylabel("Simulated Days")
        plt.title(f"System Outage Reliability (Failure Rate: {fail_pct:.2f}%)")
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
