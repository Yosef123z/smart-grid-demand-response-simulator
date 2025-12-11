import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from src.simulation import SmartGridSimulation


# Set page configuration (Title, Layout)
st.set_page_config(page_title="Smart Grid Simulator", layout="wide")


@st.cache_data
def load_data():
    """
    Loads the simulation results from the CSV file.

    @st.cache_data is a Streamlit decorator that caches the output.
    """
    try:
        df = pd.read_csv('data/simulation_results.csv')
        df['ds'] = pd.to_datetime(df['ds'])
        return df
    except FileNotFoundError:
        return None


def run_simulation():
    """Runs the simulation and clears cache."""
    with st.spinner('Running simulation... This may take a moment.'):
        sim = SmartGridSimulation(simulation_days=30)
        results = sim.run()
        results.to_csv('data/simulation_results.csv', index=False)
        load_data.clear()  # Clear the cache to reload new data
    st.success('Simulation completed! Data updated.')


def render_docs(file_path):
    """Renders a markdown file."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        st.markdown(content)
    else:
        st.error(f"Documentation file not found: {file_path}")


def render_dashboard(df):
    """Renders the main dashboard."""
    st.title("⚡ Smart Grid Demand-Response Simulator")
    st.markdown(
        "Interactive dashboard to analyze grid performance, "
        "demand forecasting, and battery optimization."
    )

    # Sidebar Actions
    st.sidebar.header("Actions")
    if st.sidebar.button("🔄 Run New Simulation"):
        run_simulation()
        st.rerun()

    if df is None:
        st.error(
            "Simulation results not found. "
            "Please run `python main.py` first or click 'Run New Simulation'."
        )
        return

    # Sidebar Metrics
    st.sidebar.header("Simulation Metrics")
    total_cost = df['cost'].sum()
    peak_load = df['grid_import'].max()
    total_demand = df['actual_demand'].sum()
    renewable_share = (
        (df['solar'].sum() + df['wind'].sum()) / total_demand * 100
    )

    st.sidebar.metric("Total Cost", f"${total_cost:,.2f}")
    st.sidebar.metric("Peak Grid Load", f"{peak_load:.2f} MW")
    st.sidebar.metric("Renewable Share", f"{renewable_share:.1f}%")

    # Main Charts
    tab1, tab2, tab3 = st.tabs(
        ["Demand & Forecast", "Grid & Battery", "Financials"]
    )

    with tab1:
        st.subheader("Demand Forecasting Performance")
        fig_demand = go.Figure()
        fig_demand.add_trace(go.Scatter(
            x=df['ds'], y=df['actual_demand'], name='Actual Demand'
        ))
        fig_demand.add_trace(go.Scatter(
            x=df['ds'], y=df['forecast_demand'], name='Forecast',
            line=dict(dash='dash')
        ))
        fig_demand.update_layout(
            xaxis_title='Time', yaxis_title='Power (MW)',
            hovermode="x unified"
        )
        st.plotly_chart(fig_demand, use_container_width=True)

        st.subheader("Renewable Generation")
        fig_ren = go.Figure()
        fig_ren.add_trace(go.Scatter(
            x=df['ds'], y=df['solar'], name='Solar', fill='tozeroy'
        ))
        fig_ren.add_trace(go.Scatter(
            x=df['ds'], y=df['wind'], name='Wind', fill='tozeroy'
        ))
        fig_ren.update_layout(
            xaxis_title='Time', yaxis_title='Power (MW)',
            hovermode="x unified"
        )
        st.plotly_chart(fig_ren, use_container_width=True)

    with tab2:
        st.subheader("Grid Import vs. Battery Dispatch")

        # Dual axis chart
        fig_grid = make_subplots(specs=[[{"secondary_y": True}]])
        fig_grid.add_trace(
            go.Scatter(
                x=df['ds'], y=df['grid_import'], name='Grid Import (MW)'
            ),
            secondary_y=False
        )
        fig_grid.add_trace(
            go.Scatter(
                x=df['ds'], y=df['battery_flow'], name='Battery Flow (MW)',
                line=dict(color='green')
            ),
            secondary_y=False
        )
        fig_grid.add_trace(
            go.Scatter(
                x=df['ds'], y=df['soc'], name='State of Charge (MWh)',
                line=dict(color='purple', dash='dot')
            ),
            secondary_y=True
        )

        fig_grid.update_layout(hovermode="x unified")
        fig_grid.update_yaxes(title_text="Power (MW)", secondary_y=False)
        fig_grid.update_yaxes(title_text="Energy (MWh)", secondary_y=True)
        st.plotly_chart(fig_grid, use_container_width=True)

    with tab3:
        st.subheader("Cost Analysis")
        df['cumulative_cost'] = df['cost'].cumsum()

        col1, col2 = st.columns(2)
        with col1:
            fig_cost = px.line(
                df, x='ds', y='cumulative_cost',
                title='Cumulative Cost Over Time'
            )
            st.plotly_chart(fig_cost, use_container_width=True)

        with col2:
            fig_price = px.line(
                df, x='ds', y='price',
                title='Electricity Price Signal ($/MWh)'
            )
            st.plotly_chart(fig_price, use_container_width=True)


# Main App Logic
df = load_data()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Project Explanation", "Technical Deep Dive"]
)

if page == "Dashboard":
    render_dashboard(df)
elif page == "Project Explanation":
    render_docs("docs/PROJECT_EXPLANATION.md")
elif page == "Technical Deep Dive":
    render_docs("docs/TECHNICAL_EXPLANATION.md")
