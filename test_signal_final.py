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
import os
from config_manager import ConfigManager

def test_final_signal():
    cfg = ConfigManager()
    cli = cfg.get('SIGNAL', 'cli_path')
    user = cfg.get('SIGNAL', 'account_phone')
    recip = cfg.get('SIGNAL', 'recipient_phone')
    cli_dir = os.path.dirname(cli)
    
    msg = "🚀 TEST OSTATECZNY: Perceptron v0.8.9 komunikuje się poprawnie!"
    
    print(f"Próba wysyłki z folderu: {cli_dir}")
    try:
        res = subprocess.run([cli, "-u", user, "send", "-m", msg, recip], 
                             cwd=cli_dir, capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ SUKCES! Sprawdź telefon.")
        else:
            print(f"❌ BŁĄD: {res.stderr}")
    except Exception as e:
        print(f"❌ WYJĄTEK: {e}")

if __name__ == "__main__":
    test_final_signal()