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
import os

class ConfigManager:
    def __init__(self, filename="intel_config_v33.ini"):
        self.filename = filename
        self.cfg = configparser.ConfigParser()
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            self._create_default()
        self.cfg.read(self.filename)
        
        # Auto-migration for new timing keys
        changed = False
        if 'TIMING' not in self.cfg:
             self.cfg['TIMING'] = {}
             changed = True
        
        # Auto-migration for Agent 3 switch
        if 'agent_3_enabled' not in self.cfg['SYSTEM']:
            self.cfg['SYSTEM']['agent_3_enabled'] = 'True'
            changed = True

        # Default values for granular timing (if missing in existing file)
        defaults = {
            'click_post_wait': '0.5',
            'scroll_step_wait': '0.05',
            'key_hotkey_wait': '0.3',
            'clipboard_copy_wait': '0.8',
            'clipboard_lag': '1.5',
            'clipboard_paste_wait': '1.5',
            'tab_switch_wait': '0.5',
            'page_load_wait': '1.0',
            'ai_wait_seconds': '120',
            'grok_wait': '150',
            'api_request_interval': '1.0'
        }
        
        for k, v in defaults.items():
            if k not in self.cfg['TIMING']:
                self.cfg['TIMING'][k] = v
                changed = True
        
        if changed:
            with open(self.filename, 'w') as f: self.cfg.write(f)

    def _create_default(self):
        self.cfg['SYSTEM'] = {
            'loop_interval_min': '30',
            'verify_pages': 'True',
            'do_screenshots': 'True'
        }
        # NOWA SEKCJA CZASOWA - Operacja Chronos
        self.cfg['TIMING'] = {
            'grok_wait': '150',      # Czas na myślenie Groka
            'copilot_wait': '60',    # Czas na myślenie Copilota
            'deepseek_wait': '180',  # DeepSeek R1 potrzebuje dużo czasu
            'qwen_wait': '60',
            'gemini_think': '120',   # Czas dla Gemini na syntezę
            'ai_wait_seconds': '120', # Globalny czas oczekiwania (jeśli nie specyficzny)
            'vision_load': '3.0',    # Czas na załadowanie strony (Bitmex/Coinglass)
            'clipboard_lag': '1.5',  # Czas dla PowerShella na wrzut obrazka
            'scroll_speed': '0.5',   # Przerwa między scrollami
            
            # --- GRANULAR TIMINGS (ms resolution possible) ---
            'click_post_wait': '0.5',      # Po kliknięciu standardowym
            'scroll_step_wait': '0.05',    # Między krokami scrolla
            'key_hotkey_wait': '0.3',      # Między klawiszami (Ctrl+A... Ctrl+C)
            'clipboard_copy_wait': '0.8',  # Po Ctrl+C
            'clipboard_paste_wait': '1.5', # Po Ctrl+V
            'tab_switch_wait': '0.5',      # Po zmianie karty
            'page_load_wait': '1.0',       # Po załadowaniu nowej strony
            'api_request_interval': '1.0'  # Minimalny odstęp między zapytaniami API
        }
        self.cfg['SECRETS'] = {
            'binance_key': 'WPISZ_TU',
            'binance_secret': 'WPISZ_TU',
            'coinglass_key': 'WPISZ_TU'
        }
        
        # Puste sekcje na koordynaty
        for sec in ["GEMINI_CONTROLS", "COINGLASS", "BITMEX", "TRADINGVIEW", "BINANCE_CONTROLS"]:
            self.cfg[sec] = {}
        for ai in ["AI_GROK", "AI_COPILOT", "AI_DEEPSEEK", "AI_QWEN"]:
            self.cfg[ai] = {}
        
        with open(self.filename, 'w') as f: self.cfg.write(f)

    def get(self, section, key, fallback=None):
        try: return self.cfg.get(section, key, fallback=fallback)
        except: return fallback

    def get_float(self, section, key, fallback=1.0):
        try: return float(self.cfg.get(section, key, fallback=fallback))
        except: return float(fallback)

    def set_and_save(self, section, key, value):
        if section not in self.cfg: self.cfg[section] = {}
        self.cfg[section][key] = str(value)
        with open(self.filename, 'w') as f: self.cfg.write(f)

    def set_temp(self, section, key, value):
        """Ustawia wartość tylko w pamięci (bez zapisu na dysk)"""
        if section not in self.cfg: self.cfg[section] = {}
        self.cfg[section][key] = str(value)