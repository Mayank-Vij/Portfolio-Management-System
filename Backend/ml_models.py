
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')  # Ensure no GUI issues in server
import matplotlib.pyplot as plt

def load_stock_data(ticker: str):
    """Helper to load stock CSV"""
    df = pd.read_csv(f"dataset/{ticker}.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    return df

def predict_next_price(ticker: str):
    """Predict next day's close price using Linear Regression"""
    try:
        df = load_stock_data(ticker)
        df = df.reset_index()

        # Feature: number of days
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['Close'].values

        model = LinearRegression()
        model.fit(X, y)

        next_day = np.array([[len(df)]])
        predicted_price = model.predict(next_day)[0]
        last_close = df['Close'].iloc[-1]
        confidence = round(100 - abs(predicted_price - last_close) / last_close * 100, 2)

        return {
            "ticker": ticker,
            "last_close": round(last_close, 2),
            "predicted_next_close": round(predicted_price, 2),
            "confidence_percentage": confidence
        }

    except Exception as e:
        return {"error": str(e)}

def predict_buy_risk(ticker: str):
    """Predict buy risk based on recent volatility"""
    try:
        df = load_stock_data(ticker)
        returns = df['Close'].pct_change().dropna()
        recent_volatility = returns.rolling(window=5).std().iloc[-1]

        if recent_volatility < 0.01:
            risk = "Low"
        elif recent_volatility < 0.02:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "ticker": ticker,
            "recent_volatility": round(recent_volatility, 4),
            "predicted_risk_level": risk
        }

    except Exception as e:
        return {"error": str(e)}

def calculate_sharpe_ratio(ticker: str):
    """Calculate Sharpe ratio (annualized)"""
    try:
        df = load_stock_data(ticker)
        returns = df['Close'].pct_change().dropna()
        mean_return = returns.mean()
        std_return = returns.std()
        sharpe_ratio = (mean_return / std_return) * np.sqrt(252)  # 252 trading days

        return {
            "ticker": ticker,
            "sharpe_ratio": round(sharpe_ratio, 2)
        }

    except Exception as e:
        return {"error": str(e)}

def get_backtest_data(ticker: str):
    """Provide simple backtest simulation on last 30 days"""
    try:
        df = load_stock_data(ticker)
        df = df.tail(30).copy()
        df['daily_return'] = df['Close'].pct_change()
        df['cumulative_return'] = (1 + df['daily_return']).cumprod()

        return df[['Date', 'Close', 'cumulative_return']].dropna().to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
# At the bottom of ml_models.py

def pca_analysis(ticker: str):
    """Perform PCA on multiple price features (OHLC) and save explained variance plot."""
    try:
        df = pd.read_csv(f"dataset/{ticker}.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').tail(60)  # Use last 60 days

        # Use multiple features for PCA
        price_data = df[['Open', 'High', 'Low', 'Close']]
        returns = price_data.pct_change().dropna()  # % change across OHLC

        pca = PCA()
        pca.fit(returns)

        explained_variance = pca.explained_variance_ratio_

        # Save the variance plot
        os.makedirs("plots", exist_ok=True)
        plt.figure(figsize=(6, 4))
        plt.plot(np.cumsum(explained_variance), marker='o')
        plt.title(f"PCA Explained Variance - {ticker}")
        plt.xlabel('Number of Components')
        plt.ylabel('Cumulative Explained Variance')
        plt.grid(True)
        path = f"plots/{ticker}_pca_variance.png"
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        return {"plot_path": path}

    except Exception as e:
        return {"error": str(e)}