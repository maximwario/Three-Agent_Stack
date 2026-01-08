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
import os
from datetime import datetime

class AgentLogger:
    def __init__(self, component_name, log_file="system_log.txt"):
        self.component = component_name.upper()
        self.log_file = log_file
        
        # Upewnij się, że plik istnieje
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"=== SYSTEM LOG STARTED: {datetime.now()} ===\n")

    def log(self, message, level="INFO"):
        """
        Format: [HH:MM:SS] [COMPONENT] [LEVEL] Message
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] [{self.component}] [{level}] {message}"
        
        # 1. Wypisz na ekran (konsola/GUI capture)
        print(formatted_msg)
        
        # 2. Dopisz do pliku
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(formatted_msg + "\n")
        except Exception as e:
            print(f"!!! CRITICAL LOGGING ERROR: {e}")