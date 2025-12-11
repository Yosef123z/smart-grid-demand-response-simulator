"""
Smart Grid Demand-Response Simulator

A Digital Twin simulation for modeling electricity demand patterns,
renewable energy integration, and battery storage optimization.

Modules:
    data_generator: Synthetic data generation for grid simulation
    forecaster: Demand forecasting using Prophet
    optimizer: Battery dispatch optimization
    simulation: Main simulation orchestrator
"""

from src.data_generator import (
    generate_demand_data,
    generate_solar_data,
    generate_wind_data,
    generate_price_data
)
from src.forecaster import DemandForecaster
from src.optimizer import GridOptimizer
from src.simulation import SmartGridSimulation

__version__ = "1.0.0"
__author__ = "Smart Grid Simulator Team"

__all__ = [
    "generate_demand_data",
    "generate_solar_data",
    "generate_wind_data",
    "generate_price_data",
    "DemandForecaster",
    "GridOptimizer",
    "SmartGridSimulation",
]
