"""
Report generation module for Company News Tracker.
Synthesizes raw data into structured equity research morning notes.
"""

from datetime import datetime, timezone
from typing import Any


def _fmt_number(value: float | int | None, prefix: str = "", suffix: str = "") -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        if abs(value) >= 1e9:
            return f"{prefix}{value / 1e9:.1f}B{suffix}"
        if abs(value) >= 1e6:
            return f"{prefix}{value / 1e6:.1f}M{suffix}"
        return f"{prefix}{value:.2f}{suffix}"
    return f"{prefix}{value}{suffix}"


def _fmt_pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def _classify_news(headlines: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Classify news items by category based on keyword analysis."""
    categories = {
        "earnings": [],
        "strategic": [],
        "operational": [],
        "regulatory": [],
        "analyst": [],
        "market": [],
        "other": [],
    }

    earnings_kw = [
        "earnings", "revenue", "profit", "loss", "eps", "guidance", "forecast",
        "quarter", "fiscal", "margin", "beat", "miss", "results", "income",
        "outlook", "raised", "lowered", "exceeded",
    ]
    strategic_kw = [
        "merger", "acquisition", "acquire", "deal", "ceo", "cfo", "board",
        "insider", "buyback", "dividend", "restructur", "spinoff", "ipo",
        "partnership", "joint venture", "appoint", "resign",
    ]
    operational_kw = [
        "launch", "product", "release", "fda", "approval", "clinical", "trial",
        "patent", "capacity", "expansion", "factory", "plant", "production",
        "capex", "r&d", "innovation",
    ]
    regulatory_kw = [
        "sec", "ftc", "doj", "antitrust", "lawsuit", "litigation", "fine",
        "penalty", "investigation", "regulatory", "compliance", "sanction",
        "tariff", "ban", "subpoena",
    ]
    analyst_kw = [
        "upgrade", "downgrade", "price target", "rating", "overweight",
        "underweight", "buy", "sell", "hold", "outperform", "analyst",
    ]

    for item in headlines:
        text = (item.get("headline", "") + " " + item.get("summary", "")).lower()
        classified = False
        for kw_list, cat in [
            (earnings_kw, "earnings"),
            (strategic_kw, "strategic"),
            (operational_kw, "operational"),
            (regulatory_kw, "regulatory"),
            (analyst_kw, "analyst"),
        ]:
            if any(kw in text for kw in kw_list):
                categories[cat].append(item)
                classified = True
                break
        if not classified:
            categories["other"].append(item)

    return categories


def _generate_section_1(data: dict[str, Any]) -> str:
    """Section 1: Idiosyncratic Corporate Developments."""
    lines = []
    classified = _classify_news(data.get("news", []))
    financials = data.get("financials", {})
    metrics = financials.get("metric", {}) if financials else {}
    earnings = data.get("earnings_surprises", [])
    insider = data.get("insider_transactions", [])
    filings = data.get("sec_filings", [])

    has_content = False

    # Earnings & Financials
    earnings_lines = []
    if earnings:
        latest = earnings[0]
        actual_eps = latest.get("actual")
        est_eps = latest.get("estimate")
        period = latest.get("period", "")
        if actual_eps is not None and est_eps is not None:
            surprise = actual_eps - est_eps
            surprise_pct = (surprise / abs(est_eps) * 100) if est_eps != 0 else 0
            beat_miss = "Beat" if surprise > 0 else "Miss"
            earnings_lines.append(
                f"  - **Latest EPS ({period}):** ${actual_eps:.2f} vs. "
                f"${est_eps:.2f} est. — **{beat_miss}** by "
                f"${abs(surprise):.2f} ({_fmt_pct(surprise_pct)})"
            )

    # Margin analysis from metrics
    gm = metrics.get("grossMarginAnnual") or metrics.get("grossMarginTTM")
    om = metrics.get("operatingMarginAnnual") or metrics.get("operatingMarginTTM")
    nm = metrics.get("netProfitMarginAnnual") or metrics.get("netProfitMarginTTM")
    if gm or om or nm:
        margin_parts = []
        if gm:
            margin_parts.append(f"Gross {gm:.1f}%")
        if om:
            margin_parts.append(f"Operating {om:.1f}%")
        if nm:
            margin_parts.append(f"Net {nm:.1f}%")
        earnings_lines.append(f"  - **Margin Profile:** {' | '.join(margin_parts)}")

    # Revenue growth
    rev_growth = metrics.get("revenueGrowthQuarterlyYoy") or metrics.get(
        "revenueGrowthTTMYoy"
    )
    if rev_growth:
        earnings_lines.append(
            f"  - **Revenue Growth (YoY):** {_fmt_pct(rev_growth)} — "
            + ("Accelerating" if rev_growth > 10 else "Decelerating" if rev_growth < 0 else "Stable")
            + " top-line trajectory."
        )

    # Earnings-related news
    for item in classified.get("earnings", [])[:3]:
        headline = item.get("headline", "")
        earnings_lines.append(f"  - {headline}")
        summary = item.get("summary", "")
        if summary:
            so_what = _extract_so_what(summary, "earnings")
            if so_what:
                earnings_lines.append(f"    - **So What?** {so_what}")

    if earnings_lines:
        has_content = True
        lines.append("**Earnings & Financials**")
        lines.extend(earnings_lines)
        lines.append("")

    # Strategic & Governance
    strategic_lines = []
    for item in classified.get("strategic", [])[:3]:
        headline = item.get("headline", "")
        strategic_lines.append(f"  - {headline}")
        summary = item.get("summary", "")
        if summary:
            so_what = _extract_so_what(summary, "strategic")
            if so_what:
                strategic_lines.append(f"    - **So What?** {so_what}")

    # Insider transactions
    if insider:
        for txn in insider[:3]:
            name = txn.get("name", "Unknown")
            shares = txn.get("share", 0)
            txn_type = "Purchase" if shares > 0 else "Sale"
            value = abs(shares * (txn.get("transactionPrice", 0) or 0))
            if value > 100000:
                strategic_lines.append(
                    f"  - **Insider {txn_type}:** {name} — "
                    f"{abs(shares):,.0f} shares ({_fmt_number(value, prefix='$')}). "
                    + (
                        "Bullish signal: management conviction."
                        if txn_type == "Purchase"
                        else "Monitor for pattern of distribution."
                    )
                )

    # Material SEC filings
    material_filings = ["8-K", "10-K", "10-Q", "S-1", "13D", "13G", "SC 13D"]
    for filing in filings:
        form = filing.get("form", "")
        if form in material_filings:
            filed_date = filing.get("filedDate", "")
            strategic_lines.append(
                f"  - **SEC Filing ({form}):** Filed {filed_date}. "
                f"Review for material disclosures."
            )

    if strategic_lines:
        has_content = True
        lines.append("**Strategic & Governance**")
        lines.extend(strategic_lines)
        lines.append("")

    # Operational Catalysts
    ops_lines = []
    for item in classified.get("operational", [])[:3]:
        headline = item.get("headline", "")
        ops_lines.append(f"  - {headline}")
        summary = item.get("summary", "")
        if summary:
            so_what = _extract_so_what(summary, "operational")
            if so_what:
                ops_lines.append(f"    - **So What?** {so_what}")

    if ops_lines:
        has_content = True
        lines.append("**Operational Catalysts**")
        lines.extend(ops_lines)
        lines.append("")

    if not has_content:
        return ""

    header = "### 1. Idiosyncratic Corporate Developments (Alpha Drivers)\n\n"
    return header + "\n".join(lines)


def _generate_section_2(data: dict[str, Any]) -> str:
    """Section 2: Demand Signals & Value Chain Read-Across."""
    lines = []
    supply_chain = data.get("supply_chain", {})

    customer_signals = supply_chain.get("customers", {})
    supplier_signals = supply_chain.get("suppliers", {})

    if not customer_signals and not supplier_signals:
        return ""

    if customer_signals:
        lines.append("**Customer Health**")
        for customer, news in customer_signals.items():
            for item in news[:2]:
                headline = item.get("headline", "")
                lines.append(f"  - **{customer}:** {headline}")
                summary = item.get("summary", "")
                if summary:
                    so_what = _extract_so_what(summary, "demand")
                    if so_what:
                        lines.append(
                            f"    - **Read-Through for {data['ticker']}:** {so_what}"
                        )
        lines.append("")

    if supplier_signals:
        lines.append("**Supply Chain Signals**")
        for supplier, news in supplier_signals.items():
            for item in news[:2]:
                headline = item.get("headline", "")
                lines.append(f"  - **{supplier}:** {headline}")
                summary = item.get("summary", "")
                if summary:
                    so_what = _extract_so_what(summary, "supply")
                    if so_what:
                        lines.append(f"    - **Implication:** {so_what}")
        lines.append("")

    if not lines:
        return ""

    header = "### 2. Demand Signals & Value Chain Read-Across\n\n"
    return header + "\n".join(lines)


def _generate_section_3(data: dict[str, Any]) -> str:
    """Section 3: Competitive Landscape & Peer Read-Across."""
    lines = []
    peer_news = data.get("peer_news", {})
    recommendations = data.get("recommendations", [])

    if not peer_news and not recommendations:
        return ""

    if peer_news:
        lines.append("**Peer Developments**")
        for peer, news in peer_news.items():
            material_news = [n for n in news if _is_material(n)]
            for item in material_news[:2]:
                headline = item.get("headline", "")
                lines.append(f"  - **{peer}:** {headline}")
                summary = item.get("summary", "")
                if summary:
                    so_what = _extract_so_what(summary, "competitive")
                    if so_what:
                        lines.append(
                            f"    - **Read-Through for {data['ticker']}:** {so_what}"
                        )
        lines.append("")

    if recommendations:
        latest = recommendations[0]
        total = (
            (latest.get("buy", 0) or 0)
            + (latest.get("hold", 0) or 0)
            + (latest.get("sell", 0) or 0)
            + (latest.get("strongBuy", 0) or 0)
            + (latest.get("strongSell", 0) or 0)
        )
        if total > 0:
            lines.append("**Consensus Positioning**")
            lines.append(
                f"  - **Analyst Consensus ({latest.get('period', 'Latest')}):** "
                f"Strong Buy: {latest.get('strongBuy', 0)} | "
                f"Buy: {latest.get('buy', 0)} | "
                f"Hold: {latest.get('hold', 0)} | "
                f"Sell: {latest.get('sell', 0)} | "
                f"Strong Sell: {latest.get('strongSell', 0)}"
            )
            bull_ratio = (
                (latest.get("strongBuy", 0) or 0) + (latest.get("buy", 0) or 0)
            ) / total
            if bull_ratio > 0.7:
                lines.append(
                    "  - Consensus is overwhelmingly bullish. "
                    "Crowded positioning may limit upside surprise."
                )
            elif bull_ratio < 0.3:
                lines.append(
                    "  - Consensus is bearish. "
                    "Any positive catalyst could drive a short-squeeze / re-rating."
                )
            lines.append("")

    if not lines:
        return ""

    header = "### 3. Competitive Landscape & Peer Read-Across\n\n"
    return header + "\n".join(lines)


def _generate_section_4(data: dict[str, Any], macro: dict[str, Any]) -> str:
    """Section 4: Macroeconomic & Thematic Overlay."""
    lines = []
    sensitivity = data.get("macro_sensitivity", {})
    sector = data.get("sector", "Unknown")

    if not sensitivity and not macro:
        return ""

    # Rates
    treasury = macro.get("treasury_10y")
    if treasury and sensitivity.get("rates") in ("high", "moderate"):
        current = treasury.get("current", "N/A")
        change = treasury.get("change", 0)
        direction = "higher" if change > 0 else "lower"
        impact = "headwind" if (change > 0 and sector in ["Technology", "Healthcare", "Communication Services"]) else "tailwind"
        lines.append(
            f"  - **10Y Treasury:** {current}% ({_fmt_pct(change)} today) — "
            f"Rates moving {direction}, a **{impact}** for {sector} multiples. "
            f"Sensitivity: **{sensitivity.get('rates', 'N/A').upper()}**."
        )

    # VIX
    vix = macro.get("vix")
    if vix:
        current = vix.get("current", "N/A")
        change = vix.get("change", 0)
        regime = "elevated vol" if current and current > 20 else "low vol"
        lines.append(
            f"  - **VIX:** {current} ({_fmt_pct(change)}) — {regime} regime."
        )

    # Economic calendar
    econ_cal = macro.get("economic_calendar", [])
    if econ_cal:
        lines.append("  - **Economic Calendar (Today):**")
        for event in econ_cal[:5]:
            event_name = event.get("event", "Unknown")
            lines.append(f"    - {event_name}")

    # Fed news
    fed_news = macro.get("fed_news", [])
    if fed_news:
        lines.append("  - **Fed/Policy:**")
        for item in fed_news[:3]:
            lines.append(f"    - {item.get('title', '')}")

    if not lines:
        return ""

    header = "### 4. Macroeconomic & Thematic Overlay (Beta Drivers)\n\n"
    return header + "\n".join(lines)


def _generate_section_5(data: dict[str, Any]) -> str:
    """Section 5: Other Material Factors."""
    classified = _classify_news(data.get("news", []))
    regulatory = classified.get("regulatory", [])

    if not regulatory:
        return ""

    lines = []
    for item in regulatory[:3]:
        headline = item.get("headline", "")
        lines.append(f"  - {headline}")
        summary = item.get("summary", "")
        if summary:
            so_what = _extract_so_what(summary, "regulatory")
            if so_what:
                lines.append(f"    - **So What?** {so_what}")

    if not lines:
        return ""

    header = "### 5. Other Material Factors (Exogenous Shocks)\n\n"
    return header + "\n".join(lines)


def _extract_so_what(summary: str, context: str) -> str:
    """Extract an actionable 'So What?' from a news summary.
    Uses keyword-based heuristic analysis to generate implications.
    """
    summary_lower = summary.lower()

    if context == "earnings":
        if any(w in summary_lower for w in ["beat", "exceeded", "above"]):
            return "Positive earnings momentum; monitor for estimate revisions upward."
        if any(w in summary_lower for w in ["miss", "below", "disappoint"]):
            return "Earnings miss signals potential downside risk to forward estimates."
        if any(w in summary_lower for w in ["guidance", "outlook", "raised"]):
            return "Forward guidance revision likely to drive consensus estimate changes."
        return "Review for quality-of-earnings signals and margin trajectory."

    if context == "strategic":
        if any(w in summary_lower for w in ["acquire", "merger", "deal"]):
            return "M&A activity — assess deal accretion/dilution and integration risk."
        if any(w in summary_lower for w in ["ceo", "cfo", "appoint", "resign"]):
            return "Leadership change introduces execution uncertainty; monitor transition."
        if any(w in summary_lower for w in ["buyback", "repurchase"]):
            return "Capital return signals management confidence in intrinsic value."
        return "Strategic shift — reassess competitive positioning and capital allocation."

    if context == "operational":
        if any(w in summary_lower for w in ["launch", "release", "new product"]):
            return "Product catalyst — monitor adoption metrics and channel feedback."
        if any(w in summary_lower for w in ["fda", "approval", "clinical"]):
            return "Regulatory catalyst with binary outcome risk to valuation."
        if any(w in summary_lower for w in ["expansion", "capacity", "capex"]):
            return "CapEx signal implies management confidence in demand trajectory."
        return "Operational development — assess impact on unit economics."

    if context == "demand":
        if any(w in summary_lower for w in ["strong", "growth", "increase", "expand"]):
            return "Positive demand signal — tailwind for upstream supplier revenue."
        if any(w in summary_lower for w in ["weak", "decline", "cut", "reduce"]):
            return "Demand softening — potential headwind to revenue expectations."
        return "Monitor for read-through to order book and pricing power."

    if context == "supply":
        if any(w in summary_lower for w in ["shortage", "constrain", "delay"]):
            return "Supply disruption risk — may impact production timelines and COGS."
        if any(w in summary_lower for w in ["expand", "ramp", "increase capacity"]):
            return "Supply normalization — potential margin tailwind as costs ease."
        return "Supply chain signal — assess impact on lead times and input costs."

    if context == "competitive":
        if any(w in summary_lower for w in ["gain", "share", "win", "strong"]):
            return "Peer strength may indicate sector tailwind (sympathy) or share loss (zero-sum)."
        if any(w in summary_lower for w in ["lose", "weak", "warn", "decline"]):
            return "Peer weakness — potential share gain opportunity if sector-specific."
        return "Peer development — assess competitive read-through."

    if context == "regulatory":
        if any(w in summary_lower for w in ["fine", "penalty", "lawsuit"]):
            return "Litigation/regulatory risk — quantify potential financial impact."
        if any(w in summary_lower for w in ["approve", "clear", "favorable"]):
            return "Regulatory tailwind — removes overhang from valuation."
        return "Exogenous risk factor — monitor for escalation or resolution."

    return ""


def _is_material(news_item: dict[str, Any]) -> bool:
    """Heuristic to determine if a news item is likely material."""
    headline = (news_item.get("headline", "") + " " + news_item.get("summary", "")).lower()
    material_kw = [
        "earnings", "revenue", "acquisition", "merger", "ceo", "cfo", "guidance",
        "fda", "lawsuit", "antitrust", "upgrade", "downgrade", "price target",
        "restructur", "layoff", "dividend", "buyback", "warning", "recall",
        "investigation", "breach", "patent",
    ]
    return any(kw in headline for kw in material_kw)


def generate_morning_note(
    ticker_data: list[dict[str, Any]], macro_data: dict[str, Any]
) -> str:
    """Generate a complete Daily Morning Note for all tickers."""
    now = datetime.now(timezone.utc)
    report_lines = [
        f"# Daily Morning Note — {now.strftime('%B %d, %Y')}",
        "",
        f"*Generated: {now.strftime('%H:%M UTC')} | Equity Research Desk*",
        "",
        "---",
        "",
    ]

    for data in ticker_data:
        ticker = data["ticker"]
        name = data.get("company_name", ticker)
        sector = data.get("sector", "N/A")
        quote = data.get("quote", {})

        current_price = quote.get("c")
        change_pct = quote.get("dp")
        prev_close = quote.get("pc")
        high = quote.get("h")
        low = quote.get("l")

        # Header block
        report_lines.append(f"## {ticker} — {name}")
        report_lines.append("")

        if current_price:
            price_direction = "up" if (change_pct and change_pct > 0) else "down"
            report_lines.append(
                f"**Price:** ${current_price:.2f} | "
                f"**Chg:** {_fmt_pct(change_pct)} | "
                f"**Range:** ${low:.2f}–${high:.2f} | "
                f"**Prev Close:** ${prev_close:.2f} | "
                f"**Sector:** {sector}"
            )
        else:
            report_lines.append(f"**Sector:** {sector}")

        mkt_cap = data.get("market_cap")
        if mkt_cap:
            report_lines.append(f"**Market Cap:** {_fmt_number(mkt_cap * 1e6, prefix='$')}")

        report_lines.append("")

        # Generate each section
        sections = [
            _generate_section_1(data),
            _generate_section_2(data),
            _generate_section_3(data),
            _generate_section_4(data, macro_data),
            _generate_section_5(data),
        ]

        active_sections = [s for s in sections if s.strip()]

        if active_sections:
            report_lines.extend(s + "\n" for s in active_sections)
        else:
            report_lines.append(
                "*No material developments in the last 24 hours. "
                "Maintain existing thesis and positioning.*"
            )
            report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

    # Disclaimer
    report_lines.extend([
        "*This report is generated from automated data aggregation and "
        "heuristic analysis. All investment decisions should incorporate "
        "independent fundamental research. Data sourced from Finnhub, "
        "public RSS feeds, and SEC filings.*",
    ])

    return "\n".join(report_lines)
