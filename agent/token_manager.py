import os, requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

def is_token_expiring_soon(hours_threshold: int = 2) -> bool:
    """
    Checks if token needs refresh.
    Upstox tokens expire at midnight IST daily.
    """
    now = datetime.now()
    midnight = now.replace(hour=23, minute=30,
                           second=0, microsecond=0)
    return now >= midnight

def refresh_upstox_token() -> dict:
    """
    Attempts to refresh using stored credentials.
    Falls back to notification if manual login needed.
    """
    api_key = os.getenv("UPSTOX_API_KEY")
    secret  = os.getenv("UPSTOX_SECRET")

    if not api_key or not secret:
        return {"status": "error",
                "message": "Upstox credentials missing in .env"}

    # Check if token is still valid
    token   = os.getenv("UPSTOX_ACCESS_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept":        "application/json"
    }
    try:
        resp = requests.get(
            "https://api.upstox.com/v2/user/profile",
            headers=headers, timeout=10
        )
        if resp.status_code == 200:
            return {"status": "valid",
                    "message": "Token still valid"}
        else:
            # Token expired — send Telegram alert
            try:
                from agent.notifications import send_telegram
                send_telegram(
                    " <b>Upstox Token Expired</b>\n\n"
                    "Run <code>python refresh_token.py</code> "
                    "to get a new token before trading today."
                )
            except:
                pass
            return {"status": "expired",
                    "message": "Token expired — manual refresh needed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = refresh_upstox_token()
    print(f"Token status: {result['status']}")
    print(f"Message: {result['message']}")