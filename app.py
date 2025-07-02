from flask import Flask, render_template, request
from model import get_stock_data, train_model
from news_model import train_model_news  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form["ticker"].upper().strip()
        df = get_stock_data(ticker)

        if df is None:
            return render_template("index.html", error="Invalid or unknown ticker.")

        # Run both models
        today_price, next_price, image_price = train_model(df, ticker)
        news_prediction, image_news = train_model_news(ticker)

        if None in (today_price, next_price, image_price, news_prediction, image_news):
            return render_template("index.html", error="Prediction failed. Try again.")

        return render_template(
            "result.html",
            ticker=ticker,
            today=today_price,
            prediction=next_price,
            image_price=image_price,
            news_prediction=news_prediction,
            image_news=image_news
        )

    return render_template("index.html")