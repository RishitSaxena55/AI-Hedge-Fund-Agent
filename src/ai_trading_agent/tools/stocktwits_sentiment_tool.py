from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from textblob import TextBlob
from collections import Counter
from datetime import datetime

class StockTwitsSentimentInput(BaseModel):
    """Input for StockTwitsSentimentTool"""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA)")
    limit: int = Field(default=30, description="Number of messages to analyze (max 30)")

class StockTwitsSentimentTool(BaseTool):
    name: str = "Analyze StockTwits Sentiment"
    description: str = """
    Analyzes trader sentiment from StockTwits - a social network for traders and investors.
    Returns sentiment scores, message volume, trending status, and bullish/bearish breakdown.
    """
    args_schema: Type[BaseModel] = StockTwitsSentimentInput
    
    def _run(self, ticker: str, limit: int = 30) -> str:
        try:
            print(f"🔍 Fetching StockTwits data for ${ticker}...")
            
            # StockTwits API endpoint (no auth needed for basic access)
            url = f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return f"Error fetching StockTwits data for {ticker}: HTTP {response.status_code}"
            
            data = response.json()
            
            if 'messages' not in data or not data['messages']:
                return f"""
StockTwits Sentiment Analysis for ${ticker}:

❌ No recent messages found.
This indicates very low trader interest/awareness.

Recommendation: Limited social momentum - focus on fundamentals/technicals.
"""
            
            messages = data['messages'][:limit]
            
            # Extract sentiment data
            bullish_count = 0
            bearish_count = 0
            neutral_count = 0
            sentiment_scores = []
            message_texts = []
            user_followers = []
            timestamps = []
            
            for msg in messages:
                # StockTwits provides explicit sentiment
                if msg.get('entities', {}).get('sentiment'):
                    sentiment = msg['entities']['sentiment']['basic']
                    if sentiment == 'Bullish':
                        bullish_count += 1
                        sentiment_scores.append(0.5)
                    elif sentiment == 'Bearish':
                        bearish_count += 1
                        sentiment_scores.append(-0.5)
                    else:
                        neutral_count += 1
                        sentiment_scores.append(0)
                else:
                    neutral_count += 1
                    # Use TextBlob for messages without explicit sentiment
                    text = msg.get('body', '')
                    blob = TextBlob(text)
                    sentiment_scores.append(blob.sentiment.polarity)
                
                message_texts.append(msg.get('body', ''))
                user_followers.append(msg.get('user', {}).get('followers', 0))
                timestamps.append(msg.get('created_at', ''))
            
            # Calculate metrics
            total_messages = len(messages)
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            
            # Top influencer messages (by follower count)
            messages_with_followers = list(zip(messages, user_followers))
            top_influencers = sorted(messages_with_followers, key=lambda x: x[1], reverse=True)[:3]
            
            # Sentiment trend (comparing recent vs older messages)
            if len(sentiment_scores) >= 10:
                recent_sentiment = sum(sentiment_scores[:10]) / 10
                older_sentiment = sum(sentiment_scores[10:]) / len(sentiment_scores[10:]) if len(sentiment_scores) > 10 else recent_sentiment
                trend = "📈 Improving" if recent_sentiment > older_sentiment + 0.1 else "📉 Declining" if recent_sentiment < older_sentiment - 0.1 else "➡️ Stable"
            else:
                trend = "➡️ Limited data"
            
            # Overall sentiment label
            if avg_sentiment > 0.3 or (bullish_count / total_messages > 0.6):
                sentiment_label = "🟢 Very Bullish"
            elif avg_sentiment > 0.1 or (bullish_count / total_messages > 0.5):
                sentiment_label = "🟢 Bullish"
            elif avg_sentiment > -0.1:
                sentiment_label = "🟡 Neutral/Mixed"
            elif avg_sentiment > -0.3 or (bearish_count / total_messages > 0.5):
                sentiment_label = "🔴 Bearish"
            else:
                sentiment_label = "🔴 Very Bearish"
            
            # Message volume assessment
            if total_messages >= 25:
                volume_label = "🔥 HIGH Activity"
            elif total_messages >= 15:
                volume_label = "📈 Moderate Activity"
            else:
                volume_label = "📉 Low Activity"
            
            # Build report
            report = f"""
StockTwits Sentiment Analysis for ${ticker}:

═══════════════════════════════════════════════════════════════
📊 OVERVIEW
═══════════════════════════════════════════════════════════════
Total Messages Analyzed: {total_messages}
Message Volume: {volume_label}
Overall Sentiment: {sentiment_label}
Sentiment Score: {avg_sentiment:.3f} (-1.0 to +1.0 scale)
Trend: {trend}

═══════════════════════════════════════════════════════════════
💬 SENTIMENT BREAKDOWN
═══════════════════════════════════════════════════════════════
🟢 Bullish: {bullish_count} ({bullish_count/total_messages*100:.1f}%)
🟡 Neutral: {neutral_count} ({neutral_count/total_messages*100:.1f}%)
🔴 Bearish: {bearish_count} ({bearish_count/total_messages*100:.1f}%)

Bull/Bear Ratio: {bullish_count/bearish_count:.2f}:1 if bearish_count > 0 else "∞" (all bulls)

═══════════════════════════════════════════════════════════════
👥 TOP INFLUENCER MESSAGES
═══════════════════════════════════════════════════════════════
"""
            
            for i, (msg, followers) in enumerate(top_influencers, 1):
                sentiment_tag = msg.get('entities', {}).get('sentiment', {}).get('basic', 'Neutral')
                sentiment_emoji = "🟢" if sentiment_tag == "Bullish" else "🔴" if sentiment_tag == "Bearish" else "🟡"
                username = msg.get('user', {}).get('username', 'Unknown')
                text = msg.get('body', '')[:100]
                
                report += f"""
{i}. {sentiment_emoji} @{username} ({followers:,} followers) - {sentiment_tag}
   "{text}..."
"""
            
            report += f"""

═══════════════════════════════════════════════════════════════
📋 RECENT MESSAGES SAMPLE
═══════════════════════════════════════════════════════════════
"""
            
            for i, msg in enumerate(messages[:5], 1):
                sentiment_tag = msg.get('entities', {}).get('sentiment', {}).get('basic', 'Neutral')
                sentiment_emoji = "🟢" if sentiment_tag == "Bullish" else "🔴" if sentiment_tag == "Bearish" else "🟡"
                username = msg.get('user', {}).get('username', 'Unknown')
                text = msg.get('body', '')[:120]
                time_ago = msg.get('created_at', '')[:19]
                
                report += f"{i}. {sentiment_emoji} @{username}: \"{text}...\"\n   Posted: {time_ago}\n\n"
            
            report += f"""
═══════════════════════════════════════════════════════════════
📋 TRADING IMPLICATIONS
═══════════════════════════════════════════════════════════════
"""
            
            # Trading recommendations based on sentiment
            if bullish_count / total_messages > 0.7 and total_messages >= 20:
                report += """
⚠️ WARNING: Extreme bullish sentiment detected
- Over 70% of traders are bullish
- Potential for overcrowding / contrarian signal
- Risk: Late to the party, possible reversal ahead
- Consider: Smaller position size or wait for pullback
"""
            elif bullish_count / total_messages > 0.6:
                report += """
✅ POSITIVE: Strong bullish consensus
- Majority of traders are bullish
- Social momentum could support upward movement
- Aligns well with technical breakouts
- Consider: Normal position size if technicals confirm
"""
            elif bearish_count / total_messages > 0.6:
                report += """
⚠️ CAUTION: Strong bearish sentiment
- Majority of traders are bearish
- Could face continued selling pressure
- Consider: Short opportunity or avoid longs
- Watch: Sentiment reversal as potential bottom signal
"""
            elif abs(bullish_count - bearish_count) <= 3:
                report += """
ℹ️ NEUTRAL: Divided sentiment
- Traders are split between bulls and bears
- Indicates uncertainty or transition period
- Focus on: Price action and volume for direction
- Wait for: Clear sentiment shift before entering
"""
            else:
                report += """
ℹ️ MIXED: No clear directional bias
- Moderate sentiment without extreme views
- Social media unlikely to be major catalyst
- Focus on: Fundamentals and technical setup
"""
            
            if total_messages < 15:
                report += """

ℹ️ LOW ACTIVITY: Limited social interest
- Under the radar / not widely discussed
- Less retail-driven volatility expected
- Could be opportunity before crowd notices
"""
            
            report += f"""

═══════════════════════════════════════════════════════════════
💡 SUMMARY
═══════════════════════════════════════════════════════════════
Sentiment: {sentiment_label}
Trend: {trend}
Volume: {volume_label}
Bull/Bear Split: {bullish_count}/{bearish_count}

Recommendation for Trading:
"""
            
            if avg_sentiment > 0.2 and bullish_count > bearish_count * 1.5:
                report += "✅ Bullish social momentum - can support long positions\n"
            elif avg_sentiment < -0.2 and bearish_count > bullish_count * 1.5:
                report += "⚠️ Bearish social pressure - avoid longs or consider shorts\n"
            elif total_messages < 10:
                report += "ℹ️ Low engagement - social sentiment not a major factor\n"
            else:
                report += "ℹ️ Neutral - rely on technicals and fundamentals\n"
            
            return report
            
        except requests.RequestException as e:
            return f"Network error fetching StockTwits data for {ticker}: {str(e)}"
        except Exception as e:
            return f"Error analyzing StockTwits sentiment for {ticker}: {str(e)}"
