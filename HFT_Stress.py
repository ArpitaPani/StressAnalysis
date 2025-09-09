import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import datetime
import requests

API_KEY = 'e8754a0704894167a8cf3b1144fe80e0'

# --- Functions ---
def fetch_spy_data(start_date, end_date):
    try:
        data = yf.download('SPY', start=start_date, end=end_date, auto_adjust=False)
        data['Returns'] = data['Close'].pct_change()
        data['Volatility'] = data['Returns'].rolling(window=10).std() * np.sqrt(252)
        data['Volume Change'] = data['Volume'].pct_change()
        return data.dropna()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def get_sentiment_score_vader(headlines):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = [analyzer.polarity_scores(text)['compound'] for text in headlines]
    return sentiment_scores, np.mean(sentiment_scores)

def calculate_stress_signals(data, sentiment_score):
    vol_threshold = data['Volatility'].mean() + data['Volatility'].std()
    sentiment_threshold = 0.1
    data['Stress Score'] = data['Volatility'] * (1 - sentiment_score)
    data['Stress Signal'] = (data['Volatility'] > vol_threshold) & (sentiment_score < sentiment_threshold)
    return data

def apply_isolation_forest(data):
    model = IsolationForest(contamination=0.1, random_state=42)
    data['Anomaly'] = model.fit_predict(data[['Volatility', 'Volume Change']])
    return data

def train_logistic_model(data):
    data['Stress Label'] = ((data['Volatility'] > data['Volatility'].mean() + data['Volatility'].std()) &
                            (data['Sentiment'] < 0.1)).astype(int)
    features = data[['Volatility', 'Sentiment', 'Volume Change']]
    labels = data['Stress Label']
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    probas = model.predict_proba(X_test)[:, 1]

    st.subheader("Logistic Regression Report")
    st.text(classification_report(y_test, predictions))
    st.write("ROC AUC Score:", roc_auc_score(y_test, probas))

    fpr, tpr, _ = roc_curve(y_test, probas)
    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc_score(y_test, probas):.2f})")
    ax.plot([0, 1], [0, 1], linestyle='--', color='gray')
    ax.set_title("ROC Curve")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend()
    st.pyplot(fig)

    data['Logistic_Prediction'] = model.predict(features)
    return data

def plot_dashboard(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='SPY Price', color='blue')
    ax.scatter(data.index[data['Stress Signal']], data['Close'][data['Stress Signal']],
               color='orange', label='Threshold Stress Signal')
    ax.scatter(data.index[data['Anomaly'] == -1], data['Close'][data['Anomaly'] == -1],
               color='red', marker='x', label='Isolation Forest Anomaly')
    ax.scatter(data.index[data['Logistic_Prediction'] == 1], data['Close'][data['Logistic_Prediction'] == 1],
               color='green', marker='^', label='Logistic Model Stress')
    ax.set_title('SPY Price and Stress Detection')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# --- Streamlit UI ---
st.set_page_config(page_title="Market Stress Dashboard", layout="wide")
st.title("📉 Market Stress Dashboard ")

query = st.text_input("Query:", value="stock market OR inflation OR recession")
date_range = st.date_input("Date Range", [datetime.date(2024, 1, 1), datetime.date(2024, 4, 1)])
start_date = date_range[0].strftime('%Y-%m-%d')
end_date = date_range[1].strftime('%Y-%m-%d')

if st.button("Fetch News & Index"):
    with st.spinner("Fetching data and analyzing..."):
        url = f'https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}'
        response = requests.get(url)
        articles = response.json().get('articles', [])
        headlines = [article['title'] for article in articles if article.get('title')]

        if not headlines:
            st.warning("No headlines found.")
        else:
            sentiment_scores, avg_sentiment = get_sentiment_score_vader(headlines)
            st.subheader("Sentiment Scores (Top 10 Headlines)")
            sentiment_df = pd.DataFrame({'Headline': headlines[:10], 'SentimentScore': sentiment_scores[:10]})
            st.dataframe(sentiment_df)

            fig, ax = plt.subplots(figsize=(10, 6))
            sentiment_df.plot.barh(x='Headline', y='SentimentScore', ax=ax, color='skyblue')
            st.pyplot(fig)

            data = fetch_spy_data(start_date, end_date)
            if data.empty:
                st.error("No market data available.")
            else:
                data['Sentiment'] = avg_sentiment
                data = calculate_stress_signals(data, avg_sentiment)
                data = apply_isolation_forest(data)
                data = train_logistic_model(data)
                plot_dashboard(data)
