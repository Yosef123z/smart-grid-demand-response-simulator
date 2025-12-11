import pandas as pd
from src.optimizer import GridOptimizer
from src.forecaster import DemandForecaster
from src.data_generator import (
    generate_demand_data,
    generate_solar_data,
    generate_wind_data,
    generate_price_data
)


class SmartGridSimulation:
    """
    Orchestrates the entire Smart Grid Digital Twin simulation.

    Workflow:
    1. Generate synthetic data (Demand, Solar, Wind, Prices).
    2. Split data into 'History' (for training) and 'Simulation' (for testing).
    3. Train the Demand Forecaster on historical data.
    4. Predict future demand.
    5. Run the Grid Optimizer to manage battery storage.
    6. Combine and save results.
    """

    def __init__(self, simulation_days=30):
        """
        Args:
            simulation_days (int): Number of days to simulate in test phase.
                                   (We generate double this amount).
        """
        self.simulation_days = simulation_days
        self.forecaster = DemandForecaster()
        self.optimizer = GridOptimizer()

    def run(self):
        """
        Executes the simulation pipeline.

        Returns:
            pd.DataFrame: The final results containing all simulation data.
        """
        # 1. Generate Data
        # We generate 2x days: First half for training, second half for test.
        total_days = self.simulation_days * 2
        print(f"Generating data for {total_days} days...")

        demand = generate_demand_data(days=total_days)
        solar = generate_solar_data(days=total_days)
        wind = generate_wind_data(days=total_days)
        prices = generate_price_data(days=total_days)

        # Merge into one DataFrame for easier handling
        data = demand.merge(solar, on='ds').merge(
            wind, on='ds'
        ).merge(prices, on='ds')

        # 2. Split Data
        # Training Data: First 'simulation_days'
        # Simulation Data: The rest
        cutoff_date = data['ds'].iloc[self.simulation_days * 24]
        history_data = data[data['ds'] < cutoff_date].copy()
        sim_data = data[
            data['ds'] >= cutoff_date
        ].copy().reset_index(drop=True)

        print(
            f"Training Forecaster on {len(history_data)} hours of history..."
        )

        # 3. Train Forecaster
        self.forecaster.train(history_data[['ds', 'y']])

        # 4. Forecast Demand
        print("Forecasting future demand...")
        forecast = self.forecaster.predict(horizon_hours=len(sim_data))

        # 5. Optimize Battery Dispatch
        print("Optimizing battery dispatch...")
        # Calculate Net Load: Demand - (Solar + Wind)
        # This is the load the grid/battery needs to serve.
        net_load = sim_data['y'] - (sim_data['solar'] + sim_data['wind'])

        # Run the optimizer
        opt_results = self.optimizer.optimize_dispatch(
            net_load, sim_data['price']
        )

        # 6. Combine Results
        final_results = pd.concat([
            sim_data,
            opt_results[['battery_flow', 'soc', 'grid_import']]
        ], axis=1)

        # Add the forecast for comparison
        final_results['forecast_demand'] = forecast['yhat'].values

        # Ensure all columns expected by tests and dashboard are present
        # 'y' is 'actual_demand'
        final_results['actual_demand'] = final_results['y']

        # 'net_load' was calculated for optimizer but not saved in opt_results
        # Recalculate or retrieve. It's in opt_results if we returned it.
        # Let's check optimizer.py. Yes, it returns 'net_load'.
        final_results['net_load'] = opt_results['net_load']

        # 'cost' is not returned by optimizer in my updated version?
        # Let's check optimizer.py.
        # My updated optimizer.py returns:
        # ['net_load', 'battery_flow', 'soc', 'grid_import'].
        # It does NOT return 'cost'. I need to calculate it here.
        # Cost = Grid Import * Price
        final_results['cost'] = (
            final_results['grid_import'] * final_results['price']
        )

        print("Simulation complete.")
        return final_results
