import asyncio
import sys
from src.ai_trading_agent.crew import AiTradingAgent
from database import init_db, save_analysis_result
from screener import MarketScreener

# Configuration
BATCH_SIZE = 1  # How many AI agents to run at the exact same time (Don't set too high or APIs will ban you)
INPUT_TICKERS = ["AAPL", "TSLA", "NVDA", "AMD", "MSFT", "GOOGL", "AMZN", "META", "NFLX", "INTC"]

async def run_single_crew(ticker):
    """
    Runs a single instance of the crew for a specific ticker.
    """
    print(f"🚀 [Async] Starting AI Crew for {ticker}...")
    
    inputs = {
        'stock_ticker': ticker,
        'account_size': '10000',
        'analysis_period': '3mo',
        'current_portfolio': 'None'
    }
    
    try:
        # We create a NEW instance of the agent for every thread
        # kickoff_async returns a Future object
        agent = AiTradingAgent()
        crew_instance = agent.crew()
        
        # Use kickoff_async for parallel execution
        result = await crew_instance.kickoff_async(inputs=inputs)
        
        # Save to Database
        save_analysis_result(ticker, str(result))
        
        return f"✅ Finished {ticker}"
    except Exception as e:
        return f"❌ Failed {ticker}: {str(e)}"

async def run_batch(tickers):
    """
    Manages the worker pool to ensure we don't exceed rate limits.
    """
    # 1. Initialize Database
    init_db()
    
    # 2. Run Screener (Synchronous is fine here as it's fast)
    screener = MarketScreener(tickers)
    candidates = screener.filter_stocks()
    
    if not candidates:
        print("No stocks passed the screener. Exiting.")
        return

    print(f"\n🤖 Spawning AI Agents for: {', '.join(candidates)}\n")

    # 3. Process in Batches (Semaphore pattern)
    # This ensures we only run BATCH_SIZE agents at once
    semaphore = asyncio.Semaphore(BATCH_SIZE)

    async def sem_task(ticker):
        async with semaphore:
            return await run_single_crew(ticker)

    # Gather all tasks
    tasks = [sem_task(ticker) for ticker in candidates]
    results = await asyncio.gather(*tasks)
    
    # 4. Final Report
    print("\n" + "="*50)
    print("🏁 BATCH EXECUTION COMPLETE")
    print("="*50)
    for res in results:
        print(res)

if __name__ == "__main__":
    # Ensure Windows compatibility for asyncio
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(run_batch(INPUT_TICKERS))