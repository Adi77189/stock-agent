# Stock Agent AI

> Autonomous AI investment agent for Indian stock markets (NSE) — analyzes live data, decides which stocks to buy, allocates your budget intelligently, and invests automatically.

---

## 🎥 Watch Full Demo

<p align="center">
  <a href="https://www.youtube.com/watch?v=BwZFpIvA5sI">
    <img src="https://img.youtube.com/vi/BwZFpIvA5sI/0.jpg" width="700">
  </a>
</p>

---

## Problem Statement

Most people want to invest in stocks but don't know which stocks to buy, how much to put in, or when to exit — so they either lose money or never invest at all. This AI agent solves that completely. You give it a budget, it analyzes 20 NSE stocks using live prices, technical indicators, and news sentiment, then decides exactly which stocks to buy, how many shares, and where to set stop-losses. It executes automatically via Upstox broker, generates a plain-English explanation of every decision, and reinvests monthly via SIP — without any manual action from you.

---

## Live URLs

| Service | URL |
|---|---|
| React Dashboard | http://localhost:3000 |
| FastAPI Backend | http://localhost:8000 |
| Swagger API Docs | http://localhost:8000/docs |

---

## Folder Structure

```
stock-agent/
│
├── agent/                          # Core AI agent
│   ├── __init__.py
│   ├── allocator.py                # Budget allocation engine
│   ├── autonomous.py               # Autonomous decision + signal resolver
│   ├── orchestrator.py             # Main agent brain
│   ├── notifications.py            # Telegram alert system        ← NEW
│   ├── token_manager.py            # Upstox token validator        ← NEW
│   ├── memory/
│   │   ├── __init__.py
│   │   └── behavior.py             # Investor behavior profiling
│   ├── prompts/                    # GPT prompt templates
│   └── tools/
│       ├── __init__.py
│       ├── advisor.py              # BUY/HOLD/SELL signal generator
│       ├── backtest.py             # Historical backtesting engine  ← NEW
│       ├── broker.py               # Upstox API v2 integration
│       ├── market_data.py          # Live NSE price fetcher (20 stocks)
│       ├── market_mood.py          # Nifty50 + India VIX mood detector
│       ├── pnl_tracker.py          # Real-time P&L + stop-loss monitor ← NEW
│       ├── risk.py                 # Risk scoring engine
│       ├── sentiment.py            # NewsAPI + GPT-4o-mini sentiment
│       └── technical.py            # RSI, MACD, MA200, indicators
│
├── backend/
│   ├── __init__.py
│   ├── database.py                 # PostgreSQL models + queries
│   ├── main.py                     # FastAPI app — 20+ endpoints
│   ├── routers/                    # Route modules
│   └── scheduler.py                # APScheduler monthly SIP + token check
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── App.css
│       ├── Dashboard.jsx           # Complete React dashboard
│       ├── index.js
│       └── index.css
│
├── data/                           # Static reference data
├── stockAgent/                     # Python virtual environment
│
├── .env                            # API keys — never commit this
├── .gitignore
├── Screenshots/                    # Project screenshots
├── README.md
├── refresh_token.py                # Daily Upstox token refresh
└── requirements.txt
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React 18, Recharts, Axios | Dashboard with live charts |
| Backend | FastAPI 2.0, Uvicorn | REST API server |
| Database | PostgreSQL 15, SQLAlchemy | Trade logs, SIP schedules |
| AI Model | OpenAI GPT-4o-mini | Sentiment scoring + report generation |
| Market Data | yfinance | Live NSE OHLCV data (20 stocks) |
| News | NewsAPI, Google News RSS | Stock headline fetching |
| Broker | Upstox API v2 | Paper + live NSE order execution |
| Scheduler | APScheduler | Monthly SIP + daily token check |
| Notifications | Telegram Bot API | Trade alerts + stop-loss warnings |
| Fonts | DM Mono, Space Grotesk | Bloomberg terminal aesthetic |

---

## Dashboard — Every Button Explained

This is the complete guide to what each button on the React dashboard does.

### Control Bar (top section)

| Button | What it does |
|---|---|
| **▶ Analyze ₹X,XXX** | Runs the full AI agent — fetches data, scores stocks, allocates budget, generates report, saves to DB. Takes ~45 seconds. Button turns red in LIVE mode. |
| **Insights** | Shows 3 cards: Bull/Base/Bear scenario simulation, agent performance metrics (total trades, accuracy, stock frequency), and rebalance recommendation. |
| **P&L** | Fetches current live prices for all your holdings, calculates profit/loss per position, highlights any stop-loss breaches with a warning. |
| **Prices** | Shows live NSE prices for all 20 stocks with today's % change in green (up) or red (down). |
| **Pulse** | Fetches Nifty50 + India VIX data, determines market regime (BULLISH/NEUTRAL/CAUTIOUS/BEARISH), shows fear meter, and loads your investor behavior profile from trade history. |
| **Signals** | Runs BUY/HOLD/SELL analysis for all 20 stocks. Shows a table with confidence bars, RSI values, distance from 52-week high. Click any row to expand full technical breakdown. |
| **Funds** | Calls Upstox API to fetch your available margin and used margin. Shows ₹0 in paper mode — shows real balance in live mode. |
| **History** | Loads all past trades from PostgreSQL. Shows date, budget, which stocks were bought, and risk level for each trade. |
| **Paper/Live toggle** | Switches between paper trading (safe simulation) and live trading (real NSE orders). Toggle turns red in LIVE mode. Always keep PAPER_MODE=true in .env until fully tested. |

### Results tabs (appear after clicking Analyze)

| Tab | What it shows |
|---|---|
| **Overview** | 4 stat cards (budget, invested, reserve, positions) + donut chart (allocation breakdown) + bar chart (AI score vs RSI for top stocks) |
| **Allocation** | Full position table — symbol, shares, buy price, amount invested, weight %, circular confidence score badge, stop-loss per position |
| **Report** | GPT-4o-mini generated 4-section investment report: Market Regime → Stock Picks with stop-losses → Portfolio Summary → Behavioral Alert |
| **Orders** | Execution status per position — PAPER_EXECUTED (simulation) or EXECUTED with real Upstox order ID (live mode) |

### Bottom sections

| Section | What it does |
|---|---|
| **P&L panel** | Shows buy price vs current price per holding, profit/loss in ₹ and %, overall portfolio return, and  alert if any position has breached its stop-loss |
| **Trade History** | Cards showing all past trades from DB — date, total budget, stocks bought with share counts |
| **Monthly SIP** | Enter an amount → click Activate SIP → agent auto-invests on 1st of every month at 9:15 AM (NSE open) without any action from you |
| **Insights panel** | Three cards: (1) Scenario simulation — bull/base/bear projected values, (2) Agent performance — trade history analysis, (3) Rebalance check — tells you if rebalancing is due |

---

## API Endpoints

All endpoints visible at `http://127.0.0.1:8000/docs`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root — API status |
| `GET` | `/health` | Health check + paper mode status |
| `POST` | `/invest` | Run full agent + save trade to DB |
| `GET` | `/history/{user_id}` | Past trades from PostgreSQL |
| `GET` | `/watchlist` | Live prices for 20 NSE stocks |
| `POST` | `/sip/setup` | Create monthly SIP schedule |
| `GET` | `/sip/{user_id}` | Get active SIP details |
| `DELETE` | `/sip/{user_id}` | Cancel active SIP |
| `GET` | `/market-mood` | Nifty50 + VIX market regime |
| `GET` | `/behavior/{user_id}` | Investor behavior profile |
| `GET` | `/funds` | Upstox account balance |
| `GET` | `/portfolio` | Current broker holdings |
| `GET` | `/verify-broker` | Test Upstox token validity |
| `GET` | `/advice/{symbol}` | BUY/HOLD/SELL for one stock |
| `GET` | `/advice-all` | Signals for all 20 stocks |
| `GET` | `/scenarios/{user_id}` | Bull / Base / Bear projections |
| `GET` | `/performance/{user_id}` | Agent accuracy + metrics |
| `GET` | `/rebalance-check/{user_id}` | Portfolio rebalance recommendation |
| `GET` | `/pnl/{user_id}` | Live P&L with stop-loss alerts ← NEW |
| `GET` | `/backtest/{symbol}` | Backtest single stock ← NEW |
| `GET` | `/backtest-portfolio/{user_id}` | Backtest full last portfolio ← NEW |
| `GET` | `/notify-mood` | Send market mood to Telegram ← NEW |

