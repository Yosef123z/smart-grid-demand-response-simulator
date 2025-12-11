# 🛠️ Smart Grid Simulator: The Deep Dive

This document is a comprehensive technical guide to the Smart Grid Simulator. It goes beyond the basics to explain the *exact* logic, code structures, and algorithms used in the project.

---

## 🧩 System Architecture

Before looking at the code, let's visualize how data flows through the system.

```mermaid
sequenceDiagram
    participant Main as main.py
    participant Sim as Simulation Class
    participant Gen as Data Generator
    participant Forecaster as Prophet Model
    participant Opt as Grid Optimizer
    participant File as CSV File

    Main->>Sim: run()
    activate Sim
    
    Note over Sim: Step 1: Create the World
    Sim->>Gen: generate_demand_data()
    Gen-->>Sim: Demand DataFrame
    Sim->>Gen: generate_solar_data()
    Gen-->>Sim: Solar DataFrame
    
    Note over Sim: Step 2: Predict the Future
    Sim->>Forecaster: train(history_data)
    Sim->>Forecaster: predict(future_horizon)
    Forecaster-->>Sim: Forecast DataFrame
    
    Note over Sim: Step 3: Solve the Puzzle
    Sim->>Opt: optimize_dispatch(net_load, prices)
    activate Opt
    Opt->>Opt: Calculate Battery Actions
    Opt-->>Sim: Optimization Results
    deactivate Opt
    
    Note over Sim: Step 4: Save & Finish
    Sim->>File: Save to simulation_results.csv
    deactivate Sim
```

---

## 🏭 Component 1: Data Generation (`src/data_generator.py`)

This module is responsible for creating the synthetic environment. It contains four main functions, each returning a Pandas DataFrame with a `ds` (timestamp) column.

### 1. `generate_demand_data(days)`
*   **Goal**: Simulate electricity consumption (Load).
*   **Logic**:
    *   **Base Load**: Starts with a constant 500 MW.
    *   **Daily Seasonality**: Adds a sine wave `sin(2*pi*t/24)` to peak in the evening (18:00).
    *   **Weekly Seasonality**: Subtracts 50 MW on weekends (Saturday/Sunday).
    *   **Noise**: Adds Gaussian noise `N(0, 20)` to simulate random appliance usage.
*   **Output**: DataFrame with columns `['ds', 'y']`.

### 2. `generate_solar_data(days)`
*   **Goal**: Simulate PV generation.
*   **Logic**:
    *   **Day/Night Cycle**: Uses a shifted sine wave that is positive between 06:00 and 18:00 and zero otherwise.
    *   **Cloud Cover**: Multiplies the output by a random factor `uniform(0.5, 1.0)` to simulate clouds reducing efficiency.
*   **Output**: DataFrame with columns `['ds', 'solar']`.

### 3. `generate_wind_data(days)`
*   **Goal**: Simulate wind turbine output.
*   **Logic**:
    *   **Wind Speed**: Samples from a **Weibull Distribution** (shape=2), which is standard for wind modeling.
    *   **Power Curve**: Converts speed to power using a cubic relationship ($P \propto v^3$) up to a rated limit (150 MW).
*   **Output**: DataFrame with columns `['ds', 'wind']`.

### 4. `generate_price_data(days)`
*   **Goal**: Simulate Time-of-Use (TOU) tariffs.
*   **Logic**:
    *   **Off-Peak**: $0.05/kWh (Night)
    *   **Mid-Peak**: $0.10/kWh (Day)
    *   **On-Peak**: $0.20/kWh (Evening 16:00-20:00)
*   **Output**: DataFrame with columns `['ds', 'price']`.

---

## 🔮 Component 2: Forecasting (`src/forecaster.py`)

This module wraps the **Facebook Prophet** library to predict future demand.

### Class: `DemandForecaster`
*   **`__init__`**: Initializes the Prophet model. We explicitly enable `daily_seasonality=True` because electricity data has a very strong 24-hour pattern.
*   **`train(history_df)`**: Fits the model to historical data. Prophet decomposes the time series into trend + seasonality + holidays.
*   **`predict(horizon_hours)`**:
    1.  Creates a "future dataframe" extending `horizon_hours` into the future.
    2.  Generates predictions (`yhat`) for these future timestamps.
    3.  Returns the forecast DataFrame.

---

## 🧠 Component 3: The Optimizer (`src/optimizer.py`)

This is the decision-making engine. It decides the battery's charge/discharge power ($P_{batt}$) for every time step.

### Class: `GridOptimizer`
*   **Parameters**:
    *   `battery_capacity`: Total energy storage (e.g., 100 MWh).
    *   **`max_power`**: Max charge/discharge rate (e.g., 50 MW).
    *   **`efficiency`**: Round-trip efficiency (e.g., 0.9 or 90%).

### Algorithm: Heuristic Control
We use a rule-based approach for speed and simplicity.
1.  **Calculate Net Load**: $NetLoad = Demand - (Solar + Wind)$.
2.  **Determine Action**:
    *   **Excess Renewables ($NetLoad < 0$)**: **CHARGE**. Store the free energy.
    *   **Peak Demand ($NetLoad > 90th Percentile$)**: **DISCHARGE**. Help the grid.
    *   **High Price ($Price > 75th Percentile$)**: **DISCHARGE**. Sell energy for profit.
    *   **Low Price ($Price < 25th Percentile$)**: **CHARGE**. Buy cheap energy.
3.  **Apply Constraints**:
    *   Limit action to `max_power`.
    *   Ensure State of Charge (SoC) stays between 0 and `battery_capacity`.
    *   Account for efficiency losses during charging/discharging.

---

## 🎮 Component 4: The Simulation Engine (`src/simulation.py`)

This class orchestrates the entire workflow.

### Class: `SmartGridSimulation`
*   **`run()`**:
    1.  **Generate**: Calls `data_generator` to create 60 days of data.
    2.  **Split**: Uses the first 30 days as "History" (for training) and the next 30 days as "Simulation" (for testing).
    3.  **Train**: Feeds "History" to the `Forecaster`.
    4.  **Forecast**: Predicts demand for the "Simulation" period.
    5.  **Optimize**: Passes the actual Net Load and Prices to the `Optimizer`.
    6.  **Result Compilation**: Merges all data (Actual, Forecast, Battery Flow, Cost) into a single `final_results` DataFrame.

---

## 📊 Component 5: The Dashboard (`dashboard.py`)

The dashboard is built with **Streamlit**, a Python library for creating data apps.

### Key Features
*   **`@st.cache_data`**: This decorator is crucial. It tells Streamlit to run the data loading function *once* and save the result. This prevents the simulation from re-running every time you interact with a chart, making the app feel snappy.
*   **`plotly.graph_objects`**: We use Plotly for interactive charts.
    *   **Dual Axis**: We often plot Power (MW) on the left axis and Price ($) or SoC (MWh) on the right axis to show correlations.
*   **`st.columns`**: Used to create a grid layout for metrics (Total Cost, Renewable Share, etc.).

---

## 🎓 Glossary of Terms

*   **DataFrame**: A table of data (rows and columns) in Python (Pandas library).
*   **Heuristic**: A practical method for solving a problem that isn't guaranteed to be perfect, but is "good enough" (e.g., our rule-based optimizer).
*   **Vectorization**: Doing math on a whole list of numbers at once, instead of one by one.
*   **Digital Twin**: A virtual replica of a physical system (our grid simulation).
*   **SoC (State of Charge)**: The percentage or amount of energy currently stored in the battery.
