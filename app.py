import streamlit as st
import time
from logic import MarketStressSimulator, StressModel
import altair as alt
import pandas as pd

st.set_page_config(page_title="ML-Powered Market Stress Dashboard", layout="wide")

st.title("🤖 ML-Powered Market Stress Dashboard")

# Initializing simulator & ML model
simulator = MarketStressSimulator()
model = StressModel()
placeholder = st.empty()

STRESS_THRESHOLD = 2.5  # threshold for visualization

while True:
    new_data = simulator.generate_data()
    df = simulator.get_dataframe()

    # Training ML model on accumulated data
    model.train(df)

    # ML Predictions
    stress_pred, regime, anomaly = model.predict(new_data)

    # Add columns for visualization
    df["stress_score"] = df["volatility"] + (1 - df["sentiment"])
    df["price_ma10"] = df["price"].rolling(window=10).mean()

    if anomaly is not None:
        df["anomaly"] = model.anomaly_model.predict(
            df[["price", "volume", "sentiment", "volatility"]]
        )

    with placeholder.container():
        st.markdown("## 📈 Market Metrics")

        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Latest Price", f"${new_data['price']:.2f}")
        col2.metric("📊 Volume", new_data["volume"])
        col3.metric("🧠 Sentiment", f"{new_data['sentiment']:.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("📉 Volatility", f"{new_data['volatility']:.2f}")

        if stress_pred == 1:
            col5.metric("⚠️ ML Stress State", "High Stress")
        elif stress_pred == 0:
            col5.metric("✅ ML Stress State", "Stable")
        else:
            col5.metric("🤔 ML Stress State", "Training...")

        if regime is not None:
            regimes = {0: "📈 Bullish", 1: "📉 Bearish", 2: "⚖️ Neutral"}
            col6.metric("🏦 Market Regime", regimes.get(regime, "Unknown"))

        # Response Strategy
        st.markdown("### 🎯 Response Strategy")
        if stress_pred == 1:
            st.error("⚠️ High Stress Detected → Suggest: Halt / Rebalance / Hedge")
        elif stress_pred == 0:
            st.success("✅ Stable → Normal Operation")
        else:
            st.info("🤔 Training model... Collecting more data")

        if anomaly == -1:
            st.warning("🚨 Anomaly Detected: Market behaving unusually!")

        # Charts
        c1, c2 = st.columns(2)

        # Price Trend with Moving Average
        with c1:
            st.subheader("📊 Price Trend (with Moving Average)")
            price_chart = (
                alt.Chart(df).mark_line().encode(x="time:T", y="price:Q") +
                alt.Chart(df).mark_line(color="orange").encode(x="time:T", y="price_ma10:Q")
            )
            st.altair_chart(price_chart, use_container_width=True)

        # Stress Trend with anomalies
        with c2:
            st.subheader("📉 Stress Trend with Anomalies")

            threshold_line = alt.Chart(pd.DataFrame({"y": [STRESS_THRESHOLD]})).mark_rule(
                color="red", strokeDash=[5, 5]
            ).encode(y="y:Q")

            stress_chart = alt.Chart(df).mark_line(color="red").encode(
                x="time:T",
                y="stress_score:Q"
            )

            # Highlight anomalies as purple dots
            if "anomaly" in df.columns:
                anomaly_points = alt.Chart(df[df["anomaly"] == -1]).mark_circle(
                    size=60, color="purple"
                ).encode(
                    x="time:T",
                    y="stress_score:Q",
                    tooltip=["time:T", "stress_score:Q"]
                )
                stress_chart = stress_chart + anomaly_points

            st.altair_chart(stress_chart + threshold_line, use_container_width=True)

        # Download Button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Market Data as CSV",
            data=csv,
            file_name="market_stress_data.csv",
            mime="text/csv",
            key=f"download_button_{len(df)}"
        )

    time.sleep(1)
