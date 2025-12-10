import streamlit as st
import sys
import os
import asyncio

# Assuming your folder structure, we add the src path:
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_trading_agent.crew import AiTradingAgent

st.set_page_config(page_title="AI Hedge Fund Agent", page_icon="📈", layout="wide")

st.title("🤖 AI Institutional Trading Agent")
st.markdown("### Powered by CrewAI & Llama 3.3 (Cerebras Inference)")

# Sidebar for Inputs
with st.sidebar:
    st.header("Trade Settings")
    ticker = st.text_input("Stock Ticker", value="MSFT").upper()
    amount = st.number_input("Capital ($)", value=10000)
    period = st.selectbox("Analysis Window", ["1mo", "3mo", "6mo", "1y"], index=1)
    
    st.info("⚠️ **Note:** This runs on the Cerebras Free Tier (1M tokens/day).")
    run_btn = st.button("🚀 Launch Analysis", type="primary")

# Main Execution Area
if run_btn:
    inputs = {
        'stock_ticker': ticker,
        'account_size': str(amount),
        'analysis_period': period,
        'current_portfolio': 'None'
    }
    
    # 👇 FIXED: Added 'with' keyword here
    with st.status("💡 Agents are thinking...", expanded=True) as status:
        st.write("Initializing AI Crew...")
        
        try:
            agent = AiTradingAgent()
            result = agent.crew().kickoff(inputs=inputs)
            
            # Update status to complete
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            
            # Parsing and Displaying the Result
            st.divider()
            st.subheader(f"📊 Trading Report: {ticker}")
            st.markdown(str(result))
            
            # Option to download report
            st.download_button(
                label="📥 Download Report",
                data=str(result),
                file_name=f"{ticker}_Analysis.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Error: {e}")
            # print full error to logs for debugging
            print(e)