"""
Data fetching module for Company News Tracker.
Aggregates news, filings, market data, and macro signals from multiple sources.
"""

import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import feedparser
import finnhub
import requests

# Sector classification for macro sensitivity analysis
SECTOR_MAP = {
    "AAPL": "Technology", "MSFT": "Technology", "GOOGL": "Technology",
    "AMZN": "Consumer Discretionary", "TSLA": "Consumer Discretionary",
    "META": "Technology", "NVDA": "Technology", "AMD": "Technology",
    "NFLX": "Communication Services", "DIS": "Communication Services",
    "JPM": "Financials", "GS": "Financials", "MS": "Financials",
    "BAC": "Financials", "WFC": "Financials",
    "JNJ": "Healthcare", "PFE": "Healthcare", "UNH": "Healthcare",
    "XOM": "Energy", "CVX": "Energy", "COP": "Energy",
    "BA": "Industrials", "CAT": "Industrials", "GE": "Industrials",
    "WMT": "Consumer Staples", "PG": "Consumer Staples", "KO": "Consumer Staples",
}

# Key competitors for read-across analysis
PEER_MAP = {
    "AAPL": ["MSFT", "GOOGL", "SAMSUNG"],
    "MSFT": ["AAPL", "GOOGL", "AMZN", "CRM"],
    "GOOGL": ["META", "MSFT", "AMZN"],
    "AMZN": ["WMT", "MSFT", "GOOGL", "SHOP"],
    "TSLA": ["F", "GM", "RIVN", "NIO", "BYD"],
    "META": ["GOOGL", "SNAP", "PINS", "MSFT"],
    "NVDA": ["AMD", "INTC", "AVGO", "QCOM"],
    "AMD": ["NVDA", "INTC", "AVGO", "QCOM"],
    "NFLX": ["DIS", "WBD", "PARA", "AMZN"],
    "JPM": ["GS", "MS", "BAC", "WFC", "C"],
    "GS": ["MS", "JPM", "BAC"],
    "JNJ": ["PFE", "MRK", "ABT", "BMY"],
    "XOM": ["CVX", "COP", "BP", "SHEL"],
    "BA": ["LMT", "RTX", "GD", "NOC"],
    "WMT": ["TGT", "COST", "AMZN"],
}

# Major customers / supply chain links
SUPPLY_CHAIN_MAP = {
    "AAPL": {"customers": [], "suppliers": ["TSM", "QCOM", "AVGO", "MU"]},
    "NVDA": {"customers": ["MSFT", "GOOGL", "META", "AMZN"], "suppliers": ["TSM"]},
    "AMD": {"customers": ["MSFT", "GOOGL", "META"], "suppliers": ["TSM"]},
    "TSLA": {"customers": [], "suppliers": ["PANA", "ALB", "CATL"]},
    "MSFT": {"customers": [], "suppliers": ["NVDA", "AMD"]},
    "AMZN": {"customers": [], "suppliers": ["NVDA", "AMD", "INTC"]},
}

# Macro factor sensitivity profiles
MACRO_SENSITIVITY = {
    "Technology": {"rates": "high", "fx": "moderate", "commodities": "low"},
    "Consumer Discretionary": {"rates": "moderate", "fx": "moderate", "commodities": "moderate"},
    "Financials": {"rates": "high", "fx": "low", "commodities": "low"},
    "Healthcare": {"rates": "high", "fx": "moderate", "commodities": "low"},
    "Energy": {"rates": "low", "fx": "moderate", "commodities": "high"},
    "Industrials": {"rates": "moderate", "fx": "moderate", "commodities": "high"},
    "Consumer Staples": {"rates": "low", "fx": "moderate", "commodities": "moderate"},
    "Communication Services": {"rates": "high", "fx": "moderate", "commodities": "low"},
}


