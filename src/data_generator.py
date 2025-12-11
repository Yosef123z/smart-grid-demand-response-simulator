import pandas as pd
import numpy as np


def generate_demand_data(days=30, start_date='2023-01-01'):
    """
    Generates synthetic hourly electricity demand data.

    The model uses a superposition of:
    1. Base Load: Constant power consumption.
    2. Daily Seasonality: Sine wave peaking in the evening.
    3. Weekly Seasonality: Lower demand on weekends.
    4. Random Noise: Gaussian noise for realistic variability.

    Formula:
    D(t) = Base + A_daily * sin(2*pi*t/24) + A_weekly + Noise

    Args:
        days (int): Number of days to simulate.
        start_date (str): Start date string (YYYY-MM-DD).

    Returns:
        pd.DataFrame: DataFrame with columns ['ds', 'y']
    """
    # Create a time range with hourly frequency
    dates = pd.date_range(start=start_date, periods=days*24, freq='H')

    # Base demand (MW) - The minimum load always present
    base_demand = 500

    # Daily seasonality (peak in evening)
    # We use a sine wave with a period of 24 hours.
    # The phase shift (-np.pi/2) aligns the peak to approx 18:00 (6 PM).
    daily_pattern = np.sin(2 * np.pi * dates.hour / 24 - np.pi/2) * 100

    # Weekly seasonality (lower on weekends)
    # If dayofweek is 5 (Saturday) or 6 (Sunday), subtract 50 MW.
    weekly_pattern = np.where(dates.dayofweek >= 5, -50, 0)

    # Random noise
    # Normal distribution with mean=0 and std_dev=20 MW.
    noise = np.random.normal(0, 20, len(dates))

    # Combine all components
    demand = base_demand + daily_pattern + weekly_pattern + noise
    demand = np.maximum(demand, 0)  # Ensure non-negative demand

    return pd.DataFrame({'ds': dates, 'y': demand})


def generate_solar_data(days=30, start_date='2023-01-01'):
    """
    Generates synthetic hourly solar generation data.

    The model simulates the sun's path and cloud cover.

    Formula:
    S(t) = P_max * max(0, sin(pi * (t_hour - 6) / 12)) * (1 - CloudCover)

    Args:
        days (int): Number of days to simulate.
        start_date (str): Start date string.

    Returns:
        pd.DataFrame: DataFrame with columns ['ds', 'solar']
    """
    dates = pd.date_range(start=start_date, periods=days*24, freq='H')

    # Solar pattern (peak at noon, zero at night)
    # We want a wave that starts at 6 AM, peaks at 12 PM, and ends at 6 PM.
    # The argument (dates.hour - 6) shifts the start to 6 AM.
    # Dividing by 12 scales the half-period to 12 hours.
    daily_pattern = np.sin(np.pi * (dates.hour - 6) / 12)

    # Clip negative values to 0 (night time) and scale to max capacity (200 MW)
    daily_pattern = np.maximum(daily_pattern, 0) * 200

    # Random cloud cover
    # Uniform distribution between 0.5 and 1.0.
    # 1.0 means clear sky, 0.5 means heavy clouds (50% reduction).
    cloud_cover = np.random.uniform(0.5, 1.0, len(dates))

    solar = daily_pattern * cloud_cover

    return pd.DataFrame({'ds': dates, 'solar': solar})


def generate_wind_data(days=30, start_date='2023-01-01'):
    """
    Generates synthetic hourly wind generation data.

    Uses a Weibull distribution for wind speed and a cubic power curve.

    Args:
        days (int): Number of days to simulate.
        start_date (str): Start date string.

    Returns:
        pd.DataFrame: DataFrame with columns ['ds', 'wind']
    """
    dates = pd.date_range(start=start_date, periods=days*24, freq='H')

    # Weibull distribution is standard for wind speed modeling.
    # shape parameter (a) = 2 (Rayleigh distribution approximation)
    # scale parameter = 5 (Average wind speed scaling)
    wind_speed = np.random.weibull(2, len(dates)) * 5

    # Power curve (simplified)
    # Power is proportional to the cube of wind speed (P ~ v^3)
    # We cap it at 150 MW (Rated Power)
    wind_power = np.minimum(wind_speed ** 3, 150)

    return pd.DataFrame({'ds': dates, 'wind': wind_power})


def generate_price_data(days=30, start_date='2023-01-01'):
    """
    Generates synthetic hourly electricity price data (Time-of-Use).

    Simulates a tariff structure with 3 tiers:
    - Off-peak: Night
    - Mid-peak: Day
    - On-peak: Evening

    Args:
        days (int): Number of days to simulate.
        start_date (str): Start date string.

    Returns:
        pd.DataFrame: DataFrame with columns ['ds', 'price']
    """
    dates = pd.date_range(start=start_date, periods=days*24, freq='H')

    # TOU Pricing Structure
    # Off-peak: 00:00-06:00, 22:00-24:00 ($0.05/kWh)
    # Mid-peak: 06:00-16:00, 20:00-22:00 ($0.10/kWh)
    # On-peak:  16:00-20:00              ($0.20/kWh)

    prices = []
    for hour in dates.hour:
        if 16 <= hour < 20:
            prices.append(0.20)
        elif 6 <= hour < 16 or 20 <= hour < 22:
            prices.append(0.10)
        else:
            prices.append(0.05)

    # Add some volatility (random fluctuations)
    # Market prices are never perfectly static.
    prices = np.array(prices) + np.random.normal(0, 0.005, len(dates))
    prices = np.maximum(prices, 0.01)  # Ensure price is at least 1 cent

    return pd.DataFrame({'ds': dates, 'price': prices})
