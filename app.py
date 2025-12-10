import os
import sys
import logging
import streamlit as st
import nltk
import agentops

# ==============================================================================
# 🔧 CONFIGURATION & SILENCING NOISE
# ==============================================================================
# We need to quiet down some libraries that get too chatty or cause threading issues
# in Streamlit's cloud environment.

# 1. Disable OpenTelemetry (OTEL). CrewAI uses this for tracking, but it runs in a 
#    background thread that Streamlit hates. Disabling it prevents the app from crashing.
os.environ["OTEL_SDK_DISABLED"] = "true"

# 2. Mute LiteLLM. It loves to log every single API call, which clutters our 
#    beautiful UI. We only want to hear from it if there's a serious ERROR.
os.environ["LITELLM_LOG"] = "ERROR"
logging.getLogger("litellm").setLevel(logging.ERROR)

# ==============================================================================
# 📂 PATHS & IMPORTS
# ==============================================================================
# Add our 'src' folder to the system path so Python can find our custom modules.
# This makes importing 'ai_trading_agent' work seamlessly.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Pre-load NLTK data. TextBlob (used for sentiment) needs these "corpora" to work.
# We check if they exist first to avoid downloading them on every single page load.
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('brown', quiet=True)
    nltk.download('punkt_tab', quiet=True)

# Import our custom CrewAI class. We wrap this in a try-block to catch path errors early.
try:
    from ai_trading_agent.crew import AiTradingAgent
except ImportError as e:
    st.error(f"🚨 Critical Error: Could not import the AI Agent. Check your 'src' folder structure.")
    st.stop()

# ==============================================================================
# 🎨 USER INTERFACE (STREAMLIT)
# ==============================================================================
st.set_page_config(
    page_title="AI Hedge Fund Agent", 
    page_icon="📈", 
    layout="wide"
)

# Header Section
st.title("🤖 AI Institutional Trading Agent")
st.markdown("""
**Your personal team of autonomous AI financial analysts.** 
""")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Analysis Settings")
    
    ticker = st.text_input(
        "Stock Ticker Symbol", 
        value="MSFT", 
        help="Enter the ticker symbol (e.g., AAPL, NVDA, TSLA)"
    ).upper()
    
    amount = st.number_input(
        "Initial Capital ($)", 
        value=10000, 
        min_value=100, 
        step=100,
        help="The amount of simulated capital to trade with."
    )
    
    period = st.selectbox(
        "Historical Data Window", 
        ["1mo", "3mo", "6mo", "1y"], 
        index=1,
        help="How far back should the technical analyst look?"
    )
    
    st.divider()
    
    # The "Go" Button
    run_btn = st.button("🚀 Launch Analysis", type="primary", use_container_width=True)
    
    # st.caption("⚠️ **Note:** Runs on Cerebras Free Tier (1M tokens/day).")

# ==============================================================================
# 🚀 MAIN EXECUTION LOOP
# ==============================================================================
if run_btn:
    # Package inputs for the agents
    inputs = {
        'stock_ticker': ticker,
        'account_size': str(amount),
        'analysis_period': period,
        'current_portfolio': 'None'
    }
    
    # Create a status container to show progress
    with st.status("💡 **Initializing AI Crew...**", expanded=True) as status:
        try:
            # 1. Start AgentOps Session (Observability)
            # We use 'auto_start_session=False' so we can control exactly when it starts.
            # Don't forget to add AGENTOPS_API_KEY to your Streamlit Secrets!
            agentops.init(
                api_key=st.secrets["AGENTOPS_API_KEY"],
                tags=["streamlit", "hedge-fund"],
                auto_start_session=False
            )
            
            # 2. Kick off the Crew
            st.write("🔍 **Agents are gathering market data...**")
            agent = AiTradingAgent()
            result = agent.crew().kickoff(inputs=inputs)
            
            # 3. Success! Update the UI
            status.update(label="✅ **Analysis Complete!**", state="complete", expanded=False)
            
            # --- Display Results ---
            st.divider()
            st.subheader(f"📊 Final Report: {ticker}")
            st.markdown(str(result))
            
            # Allow user to download the markdown report
            st.download_button(
                label="📥 Download Full Report",
                data=str(result),
                file_name=f"{ticker}_Analysis_Report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            # If anything breaks, show a nice error message and the technical details
            st.error("❌ An error occurred during execution.")
            st.error(f"Error Details: {e}")
            st.exception(e) # This helps debugging by showing the full stack trace