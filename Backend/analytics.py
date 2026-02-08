# backend/analytics.py
from fastapi import APIRouter, Query
from typing import List
import os, io, pandas as pd
from stock_data import get_price, get_live_prices, get_portfolio_value, get_technical_indicators
from risk_tools import calculate_risk_metrics, detect_anomalies
from ml_models import (
    predict_next_price, predict_buy_risk, calculate_sharpe_ratio,
    get_backtest_data, pca_analysis
)
from fastapi.responses import StreamingResponse, FileResponse

router = APIRouter()

@router.get("/stock-price/")
def stock_price(ticker: str):
    return get_price(ticker)

@router.get("/live-prices/")
def live_prices(tickers: List[str] = Query(...)):
    return get_live_prices(tickers)

@router.get("/portfolio-value/")
def portfolio_value(tickers: List[str] = Query(...), quantities: List[int] = Query(...)):
    return get_portfolio_value(tickers, quantities)

@router.get("/risk-metrics/")
def risk_metrics(ticker: str):
    return calculate_risk_metrics(ticker, save_plot=True)

@router.get("/anomalies/")
def anomalies(ticker: str):
    return detect_anomalies(ticker, save_plot=True)

@router.get("/predict-price/")
def predict_price(ticker: str):
    return predict_next_price(ticker)

@router.get("/predict-risk/")
def predict_risk(ticker: str):
    return predict_buy_risk(ticker)

@router.get("/sharpe-ratio/")
def sharpe(ticker: str):
    return calculate_sharpe_ratio(ticker)

@router.get("/backtest/")
def backtest(ticker: str):
    return get_backtest_data(ticker)

@router.get("/pca-analysis/")
def pca(ticker: str):
    return pca_analysis(ticker)

@router.get("/technical-indicators/")
def technical_indicators(ticker: str):
    return get_technical_indicators(ticker)

@router.get("/export-report/")
def export_report(ticker: str = Query(...)):
    dataset_path = "dataset/"
    file_path = os.path.join(dataset_path, f"{ticker}.csv")

    if not os.path.exists(file_path):
        return {"error": f"Dataset for {ticker} not found."}

    df = pd.read_csv(file_path)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={ticker}_report.csv"}
    )

@router.get("/download-plot/")
def download_plot(path: str):
    return FileResponse(path)
