from datetime import datetime, timedelta
import yfinance as yf
import pytse_client as tse

def fetch_price(asset):
    source = asset.data_source
    symbol = asset.source_symbol

    if source == 'yahoo_finance':
        return fetch_yahoo_finance_price(symbol)
    if source == 'tsetmc':
        return fetch_tsetmc_price(symbol)
    else:
        raise ValueError("Unsupported data source.")

def fetch_yahoo_finance_price(symbol):
    """
    symbol examples:
    - Gold: 'GC=F'
    - BTC-USD: 'BTC-USD'
    """
    try:
        ticker = yf.Ticker(symbol)
        return float(ticker.info['regularMarketPrice'])
    except Exception as e:
        print(f"Yahoo Finance error ({symbol}): {e}")
        return 0.0
    

def fetch_tsetmc_price(symbol):
    """
    Fetch the latest available closing price for a symbol from TSETMC using pytse_client.
    
    :param symbol: TSETMC ticker symbol in Persian, e.g., "فولاد"
    :return: float price or 0.0 on failure
    """
    try:
        history_df = tse.download(symbols=symbol, write_to_csv=False)
        if symbol in history_df:
            latest_price = history_df[symbol]['close'].iloc[-1]
            return float(latest_price)
        else:
            print(f"TSETMC: Symbol '{symbol}' not found in the response.")
            return 0.0
    except Exception as e:
        print(f"TSETMC error ({symbol}): {e}")
        return 0.0
    
def get_exchange_rate(currency: str, date: datetime) -> float | None:
    """
    Get the exchange rate of the given currency to USD on a specific date using Yahoo Finance.

    Args:
        currency (str): Currency code like 'GBP', 'IRR', etc.
        date (datetime): Target date for the historical exchange rate.

    Returns:
        float or None
    """
    currency = currency.upper()

    if currency == "USD":
        return 1.0

    ticker_symbol = f"{currency}USD=X"
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(start=date.strftime('%Y-%m-%d'), end=(date + timedelta(days=1)).strftime('%Y-%m-%d'))

        if not history.empty:
            return float(history["Close"].iloc[0])
        else:
            print(f"No exchange rate found for {currency} on {date.date()}")
    except Exception as e:
        print(f"Error fetching exchange rate for {currency}: {e}")
    
    return None
