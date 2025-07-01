import yfinance as yf
from sklearn.linear_model import LinearRegression

import matplotlib
matplotlib.use('Agg')  # ✅ THIS FIXES THE MACOS CRASH

import matplotlib.pyplot as plt
import os

def get_stock_data(ticker, period="60d"):
    df = yf.download(ticker, period=period)
    if df.empty:
        return None
    return df

def train_model(df, ticker):
    try:
        print("✅ Starting training for:", ticker)

        df = df[["Close"]].dropna().reset_index()
        df["Day"] = range(len(df))
        print("✅ Data prepared:", df.head())

        X = df[["Day"]]
        y = df["Close"]

        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        print("✅ Model trained.")

        next_day = [[len(df)]]
        prediction = model.predict(next_day)[0]
        print("✅ Prediction:", prediction)

        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(df["Day"], y, label="Actual")
        plt.plot(len(df), prediction, "ro", label="Prediction")
        plt.title(f"{ticker.upper()} Price Prediction")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend()

        output_path = os.path.join("static", "images")
        os.makedirs(output_path, exist_ok=True)
        filename = os.path.join(output_path, f"{ticker}_prediction.png")
        plt.savefig(filename)
        plt.close()

        print("✅ Plot saved to:", filename)
        return round(float(prediction[0]), 2), filename
    
    except Exception as e:
        print("❌ ERROR in train_model:", e)
        return None, None