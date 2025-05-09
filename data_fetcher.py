import yfinance as yf

def fetch_price(asset):
    source = asset[2]  # Data source
    symbol = asset[3]  # Asset symbol

    if source == 'yahoo_finance':
        return fetch_yahoo_finance_price(symbol)
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
