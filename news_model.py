import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from textblob import TextBlob
import requests
import pandas as pd

NEWS_API_KEY = "465c3df16e6c4942be0736eee109fea9"

# Fetch news headlines using NewsAPI
def fetch_news(ticker):
    print("🧠 Fetching news for:", ticker)
    url = f"https://newsapi.org/v2/everything?q={ticker}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "articles" not in data:
        print("❌ ERROR fetching news:", data.get("message", "Unknown error"))
        return []

    return [article["title"] for article in data["articles"][:10]]

# Perform basic sentiment analysis on the headlines
def analyze_sentiment(headlines):
    if not headlines:
        return 0.0
    total_score = 0.0
    for text in headlines:
        score = TextBlob(text).sentiment.polarity
        total_score += score
    avg_score = total_score / len(headlines)
    print("🧠 Avg sentiment:", f"{avg_score:.3f}")
    return avg_score

# Get latest price from Yahoo Finance
def get_current_price(ticker):
    df = yf.download(ticker, period="1d", interval="1m")
    if df.empty:
        return None
    latest = df["Close"].iloc[-1]
    print("📊 Current price DataFrame tail:")
    print(df.tail())
    return float(latest)

# Predict next price based on sentiment
def train_model_news(ticker):
    try:
        today_price = get_current_price(ticker)
        if today_price is None:
            return None, None

        headlines = fetch_news(ticker)
        sentiment_score = analyze_sentiment(headlines)

        # Very basic mock logic: scale sentiment to predict movement
        SCALE = 20
        predicted_price = today_price * (1 + sentiment_score * 0.01 * SCALE)

        # Plotting with line and annotation
        plt.figure(figsize=(8, 5))
        x = ["Today", "Predicted (News)"]
        y = [today_price, predicted_price]

        plt.plot(x, y, marker='o', color='purple', linewidth=2)
        for i, val in enumerate(y):
            plt.text(i, val + 1, f"${val:.2f}", ha='center', fontsize=10)

        plt.title(f"{ticker.upper()} News-Based Prediction")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.ylim(min(y) - 10, max(y) + 10)
        plt.grid(True)

        output_path = os.path.join("static", "images")
        os.makedirs(output_path, exist_ok=True)
        filename = os.path.join(output_path, f"{ticker}_news_prediction.png")
        plt.savefig(filename)
        plt.close()

        return round(predicted_price, 2), filename

    except Exception as e:
        print("❌ ERROR in train_model_news:", e)
        return None, None