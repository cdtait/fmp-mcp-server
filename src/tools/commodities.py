"""
Commodities-related tools for the FMP MCP server

This module contains tools related to the Commodities section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/commodities-list
https://site.financialmodelingprep.com/developer/docs/stable/commodities-prices
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_commodities_list() -> str:
    """
    Get a list of available commodities
    
    Returns:
        List of available commodities with their symbols
    """
    data = await fmp_api_request("commodities-list", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching commodities list: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No commodities data found"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Available Commodities",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Name | Currency | Group |",
        "|--------|------|----------|-------|"
    ]
    
    # Group commodities by type
    commodity_groups = {}
    for commodity in data:
        symbol = commodity.get('symbol', 'N/A')
        name = commodity.get('name', 'N/A')
        currency = commodity.get('currency', 'USD')
        
        # Determine the commodity group
        if any(metal in name.lower() for metal in ['gold', 'silver', 'platinum', 'palladium', 'copper']):
            group = "Metals"
        elif any(energy in name.lower() for energy in ['oil', 'gas', 'gasoline', 'diesel', 'propane', 'ethanol']):
            group = "Energy"
        elif any(agri in name.lower() for agri in ['corn', 'wheat', 'soybean', 'sugar', 'coffee', 'cotton', 'rice']):
            group = "Agricultural"
        else:
            group = "Other"
        
        result.append(f"| {symbol} | {name} | {currency} | {group} |")
    
    # Add a note about usage
    result.append("")
    result.append("*Note: Use these symbols with the get_commodities_prices function to get current values.*")
    
    return "\n".join(result)


async def get_commodities_prices(symbol: str = None) -> str:
    """
    Get current prices for commodities
    
    Args:
        symbols: Comma-separated list of commodity symbols (e.g., "OUSX,GCUSD")
                If not provided, returns all available commodities
    
    Returns:
        Current prices for the specified commodities
    """
    params = {"symbol": symbol} if symbol else {}
    data = await fmp_api_request("quote", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching commodities prices: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No price data found for commodities: {symbol if symbol else 'all'}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Commodities Prices",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Name | Price | Change | Change % | Day Range | Year Range |",
        "|--------|------|-------|--------|----------|-----------|------------|"
    ]
    
    # Group commodities by type for better organization
    commodities_by_group = {}
    
    for commodity in data:
        symbol = commodity.get('symbol', 'N/A')
        name = commodity.get('name', 'N/A')
        price = format_number(commodity.get('price', 'N/A'))
        change = commodity.get('change', 0)
        change_percent = commodity.get('changesPercentage', 0)
        
        # Determine change emoji
        change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
        
        # Format the values
        change_str = f"{change_emoji} {format_number(abs(change))}"
        change_percent_str = f"{change_percent}%"
        
        day_low = format_number(commodity.get('dayLow', 'N/A'))
        day_high = format_number(commodity.get('dayHigh', 'N/A'))
        day_range = f"{day_low} - {day_high}"
        
        year_low = format_number(commodity.get('yearLow', 'N/A'))
        year_high = format_number(commodity.get('yearHigh', 'N/A'))
        year_range = f"{year_low} - {year_high}"
        
        # Determine the commodity group
        if any(metal in name.lower() for metal in ['gold', 'silver', 'platinum', 'palladium', 'copper']):
            group = "Metals"
        elif any(energy in name.lower() for energy in ['oil', 'gas', 'gasoline', 'diesel', 'propane', 'ethanol']):
            group = "Energy"
        elif any(agri in name.lower() for agri in ['corn', 'wheat', 'soybean', 'sugar', 'coffee', 'cotton', 'rice']):
            group = "Agricultural"
        else:
            group = "Other"
        
        if group not in commodities_by_group:
            commodities_by_group[group] = []
        
        commodities_by_group[group].append({
            'symbol': symbol,
            'name': name,
            'price': price,
            'change': change_str,
            'change_percent': change_percent_str,
            'day_range': day_range,
            'year_range': year_range
        })
    
    # Add commodities to the table, grouped by type
    groups_order = ["Energy", "Metals", "Agricultural", "Other"]
    
    for group in groups_order:
        if group in commodities_by_group and commodities_by_group[group]:
            result.append(f"### {group}")
            
            for commodity in commodities_by_group[group]:
                result.append(
                    f"| {commodity['symbol']} | {commodity['name']} | "
                    f"{commodity['price']} | {commodity['change']} | "
                    f"{commodity['change_percent']} | {commodity['day_range']} | "
                    f"{commodity['year_range']} |"
                )
            
            result.append("")
    
    return "\n".join(result)