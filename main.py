import importlib
from config import (
    AUTOSCALE_DOWN_THRESHOLD,
    AUTOSCALE_UP_THRESHOLD,
    HOURS_PER_SIMULATION,
    MAX_SERVERS,
    MIN_SERVERS,
    SIMULATIONS,
)
from engine import MonteCarloEngine
from metrics import MetricsCalculator
from model import CloudModel
from visualization import Visualizer

# Dynamically import module with hyphen in filename
rng_module = importlib.import_module("random-number-generator")
RandomNumberGenerator = rng_module.RandomNumberGenerator


def main():
    print("=" * 75)
    print("  Starting 24-Hour Time-Stepped Monte Carlo Cloud Simulation")
    print("=" * 75)

    # 1. Initialize components
    generator = RandomNumberGenerator()
    model = CloudModel()
    engine = MonteCarloEngine(generator=generator, model=model)
    metrics_calc = MetricsCalculator()
    visualizer = Visualizer()

    # 2. Print sample 24-hour simulation breakdown for Day #1
    sample_day = model.run_day(rng=generator)
    print("\nSample 24-Hour Simulation Timeline (Day #1):")
    print(f"{'Hour':<6} {'Traffic (Req)':<15} {'Servers':<9} {'Utilization':<13} {'Cost ($)':<10} {'Action':<10}")
    print("─" * 75)
    for log in sample_day["hourly_logs"]:
        print(
            f"{log['hour']:02d}:00   "
            f"{log['requests']:11,.0f} req   "
            f"{log['servers']:<9d} "
            f"{log['utilization'] * 100:6.1f}%       "
            f"${log['cost']:<8.2f} "
            f"{log['action']}"
        )
    print("─" * 75)

    # 3. Setup live plotting
    visualizer.setup_live_plot()

    def live_callback(result: dict, current_iteration: int, total_iterations: int):
        visualizer.update_live_plot(
            result=result,
            iteration=current_iteration,
            total_iterations=total_iterations,
        )

    # 4. Run Monte Carlo simulation across all days
    print(
        f"\nRunning Monte Carlo simulation for {SIMULATIONS:,} days "
        f"({HOURS_PER_SIMULATION} hours/day, Base: {MIN_SERVERS}, Max: {MAX_SERVERS}, "
        f"Scale Up: >{AUTOSCALE_UP_THRESHOLD*100:.0f}%, Scale Down: <{AUTOSCALE_DOWN_THRESHOLD*100:.0f}%)..."
    )
    results = engine.run(simulations=SIMULATIONS, callback=live_callback)

    # 5. Calculate metrics
    metrics = metrics_calc.calculate(results)

    print("\n" + "=" * 75)
    print("  TIME-STEPPED SIMULATION METRICS & RELIABILITY SUMMARY")
    print("=" * 75)
    print(f"Total Simulated Days  : {len(results):,}")
    print(f"Hours per Simulation  : {HOURS_PER_SIMULATION}")
    print(f"Min / Max Servers     : {MIN_SERVERS} / {MAX_SERVERS}")
    print(f"Average Daily Cost    : ${metrics['average_cost']:,.2f}")
    print(f"Median Daily Cost     : ${metrics['median_cost']:,.2f}")
    print(f"95th Percentile Cost  : ${metrics['p95_cost']:,.2f}")
    print(f"Outage Probability    : {metrics['system_failure_rate'] * 100:.2f}% (Days with dropped requests)")
    print(f"Avg Servers Provisioned: {metrics['avg_servers_used']:.2f}")
    print(f"Max Servers Required   : {metrics['max_servers_required']}")
    print(f"Avg Hourly Utilization : {metrics['avg_utilization'] * 100:.1f}%")
    print(f"Avg Dropped Req / Day  : {metrics['avg_dropped_requests']:,.0f}")
    print("=" * 75)

    # 6. Keep final visualization graph displayed
    visualizer.finish_live_plot()


if __name__ == "__main__":
    main()
