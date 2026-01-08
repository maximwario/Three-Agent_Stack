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

def verify_signal():
    print("=== WERYFIKACJA SYGNAŁU (Metoda plikowa) ===")
    cfg = ConfigManager()
    
    # Check if config is loaded
    print(f"CLI Path: {cfg.get('SIGNAL', 'cli_path')}")
    print(f"Recipient: {cfg.get('SIGNAL', 'recipient_phone')}")

    orch = StateOrchestrator(cfg)
    
    msg = f"TEST WERYFIKACYJNY: {time.strftime('%H:%M:%S')} - Jezeli to czytasz, metoda plikowa dziala!"
    
    print(f"Wysylanie wiadomosci: '{msg}'")
    orch._send_signal(msg)
    print("Wyslano polecenie byc moze. Sprawdz telefon.")

if __name__ == "__main__":
    verify_signal()
