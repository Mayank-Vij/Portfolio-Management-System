import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_risk_metrics(ticker: str, save_plot=False):
    """Calculate standard deviation and VaR(95%) using offline data."""
    try:
        df = pd.read_csv(f"dataset/{ticker}.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        returns = df['Close'].pct_change().dropna()

        std_dev = round(returns.std(), 4)
        var_95 = round(np.percentile(returns, 5), 4)

        if save_plot:
            os.makedirs("plots", exist_ok=True)
            plt.figure(figsize=(8, 4))
            plt.hist(returns, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
            plt.axvline(var_95, color='red', linestyle='--', label=f'VaR 95%: {var_95}')
            plt.title(f"{ticker} - Daily Returns Histogram")
            plt.xlabel("Daily Return")
            plt.ylabel("Frequency")
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"plots/{ticker}_risk_histogram.png")
            plt.close()

        return {
            "ticker": ticker,
            "standard_deviation": std_dev,
            "VaR_95": var_95,
            "plot_path": f"plots/{ticker}_risk_histogram.png" if save_plot else None
        }

    except Exception as e:
        return {"error": str(e)}


def detect_anomalies(ticker: str, save_plot=False):
    """Detect anomalies based on Z-Score using offline dataset."""
    try:
        df = pd.read_csv(f"dataset/{ticker}.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        # Calculate daily returns and remove the first NaN
        returns = df['Close'].pct_change().dropna()
        dates = df['Date'].iloc[1:]  # Align dates with returns

        # Compute z-scores
        z_scores = (returns - returns.mean()) / returns.std()
        anomalies = z_scores[abs(z_scores) > 3]

        # Align anomaly dates with return indices
        anomaly_dates = dates.loc[anomalies.index]
        anomaly_returns = returns.loc[anomalies.index]

        if save_plot:
            os.makedirs("plots", exist_ok=True)
            plt.figure(figsize=(12, 4))
            plt.plot(dates, returns, label='Returns', color='blue')
            plt.scatter(anomaly_dates, anomaly_returns, color='red', label='Anomalies')
            plt.title(f"{ticker} - Return Anomalies")
            plt.xlabel("Date")
            plt.ylabel("Daily Return")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"plots/{ticker}_anomalies_plot.png")
            plt.close()

        return {
            "ticker": ticker,
            "anomalies_detected": len(anomaly_dates),
            "anomaly_dates": anomaly_dates.dt.strftime('%Y-%m-%d').tolist(),
            "plot_path": f"plots/{ticker}_anomalies_plot.png" if save_plot else None
        }

    except Exception as e:
        return {"error": str(e)}
