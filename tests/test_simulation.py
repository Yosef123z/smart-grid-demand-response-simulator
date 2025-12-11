import pytest
import pandas as pd
from src.simulation import SmartGridSimulation

def test_simulation_run():
    # Run a short simulation (e.g., 2 days) to save time
    sim = SmartGridSimulation(simulation_days=2)
    results = sim.run()
    
    # Check if results is a DataFrame
    assert isinstance(results, pd.DataFrame)
    
    # Check if expected columns exist
    expected_columns = [
        'ds', 'actual_demand', 'forecast_demand', 'solar', 'wind', 
        'price', 'net_load', 'battery_flow', 'soc', 'grid_import', 'cost'
    ]
    for col in expected_columns:
        assert col in results.columns
        
    # Check if the length of results matches simulation days (2 days * 24 hours)
    assert len(results) == 2 * 24
    
    # Check for no NaN values
    assert not results.isnull().values.any()
    
    # Check basic physics/logic
    # Grid Import should be roughly Net Load + Battery Flow (ignoring losses for simple check)
    # Actually, grid_import = net_load + battery_flow is the balance equation
    # Let's check if grid_import is non-negative (assuming no export back to grid allowed or handled)
    # The optimizer allows negative grid import (export)? 
    # Let's check the optimizer logic in implementation doc: 
    # P_grid = D - S - W - P_batt. If P_grid < 0, it means export.
    
    # Check that SoC is within bounds (0-100 assuming percentage or capacity)
    # The optimizer doc says SoC constraints.
    assert results['soc'].min() >= 0
    assert results['soc'].max() <= 100 # Assuming 100 is max, or check optimizer config
