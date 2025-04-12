"""
Calendar-related tools for the FMP MCP server

This module contains tools related to the Calendar section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/dividends-company
https://site.financialmodelingprep.com/developer/docs/stable/dividends-calendar
"""
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta

from src.api.client import fmp_api_request


def format_number(value: Any) -> str:
    """Format a number with commas, or return as-is if not a number"""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)


async def get_company_dividends(symbol: str, limit: int = 10) -> str:
    """
    Get dividend history for a specific company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, JNJ)
        limit: Number of dividend records to return (1-1000)
        
    Returns:
        Historical dividend payments and upcoming dividends
    """
    # Validate inputs
    if not 1 <= limit <= 1000:
        return "Error: limit must be between 1 and 1000"
    
    data = await fmp_api_request("dividends", {"symbol": symbol, "limit": limit})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching dividend data for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No dividend data found for symbol {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Dividend History for {symbol}",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Calculate useful metrics
    if len(data) > 0:
        # Get the most recent dividend amount
        latest_dividend = data[0].get('dividend', 0)
        
        # Check if dividend info is available
        if latest_dividend > 0:
            # Extract latest price if available
            latest_price = data[0].get('adjDividend', None)
            
            # Calculate annual yield if there are at least 4 records and they appear to be quarterly
            if len(data) >= 4:
                annual_dividend = sum(item.get('dividend', 0) for item in data[:4])
                if latest_price and annual_dividend > 0:
                    annual_yield = (annual_dividend / latest_price) * 100
                    result.append(f"**Estimated Annual Yield**: {annual_yield:.2f}%")
                result.append(f"**Estimated Annual Dividend**: ${format_number(annual_dividend)}")
            
            # Calculate average frequency
            if len(data) >= 2:
                # Extract dates and convert to datetime objects
                dates = []
                for item in data:
                    date_str = item.get('date', None)
                    if date_str:
                        try:
                            dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
                        except ValueError:
                            pass
                
                # Calculate average days between dividends
                if len(dates) >= 2:
                    intervals = [(dates[i] - dates[i+1]).days for i in range(len(dates)-1)]
                    avg_interval = sum(intervals) / len(intervals)
                    
                    if 80 <= avg_interval <= 100:
                        frequency = "Quarterly"
                    elif 170 <= avg_interval <= 190:
                        frequency = "Semi-annually"
                    elif 350 <= avg_interval <= 380:
                        frequency = "Annually"
                    elif 25 <= avg_interval <= 35:
                        frequency = "Monthly"
                    else:
                        frequency = f"Approximately every {int(avg_interval)} days"
                    
                    result.append(f"**Dividend Frequency**: {frequency}")
            
            result.append("")
    
    # Create the dividend history table
    result.append("## Dividend History")
    result.append("| Date | Dividend | Adjusted Dividend | Record Date | Payment Date | Declaration Date |")
    result.append("|------|----------|-------------------|-------------|--------------|------------------|")
    
    for div in data:
        date = div.get('date', 'N/A')
        amount = div.get('dividend', 'N/A')
        adj_amount = div.get('adjDividend', 'N/A')
        record_date = div.get('recordDate', 'N/A')
        payment_date = div.get('paymentDate', 'N/A')
        declaration_date = div.get('declarationDate', 'N/A')
        
        # Format amounts as currency
        if isinstance(amount, (int, float)):
            amount = f"${amount:.4f}"
        if isinstance(adj_amount, (int, float)):
            adj_amount = f"${adj_amount:.4f}"
        
        result.append(f"| {date} | {amount} | {adj_amount} | {record_date} | {payment_date} | {declaration_date} |")
    
    return "\n".join(result)


async def get_dividends_calendar(from_date: str = None, to_date: str = None, limit: int = 50) -> str:
    """
    Get upcoming dividend events for all stocks
    
    Args:
        from_date: Start date in YYYY-MM-DD format (defaults to today)
        to_date: End date in YYYY-MM-DD format (defaults to 30 days from today)
        limit: Number of events to return (1-3000)
        
    Returns:
        Calendar of upcoming dividend events
    """
    # Validate inputs
    if not 1 <= limit <= 3000:
        return "Error: limit must be between 1 and 3000"
    
    # Default dates if not provided
    today = datetime.now()
    
    if not from_date:
        from_date = today.strftime("%Y-%m-%d")
    
    if not to_date:
        # Default to 30 days from from_date, max 90 days total range
        to_datetime = today + timedelta(days=30)
        to_date = to_datetime.strftime("%Y-%m-%d")
    
    # Validate date formats
    try:
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
        
        # Check if date range is valid (max 90 days)
        days_diff = (to_datetime - from_datetime).days
        if days_diff < 0:
            return "Error: 'to_date' must be after 'from_date'"
        if days_diff > 90:
            return "Error: Maximum date range is 90 days"
    except ValueError:
        return "Error: dates must be in YYYY-MM-DD format"
    
    # Make API request
    params = {"from": from_date, "to": to_date, "limit": limit}
    data = await fmp_api_request("dividends-calendar", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching dividends calendar: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No dividend events found between {from_date} and {to_date}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Dividend Calendar: {from_date} to {to_date}",
        f"*Data as of {current_time}*",
        f"*Showing {min(len(data), limit)} dividend events*",
        ""
    ]
    
    # Group events by date
    events_by_date = {}
    for event in data:
        date = event.get('date', 'Unknown')
        if date not in events_by_date:
            events_by_date[date] = []
        events_by_date[date].append(event)
    
    # Sort dates
    sorted_dates = sorted(events_by_date.keys())
    
    # Events by type
    for date in sorted_dates:
        events = events_by_date[date]
        result.append(f"## {date}")
        result.append("| Symbol | Company | Dividend | Yield | Ex-Dividend Date | Payment Date | Record Date |")
        result.append("|--------|---------|----------|-------|------------------|--------------|-------------|")
        
        for event in events:
            symbol = event.get('symbol', 'N/A')
            name = event.get('name', 'N/A')
            dividend = event.get('dividend', 'N/A')
            yield_val = event.get('dividend_yield', 'N/A')
            ex_date = event.get('date', 'N/A')
            payment_date = event.get('paymentDate', 'N/A')
            record_date = event.get('recordDate', 'N/A')
            
            # Format numbers
            if isinstance(dividend, (int, float)):
                dividend = f"${dividend:.4f}"
            if isinstance(yield_val, (int, float)):
                yield_val = f"{yield_val:.2f}%"
            
            result.append(f"| {symbol} | {name} | {dividend} | {yield_val} | {ex_date} | {payment_date} | {record_date} |")
        
        result.append("")
    
    return "\n".join(result)