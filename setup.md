# Setup Guide for EPIC_AGENT_v0_9_2

This guide walks you through setting up and running the Three-Agent Stack trading bot on your local machine. It's designed for Windows (primary testing env), but adaptable to Linux/Mac with minor tweaks. Focus: Quick start with demo mode for safety.

## Prerequisites
- **OS**: Windows 10+ (for pyautogui stability; Linux/Mac OK but test GUI).
- **Python**: 3.10+ (download from [python.org](https://www.python.org/)).
- **Browser**: Chrome/Edge (open with tabs: Binance, TradingView, Coinglass, AI chats like Grok/Gemini).
- **Accounts**: Binance demo (futures), Coinglass API key (free tier OK via [reflink](https://www.coinglass.com/?ref_code=QXRIVG)).
- **Signal-CLI**: For notifications (optional but recommended).
- AI Subscription: Gemini Advanced (paid) is required. You must upload all project files to the Gemini context window before starting for the model to understand the full logic.
Display: An active screen is required (no headless mode) because the VISION module scrapes data via screen snapshots.

## Step 1: Clone the Repository
```bash
git clone https://github.com/[your_username]/three-agent_stack.git
cd three-agent_stack
```

## Step 2: Install Dependencies
Use a virtual env for isolation:
```bash
python -m venv venv
venv\Scripts\activate  # Windows; source venv/bin/activate on Linux/Mac
pip install -r requirements.txt
```

Requirements include: pyautogui, pyperclip, pynput, requests, ccxt, configparser.

## Step 3: Setup Signal-CLI (Notifications)
1. Download from [Signal.org](https://signal.org/en/download/) (v0.13+).
2. Install Java (if needed for CLI).
3. Config in `intel_config_v33.ini`:
   ```
   [SIGNAL]
   cli_path = C:\path\to\signal-cli.bat
   account_phone = +xxxxxxxxxxx  # Your Signal number
   recipient_phone = +xxxxxxxxxxx  # Same for note-to-self
   ```
4. Link device: Run `python setup_signal_qr.py` – scan QR with phone app.
5. Test: `python test_signal.py` – check phone for message.

## Step 4: Configure the Bot
Edit `intel_config_v33.ini`:
- **[SYSTEM]**: Set `loop_interval_min = 18`, `agent_3_enabled = False` (for demo – enable later).
- **[SECRETS]**: Add Coinglass API key.
- **[TIMING]**: Adjust waits (e.g., gemini_think=80s).
- **[BINANCE_CONTROLS] etc.**: For A3 (Agent_3) on/off to function properly:
1. Ensure you are on the Binance FUTURES tab.
2. Enable/check the TP/SL button.
3. In "Cancel all orders", select "All" from the dropdown (options: "All", "LIMIT", "Stop-Limit"). Note: There is no default selection, but Binance remembers the choice after the first manual selection.
- [Visual guide for manual setting the "ALL"](https://github.com/maximwario/Three-Agent_Stack/blob/main/docs/button_cancell_all.jpg) button in order cancell button "Anuluc wszystkie zlecenia" ("Cancell_All_orders").

- **[BITMEX_SETUP]**: Bitmex Configuration:
1. Open the Bitmex BTCUSD/XBTUSD chart.
2. In the Orderbook widget, set the Grouping to 200.0 or 500.0. This allows the bot to see "Whale Walls" effectively.
[Visual guide for](https://github.com/maximwario/Three-Agent_Stack/blob/main/docs/Orderbook_200_500.JPG) Bitmex Orderbook Grouping 200.0/500.0.

- **[LIST_WEBSITE]**: The initial config works when: chrome > AI (tab) > open 15 websites. Log in to the coinglass website. You can use [my referal link](https://www.coinglass.com/?ref_code=QXRIVG) if you like.

1. https://gemini.google.com/app/
2. https://www.binance.com/en/futures/BTCUSDT
3. https://www.tradingview.com/chart
4. https://www.bitmex.com/app/trade/XBTUSD
5. https://legend.coinglass.com/chart
6. https://grok.com/
7. https://copilot.microsoft.com/
8. https://chat.deepseek.com/
9. https://lmarena.ai/ (Qwen3 Max)
10. https://www.coinglass.com/BitcoinOpenInterest
11. https://www.coinglass.com/LongShortRatio
12. https://www.coinglass.com/LiquidationData
13. https://www.coinglass.com/pro/i/RsiHeatMap
14. https://www.coinglass.com/large-orderbook-statistics
15. https://www.coinglass.com/FundingRate

## Step 5: Calibration (Works on initial config_v33.ini)
Run `python main.py` → Menu → "Kalibracja".
- Hover over tabs/buttons (e.g., Binance tab, copy btn in AI chats).
- Press F2 to capture coords/images – saves to config/assets/.
- Test: `python coord_tester.py` – verify clicks.

## Step 6: Run the Bot
```bash
python main.py
```
- HUD appears: Monitor status, PnL.
- Cycle starts: Seed AI → Harvest data → Decide → Execute (if enabled).
- Stop: F3 (emergency) or menu.

## Troubleshooting
- **No Clicks?** Recalibrate – screen res changed?
- **AI Silent?** Check clipboard_lag in config; restart browser.
- **Errors?** See system_log.txt; report in issues with snippet.
- **Demo Mismatch?** Binance demo lags – use real price via API for tests.

## Tips for First Run
- Start with agent_3_enabled=False (no real trades).
- Monitor logs: `tail -f system_log.txt`.
- Custom Prompts: Edit dynamic_prompts.json for AI roles.

Enjoy your AGI trader!
