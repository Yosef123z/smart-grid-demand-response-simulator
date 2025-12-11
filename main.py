from src.simulation import SmartGridSimulation
import os
import warnings
warnings.filterwarnings("ignore")


def main():
    """
    Entry point for the Smart Grid Simulation.

    This script:
    1. Initializes the simulation environment.
    2. Runs the simulation (Data Gen -> Forecast -> Optimize).
    3. Saves the results to 'data/simulation_results.csv'.
    """
    print("Starting Smart Grid Simulation...")

    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Initialize the simulation
    # We simulate 30 days of operation (plus 30 days of history for training)
    sim = SmartGridSimulation(simulation_days=30)

    # Run the simulation
    results = sim.run()

    # Save results to CSV
    output_path = 'data/simulation_results.csv'
    results.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")
    print("You can now run 'streamlit run dashboard.py' to view the results.")


if __name__ == "__main__":
    main()