---

## Database Schema

Two tables auto-created on first run via SQLAlchemy:

```sql
-- Every investment the agent makes
trade_logs (
    id          UUID PRIMARY KEY,
    user_id     TEXT,
    budget      FLOAT,
    risk_level  TEXT,        -- conservative / moderate / aggressive
    allocation  JSON,        -- full holdings with shares, price, stop_loss
    explanation TEXT,        -- GPT-4o-mini generated 4-section report
    top_stocks  JSON,        -- ranked stock analysis data
    mode        TEXT,        -- paper / live
    created_at  TIMESTAMP
)

-- Monthly SIP automation config
sip_schedules (
    id          UUID PRIMARY KEY,
    user_id     TEXT,
    monthly_amt FLOAT,
    risk_level  TEXT,
    active      TEXT,        -- true / false
    created_at  TIMESTAMP
)
```

---

## How the Agent Works

```
User inputs: budget (e.g. ₹5000) + risk level (moderate)
                        ↓
        Fetch 6 months OHLCV for 15 stocks via yfinance
                        ↓
        Compute 6 technical indicators per stock:
        RSI (14-day) → MACD (12/26/9 EMA)
        → 200-day MA → Volume ratio
        → Momentum (20-day) → 52-week range
                        ↓
        Fetch news headlines (NewsAPI + Google News RSS)
        Send to GPT-4o-mini → sentiment score 0-100
                        ↓
        Final score = TA score (60%) + Sentiment (40%)
                        ↓
        Resolve signals per stock (autonomous.py):
        BUY / HOLD / SELL + confidence % + stop-loss level
                        ↓
        Dynamic allocation:
          Skip all SELL signal stocks
          Confidence-weighted position sizing
          Max 35% per stock (moderate risk)
          Reserve 10–20% cash based on VIX level
          Park leftover in LIQUIDBEES ETF
                        ↓
        Generate 4-section AI report via GPT-4o-mini
                        ↓
        Save full trade to PostgreSQL (trade_logs table)
                        ↓
        Execute via Upstox API (paper or live mode)
                        ↓
        Send Telegram notification with trade summary  ← NEW
                        ↓
        Bull/Base/Bear scenario simulation             ← NEW
```

