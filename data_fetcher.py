import yfinance as yf
import pytse_client as tse

def fetch_price(asset):
    source = asset[2]  # Data source
    symbol = asset[3]  # Asset symbol

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
