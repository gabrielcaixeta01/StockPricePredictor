from flask import Flask, render_template, request
from model import get_stock_data, train_model
from news_model import train_model_news
from news_scraper import get_news_articles  # você precisa criar esse módulo

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form["ticker"].upper().strip()
        df = get_stock_data(ticker)

        if df is None:
            return render_template("index.html", error="Invalid or unknown ticker.")

        # Previsões com modelos
        today_price, next_price, image_price = train_model(df, ticker)
        news_prediction, image_news = train_model_news(ticker)

        if None in (today_price, next_price, image_price, news_prediction, image_news):
            return render_template("index.html", error="Prediction failed. Try again.")

        # Notícia + sentimento
        news_articles = get_news_articles(ticker)

        # Recomendação simples
        if news_prediction > today_price and next_price > today_price:
            recommendation = "Buy – positive trend in both sentiment and historical data."
        elif news_prediction < today_price and next_price < today_price:
            recommendation = "Sell – negative trend in both models."
        else:
            recommendation = "Hold – mixed signals from models."

        return render_template(
            "result.html",
            ticker=ticker,
            today_price=today_price,
            next_price=next_price,
            news_prediction=news_prediction,
            image_price=image_price,
            news_image=image_news,
            news_articles=news_articles,
            recommendation=recommendation
        )

    return render_template("index.html")