from config import (
    ARRIVAL_RATE,
    AVG_SERVICE_TIME,
    NUM_SERVERS,
    SIMULATION_DURATION,
)
from engine import DiscreteEventEngine
from generator import RequestGenerator
from metrics import MetricsCalculator
from visualization import Visualizer


def main():
    print("=" * 75)
    print("  Discrete-Event Cloud Request Processing Simulator")
    print("=" * 75)
    print(f"Simulation Duration : {SIMULATION_DURATION} seconds")
    print(f"Arrival Rate        : {ARRIVAL_RATE} requests/second")
    print(f"Avg Service Time    : {AVG_SERVICE_TIME * 1000:.1f} ms")
    print(f"Server Pool Size    : {NUM_SERVERS} servers")
    print("=" * 75)

    # 1. Initialize components
    generator = RequestGenerator()
    engine = DiscreteEventEngine(generator=generator, num_servers=NUM_SERVERS)
    metrics_calc = MetricsCalculator()
    visualizer = Visualizer()

    # 2. Setup live plotting
    visualizer.setup_live_plot()

    def live_callback(event, current_time: float):
        visualizer.update_live_plot(engine, current_time)

    # 3. Execute discrete-event simulation engine with live visualization
    print("\nRunning discrete-event priority queue simulation...")
    simulation_result = engine.run(step_callback=live_callback)

    # Force final update to ensure full results are rendered
    visualizer.update_live_plot(engine, engine.current_time, force=True)

    # 4. Print sample event log
    print("\nSample Event Execution Trace (First 15 Events):")
    print(f"{'Time (s)':<10} {'Event':<20} {'Req ID':<8} {'Server':<10} {'Latency (ms)':<15}")
    print("─" * 75)
    for log in simulation_result["event_log"][:15]:
        server_str = f"Server {log['server_id']}" if "server_id" in log else "-"
        latency_str = f"{log['latency']*1000:8.2f} ms" if "latency" in log else "-"
        print(
            f"{log['time']:<10.4f} "
            f"{log['event']:<20} "
            f"R{log['req_id']:<7d} "
            f"{server_str:<10} "
            f"{latency_str:<15}"
        )
    print("─" * 75)

    # 5. Calculate metrics
    metrics = metrics_calc.calculate(simulation_result)

    print("\n" + "=" * 75)
    print("  SIMULATION METRICS & LATENCY SUMMARY")
    print("=" * 60)
    print(f"Total Requests Processed : {metrics['total_completed']:,}")
    print(f"Total Requests Dropped   : {metrics['total_dropped']:,}")
    print(f"Throughput               : {metrics['throughput_req_per_sec']:.2f} requests/sec")
    print(f"Overall Cluster Util.    : {metrics['overall_utilization_pct']:.2f}%")
    print("─" * 75)
    print(f"Average Latency          : {metrics['avg_latency']*1000:.2f} ms")
    print(f"P50 Latency (Median)     : {metrics['p50_latency']*1000:.2f} ms")
    print(f"P95 Latency              : {metrics['p95_latency']*1000:.2f} ms")
    print(f"P99 Latency              : {metrics['p99_latency']*1000:.2f} ms")
    print(f"Max Latency              : {metrics['max_latency']*1000:.2f} ms")
    print("─" * 75)
    print(f"Average Waiting Time     : {metrics['avg_waiting_time']*1000:.2f} ms")
    print(f"P95 Waiting Time         : {metrics['p95_waiting_time']*1000:.2f} ms")
    print(f"Max Queue Depth          : {metrics['max_queue_depth']} requests")
    print("─" * 75)
    print("Per-Server Utilization:")
    for s_name, s_info in metrics["per_server_stats"].items():
        print(f"  {s_name}: Processed {s_info['processed']:,} requests ({s_info['utilization']:.1f}% busy)")
    print("=" * 75)

    # 6. Hold interactive plot open
    visualizer.finish_live_plot()


if __name__ == "__main__":
    main()
