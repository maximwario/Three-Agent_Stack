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
import time
import json
import os
import pyperclip
from utils.logger import AgentLogger

class WebMarketCollector:
    def __init__(self, config_manager, vision_sensor):
        self.cfg = config_manager
        self.vision = vision_sensor
        self.log = AgentLogger("WEB_COLLECTOR")
        self.indicators = ["A", "B", "C", "D", "E", "F"]
        
    def collect_data(self, browser_bot):
        """
        Główna pętla zbierająca dane z 5 stron.
        Zwraca: (raport_txt, lista_ścieżek_do_obrazków)
        """
        self.log.log(">>> Rozpoczynanie sekwencji Web Scraping (5 Wskaźników)...")
        
        collected_data = {}
        image_paths = []
        
        do_txt = self.cfg.get('SYSTEM', 'web_scraping_txt', 'False') == 'True'
        do_ss = self.cfg.get('SYSTEM', 'web_scraping_ss', 'False') == 'True'
        
        if not do_txt and not do_ss:
            self.log.log("Web Scraping wyłączony w menu. Pomijam.")
            return "WEB SCRAPING DISABLED", []

        for ind in self.indicators:
            section = f"WEB_INDICATOR_{ind}"
            self.log.log(f"Przetwarzanie wskaźnika: {ind} ({section})...")
            
            # 1. Sprawdź czy sekcja ma konfigurację
            if not self.cfg.get(section, "tab_x"):
                self.log.log(f"BRAK KONFIGURACJI DLA {section}! Pomijam.", "WARN")
                collected_data[ind] = "MISSING_CONFIG"
                continue
                
            # 2. Kliknij zakładkę
            if not browser_bot.click_element(section, "tab"):
                self.log.log(f"Nie udało się kliknąć zakładki dla {ind}", "ERROR")
                continue
            
            # Czas na załadowanie strony
            time.sleep(self.cfg.get_float('TIMING', 'vision_load', 3.0))
            
            # 3. Focus & Scroll
            # Najpierw klikamy w punkt scrollowania (lub pasek przesuwania), aby ustawić widok
            browser_bot.click_element(section, "focus_scroll", verify=False)
            time.sleep(0.5)
            
            # 4. Pobieranie Tekstu (TXT)
            text_content = ""
            if do_txt:
                # Klikamy w punkt do zaznaczania tekstu
                raw_text = browser_bot.extract_text_from_page(section, "focus_text")
                clean_text = self._clean_text(raw_text)
                collected_data[ind] = clean_text
                self.log.log(f"Pobrano tekst dla {ind} ({len(clean_text)} znaków)")
            
            # 5. Screenshot (SS)
            if do_ss:
                # Używamy VisionSensor, ale musimy mu podać specyficzne klucze
                # VisionSensor oczekuje: tab_key, focus_key, tl_key, br_key
                # Tu robimy to ręcznie, bo mamy customowe klucze w configu (ss_tl, ss_br)
                try:
                    path = self.vision._capture_region(
                        section, 
                        "tab",          # już kliknięte, ale funkcja klika ponownie - to OK
                        "focus_scroll", # używamy focus_scroll jako resetu
                        "ss_tl", 
                        "ss_br", 
                        f"web_indicator_{ind}.png"
                    )
                    if path:
                        image_paths.append(path)
                except Exception as e:
                    self.log.log(f"Błąd SS dla {ind}: {e}", "ERROR")

        # Zapisz wszystko do JSON
        self._save_to_json(collected_data)
        
        report_str = self._format_report(collected_data)
        return report_str, image_paths

    def _clean_text(self, text):
        """Proste czyszczenie nadmiarowych pustych linii"""
        if not text: return ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def _save_to_json(self, data):
        package = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "web_scrape_v1",
            "indicators": data
        }
        try:
            with open('market_data_web.json', 'w', encoding='utf-8') as f:
                json.dump(package, f, indent=2, ensure_ascii=False)
            self.log.log("Zapisano market_data_web.json")
        except Exception as e:
            self.log.log(f"Błąd zapisu JSON: {e}", "ERROR")

    def _format_report(self, data):
        """Formatowanie do kontekstu Prompta (Full Data)"""
        # Przygotowujemy czytelny JSON-like string dla Gemini
        out = "\n--- WEB SCRAPED INDICATORS (FULL CONTEXT) ---\n"
        
        # Filtrujemy puste/błędne
        filtered = {k: v for k, v in data.items() if v and v != "MISSING_CONFIG"}
        
        if not filtered:
            return out + "NO DATA SCRARED.\n"
            
        # Zrzucamy całość do stringa - Gemini sobie z tym poradzi
        # options: ensure_ascii=False pozwala na polskie znaki etc.
        json_str = json.dumps(filtered, indent=2, ensure_ascii=False)
        out += json_str
        out += "\n---------------------------------------------\n"
        return out
