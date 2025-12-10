from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Create the database connection (SQLite for now)
# For scaling later, change this string to a Postgres URL
DATABASE_URL = "sqlite:///trading_bot.db"

Base = declarative_base()

class TradeAnalysis(Base):
    """
    Table to store the final analysis from the Head Trader.
    """
    __tablename__ = 'trade_analysis'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ticker = Column(String, index=True)
    decision = Column(String)  # BUY, SELL, HOLD
    entry_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit_1 = Column(Float, nullable=True)
    confidence = Column(String)
    rationale = Column(Text)
    full_report = Column(Text) # Stores the full Markdown output

# Initialize Database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Creates the tables if they don't exist."""
    Base.metadata.create_all(engine)

def save_analysis_result(ticker, result_str):
    """
    Parses the Markdown result and saves it to the DB.
    (In a real app, we would use JSON output from the agent to make parsing easier)
    """
    session = SessionLocal()
    try:
        # Simple parsing logic - you might need to adjust based on exact output format
        decision = "HOLD"
        if "DECISION: BUY" in result_str: decision = "BUY"
        elif "DECISION: SELL" in result_str: decision = "SELL"
        
        # Create record
        record = TradeAnalysis(
            ticker=ticker,
            decision=decision,
            full_report=result_str
        )
        session.add(record)
        session.commit()
        print(f"💾 Saved analysis for {ticker} to database.")
    except Exception as e:
        print(f"❌ Error saving to DB: {e}")
    finally:
        session.close()