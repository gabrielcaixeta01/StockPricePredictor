from flask import Flask, render_template, request
from model import get_stock_data, train_model

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form["ticker"].upper().strip()
        df = get_stock_data(ticker)

        if df is None:
            return render_template("index.html", error="Invalid or unknown ticker.")

        today_price, next_price, image_path = train_model(df, ticker)

        if None in (today_price, next_price, image_path):
            return render_template("index.html", error="Something went wrong while processing the prediction. Please try again.")

        return render_template(
            "result.html",
            ticker=ticker,
            today=today_price,
            prediction=next_price,
            image=image_path
        )

    return render_template("index.html")