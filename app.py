"""
Company News Tracker — Daily Morning Note Generator
Flask web application for equity research professionals.
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from data_fetcher import DataFetcher
from report_generator import generate_morning_note

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key-change-in-production")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate_report():
    """Generate a morning note for the provided tickers."""
    data = request.get_json()
    if not data or "tickers" not in data:
        return jsonify({"error": "No tickers provided"}), 400

    raw_tickers = data["tickers"]
    if isinstance(raw_tickers, str):
        tickers = [t.strip().upper() for t in raw_tickers.split(",") if t.strip()]
    else:
        tickers = [t.strip().upper() for t in raw_tickers if t.strip()]

    if not tickers:
        return jsonify({"error": "No valid tickers provided"}), 400

    if len(tickers) > 10:
        return jsonify({"error": "Maximum 10 tickers per request"}), 400

    fetcher = DataFetcher()

    # Check if API key is configured
    if not fetcher.finnhub_key:
        return jsonify({
            "error": "Finnhub API key not configured. "
            "Set FINNHUB_API_KEY in your .env file. "
            "Get a free key at https://finnhub.io/"
        }), 500

    try:
        ticker_data = []
        for ticker in tickers:
            ticker_data.append(fetcher.fetch_all_for_ticker(ticker))

        macro_data = fetcher.fetch_macro_data()
        report = generate_morning_note(ticker_data, macro_data)

        return jsonify({
            "report": report,
            "tickers": tickers,
            "status": "success",
        })
    except Exception as e:
        return jsonify({"error": f"Report generation failed: {str(e)}"}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
