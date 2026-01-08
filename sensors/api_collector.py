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
import requests
import time
import json
try:
    import ccxt
except ImportError:
    ccxt = None

from utils.logger import AgentLogger

class MarketDataCollector:
    def __init__(self, config_manager):
        self.cfg = config_manager
        self.log = AgentLogger("API_DATA")
        self.exchange = None
        
        # Pobieramy klucz z configu
        self.coinglass_key = self.cfg.get('SECRETS', 'coinglass_key')
        self.base_url = "https://open-api-v4.coinglass.com"
        
        # Inicjalizacja Binance (CCXT) - nie ruszamy tego, co działa
        self._init_exchange()

    def _init_exchange(self):
        if ccxt:
            try:
                self.exchange = ccxt.binance({'enableRateLimit': True})
            except Exception as e:
                self.log.log(f"Błąd inicjalizacji CCXT: {e}", "ERROR")

    def _cg_request(self, endpoint, params=None):
        """
        Bezpieczny wrapper do zapytań Coinglass.
        Zawiera RATE LIMITING (1s sleep) i obsługę błędów.
        """
        # 1. Sprawdzenie klucza
        if not self.coinglass_key or "WPISZ" in self.coinglass_key:
            return None
            
        headers = {
            "accept": "application/json",
            "coinglassSecret": self.coinglass_key
        }
        
        # 2. RATE LIMITING (Kluczowe dla stabilności)
        delay = self.cfg.get_float('TIMING', 'api_request_interval', fallback=1.0)
        time.sleep(delay) 
        
        try:
            url = f"{self.base_url}{endpoint}"
            # Timeout 10s, żeby nie wisieć w nieskończoność
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data["data"]
                else:
                    self.log.log(f"Coinglass API Logic Error: {data.get('msg')}", "WARN")
            elif response.status_code == 429:
                self.log.log("Coinglass RATE LIMIT EXCEEDED (429)!", "WARN")
                time.sleep(5) # Kara za przekroczenie limitu
            else:
                self.log.log(f"Coinglass HTTP Error {response.status_code}", "WARN")
                
            return None
        except Exception as e:
            self.log.log(f"Coinglass Request Exception ({endpoint}): {e}", "WARN")
            return None

    # --- GŁÓWNA METODA ---

    def get_market_report(self):
        self.log.log("Pobieranie danych rynkowych (Binance + Coinglass)...")
        
        # Faza 1: Binance (Szybka)
        bn_report = self._get_binance_data()
        
        # Faza 2: Coinglass (Wolna - ok. 6-8 sekund)
        cg_report = self._get_coinglass_data()
        
        # --- ZMIANA TUTAJ ---
        full_report = f"{bn_report}\n{cg_report}"
        
        # Zapisz do JSON (wywołanie funkcji z dołu pliku)
        self.save_report_json(full_report)
        
        return full_report
    def _get_binance_data(self):
        """Pobiera Price/Vol z Binance (Niezawodne)"""
        if not self.exchange:
            return "--- BINANCE DATA ---\nAPI ERROR: Brak biblioteki ccxt.\n"

        try:
            ticker = self.exchange.fetch_ticker('BTC/USDT')
            price = ticker['last']
            change = ticker['percentage']
            vol = ticker['quoteVolume']
            
            # Próba pobrania Funding Rate z Binance (często szybsze/dokładniejsze)
            funding_str = "N/A"
            try:
                f_data = self.exchange.fapiPublicGetPremiumIndex({'symbol': 'BTCUSDT'})
                funding_str = f"{float(f_data['lastFundingRate']) * 100:.4f}%"
            except: pass

            return (
                f"--- HARD DATA (Binance) ---\n"
                f"PRICE: ${price:,.2f}\n"
                f"24H CHANGE: {change:.2f}%\n"
                f"VOLUME (24h): ${vol:,.0f}\n"
                f"FUNDING RATE: {funding_str}\n"
            )
        except Exception as e:
            self.log.log(f"Błąd Binance API: {e}", "ERROR")
            return "--- BINANCE DATA ---\nERROR: Connection failed.\n"

    def _get_coinglass_data(self):
        """
        Pobiera 6 wskaźników z Coinglass.
        Każdy blok w osobnej sekcji try/except dla bezpieczeństwa.
        """
        if not self.coinglass_key or "WPISZ" in self.coinglass_key:
            return "\n--- COINGLASS DATA ---\nWARNING: Brak klucza API w config.ini\n"

        report_lines = ["\n--- COINGLASS ADVANCED METRICS ---"]
        
        # A. OPEN INTEREST (Zmiana 24h)
        try:
            oi_data = self._cg_request("/api/futures/openInterest/ohlc-aggregated-history", 
                                     {"symbol": "BTC", "interval": "1h", "limit": 24})
            # Safety Check: Czy mamy listę i czy ma min. 2 elementy
            if oi_data and isinstance(oi_data, list) and len(oi_data) >= 2:
                curr_oi = oi_data[-1].get('openInterest', 0)
                prev_oi = oi_data[0].get('openInterest', 0)
                
                if prev_oi > 0:
                    oi_change = ((curr_oi - prev_oi) / prev_oi) * 100
                    report_lines.append(f"OPEN INTEREST: ${curr_oi:,.0f} (24h: {oi_change:+.2f}%)")
        except Exception as e:
            self.log.log(f"OI Parse Error: {e}", "WARN")
        
        # B. LONG/SHORT RATIO (Divergence Check)
        try:
            # Dwa osobne requesty (pamiętaj o sleep w _cg_request)
            ls_global = self._cg_request("/api/futures/global-long-short-account-ratio/history", 
                                       {"symbol": "BTC", "interval": "1h", "limit": 1})
            ls_top = self._cg_request("/api/futures/top-long-short-account-ratio/history", 
                                    {"symbol": "BTC", "interval": "1h", "limit": 1})
            
            if ls_global and ls_top:
                g_ratio = ls_global[0].get('longRatio', 50)
                t_ratio = ls_top[0].get('longRatio', 50)
                
                report_lines.append(f"L/S RATIO (Retail): Long {g_ratio:.1f}% vs Short {100-g_ratio:.1f}%")
                report_lines.append(f"L/S RATIO (Whales): Long {t_ratio:.1f}% vs Short {100-t_ratio:.1f}%")
                
                # Prosta analiza dywergencji dla Agenta 2
                if g_ratio > 60 and t_ratio < 50:
                    report_lines.append(">> SIGNAL: Retail FOMO (Bullish) vs Whale Selling (Bearish)")
                elif g_ratio < 40 and t_ratio > 50:
                    report_lines.append(">> SIGNAL: Retail Panic (Bearish) vs Whale Accumulation (Bullish)")
        except Exception as e:
            self.log.log(f"L/S Parse Error: {e}", "WARN")

        # C. LIQUIDATIONS (Pain Level)
        try:
            liq_data = self._cg_request("/api/futures/liquidation/aggregated-history", 
                                      {"symbol": "BTC", "interval": "1h", "limit": 24})
            if liq_data:
                total_long = sum(item.get('longLiquidationUsd', 0) for item in liq_data)
                total_short = sum(item.get('shortLiquidationUsd', 0) for item in liq_data)
                report_lines.append(f"LIQUIDATIONS (24h): Longs ${total_long/1e6:.1f}M | Shorts ${total_short/1e6:.1f}M")
        except Exception as e: pass

        # D. HEATMAP (Liquidation Magnets)
        try:
            heatmap = self._cg_request("/api/futures/liquidation/heatmap/model2", {"symbol": "BTC"})
            if heatmap:
                # Walidacja: Czasem heatmap to lista, czasem dict z kluczem 'data'
                data_list = heatmap if isinstance(heatmap, list) else heatmap.get('data', [])
                
                if data_list:
                    # Szukamy poziomów z największym wolumenem likwidacji
                    clusters = sorted(data_list, key=lambda x: x.get('volume', 0), reverse=True)[:3]
                    report_lines.append("LIQUIDATION MAGNETS (Top 3 Levels):")
                    for c in clusters:
                        report_lines.append(f"  -> ${c.get('price', 0):,.0f} (Vol: ${c.get('volume', 0)/1e6:.1f}M)")
        except Exception as e: pass

        # E. ORDERBOOK WALLS (Whale Walls)
        try:
            # Pobieramy tylko dla Binance (największa płynność)
            ob = self._cg_request("/api/futures/orderbook/large-limit-order", 
                                {"symbol": "BTC", "exchange": "Binance"})
            if ob:
                bids = [x for x in ob if x.get('side') == 'bid']
                asks = [x for x in ob if x.get('side') == 'ask']
                
                if bids:
                    top_bid = max(bids, key=lambda x: x.get('volume', 0))
                    report_lines.append(f"BUY WALL (Support): ${top_bid.get('price',0):,.0f} (${top_bid.get('volume',0)/1e6:.1f}M)")
                if asks:
                    top_ask = max(asks, key=lambda x: x.get('volume', 0))
                    report_lines.append(f"SELL WALL (Resistance): ${top_ask.get('price',0):,.0f} (${top_ask.get('volume',0)/1e6:.1f}M)")
        except Exception as e: pass

        report_lines.append("------------------------------\n")
        return "\n".join(report_lines)

    def save_report_json(self, report_text):
        """Zapisuje ostatni raport do pliku JSON (Persistence)"""
        try:
            data_package = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "market_snapshot",
                "content": report_text
            }
            # Zapisujemy jako 'market_data_latest.json' - nadpisuje stary, by mieć zawsze świeży podgląd
            with open('market_data_latest.json', 'w', encoding='utf-8') as f:
                json.dump(data_package, f, indent=2, ensure_ascii=False)
            self.log.log("Zapisano raport do market_data_latest.json")
        except Exception as e:
            self.log.log(f"Błąd zapisu JSON: {e}", "WARN")    