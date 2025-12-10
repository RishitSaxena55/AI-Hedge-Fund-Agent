#!/usr/bin/env python
import sys
import warnings
from ai_trading_agent.crew import AiTradingAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the AI Trading Agent crew.
    """
    print("=" * 80)
    print("🤖 AI TRADING AGENT - POWERED BY DEEPSEEK CHIMERA R1T")
    print("=" * 80)
    
    # Get inputs
    stock_ticker = input("\n📊 Enter stock ticker (e.g., AAPL, TSLA, GOOGL): ").upper()
    account_size = input("💰 Enter account size in USD (e.g., 10000): ")
    analysis_period = input("📅 Analysis period (1mo, 3mo, 6mo, 1y) [default: 3mo]: ") or "3mo"
    current_portfolio = input("📂 Current portfolio holdings (comma-separated, or press Enter for none): ") or "None"
    
    print(f"\n🚀 Starting analysis for {stock_ticker}...")
    print(f"💵 Account Size: ${account_size}")
    print(f"📈 Analysis Period: {analysis_period}")
    print(f"📊 Current Portfolio: {current_portfolio}\n")
    
    inputs = {
        'stock_ticker': stock_ticker,
        'account_size': account_size,
        'analysis_period': analysis_period,
        'current_portfolio': current_portfolio
    }
    
    try:
        result = AiTradingAgent().crew().kickoff(inputs=inputs)
        
        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"\n📄 Full report saved to: trading_decision_{stock_ticker}.md\n")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise e

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'stock_ticker': 'AAPL',
        'account_size': '10000',
        'analysis_period': '3mo',
        'current_portfolio': 'None'
    }
    try:
        AiTradingAgent().crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2], 
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AiTradingAgent().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew with a specific input.
    """
    inputs = {
        'stock_ticker': 'MSFT',
        'account_size': '10000',
        'analysis_period': '3mo',
        'current_portfolio': 'AAPL:30%, GOOGL:25%'
    }
    try:
        AiTradingAgent().crew().test(
            n_iterations=int(sys.argv[1]), 
            openai_model_name=sys.argv[2], 
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
