# **📈 AI Hedge Fund**

**An AI-powered hedge fund that uses a team of autonomous agents to make trading decisions.**

This project is a Proof of Concept (PoC) exploring how multiple specialized AI agents—mimicking legendary investors and financial analysts—can collaborate to analyze stocks, assess risk, and manage a portfolio.

**⚠️ DISCLAIMER:** This project is for **educational and research purposes only**. It is **not** intended for real trading or financial investment. The creator assumes no liability for financial losses.

## **🌐 Live Demo**

Check out the interactive dashboard running live on Streamlit:

[**Click here to launch the AI Hedge Fund Dashboard**](https://www.google.com/search?q=https://share.streamlit.io/virattt/ai-hedge-fund/main/app.py)

## **🤖 The Investment Team**

The system employs a "Council of Agents," each with a distinct personality and investment philosophy. They analyze data in parallel and debate decisions before the Portfolio Manager makes the final call.

### **🧠 Valuation & Strategy Agents**

| Agent | Persona | Philosophy |
| :---- | :---- | :---- |
| **Ben Graham** | The Value Investor | Focuses on deep value, margin of safety, and net-net working capital. |
| **Warren Buffett** | The Oracle | Seeks wonderful businesses at fair prices, moats, and long-term compounding. |
| **Cathie Wood** | The Futurist | Hunts for disruptive innovation, exponential growth, and high-beta tech plays. |
| **Bill Ackman** | The Activist | Looks for undervalued companies with fixable management or operational issues. |
| **Charlie Munger** | The Quality Filter | Prioritizes business quality, rationality, and avoiding stupidity. |

### **📊 Analyst Agents**

* **Fundamentals Agent:** Analyzes 10-Ks, 10-Qs, P/E ratios, revenue growth, and balance sheet health.  
* **Technicals Agent:** Analyzes price action, moving averages (SMA/EMA), RSI, MACD, and volume trends.  
* **Sentiment Agent:** Scrapes news and social media to gauge market sentiment and fear/greed indices.  
* **Risk Manager:** Calculates portfolio exposure, volatility, and sets position limits to prevent blow-ups.  
* **Portfolio Manager:** Synthesizes all agent signals to make the final **Buy**, **Sell**, or **Hold** decision.

## **🏗️ Architecture**

The system uses **LangGraph** to create a stateful workflow. The agents operate as nodes in a graph, allowing for parallel execution and shared state management.

*\> **Note:** Replace the image above with your actual architecture diagram file (e.g., assets/architecture.png).*

### **Workflow Diagram**

1. **Parallel Execution:** Analysts work simultaneously to gather data.  
2. **State Management:** The "State" object passes data (ticker, price, analysis) between agents.  
3. **Human-in-the-loop (Optional):** Can be configured to ask for human approval before "executing" trades.

graph TD  
    User\[User Input\] \--\> Manager\[Portfolio Manager\]  
    Manager \--\> Fund\[Fundamentals Agent\]  
    Manager \--\> Tech\[Technicals Agent\]  
    Manager \--\> Sent\[Sentiment Agent\]  
    Manager \--\> Val\[Valuation Agent\]  
    Fund \--\> Risk\[Risk Manager\]  
    Tech \--\> Risk  
    Sent \--\> Risk  
    Val \--\> Risk  
    Risk \--\> Decision\[Final Trade Decision\]

## **🚀 Getting Started**

### **Prerequisites**

* **Python 3.10+**  
* **Poetry** (Python dependency manager)  
* API Keys (see below)

### **Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/virattt/ai-hedge-fund.git\](https://github.com/virattt/ai-hedge-fund.git)  
   cd ai-hedge-fund

2. **Install dependencies:**  
   poetry install

3. Set up Environment Variables:  
   Copy the example .env file and configure your keys.  
   cp .env.example .env

### **🔑 API Configuration**

Open .env and add your keys. You must provide at least one LLM provider and a financial data source.

\# LLM Providers (Pick one or more)  
OPENAI\_API\_KEY=sk-...  
ANTHROPIC\_API\_KEY=sk-...

\# Financial Data (Required for live data)  
FINANCIAL\_DATASETS\_API\_KEY=your\_key\_here

* **Financial Datasets:** Get a key from [financialdatasets.ai](https://financialdatasets.ai).  
* **OpenAI:** Uses GPT-4o by default for reasoning.

## **💻 Usage**

### **Running the Hedge Fund**

To run a specific analysis on a set of stocks:

poetry run python src/main.py \--ticker AAPL,MSFT,NVDA

### **Options**

* \--ticker: Comma-separated list of stock symbols (e.g., AAPL,TSLA,GOOG).  
* \--show-reasoning: Prints the detailed internal monologue of each agent.  
* \--start-date: Start date for analysis (YYYY-MM-DD).  
* \--end-date: End date for analysis (YYYY-MM-DD).

### **🔙 Backtesting**

Run the backtester to see how the agents would have performed historically.

poetry run python src/backtester.py \--ticker AAPL \--start-date 2023-01-01 \--end-date 2023-12-31

## **🛠️ Customization**

### **Adding a New Agent**

1. Create a new file in src/agents/.  
2. Define the agent's prompt and persona (e.g., JimSimonsAgent).  
3. Register the agent in the workflow.py graph.

### **Changing LLMs**

You can switch the underlying model in src/llm/models.py. The system supports any model compatible with LangChain (Claude 3.5 Sonnet, GPT-4o, Llama 3, etc.).

## **🤝 Contributing**

Contributions are welcome\!

1. Fork the repo.  
2. Create a feature branch (git checkout \-b feature/AmazingAgent).  
3. Commit your changes.  
4. Push to the branch.  
5. Open a Pull Request.

## **📜 License**

Distributed under the MIT License. See LICENSE for more information.

## **⚠️ Risk Disclosure**

**THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY.**

* Do not use this for real money trading.  
* The creators and contributors are not financial advisors.  
* AI models can hallucinate and make irrational decisions.  
* Past performance in backtests is not indicative of future results.