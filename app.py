import streamlit as st
import sys
import os
import asyncio
# from ai_trading_agent.crew import AiTradingAgent # Uncomment if using module import
# For simple deployment, often copying the class directly or adjusting path is easier
# Assuming your folder structure, we add the src path:
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_trading_agent.crew import AiTradingAgent

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
    
    st.status("💡 Agents are thinking...", expanded=True) as status:
        st.write("Initializing AI Crew...")
        
        # Capture standard output to display logs in UI
        class StreamlitCapture(object):
            def write(self, data):
                # Filter out raw escape codes if needed, or just log
                if data.strip():
                    st.text(data) # Print agent thoughts to UI
            def flush(self):
                pass
        
        # Redirect stdout to Streamlit
        # (Note: CrewAI logs are tricky, sometimes they print directly to terminal)
        # For a simple demo, we just run it and show the final result.
        
        try:
            agent = AiTradingAgent()
            result = agent.crew().kickoff(inputs=inputs)
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