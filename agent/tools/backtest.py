import sys, os
sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yfinance as yf
import pandas as pd
import math
from dotenv import load_dotenv
load_dotenv()

def safe(val, default=0.0):
    try:
        f = float(val)
        return default if (math.isnan(f) or math.isinf(f)) else f
    except:
        return default

def backtest_stock(symbol: str,
                   buy_date: str,
                   sell_date: str,
                   shares: int) -> dict:
    """
    Simulates what would have happened if agent
    bought on buy_date and sold on sell_date.
    """
    try:
        df = yf.download(
            f"{symbol}.NS",
            start       = buy_date,
            end         = sell_date,
            progress    = False,
            auto_adjust = True
        )

        if df.empty or len(df) < 2:
            return {"error": f"No data for {symbol}"}

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        close      = df['Close'].astype(float).dropna()
        buy_price  = round(safe(close.iloc[0]),  2)
        sell_price = round(safe(close.iloc[-1]), 2)

        if buy_price <= 0:
            return {"error": f"Invalid price for {symbol}"}

        invested   = round(buy_price  * shares, 2)
        current    = round(sell_price * shares, 2)
        profit     = round(current - invested, 2)
        pct_return = round(
            ((sell_price - buy_price) / buy_price) * 100, 2)

        return {
            "symbol":      symbol,
            "buy_date":    buy_date,
            "sell_date":   sell_date,
            "buy_price":   buy_price,
            "sell_price":  sell_price,
            "shares":      shares,
            "invested":    invested,
            "current":     current,
            "profit":      profit,
            "pct_return":  pct_return,
            "result":      "PROFIT" if profit > 0 else "LOSS"
        }
    except Exception as e:
        return {"error": str(e)}

def backtest_portfolio(holdings: list,
                       buy_date: str,
                       sell_date: str) -> dict:
    """
    Backtests an entire allocation plan.
    holdings = result from allocator — list of dicts
    """
    results        = []
    total_invested = 0
    total_current  = 0

    for h in holdings:
        symbol = h.get("symbol", "")
        shares = int(h.get("shares", 0))
        spent  = safe(h.get("spent", 0))

        if symbol == "LIQUIDBEES":
            results.append({
                "symbol":     "LIQUIDBEES",
                "invested":   spent,
                "current":    spent,
                "profit":     0,
                "pct_return": 0,
                "result":     "STABLE"
            })
            total_invested += spent
            total_current  += spent
            continue

        if shares <= 0:
            continue

        r = backtest_stock(symbol, buy_date, sell_date, shares)

        if "error" not in r:
            results.append(r)
            total_invested += r["invested"]
            total_current  += r["current"]
        else:
            print(f"  Backtest skipped {symbol}: {r['error']}")

    if total_invested == 0:
        return {"error": "No valid positions to backtest"}

    total_profit   = round(total_current - total_invested, 2)
    total_pct      = round(
        (total_profit / total_invested) * 100, 2)

    return {
        "buy_date":         buy_date,
        "sell_date":        sell_date,
        "total_invested":   round(total_invested, 2),
        "total_current":    round(total_current,  2),
        "total_profit":     total_profit,
        "total_pct_return": total_pct,
        "overall_result":   "PROFIT" if total_profit > 0 else "LOSS",
        "positions":        results
    }

if __name__ == "__main__":
    # Quick test
    test_holdings = [
        {"symbol": "WIPRO",      "shares": 4,
         "spent": 780,  "price": 195},
        {"symbol": "INFY",       "shares": 1,
         "spent": 1540, "price": 1540},
        {"symbol": "LIQUIDBEES", "shares": 2,
         "spent": 2000, "price": 1000},
    ]

    result = backtest_portfolio(
        holdings  = test_holdings,
        buy_date  = "2024-10-01",
        sell_date = "2025-01-01"
    )

    print(f"\nBacktest: {result['buy_date']} → {result['sell_date']}")
    print(f"{'='*55}")
    for p in result.get("positions", []):
        arrow = "▲" if p.get("pct_return", 0) >= 0 else "▼"
        print(f"  {p['symbol']:12} "
              f"₹{p.get('invested',0):>8} → "
              f"₹{p.get('current',0):>8}  "
              f"{arrow} {abs(p.get('pct_return',0))}%")
    print(f"{'='*55}")
    print(f"  Invested : ₹{result['total_invested']}")
    print(f"  Current  : ₹{result['total_current']}")
    print(f"  P&L      : ₹{result['total_profit']} "
          f"({result['total_pct_return']}%)")
    print(f"  Result   : {result['overall_result']}")