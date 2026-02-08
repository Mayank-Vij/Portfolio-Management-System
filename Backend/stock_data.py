from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os

# ================================
#  CONFIG
# ================================
API_KEY = "GCLOWXNNGJNB2196"     # ← replace with your real key
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Converts ticker to Indian exchange format
def format_ticker(ticker: str):
    """
    NSE stocks → add .NS
    BSE stocks → add .BSE
    Example:
    INFY → INFY.NS
    RELIANCE → RELIANCE.NS
    SBIN → SBIN.NS
    """
    if "." in ticker:    # already formatted
        return ticker
    return ticker.upper() + ".NS"


# ================================
#  LIVE PRICE — SINGLE TICKER
# ================================
def get_price(ticker: str):
    try:
        formatted = format_ticker(ticker)
        data, meta = ts.get_quote_endpoint(formatted)
        price = float(data["05. price"].iloc[0])
        return {"ticker": ticker, "price": price}
    except Exception as e:
        return {"error": str(e)}


# ================================
#  LIVE PRICES — MULTIPLE TICKERS
# ================================
def get_live_prices(tickers: list):
    resp = []
    for t in tickers:
        resp.append(get_price(t))
    return {"live_prices": resp}


# ================================
#  PORTFOLIO VALUE
# ================================
def get_portfolio_value(tickers: list, quantities: list):
    details = []
    total_value = 0

    for ticker, qty in zip(tickers, quantities):
        data = get_price(ticker)
        if "price" in data:
            value = data["price"] * qty
            total_value += value

            details.append({
                "ticker": ticker,
                "qty": qty,
                "price": data["price"],
                "value": value
            })

    return {
        "total_portfolio_value": total_value,
        "details": details
    }


# ================================
#  TECHNICAL INDICATORS
# ================================
def get_technical_indicators(ticker: str):
    try:
        formatted = format_ticker(ticker)
        df, metadata = ts.get_daily(formatted, outputsize='compact')
        df = df.sort_index()

        df['SMA_14'] = df['4. close'].rolling(14).mean()
        df['RSI_14'] = compute_rsi(df['4. close'])

        last = df.iloc[-1]
        return {
            "ticker": ticker,
            "latest_close": float(last["4. close"]),
            "SMA_14": round(float(last["SMA_14"]), 2),
            "RSI_14": round(float(last["RSI_14"]), 2)
        }
    except Exception as e:
        return {"error": str(e)}


# ================================
#  RSI CALCULATION
# ================================
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
