# logic.py
import numpy as np
import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

class MarketStressSimulator:
    def __init__(self):
        self.price = 100.0  # starting price
        self.history = []

    def generate_data(self):
        # Simulate price movement with random walk + shock events
        shock = np.random.choice([0, np.random.normal(0, 3)], p=[0.9, 0.1])
        change = np.random.normal(0, 1) + shock
        self.price = max(1, self.price + change)
        volume = np.random.randint(100, 1000)
        sentiment = np.random.uniform(-1, 1)

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

# ----------------------------
# ML Models
# ----------------------------

class StressModel:
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        self.anomaly_model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False

    def train(self, df):
        if len(df) < 30:  # need enough data
            return None

        # Features & labels
        X = df[["price", "volume", "sentiment", "volatility"]]
        y = (df["volatility"] + (1 - df["sentiment"]) > 2.5).astype(int)  # 1 = High Stress

        # Train models
        self.clf.fit(X, y)
        self.kmeans.fit(X)
        self.anomaly_model.fit(X)

        self.is_trained = True

    def predict(self, new_data):
        if not self.is_trained:
            return None, None, None

        features = [[
            new_data["price"], new_data["volume"],
            new_data["sentiment"], new_data["volatility"]
        ]]

        stress_pred = self.clf.predict(features)[0]
        regime = self.kmeans.predict(features)[0]
        anomaly = self.anomaly_model.predict(features)[0]  # -1 = anomaly

        return stress_pred, regime, anomaly
