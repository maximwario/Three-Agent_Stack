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
from utils.parsers import DataSurgeon

def test_parser():
    print("=== TEST PARSERA ZLECEŃ BINANCE ===")
    
    # Przypadek 1: Tekst z wieloma zleceniami (PL/EN mix)
    sample_text_1 = """
    Data    Para    Typ    Strona    Cena    Ilość    Zrealizowano    Wartość    Warunek aktywacji
    2024-12-27    BTCUSDT    Stop Market    Sprzedaj    Market    0.005    0.000    0.00    <= 95,500.00
    2024-12-27    BTCUSDT    Take Profit Market    Sprzedaj    Market    0.005    0.000    0.00    >= 102,000.50
    2024-12-27    BTCUSDT    Limit    Kup    90000.00    0.010    0.000    0.00    -
    """
    
    print("\n[TEST 1] Złożony przypadek:")
    result_1 = DataSurgeon.parse_binance_orders(sample_text_1)
    print(result_1)
    
    # Przypadek 2: Brak zleceń
    sample_text_2 = "Nie znaleziono danych. No records found."
    print("\n[TEST 2] Brak danych:")
    print(DataSurgeon.parse_binance_orders(sample_text_2))
    
    # Przypadek 3: Nowy format Trailing
    sample_text_3 = "Trailing Stop Market Sprzedaj <= 98,000.00"
    print("\n[TEST 3] Trailing Stop:")
    print(DataSurgeon.parse_binance_orders(sample_text_3))

if __name__ == "__main__":
    test_parser()
