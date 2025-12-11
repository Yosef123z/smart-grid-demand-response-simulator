import pandas as pd
import numpy as np


class GridOptimizer:
    """
    Optimizes battery dispatch (charge/discharge) to balance the grid.

    Uses a heuristic (rule-based) approach to:
    1. Store excess renewable energy (Solar/Wind > Demand).
    2. Discharge during peak demand to prevent grid overload.
    3. Perform price arbitrage (Buy low, Sell high).
    """

    def __init__(self, battery_capacity=100, max_power=50, efficiency=0.9):
        """
        Args:
            battery_capacity (float): Max energy storage in MWh.
            max_power (float): Max charge/discharge rate in MW.
            efficiency (float): Round-trip efficiency (0.0 to 1.0).
        """
        self.battery_capacity = battery_capacity
        self.max_power = max_power
        self.efficiency = efficiency

    def optimize_dispatch(self, net_load, prices):
        """
        Calculates the optimal battery schedule.

        Args:
            net_load (pd.Series): Demand - (Solar + Wind).
                                  Positive = Deficit (Need Grid/Battery).
                                  Negative = Excess (Renewables > Demand).
            prices (pd.Series): Electricity prices ($/kWh).

        Returns:
            pd.DataFrame: Results with columns ['net_load', 'battery_flow',
                                                'soc', 'grid_import'].
        """
        n = len(net_load)
        battery_flow = np.zeros(n)  # +ve = Charge, -ve = Discharge
        soc = np.zeros(n)           # State of Charge (MWh)
        current_soc = self.battery_capacity * 0.5  # Start at 50% charge

        # Calculate thresholds for decision making
        # We use percentiles to adapt to the specific data range.
        price_low = np.percentile(prices, 25)   # Cheap electricity
        price_high = np.percentile(prices, 75)  # Expensive electricity
        load_peak = np.percentile(net_load, 90)  # Very high demand

        for i in range(n):
            load = net_load.iloc[i]
            price = prices.iloc[i]
            action = 0  # Default: Do nothing

            # --- DECISION LOGIC ---

            # Priority 1: Absorb Excess Renewables (Self-Consumption)
            # If load is negative, we have free energy. Charge it!
            if load < 0:
                action = -load  # Charge exactly the excess amount

            # Priority 2: Peak Shaving (Grid Stability)
            # If demand is too high, discharge to help the grid.
            elif load > load_peak:
                action = -(load - load_peak)  # Discharge to cap the peak

            # Priority 3: Price Arbitrage (Economics)
            # If price is high, sell (discharge).
            elif price > price_high:
                action = -self.max_power
            # If price is low, buy (charge).
            elif price < price_low:
                action = self.max_power

            # --- CONSTRAINTS CHECK ---

            # 1. Power Limit: Cannot exceed max inverter rating
            action = np.clip(action, -self.max_power, self.max_power)

            # 2. Energy Limit (SoC): Cannot overcharge or over-discharge
            if action > 0:  # Charging
                # Max energy we can fit into the battery
                max_possible_charge = (
                    (self.battery_capacity - current_soc) / self.efficiency
                )
                action = min(action, max_possible_charge)
                # Update SoC (Accounting for efficiency loss)
                current_soc += action * self.efficiency

            else:  # Discharging
                # Max energy we can take out of the battery
                max_possible_discharge = current_soc * self.efficiency
                if abs(action) > max_possible_discharge:
                    action = -max_possible_discharge
                # Update SoC (Discharging reduces stored energy)
                # Note: Efficiency applies on output
                current_soc += action / self.efficiency

            # Store results
            battery_flow[i] = action
            soc[i] = current_soc

        # Calculate Grid Import
        # Grid Import = Net Load + Battery Charging (positive flow)
        # If Battery Discharges (negative flow), it reduces Grid Import.
        grid_import = net_load + battery_flow

        return pd.DataFrame({
            'net_load': net_load,
            'battery_flow': battery_flow,
            'soc': soc,
            'grid_import': grid_import
        })
