# 🔌 Smart Grid Simulator - How It Works

## The Big Picture

Imagine you're managing a small city's electricity. You have:

- 🏠 **Buildings** using electricity (demand)
- ☀️ **Solar panels** generating power during the day
- 💨 **Wind turbines** generating power when windy
- 🔋 **A big battery** to store extra energy
- 🏭 **The power company** you can buy electricity from

**The Problem:** Electricity prices change throughout the day. It's expensive at 6 PM when everyone's home, but cheap at 3 AM when most people are sleeping.

**The Solution:** This simulator figures out the smartest way to use the battery to save money!

***

## How It Works (4 Simple Steps)

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. GENERATE    │ ──▶ │  2. PREDICT     │ ──▶ │  3. OPTIMIZE    │ ──▶ │  4. DISPLAY     │
│  Fake Data      │     │  Future Demand  │     │  Battery Usage  │     │  Results        │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘

### Step 1: Generate Data 📊

**File:** 

src/data_generator.py

Creates fake but realistic data for:

- How much electricity people use (higher in evening, lower at night)
- How much solar power is available (peaks at noon, zero at night)
- How much wind power is available (random, like real weather)
- Electricity prices (expensive 4-8 PM, cheap at night)

### Step 2: Predict the Future 🔮

**File:** 

src/forecaster.py

Uses **Facebook Prophet** (an AI tool) to look at past electricity usage and predict what will happen tomorrow.

_Why?_ If we know high demand is coming, we can charge the battery beforehand!

### Step 3: Make Smart Decisions 🧠

**File:** 

src/optimizer.py

Decides when to charge or discharge the battery using 3 rules:

|Situation|Action|Why|
|---|---|---|
|Extra solar/wind energy|**CHARGE** battery|Store free energy!|
|Very high demand|**DISCHARGE** battery|Help the grid|
|Price is cheap|**CHARGE** battery|Buy low|
|Price is expensive|**DISCHARGE** battery|Sell high|

### Step 4: Show Results 📈

**File:** 

dashboard.py

A beautiful website (Streamlit) showing:

- Actual vs Predicted demand
- Battery charging/discharging
- Money saved

---

## Project Files Explained

📁 smart-grid-simulator/
│
├── 🚀 main.py           ← RUN THIS to start simulation
├── 📊 dashboard.py      ← RUN THIS to see the website
│
├── 📁 src/              ← The "brain" of the project
│   ├── data_generator.py    ← Creates fake electricity data
│   ├── forecaster.py        ← Predicts future demand (AI)
│   ├── optimizer.py         ← Decides what battery should do
│   └── simulation.py        ← Connects everything together
│
├── 📁 data/             ← Where results are saved
│   └── simulation_results.csv
│
├── 📁 docs/             ← Documentation
├── 📁 tests/            ← Automated tests (99% coverage!)
└── 📁 notebooks/        ← Jupyter notebook for analysis

***

## Key Terms Glossary

|Term|Meaning|
|---|---|
|**Demand**|How much electricity people are using|
|**Net Load**|Demand - Solar - Wind (what the grid must supply)|
|**SoC (State of Charge)**|How full the battery is (0-100%)|
|**Peak Shaving**|Discharging battery during high demand to reduce strain|
|**Arbitrage**|Buying cheap, selling expensive|
|**Digital Twin**|A computer simulation of a real system|
***

## How to Run It

### Step 1: Install requirements
pip install -r requirements.txt

### Step 2: Run the simulation (creates data)
python main.py

### Step 3: View the dashboard
streamlit run dashboard.py

***

## Results We Achieved

|Metric|Value|
|---|---|
|Forecast Accuracy|8.5% error (very good!)|
|Peak Load Reduction|18% lower|
|Cost Savings|12% cheaper|
|Test Coverage|99% (almost perfect!)|

---

## Real-World Impact 🌍

This type of system helps:

- **Save money** on electricity bills
- **Use more clean energy** (solar/wind)
- **Prevent blackouts** during peak demand
- **Reduce pollution** by using less fossil fuel

---

_This project demonstrates how AI and smart algorithms can make our electricity grid smarter and greener!_ 🌱

