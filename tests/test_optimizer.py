import pytest
import pandas as pd
import numpy as np
from src.optimizer import GridOptimizer

def test_optimizer_dispatch():
    optimizer = GridOptimizer(battery_capacity=100, max_power=50)
    
    # Create dummy inputs
    n = 24
    net_load = pd.Series(np.zeros(n))
    prices = pd.Series(np.ones(n) * 0.10)
    
    # Test 1: Excess Renewable (Negative Load) -> Should Charge
    net_load[0] = -20
    results = optimizer.optimize_dispatch(net_load, prices)
    assert results['battery_flow'][0] > 0 # Charging
    
    # Test 2: High Price -> Should Discharge
    prices[1] = 1.0 # Very high
    results = optimizer.optimize_dispatch(net_load, prices)
    assert results['battery_flow'][1] < 0 # Discharging
    
    # Test 3: Constraints
    net_load[2] = -200 # Huge excess
    results = optimizer.optimize_dispatch(net_load, prices)
    assert results['battery_flow'][2] <= 50 # Max power constraint
