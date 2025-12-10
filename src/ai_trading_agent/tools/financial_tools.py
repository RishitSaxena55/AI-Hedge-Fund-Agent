from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Tool 1: Real-Time Stock Data Tool
class StockDataInput(BaseModel):
    """Input for StockDataTool"""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA)")
    period: str = Field(default="1mo", description="Data period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
    interval: str = Field(default="1d", description="Data interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo")

class StockDataTool(BaseTool):
    name: str = "Get Real-Time Stock Data"
    description: str = "Fetches real-time and historical stock price data including OHLCV, volume, and market cap"
    args_schema: Type[BaseModel] = StockDataInput

    def _run(self, ticker: str, period: str = "1mo", interval: str = "1d") -> str:
        try:
            stock = yf.Ticker(ticker)
            
            # Get historical data
            hist = stock.history(period=period, interval=interval)
            
            # Get current info
            info = stock.info
            
            # Calculate basic metrics
            current_price = info.get('currentPrice', 0)
            prev_close = info.get('previousClose', 0)
            change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
            
            # Get recent data
            recent_data = hist.tail(5).to_string()
            
            result = f"""
Stock Data for {ticker}:

Current Price: ${current_price:.2f}
Previous Close: ${prev_close:.2f}
Change: {change_pct:+.2f}%

Market Cap: ${info.get('marketCap', 0):,.0f}
52 Week High: ${info.get('fiftyTwoWeekHigh', 0):.2f}
52 Week Low: ${info.get('fiftyTwoWeekLow', 0):.2f}
Average Volume: {info.get('averageVolume', 0):,.0f}

P/E Ratio: {info.get('trailingPE', 'N/A')}
EPS: ${info.get('trailingEps', 0):.2f}
Dividend Yield: {info.get('dividendYield', 0)*100:.2f}%

Recent Price History:
{recent_data}

Sector: {info.get('sector', 'N/A')}
Industry: {info.get('industry', 'N/A')}
"""
            return result
            
        except Exception as e:
            return f"Error fetching stock data for {ticker}: {str(e)}"


# Tool 2: Technical Indicators Tool
class TechnicalIndicatorsInput(BaseModel):
    """Input for TechnicalIndicatorsTool"""
    ticker: str = Field(..., description="Stock ticker symbol")
    indicators: str = Field(default="RSI,MACD,SMA,EMA", description="Comma-separated indicators to fetch")

class TechnicalIndicatorsTool(BaseTool):
    name: str = "Get Technical Indicators"
    description: str = "Fetches technical indicators like RSI, MACD, SMA, EMA, Bollinger Bands for technical analysis"
    args_schema: Type[BaseModel] = TechnicalIndicatorsInput

    def _run(self, ticker: str, indicators: str = "RSI,MACD,SMA,EMA") -> str:
        try:
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
            ti = TechIndicators(key=api_key, output_format='pandas')
            
            results = []
            indicator_list = [ind.strip() for ind in indicators.split(',')]
            
            for indicator in indicator_list:
                if indicator == "RSI":
                    data, meta = ti.get_rsi(symbol=ticker, interval='daily', time_period=14)
                    latest_rsi = data.iloc[0]['RSI']
                    results.append(f"RSI (14): {latest_rsi:.2f}")
                    
                    # Interpretation
                    if latest_rsi > 70:
                        results.append("  → Overbought (potential sell signal)")
                    elif latest_rsi < 30:
                        results.append("  → Oversold (potential buy signal)")
                    else:
                        results.append("  → Neutral")
                        
                elif indicator == "MACD":
                    data, meta = ti.get_macd(symbol=ticker, interval='daily')
                    latest = data.iloc[0]
                    results.append(f"MACD: {latest['MACD']:.4f}")
                    results.append(f"Signal: {latest['MACD_Signal']:.4f}")
                    results.append(f"Histogram: {latest['MACD_Hist']:.4f}")
                    
                    if latest['MACD'] > latest['MACD_Signal']:
                        results.append("  → Bullish crossover")
                    else:
                        results.append("  → Bearish crossover")
                        
                elif indicator == "SMA":
                    data_20, _ = ti.get_sma(symbol=ticker, interval='daily', time_period=20)
                    data_50, _ = ti.get_sma(symbol=ticker, interval='daily', time_period=50)
                    sma_20 = data_20.iloc[0]['SMA']
                    sma_50 = data_50.iloc[0]['SMA']
                    results.append(f"SMA (20): ${sma_20:.2f}")
                    results.append(f"SMA (50): ${sma_50:.2f}")
                    
                    if sma_20 > sma_50:
                        results.append("  → Bullish trend (Golden Cross)")
                    else:
                        results.append("  → Bearish trend (Death Cross)")
            
            return f"\nTechnical Indicators for {ticker}:\n" + "\n".join(results)
            
        except Exception as e:
            return f"Error fetching technical indicators: {str(e)}"


# Tool 3: Financial News Tool
class FinancialNewsInput(BaseModel):
    """Input for FinancialNewsTool"""
    ticker: str = Field(..., description="Stock ticker symbol or company name")
    days: int = Field(default=7, description="Number of days of news to fetch")

class FinancialNewsTool(BaseTool):
    name: str = "Get Financial News"
    description: str = "Fetches latest financial news and sentiment for a stock or company"
    args_schema: Type[BaseModel] = FinancialNewsInput

    def _run(self, ticker: str, days: int = 7) -> str:
        try:
            # Get company name for better search
            stock = yf.Ticker(ticker)
            company_name = stock.info.get('longName', ticker)
            
            # Search for news using Serper
            serper_api_key = os.getenv('SERPER_API_KEY')
            url = "https://google.serper.dev/search"
            
            payload = {
                "q": f"{company_name} {ticker} stock news",
                "num": 10,
                "tbm": "nws"  # News search
            }
            
            headers = {
                'X-API-KEY': serper_api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            news_items = []
            for item in data.get('news', [])[:5]:
                news_items.append(f"""
Title: {item.get('title')}
Source: {item.get('source')}
Date: {item.get('date')}
Snippet: {item.get('snippet')}
Link: {item.get('link')}
---""")
            
            return f"\nRecent News for {ticker} ({company_name}):\n" + "\n".join(news_items)
            
        except Exception as e:
            return f"Error fetching news: {str(e)}"


# Tool 4: Fundamental Analysis Tool
class FundamentalAnalysisInput(BaseModel):
    """Input for FundamentalAnalysisTool"""
    ticker: str = Field(..., description="Stock ticker symbol")

class FundamentalAnalysisTool(BaseTool):
    name: str = "Get Fundamental Data"
    description: str = "Fetches comprehensive fundamental data including financials, ratios, and valuation metrics"
    args_schema: Type[BaseModel] = FundamentalAnalysisInput

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get financial statements
            income_stmt = stock.income_stmt
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
            
            result = f"""
Fundamental Analysis for {ticker}:

=== VALUATION METRICS ===
Market Cap: ${info.get('marketCap', 0):,.0f}
Enterprise Value: ${info.get('enterpriseValue', 0):,.0f}
P/E Ratio (Trailing): {info.get('trailingPE', 'N/A')}
Forward P/E: {info.get('forwardPE', 'N/A')}
PEG Ratio: {info.get('pegRatio', 'N/A')}
Price to Book: {info.get('priceToBook', 'N/A')}
Price to Sales: {info.get('priceToSalesTrailing12Months', 'N/A')}

=== PROFITABILITY ===
Profit Margins: {info.get('profitMargins', 0)*100:.2f}%
Operating Margins: {info.get('operatingMargins', 0)*100:.2f}%
Return on Equity: {info.get('returnOnEquity', 0)*100:.2f}%
Return on Assets: {info.get('returnOnAssets', 0)*100:.2f}%

=== FINANCIAL HEALTH ===
Total Cash: ${info.get('totalCash', 0):,.0f}
Total Debt: ${info.get('totalDebt', 0):,.0f}
Debt to Equity: {info.get('debtToEquity', 'N/A')}
Current Ratio: {info.get('currentRatio', 'N/A')}
Quick Ratio: {info.get('quickRatio', 'N/A')}

=== GROWTH METRICS ===
Revenue Growth: {info.get('revenueGrowth', 0)*100:.2f}%
Earnings Growth: {info.get('earningsGrowth', 0)*100:.2f}%
Revenue (TTM): ${info.get('totalRevenue', 0):,.0f}
Earnings Per Share: ${info.get('trailingEps', 0):.2f}

=== DIVIDEND INFO ===
Dividend Yield: {info.get('dividendYield', 0)*100:.2f}%
Dividend Rate: ${info.get('dividendRate', 0):.2f}
Payout Ratio: {info.get('payoutRatio', 0)*100:.2f}%

=== ANALYST RATINGS ===
Target Price: ${info.get('targetMeanPrice', 0):.2f}
Recommendation: {info.get('recommendationKey', 'N/A').upper()}
Number of Analysts: {info.get('numberOfAnalystOpinions', 0)}
"""
            return result
            
        except Exception as e:
            return f"Error fetching fundamental data: {str(e)}"


# Tool 5: Portfolio Risk Calculator
class PortfolioRiskInput(BaseModel):
    """Input for PortfolioRiskTool"""
    tickers: str = Field(..., description="Comma-separated list of tickers")
    weights: str = Field(..., description="Comma-separated weights (should sum to 1)")
    period: str = Field(default="1y", description="Historical period for calculation")

class PortfolioRiskTool(BaseTool):
    name: str = "Calculate Portfolio Risk"
    description: str = "Calculates portfolio risk metrics including volatility, Sharpe ratio, and VaR"
    args_schema: Type[BaseModel] = PortfolioRiskInput

    def _run(self, tickers: str, weights: str, period: str = "1y") -> str:
        try:
            ticker_list = [t.strip() for t in tickers.split(',')]
            weight_list = [float(w.strip()) for w in weights.split(',')]
            
            if len(ticker_list) != len(weight_list):
                return "Error: Number of tickers must match number of weights"
            
            if abs(sum(weight_list) - 1.0) > 0.01:
                return f"Error: Weights must sum to 1.0 (current sum: {sum(weight_list)})"
            
            # Download data
            data = yf.download(ticker_list, period=period, progress=False)['Adj Close']
            
            # Calculate returns
            returns = data.pct_change().dropna()
            
            # Portfolio metrics
            portfolio_return = (returns.mean() * weight_list).sum() * 252  # Annualized
            portfolio_volatility = (returns @ weight_list).std() * (252 ** 0.5)  # Annualized
            
            # Sharpe Ratio (assuming 4% risk-free rate)
            risk_free_rate = 0.04
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
            
            # Value at Risk (VaR) at 95% confidence
            var_95 = returns @ weight_list
            var_95 = var_95.quantile(0.05)
            
            # Maximum Drawdown
            cumulative = (1 + returns @ weight_list).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min()
            
            # Individual stock metrics
            stock_metrics = []
            for ticker, weight in zip(ticker_list, weight_list):
                vol = returns[ticker].std() * (252 ** 0.5)
                ret = returns[ticker].mean() * 252
                stock_metrics.append(f"{ticker}: Weight {weight*100:.1f}%, Return {ret*100:.2f}%, Volatility {vol*100:.2f}%")
            
            result = f"""
Portfolio Risk Analysis:

=== PORTFOLIO COMPOSITION ===
{chr(10).join(stock_metrics)}

=== PORTFOLIO METRICS ===
Expected Annual Return: {portfolio_return*100:.2f}%
Annual Volatility: {portfolio_volatility*100:.2f}%
Sharpe Ratio: {sharpe_ratio:.2f}

=== RISK METRICS ===
Value at Risk (95%): {var_95*100:.2f}% (daily)
Maximum Drawdown: {max_drawdown*100:.2f}%

=== RISK ASSESSMENT ===
"""
            if sharpe_ratio > 1:
                result += "✓ Good risk-adjusted returns (Sharpe > 1)\n"
            else:
                result += "⚠ Below-average risk-adjusted returns (Sharpe < 1)\n"
                
            if max_drawdown < -0.20:
                result += "⚠ High drawdown risk (>20%)\n"
            else:
                result += "✓ Acceptable drawdown levels\n"
                
            if portfolio_volatility > 0.30:
                result += "⚠ High volatility portfolio (>30%)\n"
            else:
                result += "✓ Moderate volatility\n"
            
            return result
            
        except Exception as e:
            return f"Error calculating portfolio risk: {str(e)}"
