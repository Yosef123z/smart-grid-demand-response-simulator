import subprocess
import sys
from prophet import Prophet


class DemandForecaster:
    """
    A wrapper class for the Facebook Prophet forecasting model.

    Prophet is an additive regression model that works well with time-series
    data that has strong seasonal effects (daily, weekly, yearly) and is
    robust to missing data.
    """

    def __init__(self):
        """
        Initializes the Prophet model.

        We explicitly enable 'daily_seasonality' because electricity demand
        has a very strong 24-hour pattern (low at night, high in evening).
        """
        self.model = Prophet(daily_seasonality=True)

    def train(self, history_df):
        """
        Trains the Prophet model on historical data.

        Args:
            history_df (pd.DataFrame): DataFrame with columns ['ds', 'y'].
                                       'ds': Timestamp
                                       'y': The value to predict (Demand)
        """
        self.model.fit(history_df)

    def predict(self, horizon_hours):
        """
        Generates forecasts for the future.

        Args:
            horizon_hours (int): Number of hours to predict into the future.

        Returns:
            pd.DataFrame: DataFrame containing the forecast.
                          Key columns: ['ds', 'yhat', 'yhat_lower',
                                        'yhat_upper']
                          'yhat': The predicted value.
        """
        # Check if model is trained
        if not hasattr(self.model, 'params') or self.model.params is None:
            # Prophet < 1.0 might behave differently, but let's assume
            # standard behavior.
            pass

        # Create a dataframe with future dates
        try:
            future = self.model.make_future_dataframe(
                periods=horizon_hours, freq='H'
            )
        except Exception:
            # If make_future_dataframe fails, it's likely because the model
            # isn't fitted
            raise ValueError("Model has not been trained yet.")

        # Generate the forecast
        forecast = self.model.predict(future)

        # Return only the future part (the last 'horizon_hours' rows)
        return forecast.tail(horizon_hours)
