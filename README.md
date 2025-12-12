# 🤖 AI Hedge Fund Agent

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-hedge-fund-agent.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange)](https://www.crewai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An institutional-grade, multi-agent AI trading system powered by Llama 3.3 70B and CrewAI that performs comprehensive stock analysis and generates actionable trading decisions.**

[**🚀 Live Demo**](https://ai-hedge-fund-agent.streamlit.app/) | [**📖 Documentation**](#getting-started)

---

## 📊 Overview

The **AI Hedge Fund Agent** is a sophisticated multi-agent system that replicates the decision-making process of a professional hedge fund trading desk. It combines technical analysis, fundamental analysis, sentiment analysis, risk management, and portfolio optimization to generate data-driven trading recommendations.

### 🎯 Key Features

- **8 Specialized AI Agents** working in coordination
- **Real-time Market Data** integration via Yahoo Finance
- **Technical Analysis** with 10+ indicators (RSI, MACD, Moving Averages, etc.)
- **Fundamental Analysis** including P/E, ROE, debt ratios, and growth metrics
- **Sentiment Analysis** from financial news and social media (StockTwits)
- **Advanced Risk Management** with position sizing and stop-loss calculation
- **Portfolio Optimization** considering diversification and correlation
- **Professional Trading Reports** with specific entry/exit prices and rationale

---

## 🏗️ Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────────────┐
│                    HEAD TRADER (Decision Maker)                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        │                                               │
┌───────▼────────┐                            ┌────────▼─────────┐
│   Technical    │                            │   Fundamental    │
│    Analysis    │                            │     Analysis     │
└───────┬────────┘                            └────────┬─────────┘
        │                                               │
┌───────▼────────┐  ┌──────────────┐  ┌──────────────▼─────────┐
│  Market Data   │  │   Sentiment  │  │   Risk Management      │
│   Gathering    │  │   Analysis   │  │   & Portfolio Opt.     │
└────────────────┘  └──────────────┘  └────────────────────────┘
```

### Agent Roles

| Agent | Role | Responsibilities |
|-------|------|------------------|
| 🔍 **Market Data Analyst** | Data Collection | Real-time prices, historical data, volume analysis |
| 📈 **Technical Analyst** | Chart Analysis | RSI, MACD, SMA, chart patterns, entry/exit points |
| 💰 **Fundamental Analyst** | Financial Health | P/E ratios, earnings, balance sheets, fair value |
| 📰 **News Sentiment Analyst** | News Monitoring | Recent news, earnings, events, media sentiment |
| 🐦 **Social Sentiment Analyst** | Retail Tracking | StockTwits sentiment, retail trader psychology |
| ⚠️ **Risk Manager** | Risk Assessment | Position sizing, stop-loss, risk-reward ratios |
| 🎯 **Portfolio Strategist** | Portfolio Optimization | Asset allocation, diversification, correlation |
| 👔 **Head Trader** | Final Decision | Synthesizes all data, makes BUY/SELL/HOLD decision |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Cerebras API Key ([Get one free](https://cloud.cerebras.ai/))
- SerperDev API Key ([Get one free](https://serper.dev/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-hedge-fund-agent.git
cd ai-hedge-fund-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
CEREBRAS_API_KEY=your_cerebras_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### Quick Start

#### Option 1: Streamlit Web App (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

#### Option 2: Command Line Interface

```bash
python main.py
```

Follow the prompts to enter:
- Stock ticker (e.g., AAPL, MSFT, TSLA)
- Account size ($10,000 default)
- Analysis period (1mo, 3mo, 6mo, 1y)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **AI Framework** | [CrewAI](https://www.crewai.com/) |
| **LLM** | [Llama 3.3 70B](https://www.cerebras.ai/) via Cerebras |
| **Web Framework** | [Streamlit](https://streamlit.io/) |
| **Market Data** | [yfinance](https://github.com/ranaroussi/yfinance) |
| **News Search** | [SerperDev](https://serper.dev/) |
| **Sentiment Data** | [StockTwits API](https://stocktwits.com/) |
| **Technical Analysis** | pandas, numpy, ta-lib |

---

## 📖 Usage Examples

### Example 1: Basic Stock Analysis

```python
from ai_trading_agent.crew import AiTradingAgent

inputs = {
    'stock_ticker': 'AAPL',
    'account_size': '10000',
    'analysis_period': '3mo',
    'current_portfolio': 'None'
}

agent = AiTradingAgent()
result = agent.crew().kickoff(inputs=inputs)
print(result)
```

### Example 2: Portfolio Diversification

```python
inputs = {
    'stock_ticker': 'MSFT',
    'account_size': '50000',
    'analysis_period': '6mo',
    'current_portfolio': 'AAPL:30%, GOOGL:25%, TSLA:20%'
}

result = AiTradingAgent().crew().kickoff(inputs=inputs)
```

---

## 📊 Sample Output

```markdown
**DECISION: BUY**

**EXECUTION DETAILS:**
- Entry Price: $492.50
- Position Size: 40 shares ($19,700)
- Stop-Loss: $485.00 (risk: $300)
- Target 1: $495.00 (reward: $100)
- Target 2: $500.00 (reward: $300)
- Target 3: $505.00 (reward: $500)
- Risk-Reward Ratio: 1:1.67
- Holding Period: 2-4 weeks
- Confidence: Medium

**RATIONALE:**
The decision to buy MSFT is based on comprehensive analysis showing:
- Strong bullish technical indicators with support at $484.38
- Solid fundamentals with 7.9% revenue growth and healthy balance sheet
- Positive sentiment from both institutional and retail traders
- Favorable risk-reward setup with clear entry and exit levels

**KEY FACTORS:**
- Technical: Bullish trend with RSI at 58 (neutral), MACD positive
- Fundamental: P/E of 34.99, strong cash position, moderate debt
- Sentiment: 60% positive news sentiment, bullish social media
- Risk: Medium risk with 2% account risk ($200 max loss)
```

---

## ⚙️ Configuration

### Customizing Agent Behavior

Edit `src/ai_trading_agent/config/agents.yaml` to modify agent personalities:

```yaml
technical_analyst:
  role: Expert Technical Analyst
  goal: Perform detailed technical analysis with precise entry/exit points
  backstory: You are a CMT with 15 years of experience...
```

### Customizing Tasks

Edit `src/ai_trading_agent/config/tasks.yaml` to modify analysis depth:

```yaml
perform_technical_analysis:
  description: |
    1. Calculate RSI, MACD, and moving averages
    2. Identify chart patterns
    3. Set entry/exit targets
  expected_output: Comprehensive technical report with price targets
```

---

## 🔧 Advanced Features

### Custom Tools Integration

Add your own data sources by creating custom tools:

```python
from crewai_tools import BaseTool

class CustomDataTool(BaseTool):
    name: str = "Custom Data Tool"
    description: str = "Fetches data from custom source"
    
    def _run(self, ticker: str) -> str:
        # Your custom logic here
        return data
```

### Memory and Learning

Enable agent memory for context retention:

```python
crew = Crew(
    agents=self.agents,
    tasks=self.tasks,
    memory=True,  # Enable memory
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)
```

---

## 📈 Performance Metrics

The system has been tested on 100+ stocks with the following characteristics:

- **Average Analysis Time**: 45-60 seconds per stock
- **API Calls per Analysis**: ~15-20 calls
- **Accuracy** (backtested): Not yet validated (paper trading recommended)
- **Risk Management**: Adheres to 2% max account risk rule

⚠️ **Important**: This is an analytical tool, not financial advice. Always paper trade first and validate strategies before using real money.

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'apscheduler'`
```bash
# This is a non-critical LiteLLM warning, suppress it:
export OTEL_SDK_DISABLED=true
```

**Issue**: `HTTP 403 on StockTwits`
```bash
# StockTwits may block automated requests
# The system will continue with simulated data
```

**Issue**: Technical indicators return "premium endpoint"
```bash
# Alpha Vantage free tier limitations
# Switch to yfinance implementation (already included)
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution

- [ ] Additional data sources (Bloomberg, Reuters, etc.)
- [ ] More technical indicators (Ichimoku, Elliott Wave, etc.)
- [ ] Backtesting framework
- [ ] Real broker integration (Alpaca, Interactive Brokers)
- [ ] Options analysis capabilities
- [ ] Crypto support
- [ ] Multi-language support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**This software is for educational and research purposes only.**

- This is NOT financial advice
- Past performance does not guarantee future results
- Trading stocks involves risk of loss
- Always do your own research and consult with licensed financial advisors
- The creators are not responsible for any financial losses incurred

**Recommended Usage**: Paper trading and backtesting before any real money deployment.

---

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) - Multi-agent orchestration framework
- [Cerebras](https://www.cerebras.ai/) - Fast inference for Llama 3.3 70B
- [Streamlit](https://streamlit.io/) - Beautiful web interface
- [yfinance](https://github.com/ranaroussi/yfinance) - Reliable market data

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/RishitSaxena55/AI-Hedge-Fund-Agent/issues)
- **Discussions**: [Join the community](https://github.com/RishitSaxena55/AI-Hedge-Fund-Agent/discussions)
- **LinkedIn**: [Connect with the author]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/rishit-saxena-12922531b/))
- **Email**: rishitsaxena55@gmail.com

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=RishitSaxena55/AI-Hedge-Fund-Agent&type=Date)](https://github.com/RishitSaxena55/AI-Hedge-Fund-Agent&Date)

---

<div align="center">

**If you found this project helpful, please consider giving it a ⭐️!**

Made with ❤️ by [](https://github.com/RishitSaxena55/AI-Hedge-Fund-Agent)

[⬆ Back to Top](#-AI-Hedge-Fund-Agent)

</div>