---

## New Features Added

### 1. Real-time P&L Tracker
- Fetches live current prices for all holdings
- Calculates profit/loss per position in ₹ and %
- Detects stop-loss breaches and highlights them
- Shows overall portfolio return vs invested amount
- Accessible via `GET /pnl/{user_id}` or P&L button on dashboard

### 2. Telegram Notifications
- Sends trade execution summary to your Telegram after every investment
- Sends market mood alerts (BULLISH/BEARISH changes)
- Sends stop-loss breach warnings per position
- Setup: create bot via @BotFather, add token to .env
- Requires: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in .env

### 3. Historical Backtesting
- Tests how any stock performed between two dates
- Backtests your full last portfolio from trade date to today
- Returns buy price, sell price, shares, invested, current value, P&L %
- Accessible via `/backtest/{symbol}` and `/backtest-portfolio/{user_id}`

### 4. Auto Token Check
- Scheduler checks Upstox token validity at 8:45 AM every morning
- Sends Telegram alert if token has expired before market opens
- Prevents failed trades due to stale tokens
- Lives in `agent/token_manager.py`

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 15 with pgAdmin 4
- Upstox demat account (free, needs PAN + Aadhaar)
- OpenAI API account with credits
- Telegram account (for notifications — optional)

### Step 1 — Clone the repo