class DataFetcher:
    """Fetches and aggregates financial data from multiple sources."""

    def __init__(self, finnhub_api_key: str | None = None):
        self.finnhub_key = finnhub_api_key or os.getenv("FINNHUB_API_KEY", "")
        self.finnhub_client = None
        if self.finnhub_key:
            self.finnhub_client = finnhub.Client(api_key=self.finnhub_key)
        self._request_timestamps: list[float] = []

    def _rate_limit(self) -> None:
        """Simple rate limiter: max 30 requests per minute for Finnhub free tier."""
        now = time.time()
        self._request_timestamps = [t for t in self._request_timestamps if now - t < 60]
        if len(self._request_timestamps) >= 28:
            sleep_time = 60 - (now - self._request_timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        self._request_timestamps.append(time.time())

    def fetch_company_profile(self, ticker: str) -> dict[str, Any]:
        """Fetch company profile from Finnhub."""
        if not self.finnhub_client:
            return {}
        try:
            self._rate_limit()
            return self.finnhub_client.company_profile2(symbol=ticker) or {}
        except Exception:
            return {}

    def fetch_company_news(self, ticker: str) -> list[dict[str, Any]]:
        """Fetch recent news for a ticker from Finnhub."""
        if not self.finnhub_client:
            return []
        try:
            self._rate_limit()
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
            news = self.finnhub_client.company_news(ticker, _from=yesterday, to=today)
            return news[:20] if news else []
        except Exception:
            return []

    def fetch_quote(self, ticker: str) -> dict[str, Any]:
        """Fetch real-time quote data."""
        if not self.finnhub_client:
            return {}
        try:
            self._rate_limit()
            return self.finnhub_client.quote(ticker) or {}
        except Exception:
            return {}

    def fetch_basic_financials(self, ticker: str) -> dict[str, Any]:
        """Fetch basic financial metrics."""
        if not self.finnhub_client:
            return {}
        try:
            self._rate_limit()
            return self.finnhub_client.company_basic_financials(ticker, "all") or {}
        except Exception:
            return {}

    def fetch_insider_transactions(self, ticker: str) -> list[dict[str, Any]]:
        """Fetch recent insider transactions."""
        if not self.finnhub_client:
            return []
        try:
            self._rate_limit()
            result = self.finnhub_client.stock_insider_transactions(ticker)
            if result and "data" in result:
                recent = []
                cutoff = datetime.now(timezone.utc) - timedelta(days=7)
                for txn in result["data"][:10]:
                    txn_date = txn.get("transactionDate", "")
                    if txn_date:
                        try:
                            if datetime.strptime(txn_date, "%Y-%m-%d").replace(
                                tzinfo=timezone.utc
                            ) >= cutoff:
                                recent.append(txn)
                        except ValueError:
                            pass
                return recent
            return []
        except Exception:
            return []

    def fetch_sec_filings(self, ticker: str) -> list[dict[str, Any]]:
        """Fetch recent SEC filings from Finnhub."""
        if not self.finnhub_client:
            return []
        try:
            self._rate_limit()
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).strftime(
                "%Y-%m-%d"
            )
            result = self.finnhub_client.filings(
                symbol=ticker, _from=thirty_days_ago, to=today
            )
            return result[:5] if result else []
        except Exception:
            return []

    def fetch_recommendation_trends(self, ticker: str) -> list[dict[str, Any]]:
        """Fetch analyst recommendation trends."""
        if not self.finnhub_client:
            return []
        try:
            self._rate_limit()
            result = self.finnhub_client.recommendation_trends(ticker)
            return result[:3] if result else []
        except Exception:
            return []

    def fetch_earnings_surprises(self, ticker: str) -> list[dict[str, Any]]:
        """Fetch recent earnings surprises."""
        if not self.finnhub_client:
            return []
        try:
            self._rate_limit()
            result = self.finnhub_client.company_earnings(ticker, limit=4)
            return result if result else []
        except Exception:
            return []

    def fetch_peer_news(self, ticker: str) -> dict[str, list[dict[str, Any]]]:
        """Fetch news for peer companies for read-across analysis."""
        peers = PEER_MAP.get(ticker, [])[:3]
        peer_news = {}
        for peer in peers:
            news = self.fetch_company_news(peer)
            if news:
                peer_news[peer] = news[:5]
        return peer_news

    def fetch_supply_chain_signals(self, ticker: str) -> dict[str, Any]:
        """Fetch news for key supply chain partners."""
        chain = SUPPLY_CHAIN_MAP.get(ticker, {"customers": [], "suppliers": []})
        signals = {"customers": {}, "suppliers": {}}
        for customer in chain.get("customers", [])[:2]:
            news = self.fetch_company_news(customer)
            if news:
                signals["customers"][customer] = news[:3]
        for supplier in chain.get("suppliers", [])[:2]:
            news = self.fetch_company_news(supplier)
            if news:
                signals["suppliers"][supplier] = news[:3]
        return signals

    def fetch_macro_data(self) -> dict[str, Any]:
        """Fetch macro indicators from public RSS feeds and Finnhub."""
        macro = {
            "treasury_10y": None,
            "dxy": None,
            "oil_wti": None,
            "vix": None,
            "economic_calendar": [],
            "fed_news": [],
        }

        # Fetch market indices from Finnhub
        if self.finnhub_client:
            for symbol, key in [("^TNX", "treasury_10y"), ("^VIX", "vix")]:
                try:
                    self._rate_limit()
                    q = self.finnhub_client.quote(symbol)
                    if q and q.get("c"):
                        macro[key] = {"current": q["c"], "change": q.get("dp", 0)}
                except Exception:
                    pass

        # Fetch Fed/macro news from RSS
        try:
            feed = feedparser.parse(
                "https://www.federalreserve.gov/feeds/press_all.xml"
            )
            for entry in feed.entries[:5]:
                macro["fed_news"].append(
                    {
                        "title": entry.get("title", ""),
                        "published": entry.get("published", ""),
                        "link": entry.get("link", ""),
                    }
                )
        except Exception:
            pass

        # Fetch economic calendar from Finnhub
        if self.finnhub_client:
            try:
                self._rate_limit()
                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                cal = self.finnhub_client.calendar_economic()
                if cal and "economicCalendar" in cal:
                    for event in cal["economicCalendar"][:10]:
                        if event.get("date", "") == today:
                            macro["economic_calendar"].append(event)
            except Exception:
                pass

        return macro

    def fetch_all_for_ticker(self, ticker: str) -> dict[str, Any]:
        """Aggregate all data for a single ticker."""
        ticker = ticker.upper().strip()
        profile = self.fetch_company_profile(ticker)
        return {
            "ticker": ticker,
            "company_name": profile.get("name", ticker),
            "sector": SECTOR_MAP.get(ticker, profile.get("finnhubIndustry", "Unknown")),
            "market_cap": profile.get("marketCapitalization", None),
            "profile": profile,
            "quote": self.fetch_quote(ticker),
            "news": self.fetch_company_news(ticker),
            "financials": self.fetch_basic_financials(ticker),
            "insider_transactions": self.fetch_insider_transactions(ticker),
            "sec_filings": self.fetch_sec_filings(ticker),
            "recommendations": self.fetch_recommendation_trends(ticker),
            "earnings_surprises": self.fetch_earnings_surprises(ticker),
            "peer_news": self.fetch_peer_news(ticker),
            "supply_chain": self.fetch_supply_chain_signals(ticker),
            "macro_sensitivity": MACRO_SENSITIVITY.get(
                SECTOR_MAP.get(ticker, ""), {}
            ),
        }
