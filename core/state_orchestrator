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
import threading
import json
import re
import pyautogui
import pyperclip
import subprocess
from enum import Enum, auto

# FIX ŚCIEŻEK
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.logger import AgentLogger
from utils.json_cleaner import save_mission_state, load_mission_state
from utils.parsers import DataSurgeon
from agents.strategist import StrategistAgent
from agents.tactician import TacticianLink
from agents.browser_bot import BrowserBot
from agents.consultants import IntelligenceCouncil
from sensors.vision import VisionSensor
from sensors.api_collector import MarketDataCollector
from sensors.web_collector import WebMarketCollector
from utils.signal_messenger import SignalMessenger

class BotState(Enum):
    BOOT = auto()
    SEED_COUNCIL = auto()
    DATA_HARVEST = auto()
    ACTIVE_WAIT = auto()
    COLLECT_COUNCIL = auto()
    SYNTHESIS = auto()
    DISPATCH = auto()
    EXECUTION = auto()
    COOLDOWN = auto()
    ERROR_RECOVERY = auto()

class StateOrchestrator:
    def __init__(self, config_manager, hud_ref=None):
        self.cfg = config_manager
        self.hud = hud_ref
        self.log = AgentLogger("STATE_ORCH")
        self.bot = BrowserBot(config_manager)
        
        # 0. PRZYWRACANIE KONTEKSTU (Z Twojej stabilnej wersji)
        self.boot_state = {}
        if os.path.exists("runtime_state.json"):
            try:
                with open("runtime_state.json", 'r') as f: 
                    self.boot_state = json.load(f)
                    self.log.log(f"Przywrócono stan z: {self.boot_state.get('last_update','?')}", "SYSTEM")
            except Exception as e:
                self.log.log(f"Nie wczytano stanu: {e}", "WARN")  # Teraz wiemy co jest błędem

        self.strategist = StrategistAgent(config_manager, boot_state=self.boot_state)
        self.council = IntelligenceCouncil(config_manager, self.strategist, self.hud)
        self.tactician = TacticianLink(config_manager, self.bot)
        self.vision = VisionSensor(config_manager)
        self.api_data = MarketDataCollector(config_manager)
        self.web_collector = WebMarketCollector(config_manager, self.vision)
        self.signal = SignalMessenger(config_manager)
        
        # Dane przepływu
        self.state = BotState.BOOT
        self.state_start_time = time.time()
        self.is_running = False
        self.mission_state = load_mission_state()
        self.full_report = ""
        self.image_paths = []
        self.raw_gemini_response = ""
        self.decisions_list = []
        self.cycle_start_time = 0
        self.last_error = "None"
        self.last_error = "None"
        self.btc_price = "N/A"
        self.user_message_queue = [] # Kolejka wiadomości od operatora

    def _send_signal(self, message):
        """Metoda z wymuszonym kodowaniem UTF-8 dla ikon."""
        cli_path = self.cfg.get('SIGNAL', 'cli_path')
        account = self.cfg.get('SIGNAL', 'account_phone', fallback="").strip()
        recipient = self.cfg.get('SIGNAL', 'recipient_phone', fallback="").strip()

        if not cli_path or not account or not recipient or not message:
            return

        try:
            bin_dir = os.path.dirname(cli_path) 
            base_dir = os.path.dirname(bin_dir) 
            lib_dir = os.path.join(base_dir, "lib")
            classpath = os.path.join(lib_dir, "*")
            
            cmd_list = [
                "java", 
                "-Dfile.encoding=UTF-8",  # <--- WYMUSZENIE UTF-8 DLA IKON
                "-cp", classpath, 
                "org.asamk.signal.Main", 
                "-u", account, 
                "send", 
                recipient,
                "-m", message
            ]
            
            res = subprocess.run(
                cmd_list, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=60, 
                cwd=base_dir
            )

            if res.returncode == 0 or "Sent message" in res.stdout:
                self.log.log(f"Signal wysłany do {recipient}")
            else:
                self.log.log(f"SIGNAL FAIL: {res.stderr[:100]}", "ERROR")
                    
        except Exception as e:
            self.log.log(f"Wyjątek Signal: {e}", "ERROR")

    def transition_to(self, next_state):
        duration = round(time.time() - self.state_start_time, 2)
        old_name = self.state.name if self.state else "NONE"
        self.log.log(f"FINISH: {old_name} ({duration}s)", "FSM")
        self.log.log(f"TRANSITION: {old_name} -> {next_state.name}", "FSM")
        self.state = next_state
        self.state_start_time = time.time()
        if self.hud and self.hud.is_alive(): self.hud.log_action(f"FSM: {next_state.name}")

    def _update_status(self, action_msg, countdown=0):
        if self.hud and self.hud.is_alive():
            self.hud.update_mission(self.state.name, countdown, action_msg)
        save_mission_state(self.state.name, self.mission_state.get('active_position', False), action_msg)

    def start_loop(self):
        if self.is_running: return
        self.is_running = True
        self.log.log("=== START FSM SYSTEM v0.9.4 ===")
        threading.Thread(target=self.run_fsm, daemon=True).start()

    def stop_loop(self):
        self.is_running = False
        self.log.log("ZATRZYMANO SYSTEM (FSM).")

    def run_fsm(self):
        while self.is_running:
            try:
                self.run_fsm_step()
            except Exception as e:
                self.last_error = str(e)
                self.log.log(f"Błąd krytyczny: {e}", "ERROR")
                pyautogui.keyUp('ctrl')
                self.transition_to(BotState.ERROR_RECOVERY)
                time.sleep(1)

    def run_fsm_step(self):
        if self.state == BotState.BOOT: self.handle_boot()
        elif self.state == BotState.SEED_COUNCIL: self.handle_seed()
        elif self.state == BotState.DATA_HARVEST: self.handle_harvest()
        elif self.state == BotState.ACTIVE_WAIT: self.handle_wait()
        elif self.state == BotState.COLLECT_COUNCIL: self.handle_collect_council()
        elif self.state == BotState.SYNTHESIS: self.handle_synthesis()
        elif self.state == BotState.DISPATCH: self.handle_dispatch()
        elif self.state == BotState.EXECUTION: self.handle_execution()
        elif self.state == BotState.COOLDOWN: self.handle_cooldown()
        elif self.state == BotState.ERROR_RECOVERY: self.handle_recovery()

    def handle_seed(self):
        self._update_status("Seeding AI Council")
        self.council.seed_questions() # Faza 1: Zasiew
        self.transition_to(BotState.DATA_HARVEST)

    def handle_harvest(self):
        """Zbiera dane i priorytetyzuje instrukcje z Signala."""
        self._update_status("Scraping Market Data & Signal")
        if self.hud: self.hud.update_mission("HARVESTING", 0, "DATA")
        
        # 1. Odbiór wiadomości (Konsolidacja kolejki)
        user_directives = ""
        try:
            last_minute_msg = self.signal.receive_latest()
            if last_minute_msg:
                self.user_message_queue.append(last_minute_msg)
            
            if self.user_message_queue:
                user_directives = "\n".join(self.user_message_queue)
                self.log.log(f">>> SKONSOLIDOWANO {len(self.user_message_queue)} WIADOMOŚCI OPERATORA <<<", "SYSTEM")
                self.user_message_queue = [] # Czyścimy po pobraniu
        except Exception as e:
            self.log.log(f"Błąd sprawdzania Signala: {e}", "WARN")

        # 2-4. BINANCE, TV, API (Pobieranie danych rynkowych)
        bn_data = {}
        clean_orders = "No Active Orders"
        tv_data = {}

        if self.bot.click_element("BINANCE_CONTROLS", "bin_tab"):
            self.bot.click_element("BINANCE_INTERNAL", "bn_sub_positions", verify=False)
            time.sleep(0.5)
            foc = "bn_pos_focus" if self.cfg.get("BINANCE_INTERNAL", "bn_pos_focus_x") else "bin_focus"
            pos_txt = self.bot.extract_text_from_page("BINANCE_INTERNAL", foc)
            bn_data = DataSurgeon.parse_binance_position(pos_txt)
            
            self.bot.click_element("BINANCE_INTERNAL", "bn_sub_orders", verify=False)
            time.sleep(0.5)
            ord_txt = self.bot.extract_text_from_page("BINANCE_INTERNAL", foc)
            clean_orders = DataSurgeon.parse_binance_orders(ord_txt)

        if self.bot.click_element("TRADINGVIEW", "tv_tab"):
            foc_tv = "tv_pos_focus" if self.cfg.get("TRADINGVIEW_INTERNAL", "tv_pos_focus_x") else "tv_focus"
            tv_txt = self.bot.extract_text_from_page("TRADINGVIEW_INTERNAL", foc_tv)
            tv_data = DataSurgeon.parse_tv_position(tv_txt)

        api_text = self.api_data.get_market_report()
        pm = re.search(r'PRICE: \$([\d,\.]+)', api_text)
        self.btc_price = pm.group(1) if pm else "N/A"

        # [NEW] SCREENSHOT LOGIC RESTORED
        if self.cfg.get('SYSTEM', 'do_screenshots', fallback='True') == 'True':
            if self.bot.click_element("COINGLASS", "cg_tab_main"):
                p = self.vision.capture_heatmap()
                if p: self.image_paths.append(p)
            if self.bot.click_element("BITMEX", "bm_tab"):
                time.sleep(2.0)
                p_btm = self.vision.capture_orderbook()
                if p_btm: self.image_paths.append(p_btm)

        # 5. --- BUDOWA REKORDU HISTORII ---
        record = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "src": "SYSTEM_CYCLE",
            "data": {
                "btc_price": self.btc_price,
                "bn": bn_data,
                "bn_orders": clean_orders,
                "tv": tv_data,
                "wallet": bn_data.get('wallet', 'N/A'),
                "user_notes": user_directives if user_directives else "None"
            }
        }
        
        # 6. Zapis do historii JSONL
        try:
            with open("market_history.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            self.log.log(f"Błąd zapisu historii: {e}", "WARN")

        # 7. --- BUDOWA RAPORTU KOŃCOWEGO ---
        self.full_report = ""
        if user_directives:
            self.full_report += "!!! [HUMAN OPERATOR MESSAGES] !!!\n"
            self.full_report += f"{user_directives}\n"
            self.full_report += "!!! [END OF MESSAGES] !!!\n\n"
            
        self.full_report += f"--- SNAPSHOT DANYCH ({record['time']}) ---\n"
        self.full_report += f"BTC PRICE: ${record['data']['btc_price']}\n"
        self.full_report += f"\n--- BINANCE ---\nSTATUS: {bn_data.get('status','?')}\nSIZE: {bn_data.get('size','?')}\n"
        self.full_report += f"ENTRY: {bn_data.get('entry','?')}\nPNL: {bn_data.get('pnl','0.0')}$\n"
        self.full_report += f"ORDERS:\n{clean_orders}\n"
        self.full_report += f"\n--- TV ---\nSTATUS: {tv_data.get('status','?')}\nSIZE: {tv_data.get('size','?')}\n"
        self.full_report += f"PNL: {tv_data.get('pnl','0.0')}\n"

        # 8. [NEW] WEB INDICATORS RESTORED
        # Sprawdzamy czy włączone jest TXT lub SS (bo collector obsługuje oba)
        do_web_txt = self.cfg.get('SYSTEM', 'web_scraping_txt', fallback='False') == 'True'
        do_web_ss = self.cfg.get('SYSTEM', 'web_scraping_ss', fallback='False') == 'True'
        
        if do_web_txt or do_web_ss:
            web_rep, web_imgs = self.web_collector.collect_data(self.bot)
            self.full_report += f"\n{web_rep}\n"
            if web_imgs:
                self.image_paths.extend(web_imgs)
        
        # 9. Powiadomienie Signal
        sig_msg = f"🔄 Nowy Cykl: {record['time']}\nBTC: {self.btc_price}\nBN Status: {bn_data.get('status','?')}\nPNL: {bn_data.get('pnl','0.0')}$"
        self._send_signal(sig_msg)

        if self.hud:
            self.hud.update_market(self.btc_price)
            self.hud.update_bn_data(bn_data)
            self.hud.update_tv_data(tv_data)

        self.transition_to(BotState.ACTIVE_WAIT)

    def _background_harvest(self):
        """Aktywny skan tła uwzględniający Signal co minutę."""
        self.log.log(">>> [MINUTOWY SKAN TŁA + SIGNAL] <<<")
        
        bg_directives = ""
        try:
            bg_directives = self.signal.receive_latest()
            if bg_directives:
                self.user_message_queue.append(bg_directives)
                self.log.log("Tło: Przechwycono wiadomość operatora.", "SIGNAL")
        except Exception as e:
            self.log.log(f"Błąd Signal w tle: {e}", "WARN")

        snapshot_data = {
            "bn": {}, 
            "bn_orders": "No Data",
            "tv": {},
            "user_notes": bg_directives if bg_directives else "None"
        }
        # ... (zapis do market_history.jsonl) ...    
        # 1. BINANCE
        if self.bot.click_element("BINANCE_CONTROLS", "bin_tab"):
            self.bot.click_element("BINANCE_INTERNAL", "bn_sub_positions")
            time.sleep(1.0)
            txt_pos = self.bot.extract_text_from_page("BINANCE_INTERNAL", "bn_pos_focus")
            snapshot_data["bn"] = DataSurgeon.parse_binance_position(txt_pos)
            
            self.bot.click_element("BINANCE_INTERNAL", "bn_sub_orders")
            time.sleep(1.0)
            txt_ord = self.bot.extract_text_from_page("BINANCE_INTERNAL", "bn_pos_focus")
            snapshot_data["bn_orders"] = DataSurgeon.parse_binance_orders(txt_ord)

        # 2. TRADINGVIEW
        if self.bot.click_element("TRADINGVIEW", "tv_tab"):
            txt_tv = self.bot.extract_text_from_page("TRADINGVIEW_INTERNAL", "tv_pos_focus")
            snapshot_data["tv"] = DataSurgeon.parse_tv_position(txt_tv)

        # 3. Zapis do historii
        record = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "src": "BACKGROUND_SCAN",
            "data": snapshot_data
        }
        try:
            with open("market_history.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            self.log.log(f"Błąd zapisu skanu tła: {e}", "WARN")

        if self.hud:
            self.hud.update_bn_data(snapshot_data["bn"])
            self.hud.update_tv_data(snapshot_data["tv"])
    
    def handle_wait(self):
        elapsed = time.time() - self.cycle_start_time
        waits = [self.cfg.get_float('TIMING', 'ai_wait_seconds', 120)]
        req_wait = int(max(waits))
        rem = req_wait - elapsed
        if rem > 0:
            if self.hud: self.hud.update_mission("WAITING", int(rem), "AI THINKING")
            self.council.active_wait_cycle(rem)
        self.transition_to(BotState.COLLECT_COUNCIL)

    def handle_collect_council(self):
        self._update_status("Harvesting AI Council")
        self.full_report += self.council.harvest_responses() # Zbiera z Groka itp.
        self.transition_to(BotState.SYNTHESIS)

    def handle_synthesis(self):
        """Analiza Master Gemini - Wysyłka pełnego raportu."""
        self._update_status("Gemini Master Synthesis")
        if self.bot.click_element("GEMINI_CONTROLS", "gem_tab"):
            

            self.bot.click_element("GEMINI_CONTROLS", "gem_input")
            
            # Wklejanie obrazów
            for img in self.image_paths:
                if self.bot.copy_image_to_clipboard(img):
                    self.bot.paste_content()
                    time.sleep(1.5)
            
            # Prompt tekstowy
            self.bot.paste_text(self.strategist.construct_prompt(self.full_report))
            if not self.bot.find_and_click_image("btn_send_GEMINI.png"):
                if not self.bot.click_element("GEMINI_CONTROLS", "gem_send"): 
                    pyautogui.press('enter')
            
            # Czekanie na analizę
            think_t = int(self.cfg.get_float('TIMING', 'gemini_think', 120))
            for i in range(think_t, 0, -1):
                if not self.is_running: return
                self._update_status("Gemini Thinking...", i)
                time.sleep(1)
            
            # Kopiowanie odpowiedzi
            self.bot.scroll_to_bottom("GEMINI_CONTROLS", "gem_scroll_point")
            time.sleep(3.0)
            pyperclip.copy("")
            resp = ""
            if self.bot.find_and_click_image("btn_copy_GEMINI.png") or self.bot.click_element("GEMINI_CONTROLS", "gem_copy"):
                for _ in range(4):
                    time.sleep(2.0)
                    resp = pyperclip.paste()
                    if len(resp) > 10: break
            
            if len(resp) > 10:
                self.raw_gemini_response = resp
                self.log.log(f"Przechwycono pełny raport Gemini ({len(resp)} znaków).")
                
                # SIGNAL 2: WYSYŁKA CAŁEGO TEKSTU
                # Jeśli tekst jest bardzo długi, Signal-CLI może go uciąć przy przekazywaniu przez shella.
                # Upewniamy się, że wysyłamy wszystko.
                header = f"[PEŁNY RAPORT STRATEGICZNY {time.strftime('%H:%M:%S')}]\n\n"
                full_message = header + resp
                
                # Opcjonalne dzielenie, jeśli wiadomość przekracza 4000 znaków (limit niektórych klientów)
                if len(full_message) > 4000:
                    self._send_signal(full_message[:4000])
                    self._send_signal("...[CIĄG DALSZY]...\n" + full_message[4000:])
                else:
                    self._send_signal(full_message)
                
                self.transition_to(BotState.DISPATCH)
            else:
                self.last_error = "Gemini Copy Failed"
                self.transition_to(BotState.ERROR_RECOVERY)

    def handle_dispatch(self):
        self._update_status("Processing Decisions")
        self.decisions_list = self.strategist.process_response(self.raw_gemini_response)
        if self.decisions_list: self.transition_to(BotState.EXECUTION)
        else: self.transition_to(BotState.COOLDOWN)

    def handle_execution(self):
        self._update_status("Agent 3 Executing Orders")
        d_list = self.decisions_list if isinstance(self.decisions_list, list) else [self.decisions_list]
        for decision in d_list:
            if not decision or not self.is_running: continue
            self.tactician.dispatch_order(decision)
            save_mission_state("EXECUTED", self.mission_state.get('active_position'), decision.get('action', 'HOLD'))
        self.transition_to(BotState.COOLDOWN)

    # W handle_boot dodaj inicjalizację pliku:
    def handle_boot(self):
        self._update_status("Initialising components")
        
        # 1. Pobieramy zaległe wiadomości ze startu
        try:
            boot_msgs = self.signal.receive_latest()
            if boot_msgs:
                self.log.log(f"Pobrano wiadomości startowe: {len(boot_msgs)}", "SYSTEM")
                self.user_message_queue.append(boot_msgs)
        except Exception as e:
            self.log.log(f"Signal boot check fail: {e}", "WARN")

        self.full_report = ""; self.image_paths = []; self.decisions_list = []
        self.cycle_start_time = time.time()
        # self.transition_to(BotState.SEED_COUNCIL) # zakomentowana, bo jest podwójnie wstawiona ta linijka

        if not os.path.exists("market_trend.json"):
            with open("market_trend.json", 'w') as f: json.dump([], f)
        self.transition_to(BotState.SEED_COUNCIL)

    # --- NOWA FUNKCJA handle_cooldown ---
    def handle_cooldown(self):
        total_wait = int(self.cfg.get('SYSTEM', 'loop_interval_min', 17)) * 60
        scan_interval = self.cfg.get_float('TIMING', 'background_scan_interval', 60.0)
    
        start_wait = time.time()
        last_scan = 0
    
        while (time.time() - start_wait) < total_wait:
            if not self.is_running: return
        
            elapsed = time.time() - start_wait
            remaining = total_wait - elapsed
        
            # 1. Główny mechanizm skanowania (Bezpiecznik w configu/HUD)
            scan_enabled = self.cfg.get('SYSTEM', 'background_scan_enabled', 'True') == 'True'
            if scan_enabled and (time.time() - last_scan) > scan_interval:
                self._background_harvest()
                last_scan = time.time()
        
            self._update_status("Sleeping/Monitoring", int(remaining))
            time.sleep(5) # Krótki sleep pętli sterującej
        
        self.transition_to(BotState.BOOT)

    def handle_recovery(self):
        self._update_status("Recovery Mode", 60)
        pyautogui.keyUp('ctrl'); pyautogui.keyUp('shift'); pyautogui.keyUp('alt')
        pyautogui.press('f5'); pyperclip.copy("")
        time.sleep(60)
        self.transition_to(BotState.BOOT)

    def run_once(self):
        def _once():
            self.is_running = True
            while self.is_running and self.state != BotState.COOLDOWN:
                self.run_fsm_step()
            self.is_running = False
        threading.Thread(target=_once, daemon=True).start()