```bash
git clone https://github.com/Adi77189/stock-agent.git
cd stock-agent
```

### Step 2 — Create virtual environment

```bash
python -m venv stockAgent

# Windows
stockAgent\Scripts\activate

# Mac/Linux
source stockAgent/bin/activate
```

### Step 3 — Install Python packages

```bash
pip install -r requirements.txt
```

### Step 4 — Install frontend packages

```bash
cd frontend
npm install
cd ..
```

### Step 5 — Create .env in project root

```env
# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# NewsAPI — free at newsapi.org
NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Upstox broker
UPSTOX_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
UPSTOX_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
UPSTOX_ACCESS_TOKEN=eyJ0eXAiOiJKV1Qi...

# PostgreSQL
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/stockagent

# Telegram (optional — for alerts)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# App config
PAPER_MODE=true
ENVIRONMENT=development
```

### Step 6 — Create PostgreSQL database

Open pgAdmin 4 → Servers → PostgreSQL → right-click **Databases** → Create → Database → name: `stockagent` → Save.

```bash
python backend/database.py
# Expected: Database tables created successfully
```

### Step 7 — Start backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Expected:
```
Database tables created successfully
Database ready
[Scheduler] Started — SIP runs on 1st of every month at 9:15 AM
INFO: Application startup complete.
```

### Step 8 — Start frontend

```bash
cd frontend
npm start
# Opens automatically at http://localhost:3000
```

---

## API Keys — Where to Get Them

| Key | URL | Cost | Notes |
|---|---|---|---|
| `OPENAI_API_KEY` | platform.openai.com/api-keys | ~₹0.33/run | Needs credit card |
| `NEWS_API_KEY` | newsapi.org/register | Free | 100 req/day on free tier |
| `UPSTOX_API_KEY` | developer.upstox.com | Free | Needs demat account |
| `UPSTOX_ACCESS_TOKEN` | Run `refresh_token.py` | Free | Expires every 24 hours |
| `DATABASE_URL` | Local PostgreSQL | Free | pgAdmin install |
| `TELEGRAM_BOT_TOKEN` | @BotFather on Telegram | Free | Optional — for alerts |

**Getting Upstox API credentials:**
1. Open demat account at upstox.com
2. Go to developer.upstox.com → sign in → Create New App
3. App name: `stock-agent` | Redirect URL: `http://127.0.0.1:8000/callback`
4. Copy `API Key` and `Secret Key` to `.env`
5. Run `python refresh_token.py` each morning to get `UPSTOX_ACCESS_TOKEN`

**Getting Telegram bot:**
1. Open Telegram → search `@BotFather` → send `/newbot`
2. Give it a name → copy the token to `.env`
3. Send any message to your bot
4. Visit `https://api.telegram.org/bot{TOKEN}/getUpdates` → copy `chat.id`

---

## Daily Token Refresh

Upstox access token expires every 24 hours (SEBI mandate). Run each morning:

```bash
python refresh_token.py
```

Token validator also runs automatically at 8:45 AM and sends a Telegram alert if expired.

---

## Switching to Live Trading

```bash
# 1. Refresh token
python refresh_token.py

# 2. Set live mode in .env
PAPER_MODE=false

# 3. Restart backend
uvicorn backend.main:app --reload --port 8000
```

On dashboard: flip **Paper Mode** toggle → button turns red → click **Analyze** → confirm popup → real NSE market orders placed via Upstox.

---

## Test Each Module

