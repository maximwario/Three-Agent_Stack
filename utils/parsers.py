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

class DataSurgeon:
    """
    Chirurg Danych v0.5.0: Zasada Kotwicy (ROI).
    """

    @staticmethod
    def _clean(text):
        if not text: return 0.0
        try:
            # Zamień przecinek na kropkę, usuń spacje, obsłuż minusy
            clean = text.replace(' ', '').replace(',', '.').replace('−', '-')
            return float(clean)
        except: return 0.0

    @staticmethod
    def parse_binance_position(raw_text):
        res = {"status": "NO DATA", "size": "?", "entry": "?", "pnl": 0.0, "tp_sl": "--/--"}
        if not raw_text or "NO DATA" in raw_text: return res
        
        # 1. FLAT Check
        if "Nie masz pozycji" in raw_text or "No Open Positions" in raw_text:
            res["status"] = "FLAT"
            return res

        try:
            # 2. PnL - ZASADA KOTWICY (ROI)
            # Szukamy liczby USDT, po której (w bliskiej odległości) występuje nawias z procentem (ROI)
            # Wzorzec w tekście: "+0,69 USDT\n(+0,13%)"
            # Regex: (Liczba) ... USDT ... ( ... % )
            
            # Najpierw usuwamy białe znaki dla łatwiejszego dopasowania
            flat_text = re.sub(r'\s+', ' ', raw_text)
            
            # Regex: Grupa 1 (PnL) ... USDT ... ( ... % )
            # Szukamy liczby, która ma po sobie 'USDT' a potem '('
            roi_anchor = re.search(r'([+-]?[\d,.]+)\s*USDT\s*\([+-]?[\d,.]+%?\)', flat_text)
            
            if roi_anchor:
                res['pnl'] = DataSurgeon._clean(roi_anchor.group(1))
                res['status'] = "OPEN"
            else:
                # Fallback: Jeśli nie ma ROI, szukamy po staremu (ale po usunięciu Salda)
                clean_text = re.sub(r'(Dost\.|Avail|Saldo|Balance|Koszt).*?USDT', '', raw_text, flags=re.IGNORECASE)
                pnl_match = re.search(r'([+-]\s*[\d\s]+[.,]\d+)\s*USDT', clean_text)
                if pnl_match:
                    res['pnl'] = DataSurgeon._clean(pnl_match.group(1))
                    res['status'] = "OPEN"

            # 3. Size & Entry (Standard)
            split_match = re.search(r'([\d,.]+)\s*BTC\s*([\d\s]+[.,]\d+)', raw_text)
            if split_match:
                res['size'] = split_match.group(1).replace('\n','').replace('\r','').strip()
                res['entry'] = split_match.group(2).replace(' ', '').replace('\n','').replace('\r','').strip()
            else:
                sz = re.search(r'([\d,.]+)\s*BTC', raw_text)
                en = re.search(r'(?:Cena|Entry|Mark).*?([\d\s]+[.,]\d+)', raw_text)
                if sz: res['size'] = sz.group(1).replace('\n','').replace('\r','').strip()
                if en: res['entry'] = en.group(1).replace(' ', '').replace('\n','').replace('\r','').strip()

            # 4. TP/SL
            tpsl_match = re.search(r'([\d\s]+[.,]\d+)\s*/\s*([\d\s]+[.,]\d+)', raw_text)
            if tpsl_match:
                t = tpsl_match.group(1).replace(' ', '').replace('\n','').replace('\r','')
                s = tpsl_match.group(2).replace(' ', '').replace('\n','').replace('\r','')
                
                # Fix artifact: Size blending into TP (e.g. Size 0.027, TP becomes 02790000)
                sz_digits = re.sub(r'[^\d]', '', res.get('size', '')) # np. "0027"
                if sz_digits:
                    # Spróbuj usunąć pełne cyfry size
                    if t.startswith(sz_digits): 
                        t = t[len(sz_digits):]
                    # Spróbuj usunąć bez wiodącego zera (np. 027)
                    elif sz_digits.startswith('0') and t.startswith(sz_digits[1:]):
                        t = t[len(sz_digits)-1:]

                res['tp_sl'] = f"{t}/{s}"

        except Exception as e: 
            print(f"Parser Err: {e}")
            
        return res

    @staticmethod
    @staticmethod
    def parse_binance_orders(raw_text):
        """
        Rygorystyczny Chirurg v0.6.0: Tylko pewne dane.
        Wyciąga Typ i Cenę. Jeśli brak ceny -> nie raportuje zlecenia.
        """
        if not raw_text or any(x in raw_text for x in ["Nie znaleziono", "No records", "No Open Positions"]): 
            return "No Active Orders"

        found_orders = []
        # Normalizacja tekstu
        clean_text = re.sub(r'\s+', ' ', raw_text)
        
        # Słownik wzorców: (Etykieta, Regex) - szukamy tylko konkretnych wartości cenowych
        patterns = [
            ("STOP", r'(?:Stop Market|Stop Loss).*?((?:<=|>=)\s*[\d\s]+[.,]\d+)'),
            ("TP",   r'(?:Take Profit).*?((?:<=|>=)\s*[\d\s]+[.,]\d+)'),
            ("LIMIT", r'(?:Limit|Limit Maker)\s+[\d,.]+\s+[\d,.]+\s+([\d\s]+[.,]\d+)'),
            ("TRAIL", r'(?:Trailing).*?((?:<=|>=)\s*[\d\s]+[.,]\d+)')
        ]

        try:
            for label, pattern in patterns:
                matches = re.findall(pattern, clean_text, re.IGNORECASE)
                for price_val in matches:
                    # Czyścimy cenę
                    price_str = price_val.replace(' ', '').replace('USDT', '')
                    found_orders.append(f"- {label}: {price_str}")
            
            # ZASADA KASYNA: Jeśli nic nie pasuje do wzorca, zwracamy brak, a nie domysły
            if not found_orders:
                return "No Active Orders"
        
        except Exception as e:
            return f"Parse Error: {e}"

        return "\n".join(found_orders)

    @staticmethod
    def parse_tv_position(raw_text):
        res = {"status": "WAITING", "size": "POS", "entry": "?", "pnl": 0.0}
        if not raw_text: return res
        try:
            # PnL TV
            pnl_match = re.search(r'([−-]?[\d\.,\s]+)\s*(?:USD|USDT)', raw_text)
            if pnl_match:
                res['pnl'] = DataSurgeon._clean(pnl_match.group(1))
                res['status'] = "ACTIVE"
            
            # Entry TV
            entry_matches = re.findall(r'(\d{2,3}[, ]?\d{3}[.,]\d{2})', raw_text)
            if entry_matches: res['entry'] = entry_matches[0].replace(' ', '')
            
            # Size TV
            side = re.search(r'(Long|Short)\s*(\d*)', raw_text, re.IGNORECASE)
            if side: 
                q = side.group(2) if side.group(2) else ""
                res['size'] = f"{side.group(1)[0]} {q}"
        except: pass
        return res
    
    @staticmethod
    def parse_binance_balance(raw_text):
        """Wyciąga dostępne saldo z surowego tekstu Binance."""
        if not raw_text or "NO DATA" in raw_text: return 0.0
        try:
            # Szukamy kwoty przy słowach kluczowych: Dost., Avail, Saldo, Balance
            balance_match = re.search(r'(?:Dost\.|Avail|Available|Saldo|Balance).*?([\d\s]+[.,]\d+)\s*USDT', raw_text, re.IGNORECASE | re.DOTALL)
            if balance_match:
                return DataSurgeon._clean(balance_match.group(1))
        except Exception as e:
            print(f"Balance Parser Err: {e}")
        return 0.0