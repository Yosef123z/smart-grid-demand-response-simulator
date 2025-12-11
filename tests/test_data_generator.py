import pytest
import pandas as pd
from src.data_generator import generate_demand_data, generate_solar_data, generate_wind_data, generate_price_data

def test_generate_demand_data():
    df = generate_demand_data(days=5)
    assert len(df) == 5 * 24
    assert 'ds' in df.columns
    assert 'y' in df.columns
    assert df['y'].min() >= 0

def test_generate_solar_data():
    df = generate_solar_data(days=5)
    assert len(df) == 5 * 24
    assert 'solar' in df.columns
    assert df['solar'].min() >= 0
    assert df['solar'].max() <= 200

def test_generate_wind_data():
    df = generate_wind_data(days=5)
    assert len(df) == 5 * 24
    assert 'wind' in df.columns
    assert df['wind'].min() >= 0
    assert df['wind'].max() <= 150

def test_generate_price_data():
    df = generate_price_data(days=5)
    assert len(df) == 5 * 24
    assert 'price' in df.columns
    assert df['price'].min() > 0
