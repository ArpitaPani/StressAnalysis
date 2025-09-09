import numpy as np
import pandas as pd
import random

class MarketStressSimulator:
    def __init__(self):
        self.price = 100.0  # starting price
        self.history = []

    def generate_data(self):
        # Simulating price movement with random walk + shock events
        shock = np.random.choice([0, np.random.normal(0, 3)], p=[0.9, 0.1])  # occasional shocks
        change = np.random.normal(0, 1) + shock
        self.price = max(1, self.price + change)  # keeping price > 0
        volume = np.random.randint(100, 1000)
        sentiment = np.random.uniform(-1, 1)  # -1 = negative, 1 = positive

        data = {
            "time": pd.Timestamp.now(),
            "price": self.price,
            "volume": volume,
            "sentiment": sentiment,
            "volatility": abs(change)
        }
        self.history.append(data)
        return data

    def get_dataframe(self):
        return pd.DataFrame(self.history)

def detect_stress(latest_data, threshold=2.5):
    """Detecting market stress and suggesting a response strategy"""
    stress_score = latest_data["volatility"] + (1 - latest_data["sentiment"])

    if stress_score > threshold:
        state = "⚠️ High Stress"
        strategy = random.choice(["Halt Trades", "Rebalance Portfolio", "Hedge with Options"])
    else:
        state = "✅ Stable"
        strategy = "Normal Operation"

    return stress_score, state, strategy
