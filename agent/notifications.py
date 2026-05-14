import os
import requests
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN  = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message: str) -> bool:
    """Send message via Telegram bot."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured — skipping notification")
        return False
    try:
        url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        resp = requests.post(url, json={
            "chat_id":    TELEGRAM_CHAT_ID,
            "text":       message,
            "parse_mode": "HTML"
        }, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def notify_trade_executed(allocation: dict, mode: str):
    holdings = allocation.get("holdings", [])
    lines    = [f"<b>Stock Agent AI — Trade Executed ({mode.upper()})</b>\n"]

    for h in holdings:
        if h["symbol"] == "LIQUIDBEES":
            continue
        lines.append(
            f"• <b>{h['symbol']}</b> — {h['shares']} shares "
            f"@ ₹{h['price']} = ₹{h['spent']}\n"
            f"  Action: {h.get('action','BUY')} | "
            f"Confidence: {h.get('confidence',0)}% | "
            f"Stop-loss: ₹{h.get('stop_loss', 'N/A')}"
        )

    lines.append(f"\n<b>Total invested:</b> ₹{allocation.get('total_spent', 0)}")
    lines.append(f"<b>Reserve:</b> ₹{allocation.get('reserve', 0)}")
    send_telegram("\n".join(lines))

def notify_market_mood(mood: dict):
    emoji = "🟢" if mood["color"] == "green" else \
            "🔴" if mood["color"] == "red"   else \
            "🟡" if mood["color"] == "yellow" else "🔵"

    msg = (
        f"{emoji} <b>Market Pulse Update</b>\n\n"
        f"Regime: <b>{mood['mood']}</b>\n"
        f"Nifty: {mood['nifty']} ({mood['nifty_change']}%)\n"
        f"VIX: {mood['india_vix']} — "
        f"{'High fear' if mood['high_fear'] else 'Low fear'}\n\n"
        f"<i>{mood['advice']}</i>"
    )
    send_telegram(msg)

def notify_stop_loss_alert(symbol: str, 
                           current_price: float,
                           stop_loss: float):
    msg = (
        f" <b>Stop-Loss Alert</b>\n\n"
        f"Stock: <b>{symbol}</b>\n"
        f"Current price: ₹{current_price}\n"
        f"Stop-loss level: ₹{stop_loss}\n\n"
        f"Consider reviewing your position."
    )
    send_telegram(msg)

if __name__ == "__main__":
    # Test
    send_telegram("Stock Agent AI — Telegram connected successfully!")
    print("Test message sent. Check your Telegram.")