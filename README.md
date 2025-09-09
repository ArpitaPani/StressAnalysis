# 🤖 ML-Powered Market Stress Dashboard

This project is a **Streamlit web application** that simulates and visualizes **market stress analysis** in a **High-Frequency Trading (HFT)** environment.

It demonstrates how market stress can be **detected, classified, and explained using Machine Learning models** alongside real-time data simulation.

---

## 🚀 Features

* 📈 **Real-time Market Simulation** (price, volume, sentiment, volatility)
* 🤖 **ML Integration**:

  * **Random Forest Classifier** → Predicts Stable ✅ or High Stress ⚠️
  * **KMeans Clustering** → Detects Market Regimes (Bullish 📈, Bearish 📉, Neutral ⚖️)
  * **Isolation Forest** → Detects anomalies (🚨 unusual stress events)
* 🔎 **Stress Detection** (volatility + sentiment-based stress score)
* ⚠️ **Stress State Classification** (via ML instead of simple thresholds)
* 🏦 **Market Regime Analysis** with clustering
* 🎯 **Response Strategy Suggestions** (Normal Operation / Halt / Rebalance / Hedge)
* 📊 **Visualizations**:

  * Price Trend chart with **10-step moving average**
  * Stress Trend chart with **threshold alert line and anomaly markers**
* 📥 **Download Button** to export market data as CSV
* ✨ **Professional UI** with icons, color coding, and organized layout

---

## 🏗️ Project Structure

```
StressAnalysis/
│── app.py            # Main Streamlit application (ML-powered)
│── logic.py          # Simulation & ML models (Random Forest, KMeans, Isolation Forest)
│── README.md         # Project documentation
│── requirements.txt  # Dependencies
```

---

## 🛠️ Installation & Setup

1. Clone the repository or download the files:

   ```bash
   git clone https://github.com/your-username/StressAnalysis.git
   cd StressAnalysis
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

---

## 📂 How It Works

1. **Data Simulation**

   * Market price follows a random walk with occasional shocks
   * Volume and sentiment are randomly generated
   * Volatility is measured as absolute price change

2. **ML Models**

   * **Random Forest** → Classifies stress state (Stable or High Stress)
   * **KMeans** → Clusters data into regimes (Bullish, Bearish, Neutral)
   * **Isolation Forest** → Detects anomalies in stress patterns

3. **Stress Detection & Response**

   * ML predicts stress state instead of static threshold rules
   * Provides **Response Strategies** depending on detected stress

4. **Visualization**

   * Price Trend (with 10-step moving average)
   * Stress Trend (with red threshold line and purple anomaly dots)

5. **Data Export**

   * Download all simulated market data as a CSV file for further analysis

---

## 📸 Demo Preview

👉 After running, the dashboard will look like this:

* Top section: Market Metrics (Price, Volume, Sentiment) and ML-driven Stress Analysis
* Market Regime classification and Response Strategy
* Bottom section: Side-by-side charts of Price Trend (with moving average) and Stress Trend (with anomaly highlights)
* Download button for exporting data

---

## 🔧 Key Hyperparameters

* `n_estimators=100` → Number of trees in Random Forest (balances accuracy and speed).
* `random_state=42` → Ensures reproducible randomness (common DS convention).
* `contamination=0.05` → Isolation Forest parameter for expected anomaly rate (5%).

---

## 🧑‍💻 Author

* **Arpita Pani**
  Bachelor's in Computer Engineering, Silicon University (Graduation 2026)

---

## 📜 License

This project is for **educational purposes** and demonstration of **behavioral finance stress modeling with ML**.
You are free to modify and extend it and explore what more you can do. I would be updating it regularly as i explore more things and find it interesting to add to this project.
