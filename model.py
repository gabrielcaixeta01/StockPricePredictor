import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Prevent crash on macOS GUI
import matplotlib.pyplot as plt
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def get_stock_data(ticker, period="60d"):
    df = yf.download(ticker, period=period)
    if df.empty:
        return None
    return df

def train_model(df, ticker):
    try:
        print("✅ Starting training for:", ticker)

        df.reset_index(inplace=True)
        df = df[["Date", "Close", "Volume"]].dropna().reset_index(drop=True)
        df["Day"] = range(len(df))
        df["MA5"] = df["Close"].rolling(5).mean().fillna(method='bfill')

        X = df[["Day", "MA5", "Volume"]]
        y = df["Close"]

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        print("✅ Model trained.")

        # Predict today's price
        today_day = pd.DataFrame({
            "Day": [len(df) - 1],
            "MA5": [df["MA5"].iloc[-2]],
            "Volume": [df["Volume"].iloc[-2]]
        })
        today_prediction = model.predict(today_day)[0]
        print("✅ Today prediction:", today_prediction)

        # Predict next day's price
        next_day = pd.DataFrame({
            "Day": [len(df)],
            "MA5": [df["MA5"].iloc[-1]],
            "Volume": [df["Volume"].iloc[-1]]
        })
        next_prediction = model.predict(next_day)[0]
        print("✅ Next day prediction:", next_prediction)

        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(df["Date"], df["Close"], label="Actual")
        plt.scatter(df["Date"].iloc[-1], today_prediction, color="blue", label="Today Prediction")
        plt.scatter(df["Date"].iloc[-1] + pd.Timedelta(days=1), next_prediction, color="red", label="Next Day Prediction")

        plt.title(f"{ticker.upper()} Price Prediction")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        output_path = os.path.join("static", "images")
        os.makedirs(output_path, exist_ok=True)
        filename = os.path.join(output_path, f"{ticker}_prediction.png")
        plt.savefig(filename)
        plt.close()
        print("✅ Plot saved to:", filename)

        return (
            round(float(today_prediction), 2),
            round(float(next_prediction), 2),
            filename
        )

    except Exception as e:
        print("❌ ERROR in train_model:", e)
        return None, None, None