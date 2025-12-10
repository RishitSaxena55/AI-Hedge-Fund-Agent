import yfinance as yf
import pandas as pd
import warnings

# Suppress standard warnings for cleaner output
warnings.simplefilter(action='ignore', category=FutureWarning)

class MarketScreener:
    def __init__(self, tickers):
        self.tickers = tickers

    def filter_stocks(self):
        """
        Returns a list of tickers that meet basic technical criteria.
        """
        candidates = []
        print(f"🔍 Screening {len(self.tickers)} stocks for opportunities...")

        # Download data in batch
        # We use 'auto_adjust=True' to get the actual price behavior
        data = yf.download(self.tickers, period="6mo", group_by='ticker', progress=True, auto_adjust=True)

        print("\n📊 SCREENER RESULTS:")
        print(f"{'TICKER':<8} | {'PRICE':<10} | {'TREND':<15} | {'STATUS'}")
        print("-" * 50)

        for ticker in self.tickers:
            try:
                # 1. Extract and COPY the dataframe to avoid SettingWithCopyWarning
                # Handle cases where only one ticker is downloaded (structure changes)
                if len(self.tickers) == 1:
                    df = data.copy()
                else:
                    df = data[ticker].copy()
                
                if df.empty: 
                    continue

                # 2. Calculate Indicators
                df['SMA_50'] = df['Close'].rolling(window=50).mean()
                df['SMA_200'] = df['Close'].rolling(window=200).mean()
                df['Volume_Avg'] = df['Volume'].rolling(window=20).mean()
                
                # Get the latest valid row
                latest = df.iloc[-1]
                
                # 3. Define Logic
                price = latest['Close']
                sma_50 = latest['SMA_50']
                sma_200 = latest['SMA_200']
                volume = latest['Volume_Avg']
                
                # RELAXED CRITERIA FOR TESTING:
                # 1. Price is above $10 (avoid penny stocks)
                # 2. Volume is decent (> 500k)
                # 3. NOT in a massive crash (Price > 0.9 * SMA50) -> allows slight downtrends
                
                is_valid_price = price > 10
                is_liquid = volume > 500_000
                is_not_crashing = price > (sma_50 * 0.9) # Only filter if price is 10% below 50 SMA

                if is_valid_price and is_liquid and is_not_crashing:
                    candidates.append(ticker)
                    status = "✅ PASSED"
                    trend = "Bullish" if price > sma_200 else "Recovering"
                else:
                    status = "❌ REJECTED"
                    if not is_liquid: trend = "Low Vol"
                    elif not is_not_crashing: trend = "Downtrend"
                    else: trend = "Penny Stock"

                print(f"{ticker:<8} | ${price:<9.2f} | {trend:<15} | {status}")
                    
            except Exception as e:
                print(f"{ticker:<8} | {'ERROR':<10} | {str(e):<15} | ❌ ERROR")
                continue
                
        print("-" * 50)
        print(f"🎯 Found {len(candidates)} candidates for AI analysis.\n")
        
        # If no candidates found, force add AAPL just for testing
        if not candidates:
            print("⚠️ No strict matches found. Adding 'AAPL' and 'MSFT' for testing purposes.")
            return ['AAPL', 'MSFT']
            
        return candidates