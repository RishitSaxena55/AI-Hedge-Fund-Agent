# **🤖 AI Hedge Fund Agent**

**AI Hedge Fund Agent** is an autonomous, institutional-grade financial analysis system powered by **CrewAI** and **DeepSeek R1T**. It simulates a professional hedge fund's investment committee, orchestrating a team of specialized AI agents to perform comprehensive due diligence, risk assessment, and sentiment analysis on any given stock ticker.

The system is wrapped in a modern **Streamlit** interface, allowing users to launch complex multi-agent workflows with a single click and receive a detailed, actionable trading report.

## **🚀 Features**

* **Multi-Agent Architecture:** A team of 8 specialized agents working sequentially and collaboratively.  
* **Real-Time Data Ingestion:**  
  * **Market Data:** Live price, volume, and historical data via yfinance.  
  * **Technical Analysis:** RSI, MACD, SMA, and Bollinger Bands via Alpha Vantage.  
  * **Fundamental Analysis:** Balance sheets, P/E ratios, and growth metrics.  
* **Dual-Layer Sentiment Analysis:**  
  * **News:** Global news search and sentiment scoring via Serper (Google News).  
  * **Social:** Retail trader psychology and "hype" analysis via StockTwits.  
* **Institutional Risk Management:** Automated position sizing, Stop-Loss calculation, and VaR (Value at Risk) assessment.  
* **Interactive Dashboard:** A clean Streamlit UI to input capital, tickers, and view real-time agent thought processes.

## **🧠 System Architecture**

The system utilizes a hierarchical workflow where specialized analysts pass their findings to strategists, culminating in a final decision by the Head Trader.

graph TD  
    User\[User Input\] \--\> Market\[Market Data Analyst\]  
    Market \--\> Tech\[Technical Analyst\]  
    Tech \--\> Fund\[Fundamental Analyst\]  
    Fund \--\> News\[News Sentiment Analyst\]  
    News \--\> Social\[Social Sentiment Analyst\]  
    Social \--\> Risk\[Risk Manager\]  
    Risk \--\> Port\[Portfolio Strategist\]  
    Port \--\> Head\[Head Trader\]  
    Head \--\> Report\[Final Decision & Report\]

## **🛠️ The Agent Team**

| Agent | Role | Tools & Capabilities |
| :---- | :---- | :---- |
| **Market Data Analyst** | Data Aggregation | Fetches OHLCV data, market cap, and volume profiles using yfinance. |
| **Technical Analyst** | Chart Pattern Recognition | Analyzes RSI, MACD, and Moving Averages using Alpha Vantage. |
| **Fundamental Analyst** | Value Investing | Evaluates financial health, debt-to-equity, and profit margins. |
| **News Analyst** | Macro Sentiment | Scrapes Google News via Serper for catalysts and global events. |
| **Social Analyst** | Crowd Psychology | **Unique Feature:** Scrapes StockTwits to gauge retail fear/greed. |
| **Risk Manager** | Capital Protection | Calculates max drawdown, position sizing (2% rule), and stop-losses. |
| **Portfolio Strategist** | Asset Allocation | Checks correlation with existing holdings and sector exposure. |
| **Head Trader** | Decision Maker | Synthesizes all 7 reports to issue a BUY/SELL/HOLD command. |

## **📦 Installation**

### **Prerequisites**

* Python 3.10 or higher  
* [Alpha Vantage API Key](https://www.alphavantage.co/) (Free)  
* [Serper API Key](https://serper.dev/) (Free tier available)  
* [OpenRouter API Key](https://openrouter.ai/) (For DeepSeek/LLM access)

### **1\. Clone the Repository**

git clone \[https://github.com/yourusername/ai-hedge-fund-agent.git\](https://github.com/yourusername/ai-hedge-fund-agent.git)  
cd ai-hedge-fund-agent

### **2\. Install Dependencies**

pip install \-r requirements.txt

*Note: You may need to download NLTK data manually if the automatic download fails:*

import nltk  
nltk.download('punkt')

### **3\. Configure Environment Variables**

Create a .env file in the root directory:

\# LLM Provider (DeepSeek via OpenRouter)  
OPENROUTER\_API\_KEY=sk-or-your-key-here

\# Tool API Keys  
SERPER\_API\_KEY=your-serper-key  
ALPHA\_VANTAGE\_API\_KEY=your-alpha-vantage-key

## **💻 Usage**

To launch the web interface, run the following command in your terminal:

streamlit run app.py

1. Open your browser to http://localhost:8501.  
2. **Sidebar:** Enter the Stock Ticker (e.g., NVDA, TSLA).  
3. **Sidebar:** Set your Account Size and Analysis Period.  
4. Click **"🚀 Launch Analysis"**.  
5. Watch the agents work in real-time within the expandable status container.  
6. Download the final Markdown report when finished.

## **📂 Project Structure**

ai-hedge-fund-agent/  
├── src/  
│   └── ai\_trading\_agent/  
│       ├── config/  
│       │   ├── agents.yaml       \# Agent persona definitions  
│       │   └── tasks.yaml        \# Detailed instruction sets  
│       ├── tools/  
│       │   ├── financial\_tools.py      \# yfinance & Alpha Vantage wrappers  
│       │   └── stocktwits\_sentiment\_tool.py \# Custom scraper  
│       ├── crew.py               \# Main CrewAI orchestration logic  
│       └── main.py               \# CLI entry point (optional)  
├── app.py                        \# Streamlit User Interface  
├── .env                          \# API Keys (gitignored)  
├── requirements.txt  
└── README.md

## **⚠️ Disclaimer**

Not Financial Advice.  
This project is for educational and research purposes only. The "AI Hedge Fund Agent" generates responses based on available data and Large Language Model interpretations, which can be hallucinated, inaccurate, or outdated. Never trade real money based solely on the output of this software. Always conduct your own due diligence or consult a certified financial advisor.

## **🤝 Contributing**

Contributions are welcome\! Please feel free to submit a Pull Request.

1. Fork the project  
2. Create your feature branch (git checkout \-b feature/AmazingFeature)  
3. Commit your changes (git commit \-m 'Add some AmazingFeature')  
4. Push to the branch (git push origin feature/AmazingFeature)  
5. Open a Pull Request

## **📄 License**

Distributed under the MIT License. See LICENSE for more information.