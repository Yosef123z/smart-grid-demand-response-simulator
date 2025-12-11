import pytest
import pandas as pd
from src.forecaster import DemandForecaster

def test_forecaster_train_predict():
    # Create dummy history
    dates = pd.date_range(start='2023-01-01', periods=48, freq='H')
    history = pd.DataFrame({'ds': dates, 'y': [100] * 48})
    
    forecaster = DemandForecaster()
    forecaster.train(history)
    
    forecast = forecaster.predict(horizon_hours=24)
    assert len(forecast) == 24
    assert 'ds' in forecast.columns
    assert 'yhat' in forecast.columns

def test_forecaster_not_trained():
    forecaster = DemandForecaster()
    with pytest.raises(ValueError):
        forecaster.predict(24)
