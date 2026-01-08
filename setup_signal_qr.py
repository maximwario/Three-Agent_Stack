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
import subprocess
import qrcode
import sys
import os
import time
from config_manager import ConfigManager

def generate_local_signal_qr():
    cfg = ConfigManager()
    cli_path = cfg.get('SIGNAL', 'cli_path')
    
    print("--- BEZPIECZNE LINKOWANIE SIGNAL ---")
    print(f"Uruchamiam: {cli_path}")
    
    # 1. Uruchomienie komendy linkowania w trybie przechwytywania wyjścia
    # -n "EPIC_AGENT" to nazwa Twojego urządzenia widoczna w telefonie
    cmd = [cli_path, "link", "-n", "EPIC_AGENT"]
    
    try:
        # Uruchamiamy proces i czytamy go linia po linii
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print("\nCzekam na link parowania z Signal-CLI...")
        
        uri = None
        for line in process.stdout:
            # Szukamy linii zaczynającej się od sgnl://
            if "sgnl://linkout" in line:
                uri = line.strip()
                break
            print(f"Status: {line.strip()}")

        if uri:
            print("\n✅ Link przechwycony bezpiecznie!")
            print("Generuję kod QR lokalnie...")

            # 2. Tworzenie obiektu QR
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(uri)
            qr.make(fit=True)

            # 3. Tworzenie i wyświetlanie obrazu
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Zapisz tymczasowo i otwórz w systemowej przeglądarce zdjęć
            temp_path = "signal_link_qr.png"
            img.save(temp_path)
            
            print(f"\n🚀 KOD QR WYGENEROWANY: {os.path.abspath(temp_path)}")
            print("Zeskanuj go teraz telefonem: Signal -> Ustawienia -> Powiązane urządzenia -> Dodaj (+)")
            
            # Otwórz obrazek automatycznie (działa na Windows)
            os.startfile(temp_path)
            
            print("\nPo zeskanowaniu kod zostanie usunięty za 60 sekund dla bezpieczeństwa...")
            time.sleep(60)
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print("Plik tymczasowy usunięty.")
        else:
            print("\n❌ Nie udało się odnaleźć linku w wyjściu programu.")
            
    except Exception as e:
        print(f"\n❌ BŁĄD KRYTYCZNY: {e}")

if __name__ == "__main__":
    generate_local_signal_qr()