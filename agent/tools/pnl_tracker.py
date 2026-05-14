import sys, os
sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yfinance as yf
import pandas as pd
import math
from backend.database import get_trade_history

def safe(val, default=0.0):
    try:
        f = float(val)
        return default if (math.isnan(f) or math.isinf(f)) else f
    except:
        return default

def get_current_price(symbol: str) -> float:
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        hist   = ticker.history(period="2d")
        if hist.empty:
            return 0.0
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)
        return safe(hist['Close'].astype(float).iloc[-1])
    except:
        return 0.0

def calculate_pnl(user_id: str) -> dict:
    """
    Reads last trade from DB, fetches current prices,
    calculates P&L per position.
    """
    trades = get_trade_history(user_id)
    if not trades:
        return {"error": "No trades found"}

    last_trade = trades[0]
    holdings   = last_trade["allocation"].get("holdings", [])
    trade_date = last_trade["created_at"]

    positions  = []
    total_invested = 0
    total_current  = 0

    for h in holdings:
        symbol     = h["symbol"]
        buy_price  = safe(h.get("price", 0))
        shares     = int(h.get("shares", 0))
        invested   = safe(h.get("spent", 0))

        if symbol == "LIQUIDBEES":
            current_price = 1000.0
        else:
            current_price = get_current_price(symbol)

        if current_price == 0:
            current_price = buy_price

        current_value = round(current_price * shares, 2)
        pnl           = round(current_value - invested, 2)
        pnl_pct       = round((pnl / invested) * 100, 2) if invested > 0 else 0
        stop_loss     = safe(h.get("stop_loss", buy_price * 0.95))
        sl_hit        = current_price <= stop_loss

        positions.append({
            "symbol":        symbol,
            "shares":        shares,
            "buy_price":     round(buy_price, 2),
            "current_price": round(current_price, 2),
            "invested":      invested,
            "current_value": current_value,
            "pnl":           pnl,
            "pnl_pct":       pnl_pct,
            "stop_loss":     round(stop_loss, 2),
            "sl_hit":        sl_hit,
            "status":        "STOP LOSS HIT" if sl_hit else
                             "PROFIT" if pnl > 0 else "LOSS"
        })

        total_invested += invested
        total_current  += current_value

    total_pnl     = round(total_current - total_invested, 2)
    total_pnl_pct = round((total_pnl / total_invested) * 100, 2) \
                    if total_invested > 0 else 0

    return {
        "user_id":       user_id,
        "trade_date":    trade_date,
        "positions":     positions,
        "total_invested": round(total_invested, 2),
        "total_current":  round(total_current, 2),
        "total_pnl":      total_pnl,
        "total_pnl_pct":  total_pnl_pct,
        "overall_status": "PROFIT" if total_pnl > 0 else "LOSS",
        "stop_loss_alerts": [
            p["symbol"] for p in positions if p["sl_hit"]
        ]
    }

if __name__ == "__main__":
    result = calculate_pnl("demo_user")
    print(f"\n{'='*50}")
    print(f"  PORTFOLIO P&L REPORT")
    print(f"{'='*50}")
    for p in result.get("positions", []):
        arrow = "▲" if p["pnl"] >= 0 else "▼"
        sl    = "  SL HIT" if p["sl_hit"] else ""
        print(f"  {p['symbol']:12} "
              f"Buy: ₹{p['buy_price']:>8} → "
              f"Now: ₹{p['current_price']:>8} | "
              f"{arrow} ₹{abs(p['pnl'])} ({p['pnl_pct']}%){sl}")
    print(f"{'='*50}")
    print(f"  Total P&L: ₹{result['total_pnl']} "
          f"({result['total_pnl_pct']}%) — {result['overall_status']}")
    if result["stop_loss_alerts"]:
        print(f"  Stop-loss alerts: {result['stop_loss_alerts']}")