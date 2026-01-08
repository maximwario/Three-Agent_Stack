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
import configparser
import pyautogui
import time
import os
import sys

CONFIG_FILE = "intel_config_v33.ini"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Brak pliku {CONFIG_FILE}!")
        return None
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def test_coordinate(config, section, key_base):
    x_key = f"{key_base}_x"
    y_key = f"{key_base}_y"
    
    if not config.has_option(section, x_key) or not config.has_option(section, y_key):
        print(f"⚠️ Brak klucza {key_base} w sekcji {section}!")
        return

    x = config.getint(section, x_key)
    y = config.getint(section, y_key)
    
    print(f"\n🎯 TESTOWANIE: {section} -> {key_base}")
    print(f"   Koordynaty: X={x}, Y={y}")
    print("   Ruszam myszką w to miejsce za 3 sekundy... (Nie ruszaj myszką!)")
    time.sleep(1)
    print("   2...")
    time.sleep(1)
    print("   1...")
    time.sleep(1)
    
    try:
        # Powolny ruch żeby użytkownik widział gdzie jedzie
        pyautogui.moveTo(x, y, duration=2.0)
        print("✅ Dotarłem do celu! Sprawdź czy kursor jest nad właściwym elementem.")
    except Exception as e:
        print(f"❌ Błąd ruchu myszką: {e}")

def main():
    print("=== TESTER KOORDYNATÓW EPIC AGENT ===")
    config = load_config()
    if not config: return

    # Lista kluczowych elementów do sprawdzenia (z naciskiem na te problematyczne)
    keys_to_check = [
        ("BINANCE_CONTROLS", "bin_confirm"),
        ("BINANCE_CONTROLS", "bin_cancel_all"),
        ("BINANCE_CONTROLS", "bin_close_all"),
        ("BINANCE_CONTROLS", "bin_tpsl"),
        ("BINANCE_CONTROLS", "bin_modal_confirm"),
        ("BINANCE_INTERNAL", "bn_sub_orders"),
        ("BINANCE_INTERNAL", "bn_sub_positions")
    ]

    while True:
        print("\nWybierz element do przetestowania:")
        for i, (sec, key) in enumerate(keys_to_check):
            print(f"{i+1}. {key} (Sekcja: {sec})")
        print("0. Wyjście")
        
        choice = input("\nTwój wybór (numer): ").strip()
        
        if choice == '0':
            print("👋 Do widzenia.")
            break
            
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(keys_to_check):
                sec, key = keys_to_check[idx]
                test_coordinate(config, sec, key)
                input("\n[Naciśnij ENTER aby kontynuować]")
            else:
                print("❌ Nieprawidłowy numer.")
        except ValueError:
            print("❌ Wpisz liczbę.")

if __name__ == "__main__":
    main()
