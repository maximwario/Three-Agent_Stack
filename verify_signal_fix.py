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
import sys
import os
import time
import json
import subprocess
from unittest.mock import MagicMock, patch

# Add parent dir to path
sys.path.append(os.getcwd())

from config_manager import ConfigManager
from utils.signal_messenger import SignalMessenger

def test_parsing_logic():
    print("--- TEST: Logika PArsowania (Mock) ---")
    cfg = ConfigManager()
    
    # Mock config to ensure typical numbers
    cfg.get = MagicMock(side_effect=lambda s, k, f=None: 
        "+33 6 04 15 86 75" if k == 'account_phone' or k == 'recipient_phone' else f
    )
    
    messenger = SignalMessenger(cfg)
    
    # Mock subprocess output with mixed formats
    mock_stdout = """
{"envelope":{"source":"+xxXXXxxXXxx","relay":"null","timestamp":1700000000000,"dataMessage":{"timestamp":1700000000000,"message":"Test Message 1 (Clean Source)","expiresInSeconds":0,"viewOnce":false},"syncMessage":{"sentMessage":{"timestamp":1700000000000,"message":"My Sent Message","destination":"+33604158675","expiresInSeconds":0,"viewOnce":false}}}}
{"envelope":{"source":"+XX XXX XXX XXX","relay":"null","timestamp":1700000001000,"dataMessage":{"timestamp":1700000001000,"message":"Test Message 2 (Spaced Source)","expiresInSeconds":0,"viewOnce":false}}}
{"envelope":{"source":"+123456789","relay":"null","timestamp":1700000002000,"dataMessage":{"timestamp":1700000002000,"message":"Spam Message","expiresInSeconds":0,"viewOnce":false}}}
{"envelope":{"source":"+xxXXXxxXXxx","relay":"null","timestamp":1700000003000},"syncMessage":{"sentMessage":{"timestamp":1700000003000,"message":"Sync Note To Self","destination":"+xxXXXxxXXxx","expiresInSeconds":0,"viewOnce":false}}}
    """
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = mock_stdout
        mock_run.return_value.returncode = 0
        
        result = messenger.receive_latest()
        
        print("\n[WYNIK PARSOWANIA]:")
        print(result)
        
        # Weryfikacja
        assert "Test Message 1" in result, "Nie wykryto wiadomości 1 (czysty numer)"
        assert "Test Message 2" in result, "Nie wykryto wiadomości 2 (numer ze spacjami)"
        assert "Spam Message" not in result, "Błędnie wykryto spam od obcego numeru"
        assert "Sync Note To Self" in result, "Nie wykryto wiadomości typu sync/note-to-self"
        print("\n[SUKCES] Logika normalizacji numerów działa poprawnie.")

def test_real_connection():
    print("\n--- LIVE SIGNAL MONITOR (DIAGNOSTIC MODE) ---")
    cfg = ConfigManager()
    messenger = SignalMessenger(cfg)
    
    # 0. DIAGNOSTYKA WSTĘPNA
    print(f"[DIAG] Signal Path: {messenger.cli_path}")
    print(f"[DIAG] Account: {messenger.account}")
    
    # Test wersji
    try:
        ver_cmd = [messenger.cli_path, "--version"]
        v_res = subprocess.run(ver_cmd, capture_output=True, text=True)
        print(f"[DIAG] Version Check: {v_res.stdout.strip()} (Err: {v_res.stderr.strip()})")
    except Exception as e:
        print(f"[DIAG] Version Check FAIL: {e}")

    print("\n--- Rozpoczynam pętlę nasłuchu (Ctrl+C to stop) ---")
    print("Wysyłaj wiadomości teraz. Czekam...")
    
    try:
        while True:
            # Używamy subprocess bezpośrednio tutaj, żeby widzieć co się dzieje "pod maską"
            # ponieważ receive_latest konsumuje wyjście i jeśli coś pójdzie nie tak w parsowaniu, to tego nie zobaczymy.
            # Zamiast tego zrobimy trick: wywołamy receive_latest, ale wcześniej ustawimy loggerowi printowanie wszystkiego.
            
            # Jednak receive_latest ma w sobie:
            # self.log.log(f"RAW SIGNAL DATA: {result.stdout[:200]}...", "DEBUG")
            
            # Więc jeśli logger działa, powinno być widać.
            # Może user nie widzi DEBUG logów? Klasa loggera ma domyślnie print.
            
            # Zróbmy więc tak: wywołamy receive --json RĘCZNIE w pętli testowej (tak jak było wcześniej),
            # ale tym razem użyjemy poprawionej logiki parsowania z messenger.normalize_phone itd.
            
            cmd = [messenger.cli_path, "-u", messenger.account, "-o", "json", "receive"]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            if res.stderr and "WARN" not in res.stderr and "INFO" not in res.stderr:
                 print(f"[STDERR]: {res.stderr.strip()}")
            
            if res.stdout.strip():
                # print(f"\n[RAW DATA OUTPUT]:\n{res.stdout.strip()}") # Suppressed raw output
                
                # Teraz parsujemy to RĘCZNIE używając logiki którą znamy
                # Skopiowane z signal_messenger.py dla pewności widoku w teście
                
                my_clean = messenger.normalize_phone(messenger.recipient)
                
                for line in res.stdout.strip().split('\n'):
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        msg_found = False
                        
                        # Case 1: dataMessage
                        if 'envelope' in data:
                            env = data.get('envelope', {})
                            src = env.get('source', '')
                            clean_src = messenger.normalize_phone(src)
                            
                            if 'dataMessage' in env:
                                txt = env['dataMessage'].get('message')
                                if txt:
                                    print(f" >> [DATA MSG] Od: {src} -> {txt}")
                                    msg_found = True

                            # NEW: Check syncMessage inside envelope
                            if 'syncMessage' in env:
                                sync = env.get('syncMessage', {})
                                sent = sync.get('sentMessage', {})
                                dest = sent.get('destination', '')
                                txt = sent.get('message')
                                if txt:
                                    print(f" >> [SYNC MSG] Do: {dest} -> {txt}")
                                    msg_found = True
                        
                        # Case 2: syncMessage (Note to self) - Top level
                        if not msg_found and 'syncMessage' in data:
                            sync = data.get('syncMessage', {})
                            sent = sync.get('sentMessage', {})
                            dest = sent.get('destination', '')
                            clean_dest = messenger.normalize_phone(dest)
                            txt = sent.get('message')
                            
                            if txt:
                                print(f" >> [SYNC MSG] Do: {dest} -> {txt}")
                                msg_found = True
                                
                        if not msg_found:
                             print(f" >> [INFO] Inny typ komunikatu: {list(data.keys())}")
                             print(f" [RAW]: {line}")

                    except Exception as e:
                        print(f" >> [ERROR] Błąd parsowania JSON: {e}")
            else:
                 print(".", end="", flush=True)

            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n[STOP] Zatrzymano monitorowanie.")
    except Exception as e:
        print(f"\n[BŁĄD KRYTYCZNY] {e}")

if __name__ == "__main__":
    test_parsing_logic()
    test_real_connection()

