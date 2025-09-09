import streamlit as st
import time
from logic import MarketStressSimulator, detect_stress
import altair as alt

st.set_page_config(page_title="Market Stress Dashboard", layout="wide")

st.title("📊 Real-Time Market Stress Dashboard")

# Initializing simulator
simulator = MarketStressSimulator()
placeholder = st.empty()

# Real-time loop
while True:
    new_data = simulator.generate_data()
    df = simulator.get_dataframe()

    stress_score, state, strategy = detect_stress(new_data)

    # Adding stress_score column for plotting
    df["stress_score"] = df.apply(lambda row: row["volatility"] + (1 - row["sentiment"]), axis=1)

    with placeholder.container():
        col1, col2 = st.columns(2)

        # Market Metrics
        with col1:
            st.subheader("Market Metrics")
            st.metric("Latest Price", f"${new_data['price']:.2f}")
            st.metric("Volume", new_data["volume"])
            st.metric("Sentiment", f"{new_data['sentiment']:.2f}")

        # Stress Analysis + Response Strategy
        with col2:
            st.subheader("Stress Analysis")
            st.metric("Volatility", f"{new_data['volatility']:.2f}")
            st.metric("Stress Score", f"{stress_score:.2f}")
            if "Stable" in state:
                st.success(state)
            else:
                st.error(state)

            st.subheader("Response Strategy")
            st.write(strategy)

        # Charts in two columns
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Price Trend")
            price_chart = alt.Chart(df).mark_line().encode(
                x="time:T",
                y="price:Q"
            )
            st.altair_chart(price_chart, use_container_width=True)

        with c2:
            st.subheader("Stress Trend")
            stress_chart = alt.Chart(df).mark_line(color="red").encode(
                x="time:T",
                y="stress_score:Q"
            )
            st.altair_chart(stress_chart, use_container_width=True)

    time.sleep(1)  # it is refreshed every second
