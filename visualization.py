import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    """Visualizes discrete-event simulation performance metrics with live updating plots."""

    def __init__(self) -> None:
        self.fig = None
        self.axes = None
        self.last_update_time = -1.0

    def setup_live_plot(self) -> None:
        """Setup matplotlib interactive mode with 4 live visualization subplots."""
        plt.ion()
        self.fig, self.axes = plt.subplots(2, 2, figsize=(14, 10))
        self.fig.subplots_adjust(wspace=0.3, hspace=0.35, top=0.9, bottom=0.08)

    def update_live_plot(self, engine, current_time: float, force: bool = False) -> None:
        """Update live subplots for latency, queue depth, server utilization, and waiting times."""
        if self.fig is None or self.axes is None:
            self.setup_live_plot()

        # Update every 2 seconds of simulation time or when forced at simulation end
        if not force and (current_time - self.last_update_time < 2.0):
            return
        self.last_update_time = current_time

        completed = engine.completed_requests
        queue = engine.request_queue
        servers = engine.servers

        (ax1, ax2), (ax3, ax4) = self.axes

        # 1. Latency Distribution
        ax1.clear()
        if completed:
            latencies_ms = [r.latency * 1000 for r in completed]
            p50 = float(np.median(latencies_ms))
            p95 = float(np.percentile(latencies_ms, 95))
            p99 = float(np.percentile(latencies_ms, 99))

            ax1.hist(latencies_ms, bins=35, color="skyblue", edgecolor="black", alpha=0.7)
            ax1.axvline(p50, color="green", linestyle="--", label=f"P50: {p50:.1f}ms")
            ax1.axvline(p95, color="orange", linestyle="--", label=f"P95: {p95:.1f}ms")
            ax1.axvline(p99, color="red", linestyle="--", label=f"P99: {p99:.1f}ms")
            ax1.legend(loc="upper right", fontsize=8)

        ax1.set_xlabel("Latency (ms)")
        ax1.set_ylabel("Requests")
        ax1.set_title("Request Latency Distribution")
        ax1.grid(True, linestyle="--", alpha=0.5)

        # 2. Queue Depth Timeline
        ax2.clear()
        if queue.depth_history:
            q_times, q_depths = zip(*queue.depth_history)
            ax2.step(q_times, q_depths, where="post", color="darkred", linewidth=1.5)
        ax2.set_xlabel("Simulation Time (s)")
        ax2.set_ylabel("Queue Depth")
        ax2.set_title(f"Request Queue Depth (Current: {len(queue)})")
        ax2.grid(True, linestyle="--", alpha=0.5)

        # 3. Server Utilization
        ax3.clear()
        s_names = [f"Server {s.id}" for s in servers]
        s_utils = [
            (s.total_busy_time / current_time * 100) if current_time > 0 else 0.0
            for s in servers
        ]
        bars3 = ax3.bar(s_names, s_utils, color="teal", edgecolor="black", alpha=0.8)
        ax3.set_ylabel("Utilization (%)")
        ax3.set_title("Server Utilization")
        ax3.set_ylim(0, 110)
        ax3.grid(True, linestyle="--", alpha=0.5)

        for bar in bars3:
            h = bar.get_height()
            ax3.text(
                bar.get_x() + bar.get_width() / 2.0,
                h + 1,
                f"{h:.1f}%",
                ha="center",
                va="bottom",
                fontsize=8,
            )

        # 4. Waiting Time Distribution
        ax4.clear()
        if completed:
            waiting_ms = [r.waiting_time * 1000 for r in completed]
            ax4.hist(waiting_ms, bins=35, color="mediumpurple", edgecolor="black", alpha=0.7)
        ax4.set_xlabel("Queue Waiting Time (ms)")
        ax4.set_ylabel("Requests")
        ax4.set_title("Queue Waiting Time Distribution")
        ax4.grid(True, linestyle="--", alpha=0.5)

        self.fig.suptitle(
            f"Live Discrete-Event Simulator (Time: {current_time:.2f}s | Processed: {len(completed):,})",
            fontsize=13,
            fontweight="bold",
        )
        plt.draw()
        plt.pause(0.001)

    def finish_live_plot(self) -> None:
        """Turn off interactive mode and hold the final plot open."""
        plt.ioff()
        plt.show()

    def plot_latency_distribution(self, simulation_result: dict) -> None:
        """Plot request latency histogram with P50, P95, and P99 percentiles."""
        completed = simulation_result["completed_requests"]
        if not completed:
            print("No completed requests to plot.")
            return

        latencies = [r.latency * 1000 for r in completed]
        p50 = float(np.median(latencies))
        p95 = float(np.percentile(latencies, 95))
        p99 = float(np.percentile(latencies, 99))

        plt.figure(figsize=(10, 6))
        plt.hist(latencies, bins=50, color="skyblue", edgecolor="black", alpha=0.7)

        plt.axvline(p50, color="green", linestyle="--", linewidth=2, label=f"P50 ({p50:.1f} ms)")
        plt.axvline(p95, color="orange", linestyle="--", linewidth=2, label=f"P95 ({p95:.1f} ms)")
        plt.axvline(p99, color="red", linestyle="--", linewidth=2, label=f"P99 ({p99:.1f} ms)")

        plt.xlabel("Latency (ms)")
        plt.ylabel("Request Count")
        plt.title("Cloud Request Latency Distribution")
        plt.legend(loc="upper right", fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.show()

    def plot_dashboard(self, simulation_result: dict) -> None:
        """Static plot wrapper."""
        self.plot_latency_distribution(simulation_result)