```bash
# Live prices — should show 20 stocks, no NaN
python -m agent.tools.market_data

# Technical indicators
python -m agent.tools.technical

# Sentiment scoring (needs OPENAI_API_KEY)
python -m agent.tools.sentiment

# Market mood — Nifty + VIX
python -m agent.tools.market_mood

# Budget allocation
python -m agent.allocator

# Autonomous system + scenario simulation
python -m agent.autonomous

# Full agent end-to-end (~45 seconds)
python -m agent.orchestrator

# Broker connection
python -m agent.tools.broker

# Backtesting
python -m agent.tools.backtest

# P&L tracker
python -m agent.tools.pnl_tracker

# Telegram test
python -m agent.notifications
```

---

## Verify All Keys Loaded

```bash
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
keys = ['OPENAI_API_KEY','NEWS_API_KEY',
        'UPSTOX_API_KEY','UPSTOX_SECRET',
        'UPSTOX_ACCESS_TOKEN','DATABASE_URL',
        'TELEGRAM_BOT_TOKEN','PAPER_MODE']
for k in keys:
    v = os.getenv(k)
    print(f'  {\"OK\" if v else \"MISSING\"}  {k}')
"
```

---

## What Makes This Different

| Feature | Groww | Smallcase | Zerodha | This Project |
|---|---|---|---|---|
| AI stock selection | No | No | No | Yes |
| Explains every decision | No | No | No | Yes |
| Auto-executes trades | No | No | No | Yes |
| Market mood detection | No | No | No | Yes |
| Stop-loss per position | No | No | Manual | Automatic |
| Real-time P&L tracking | No | No | No | Yes |
| Telegram trade alerts | No | No | No | Yes |
| Historical backtesting | No | No | No | Yes |
| Behavioral coaching | No | No | No | Yes |
| Bull/Bear scenario sim | No | No | No | Yes |
| Intelligent SIP | Basic | Basic | Basic | AI-driven |
| Rebalance alerts | No | No | No | Yes |

---

## Risk Management

- Max 35% in any single stock (moderate), 25% (conservative), 50% (aggressive)
- Cash reserve: 10% neutral, 15% cautious, 20% bearish market
- Skips all SELL-signal stocks during allocation
- Stop-loss: 5% below entry (low volatility), 7% (high volatility)
- Scenario projections: 3 cases over 6-month horizon
- VIX-aware: increases reserve automatically when VIX > 20
- Real-time breach detection via P&L tracker with instant Telegram alert

---

## Known Limitations

- yfinance data is ~15 minutes delayed (free tier)
- Upstox token requires manual daily refresh (SEBI rule) — auto-check added but manual login still needed
- NewsAPI free plan works on localhost only, not on deployed servers
- Agent learning improves with more trade history (10+ trades recommended)
- Live trading requires active SEBI-registered Upstox demat account

---

## Future Roadmap

- [x] Real-time P&L tracking with stop-loss monitoring
- [x] Telegram trade execution alerts
- [x] Historical backtesting engine
- [x] Auto token validity check
- [ ] Full auto Upstox token refresh (no manual step)
- [ ] JWT multi-user authentication
- [ ] Docker + cloud deployment (AWS / Railway)
- [ ] F&O options signal generation
- [ ] Backtesting dashboard with equity curves in React
- [ ] Mobile app (React Native)

---

## License

MIT — free to use, modify, and distribute with attribution.

---

## Author

**Aditya Singh Bhadauria** — AI/ML Engineer & Full Stack Developer

Built end-to-end using Python, FastAPI, React, PostgreSQL, and OpenAI API.

- GitHub: [github.com/Adi77189](https://github.com/Adi77189)
- LinkedIn: [linkedin.com/in/aditya-bhadauria-9b8082302](https://www.linkedin.com/in/aditya-bhadauria-9b8082302/)
- Email: adityabhadauria1904@gmail.com

> *"Groww shows you stocks. Zerodha gives you tools. This agent makes the decision, explains the reasoning, executes the trade, and learns from outcomes — automatically."*