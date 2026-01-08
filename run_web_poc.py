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
import time
import os
import sys

# Ustawienie ścieżek
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config_manager import ConfigManager
from agents.browser_bot import BrowserBot
from sensors.vision import VisionSensor
from sensors.web_collector import WebMarketCollector

def main():
    print("=== PERCEPTRON WEB COLLECTOR PoC ===")
    print("Inicjalizacja modułów...")
    
    cfg = ConfigManager()
    
    # Sprawdzenie czy jest jakakolwiek konfiguracja
    if not cfg.get("WEB_INDICATOR_A", "tab_x"):
        print("\n[UWAGA] Wygląda na to, że nie przeprowadzono jeszcze kalibracji (brak WEB_INDICATOR_A).")
        print("Skrypt pominie brakujące wskaźniki i wypisze 'MISSING_CONFIG'.")
        print("Aby to naprawić, uruchom main.py -> Kalibracja -> WEB INDICATORS.\n")
    
    bot = BrowserBot(cfg)
    vision = VisionSensor(cfg)
    collector = WebMarketCollector(cfg, vision)
    
    # Wymuś włączenie na czas testu (TYLKO W PAMIĘCI - nie nadpisuje pliku .ini)
    cfg.set_temp('SYSTEM', 'web_scraping_txt', 'True')
    cfg.set_temp('SYSTEM', 'web_scraping_ss', 'True')
    
    print("Rozpoczynanie cyklu zbierania danych (5 sekund na przełączenie okna)...")
    time.sleep(5)
    
    report, images = collector.collect_data(bot)
    
    print("\n\n=== RAPORT KOŃCOWY ===")
    print(report)
    print("\n=== OBRAZKI ===")
    for img in images:
        print(f"- {img}")
        
    print("\nZapisano dane do: market_data_web.json")
    print("Naciśnij Enter aby zakończyć.")
    input()

if __name__ == "__main__":
    main()
