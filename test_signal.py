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
    
    print("--- BEZPIECZNE LINKOWANIE SIGNAL (v2) ---")
    print(f"Uruchamiam: {cli_path}")
    
    # Uruchomienie linkowania
    cmd = [cli_path, "link", "-n", "EPIC_AGENT"]
    
    try:
        # Uruchamiamy proces
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        print("\nCzekam na link parowania... (To może potrwać do 10-15 sekund)")
        
        uri = None
        # Czytamy wyjście linia po linii
        for line in process.stdout:
            clean_line = line.strip()
            # Szukamy dowolnego linku sgnl://
            if "sgnl://" in clean_line:
                start_idx = clean_line.find("sgnl://")
                uri = clean_line[start_idx:].strip()
                break
            # Wyświetlamy status, żebyś wiedział co się dzieje
            if clean_line:
                print(f"Signal-CLI: {clean_line}")

        if uri:
            print(f"\n✅ Link przechwycony!")
            print(f"URI: {uri[:60]}...")
            
            # Generowanie QR
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(uri)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Ścieżka do pliku w folderze bota
            script_dir = os.path.dirname(os.path.abspath(__file__))
            temp_path = os.path.join(script_dir, "signal_link_qr.png")
            
            img.save(temp_path)
            
            print(f"\n🚀 KOD QR ZAPISANY: {temp_path}")
            print("\n--- INSTRUKCJA ---")
            print("1. Otwórz Signal w telefonie.")
            print("2. Ustawienia -> Powiązane urządzenia -> Dodaj (+).")
            print("3. Zeskanuj kod z obrazka, który teraz otworzę.")
            
            # Otwarcie obrazka
            try:
                os.startfile(temp_path)
            except:
                print("⚠️ Nie udało się otworzyć automatycznie. Znajdź plik signal_link_qr.png w folderze bota.")

            print("\nCzekam... NIE ZAMYKAJ tego okna, dopóki telefon nie potwierdzi połączenia.")
            input("\n👉 NACIŚNIJ [ENTER] PO ZESKANOWANIU, ABY ZAKOŃCZYĆ...")
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print("✅ Plik tymczasowy usunięty. Teraz uruchom test_signal.py")
        else:
            print("\n❌ BŁĄD: Nie znaleziono linku w wyjściu programu.")
            
    except Exception as e:
        print(f"\n❌ BŁĄD KRYTYCZNY: {e}")

if __name__ == "__main__":
    generate_local_signal_qr()