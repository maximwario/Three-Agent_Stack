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
from config_manager import ConfigManager
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def test_multi_m():
    print("=== TEST MULTI -m ARGUMENTS ===")
    cfg = ConfigManager()
    cli_path = cfg.get('SIGNAL', 'cli_path')
    account = cfg.get('SIGNAL', 'account_phone')
    recipient = cfg.get('SIGNAL', 'recipient_phone')
    
    if not cli_path:
        print("No Config found")
        return

    cli_dir = os.path.dirname(cli_path)
    
    # Try sending: -m "Line 1" -m "Line 2"
    cmd_list = [
        cli_path, 
        "-u", account, 
        "send", 
        "-m", "Line 1 📊", 
        "-m", "Line 2 🚀", 
        recipient
    ]
    
    print(f"Executing: {cmd_list}")
    
    try:
        res = subprocess.run(
            cmd_list, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            cwd=cli_dir
        )
        if res.returncode == 0:
            print("SUCCESS! Check phone for 2 lines.")
        else:
            print(f"FAIL: {res.stderr}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_multi_m()
