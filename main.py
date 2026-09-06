import importlib
from config import ITERATIONS
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
            current_cost=result["cost"],
            iteration=current_iteration,
            total_iterations=total_iterations,
        )

    # 3. Run Monte Carlo simulation with live visualization
    print(f"Running simulation for {ITERATIONS:,} iterations...")
    results = engine.run(iterations=ITERATIONS, callback=live_callback)

    # 4. Calculate metrics
    metrics = metrics_calc.calculate(results)

    print("\n" + "=" * 60)
    print("  SIMULATION RESULTS & METRICS SUMMARY")
    print("=" * 60)
    print(f"Total Iterations : {len(results):,}")
    print(f"Average Cost     : ${metrics['average']:,.2f}")
    print(f"Median Cost      : ${metrics['median']:,.2f}")
    print(f"Minimum Cost     : ${metrics['minimum']:,.2f}")
    print(f"Maximum Cost     : ${metrics['maximum']:,.2f}")
    print(f"95th Percentile  : ${metrics['p95']:,.2f}")
    print("=" * 60)

    # 5. Keep final visualization graph displayed
    visualizer.finish_live_plot()


if __name__ == "__main__":
    main()
