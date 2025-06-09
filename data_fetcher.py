import yfinance as yf
import pytse_client as tse

def fetch_price(asset):
    symbol = asset.symbol

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
    
def fetch_gold_price():
    symbol = "طلا"
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
