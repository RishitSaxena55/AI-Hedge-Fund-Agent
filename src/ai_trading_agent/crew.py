from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from typing import List
import os
from dotenv import load_dotenv
from .tools.stocktwits_sentiment_tool import StockTwitsSentimentTool


# Import custom tools
from .tools.financial_tools import (
    StockDataTool,
    TechnicalIndicatorsTool,
    FinancialNewsTool,
    FundamentalAnalysisTool,
    PortfolioRiskTool
)

load_dotenv()

@CrewBase
class AiTradingAgent():
    """Advanced AI Trading Agent Crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    # Initialize DeepSeek Chimera R1T
    llm = LLM(
        model="cerebras/llama-3.3-70b", 
        api_key=os.getenv("CEREBRAS_API_KEY"),
        base_url="https://api.cerebras.ai/v1", # Optional but safe to add
        temperature=0.7
    )
    
    # Initialize tools
    stock_data_tool = StockDataTool()
    technical_indicators_tool = TechnicalIndicatorsTool()
    financial_news_tool = FinancialNewsTool()
    fundamental_analysis_tool = FundamentalAnalysisTool()
    portfolio_risk_tool = PortfolioRiskTool()
    serper_tool = SerperDevTool()
    stocktwits_sentiment_tool = StockTwitsSentimentTool()

    
    @agent
    def market_data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_data_analyst'],
            tools=[self.stock_data_tool],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def technical_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_analyst'],
            tools=[self.technical_indicators_tool, self.stock_data_tool],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def fundamental_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['fundamental_analyst'],
            tools=[self.fundamental_analysis_tool],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def news_sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['news_sentiment_analyst'],
            tools=[self.financial_news_tool, self.serper_tool],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def social_sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['social_sentiment_analyst'],
            tools=[self.stocktwits_sentiment_tool],
            llm=self.llm,
            verbose=True
        )

    
    @agent
    def risk_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_manager'],
            tools=[self.stock_data_tool],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def portfolio_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['portfolio_strategist'],
            tools=[self.portfolio_risk_tool, self.stock_data_tool],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def head_trader(self) -> Agent:
        return Agent(
            config=self.agents_config['head_trader'],
            tools=[],  # Decision maker doesn't need tools, uses team analysis
            llm=self.llm,
            verbose=True
        )
    
    # Tasks
    @task
    def gather_market_data(self) -> Task:
        return Task(
            config=self.tasks_config['gather_market_data']
        )
    
    @task
    def perform_technical_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['perform_technical_analysis']
        )
    
    @task
    def analyze_fundamentals(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_fundamentals']
        )
    
    @task
    def analyze_news_sentiment(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_news_sentiment']
        )
    
    @task
    def analyze_social_sentiment(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_social_sentiment']
        )

    @task
    def assess_risk(self) -> Task:
        return Task(
            config=self.tasks_config['assess_risk']
        )
    
    @task
    def optimize_portfolio_allocation(self) -> Task:
        return Task(
            config=self.tasks_config['optimize_portfolio_allocation']
        )
    
    @task
    def make_trading_decision(self) -> Task:
        return Task(
            config=self.tasks_config['make_trading_decision']
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the AI Trading Agent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # memory=True,  # Enable memory for context retention
            # embedder={
            #     "provider": "openai",
            #     "config": {
            #         "model": "text-embedding-3-small"
            #     }
            # }
        )
