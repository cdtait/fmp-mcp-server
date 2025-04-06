"""
Prompt templates for the FMP MCP server
"""
from typing import Dict, Any, Optional, List


def company_analysis(symbol: str) -> str:
    """
    Generate a comprehensive company analysis
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
    """
    return f"""Please provide a comprehensive analysis of {symbol} as an investment opportunity.

Include the following in your analysis:
1. Company overview and business model
2. Financial health assessment (revenue growth, profitability, debt levels)
3. Competitive position and market trends
4. Key strengths, weaknesses, opportunities, and threats
5. Valuation analysis (P/E ratio, PEG, price-to-book compared to peers and historical averages)
6. Recent news and developments that might impact the stock
7. Summary and investment recommendation (buy, hold, or sell)

Base your analysis on the financial data and company information available through the tools and resources."""


def financial_statement_analysis(symbol: str, statement_type: str) -> str:
    """
    Analyze a company's financial statements
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
        statement_type: Type of statement to analyze (income, balance, cash-flow)
    """
    statement_names = {
        "income": "Income Statement",
        "balance": "Balance Sheet",
        "cash-flow": "Cash Flow Statement"
    }
    
    statement_name = statement_names.get(statement_type, statement_type.capitalize())
    
    return f"""Please analyze the {statement_name} for {symbol} and provide insights.

For your analysis:
1. Identify the most significant line items and explain their importance
2. Highlight any notable trends over the past few years
3. Calculate and interpret key ratios relevant to this statement
4. Compare the metrics to industry averages if possible
5. Point out any red flags or positive indicators
6. Provide context on how these financials impact the company's overall health

Be thorough but concise, focusing on the most important aspects that would matter to an investor."""


def stock_comparison(symbols: str) -> str:
    """
    Compare multiple stocks for investment decision-making
    
    Args:
        symbols: Comma-separated list of stock symbols (e.g., AAPL,MSFT,GOOGL)
    """
    symbol_list = symbols.split(",")
    symbols_formatted = ", ".join(symbol_list)
    
    return f"""Please compare the following stocks: {symbols_formatted}.

Provide a detailed comparison including:
1. Business overview for each company
2. Financial performance metrics (growth rates, margins, ROE, etc.)
3. Valuation metrics (P/E, P/S, PEG, etc.)
4. Dividend information if applicable
5. Recent stock performance
6. Strengths and weaknesses of each company
7. Competitive positioning within their industry
8. Future growth prospects

Conclude with a ranking of these stocks from most to least attractive investment opportunity based on the data, and explain your reasoning.

Use available financial tools and resources to gather the necessary data for your analysis."""


def market_outlook() -> str:
    """
    Generate a market outlook and analysis of current conditions
    """
    return """Please provide a comprehensive outlook on the current market conditions.

Include in your analysis:
1. Current state of major market indexes (S&P 500, Dow Jones, NASDAQ)
2. Sector performance (identify strongest and weakest sectors)
3. Market sentiment indicators
4. Recent economic data and its impact on markets
5. Interest rate environment and monetary policy outlook
6. Key market risks and opportunities
7. Potential catalysts that could move markets in the near term
8. Overall market positioning recommendation (defensive, neutral, aggressive)

Base your analysis on the most recent available data, and be sure to consider both technical and fundamental factors in your assessment."""


def investment_idea_generation(criteria: str) -> str:
    """
    Generate investment ideas based on specified criteria
    
    Args:
        criteria: Investment criteria (e.g., growth, value, dividend, sector)
    """
    return f"""Based on the criteria "{criteria}", please generate a list of promising investment ideas.

For each investment idea:
1. Identify the company/asset and provide a brief overview
2. Explain why it meets the specified criteria
3. Highlight key financial metrics that support the investment thesis
4. Discuss potential catalysts that could drive performance
5. Address key risks to be aware of
6. Suggest an appropriate position size or portfolio allocation

Aim to provide diverse ideas that align with the criteria while offering different risk/reward profiles. Use available financial tools and resources to inform your recommendations."""


def technical_analysis(symbol: str) -> str:
    """
    Perform technical analysis on a stock
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
    """
    return f"""Please perform a comprehensive technical analysis for {symbol}.

In your analysis, include:
1. Current price action and trend direction
2. Key support and resistance levels
3. Analysis of volume patterns
4. Important technical indicators (moving averages, RSI, MACD, etc.)
5. Chart patterns and formations
6. Identification of potential entry and exit points
7. Overall technical outlook (bullish, bearish, or neutral)

Base your analysis on the available historical price data and standard technical analysis principles. Provide specific price levels where possible and explain the significance of key technical signals."""


def economic_indicator_analysis(indicator: str) -> str:
    """
    Analyze an economic indicator and its market implications
    
    Args:
        indicator: Economic indicator (e.g., inflation, GDP, unemployment, interest rates)
    """
    return f"""Please provide a detailed analysis of current {indicator} data and its implications for financial markets.

Include in your analysis:
1. Recent trends in {indicator} data
2. Historical context for current {indicator} levels
3. How {indicator} is likely to impact different asset classes (stocks, bonds, commodities, etc.)
4. Sectors that typically benefit or suffer from the current {indicator} environment
5. Central bank or government response to {indicator} trends
6. Forward-looking projections for {indicator}
7. Investment strategies appropriate for the current {indicator} environment

Provide specific examples of securities or sectors that may be particularly affected, with reasoning based on economic principles and historical market behavior."""