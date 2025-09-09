# 📊 Real-Time Market Stress Dashboard

This project is a **Streamlit web application** that simulates and visualizes **market stress analysis** in a **High-Frequency Trading (HFT)** environment.  

It demonstrates how market stress can be detected and managed using metrics like **volatility, sentiment, and stress score**, along with a suggested **response strategy**.  

---

## 🚀 Features

- 📈 **Real-time Market Simulation** (price, volume, sentiment, volatility)
- 🔎 **Stress Detection** (volatility + sentiment-based stress score)
- ⚠️ **Stress State Classification** (Stable ✅ or High Stress ⚠️)
- 🎯 **Response Strategy Suggestions** (Normal Operation / Halt / Rebalance / Hedge)
- 📊 **Visualizations**:
  - Price Trend chart
  - Stress Trend chart (with live updates)

---

## 🏗️ Project Structure

```
StressAnalysis/
│── app.py        # Main Streamlit application
│── logic.py      # Simulation & stress detection logic
│── README.md     # Project documentation
│── requirements.txt # Dependencies
```

---

## 🛠️ Installation & Setup

1. Clone the repository or download the files:
   git clone <this_repo_id>
   cd StressAnalysis

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate   # For Mac/Linux Users
   venv\Scripts\activate      # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Run the Streamlit app:
   streamlit run app.py


---

## 📂 How It Works

1. **Data Simulation**  
   - Market price follows a random walk with occasional shocks  
   - Volume and sentiment are randomly generated  
   - Volatility is measured as absolute price change  

2. **Stress Detection**  
   - Stress Score = `volatility + (1 - sentiment)`  
   - If score > 2.5 → High Stress ⚠️  
   - Else → Stable ✅  

3. **Response Strategy**  
   - Normal Operation (if Stable)  
   - Halt Trades / Rebalance / Hedge (if High Stress)  

4. **Visualization**  
   - Price Trend (time vs. price)  
   - Stress Trend (time vs. stress score)  

---

## 📸 Demo Preview

👉 After running, the dashboard will look like this:

- Left side: Market Metrics  
- Right side: Stress Analysis + Response Strategy  
- Bottom: Price Trend & Stress Trend charts updating live  

---

## 🧑‍💻 Author

- **Arpita Pani**  
  Bachelor's in Computer Engineering, Silicon University (Graduation 2026)  

---

## 📜 License

This project is for **educational purposes** and demonstration of **behavioral finance stress modeling**.  
You are free to modify and extend it and explore what more you can do. I would be updating it regularly as i explore more things and find it interesting to add to this project.
