import pytse_client as tse

def fetch_min_price(asset):
    symbol = asset.symbol

    try:
        asset_real_time_info = tse.Ticker(symbol).get_ticker_real_time_info_response()
        if asset_real_time_info:
            latest_price = asset_real_time_info.high_price
            return float(latest_price)
        else:
            print(f"TSETMC: Symbol '{symbol}' not found in the response.")
            return 0.0
    except Exception as e:
        print(f"TSETMC error ({symbol}): {e}")
        return 0.0
    
def fetch_max_price(asset):
    symbol = asset.symbol

    try:
        asset_real_time_info = tse.Ticker(symbol).get_ticker_real_time_info_response()
        if asset_real_time_info:
            latest_price = asset_real_time_info.low_price
            return float(latest_price)
        else:
            print(f"TSETMC: Symbol '{symbol}' not found in the response.")
            return 0.0
    except Exception as e:
        print(f"TSETMC error ({symbol}): {e}")
        return 0.0
    
def fetch_gold_price():
    try:
        gold_real_time_info = tse.Ticker("طلا").get_ticker_real_time_info_response()
        if gold_real_time_info:
            latest_price = gold_real_time_info.adj_close
            return float(latest_price)
        else:
            print(f"TSETMC: Symbol 'طلا' not found in the response.")
            return 0.0
    except Exception as e:
        print(f"TSETMC error (طلا): {e}")
        return 0.0
