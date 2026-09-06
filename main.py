import importlib
from config import ITERATIONS, NUMBER_OF_SERVERS
from engine import MonteCarloEngine
from metrics import MetricsCalculator
from model import CloudModel
from visualization import Visualizer

# Dynamically import module with hyphen in filename
rng_module = importlib.import_module("random-number-generator")
RandomNumberGenerator = rng_module.RandomNumberGenerator


def main():
    print("=" * 60)
    print("  Starting Monte Carlo Cloud Infrastructure Cost Simulation")
    print("=" * 60)

    # 1. Initialize components
    generator = RandomNumberGenerator()
    model = CloudModel()
    engine = MonteCarloEngine(generator=generator, model=model)
    metrics_calc = MetricsCalculator()
    visualizer = Visualizer()

    # 2. Setup live plotting
    visualizer.setup_live_plot()

    def live_callback(result: dict, current_iteration: int, total_iterations: int):
        visualizer.update_live_plot(
            result=result,
            iteration=current_iteration,
            total_iterations=total_iterations,
        )

    # 3. Run Monte Carlo simulation with live visualization
    print(f"Running simulation for {ITERATIONS:,} iterations ({NUMBER_OF_SERVERS} servers)...")
    results = engine.run(iterations=ITERATIONS, callback=live_callback)

    # 4. Calculate metrics
    metrics = metrics_calc.calculate(results)

    print("\n" + "=" * 60)
    print("  SIMULATION RESULTS & METRICS SUMMARY")
    print("=" * 60)
    print(f"Total Iterations     : {len(results):,}")
    print(f"Number of Servers    : {NUMBER_OF_SERVERS}")
    print(f"Average Cost         : ${metrics['average']:,.2f}")
    print(f"Median Cost          : ${metrics['median']:,.2f}")
    print(f"Minimum Cost         : ${metrics['minimum']:,.2f}")
    print(f"Maximum Cost         : ${metrics['maximum']:,.2f}")
    print(f"95th Percentile Cost : ${metrics['p95']:,.2f}")
    print(f"System Failure Rate  : {metrics['system_failure_rate'] * 100:.2f}%")
    print(f"Avg Failed Servers   : {metrics['avg_failed_servers']:.2f}")
    print(f"Avg Dropped Requests : {metrics['avg_dropped_requests']:,.0f}")
    print(f"Max Dropped Requests : {metrics['max_dropped_requests']:,.0f}")

    print("\n--- Per-Server Failures Breakdown ---")
    for s_name, f_cnt in metrics["per_server_failures"].items():
        fail_pct = (f_cnt / len(results)) * 100
        print(f"  {s_name:10s} : {f_cnt:,} failures ({fail_pct:.2f}%)")
    print("=" * 60)

    # 5. Keep final visualization graph displayed
    visualizer.finish_live_plot()


if __name__ == "__main__":
    main()
