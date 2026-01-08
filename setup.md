# Setup Guide for EPIC_AGENT_v0_9_2

This guide walks you through setting up and running the Three-Agent Stack trading bot on your local machine. It's designed for Windows (primary testing env), but adaptable to Linux/Mac with minor tweaks. Focus: Quick start with demo mode for safety.

## Prerequisites
- **OS**: Windows 10+ (for pyautogui stability; Linux/Mac OK but test GUI).
- **Python**: 3.10+ (download from [python.org](https://www.python.org/)).
- **Browser**: Chrome/Edge (open with tabs: Binance, TradingView, Coinglass, AI chats like Grok/Gemini).
- **Accounts**: Binance demo (futures), Coinglass API key (free tier OK via [reflink](https://www.coinglass.com/?ref_code=QXRIVG)).
- **Signal-CLI**: For notifications (optional but recommended).

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
- **[BINANCE_CONTROLS] etc.**: Calibrate later.

## Step 5: Calibration (Must-Do!)
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
