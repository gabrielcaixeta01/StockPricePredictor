# Stock Price Predictor with Machine Learning
#### Video Demo:  <URL HERE>
#### Description: Welcome to the **Stock Price Predictor**, a web-based application built using Python, Flask, and Machine Learning. 
This project allows users to input a stock ticker (e.g., `AAPL` for Apple) and receive a prediction for the next day's closing price, visualized alongside recent historical data. 
This project was developed as a final submission for Harvard’s **CS50x** course and serves as a showcase of my skills as a full-stack developer with a growing interest in Machine Learning and Financial Technology (FinTech).

---

## 🔍 Overview

The Stock Price Predictor combines historical stock data with a machine learning regression model to estimate future prices. Using the `yfinance` API, the application retrieves the past 60 days of stock data for a given ticker, processes it, and feeds it into a predictive model that estimates the next closing price. The output is displayed both as a numerical value and as a chart comparing actual historical prices to the prediction.

This project highlights how data science and machine learning can be used in a practical, real-world application — forecasting financial trends — with an intuitive and user-friendly interface.

---

## 🎯 Objectives

- Fetch real-time stock data from a reliable public API
- Apply a machine learning algorithm to forecast stock prices
- Build a clean and minimal web interface with Flask
- Deploy a system that communicates predictions clearly to users
- Structure the project for readability, extensibility, and maintainability

---

## 🧠 Technologies Used

### 💻 Back-End
- **Python 3.12**
- **Flask** — Web framework for routing and rendering templates
- **yfinance** — To retrieve historical stock market data
- **scikit-learn** — For machine learning model training and prediction
- **pandas** — For data manipulation
- **matplotlib** — To generate prediction charts

### 🌐 Front-End
- **HTML5** with Jinja2 templating
- **Custom CSS** (can be replaced with Bootstrap for styling improvements)

### 🗂 Project Structure