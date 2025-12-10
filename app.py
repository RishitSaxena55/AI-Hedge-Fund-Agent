import streamlit as st
import sys
import os
import nltk  # Ensure nltk is imported

# 1. SETUP PATHS & NLTK (Must happen before imports)
# Add 'src' to python path so we can import modules inside it
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Download NLTK data to fix TextBlob error
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('brown')
    nltk.download('punkt_tab')

# 2. IMPORT CREW
try:
    # ✅ CORRECT: No 'src.' prefix because 'src' is in path
    from ai_trading_agent.crew import AiTradingAgent
except ImportError as e:
    st.error(f"🚨 Import Error: {e}")
    st.info(f"Current Path: {sys.path}")
    st.stop()

# 3. APP UI
st.set_page_config(page_title="AI Hedge Fund Agent", page_icon="📈", layout="wide")
st.title("🤖 AI Institutional Trading Agent")
# st.markdown("### Powered by CrewAI & Llama 3.3 (Cerebras Inference)")

with st.sidebar:
    st.header("Trade Settings")
    ticker = st.text_input("Stock Ticker", value="MSFT").upper()
    amount = st.number_input("Capital ($)", value=10000)
    period = st.selectbox("Analysis Window", ["1mo", "3mo", "6mo", "1y"], index=1)
    # st.info("⚠️ **Note:** Runs on Cerebras Free Tier (1M tokens/day).")
    run_btn = st.button("🚀 Launch Analysis", type="primary")

if run_btn:
    inputs = {
        'stock_ticker': ticker,
        'account_size': str(amount),
        'analysis_period': period,
        'current_portfolio': 'None'
    }
    
    # ✅ FIXED: Added 'with' keyword
    with st.status("💡 Agents are thinking...", expanded=True) as status:
        st.write("Initializing AI Crew...")
        try:
            agent = AiTradingAgent()
            result = agent.crew().kickoff(inputs=inputs)
            
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            st.divider()
            st.subheader(f"📊 Trading Report: {ticker}")
            st.markdown(str(result))
            
            st.download_button(
                label="📥 Download Report",
                data=str(result),
                file_name=f"{ticker}_Analysis.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"Error: {e}")
            print(e)