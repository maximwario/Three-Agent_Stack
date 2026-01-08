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
import json
import time
from utils.logger import AgentLogger

class SignalMessenger:
    def __init__(self, config_manager):
        self.cfg = config_manager
        self.log = AgentLogger("SIGNAL")
        self.cli_path = self.cfg.get('SIGNAL', 'cli_path', 'signal-cli')
        self.account = self.cfg.get('SIGNAL', 'account_phone', '')
        self.recipient = self.cfg.get('SIGNAL', 'recipient_phone', '')

    def normalize_phone(self, phone):
        """Czyści numer telefonu dla pewnego porównania."""
        if not phone: return ""
        return "".join([c for c in str(phone) if c.isdigit() or c == '+'])

    def receive_latest(self):
        """Pobiera wiadomości i rozpoznaje dyrektywy Note-to-Self."""
        if not self.account: return ""
        collected_msgs = []
        my_clean = self.normalize_phone(self.recipient)
        bot_clean = self.normalize_phone(self.account)
        
        try:
            cmd = [self.cli_path, "-u", self.account, "-o", "json", "receive"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, encoding='utf-8')
            
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        env = data.get('envelope', {})
                        ts_raw = env.get('timestamp', data.get('timestamp', 0))
                        ts = time.strftime('%H:%M', time.localtime(ts_raw/1000))

                        # 1. Standardowa wiadomość (dataMessage)
                        if 'dataMessage' in env:
                            src = self.normalize_phone(env.get('source', ''))
                            txt = env['dataMessage'].get('message')
                            if txt and (src == my_clean or src == bot_clean):
                                collected_msgs.append(f"[{ts}] USER: {txt}")

                        # 2. Wiadomość synchronizowana (syncMessage - Twoje notatki)
                        sync = env.get('syncMessage') or data.get('syncMessage')
                        if sync and 'sentMessage' in sync:
                            sent = sync['sentMessage']
                            dest = self.normalize_phone(sent.get('destination', ''))
                            txt = sent.get('message')
                            if txt and (dest == my_clean or dest == bot_clean):
                                collected_msgs.append(f"[{ts}] USER (NoteToSelf): {txt}")

                    except json.JSONDecodeError: continue
        except Exception as e:
            self.log.log(f"Błąd Signal Receive: {e}", "ERROR")
            
        return "\n".join(collected_msgs) if collected_msgs else ""

    def send(self, message):
        """Wysyła wiadomość do użytkownika."""
        if not self.account or not self.recipient: return False
        try:
            cmd = [self.cli_path, "-u", self.account, "send", "-m", message, self.recipient]
            subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
            return True
        except Exception as e:
            self.log.log(f"Błąd wysyłania Signal: {e}", "WARN")
            return False