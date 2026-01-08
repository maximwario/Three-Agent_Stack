# -*- coding: utf-8 -*-
# Copyright (C) 2026 plaisant
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from core.state_orchestrator import StateOrchestrator
from config_manager import ConfigManager
import time
import sys

# Force UTF-8 for stdout/stderr to avoid print errors in console
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def verify_signal_emojis():
    print("=== WERYFIKACJA SYGNAŁU (EMOJI TEST) ===")
    cfg = ConfigManager()
    
    # Check if config is loaded
    print(f"CLI Path: {cfg.get('SIGNAL', 'cli_path')}")
    print(f"Recipient: {cfg.get('SIGNAL', 'recipient_phone')}")

    orch = StateOrchestrator(cfg)
    
    # Exact message structure from handle_harvest with Emojis
    msg = (
        f"📊 HUD UPDATE TEST\n"
        f"BTC: 95000.00\n"
        f"BN PNL: 15.5$ (LONG)\n"
        f"TV PNL: -5.0$ (BTCUSDT)\n"
        f"Faza: HARVEST DONE 🚀"
    )
    
    print(f"Wysylanie wiadomosci Z EMOJI:\n{msg}")
    print("-" * 20)
    
    # We call the internal method
    orch._send_signal(msg)
    
    print("Test zakonczony. Sprawdz telefon.")

if __name__ == "__main__":
    verify_signal_emojis()
