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
import re
import json
import os
import logging
from datetime import datetime

# Plik stanu misji (Pamięć po restarcie)
STATUS_FILE = "mission_status.json"

def clean_json_payload(text):
    """
    Czyści tekst z Markdown i błędów JSON przed parsowaniem.
    Pochodzenie: Agent1_v8_4 (The Tank Strategy)
    """
    if not text:
        return ""
        
    # 1. Usuń znaczniki kodu Markdown ```json ... ```
    text = re.sub(r'```json', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```', '', text)
    
    # 2. Usuń przecinki przed zamknięciem nawiasu (trailing commas)
    text = re.sub(r',(\s*[\}\]])', r'\1', text)
    
    return text.strip()

def safe_parse_json(text_payload):
    """
    Próbuje sparsować JSON, zwraca dict lub None.
    NIE rzuca wyjątkami (Silent Fail z logiem).
    """
    cleaned = clean_json_payload(text_payload)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Fallback: Spróbuj sparsować jako słownik Python (np. single quotes)
        try:
            import ast
            return ast.literal_eval(cleaned)
        except:
            print(f"[JSON ERROR] {e}") 
            return None
    except Exception:
        return None

def save_mission_state(status="IDLE", active_position=False, last_action="NONE"):
    """Zapisuje stan misji do pliku, aby przetrwać restart."""
    data = {
        "timestamp": str(datetime.now()),
        "status": status,
        "active_position": active_position,
        "last_action": last_action
    }
    try:
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[STATE ERROR] Nie udało się zapisać stanu: {e}")

def load_mission_state():
    """Wczytuje stan misji."""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"status": "IDLE", "active_position": False, "last_action": "NONE"}