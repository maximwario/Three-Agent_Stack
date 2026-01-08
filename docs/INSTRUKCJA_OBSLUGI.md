# PERCEPTRON v0.8.0 (FSM Edition) – Instrukcja Obsługi

## 1. Wstęp
**Perceptron v0.8.0** to zaawansowany agent tradingowy wykorzystujący sztuczną inteligencję do analizy rynku i podejmowania decyzji. System działa w oparciu o architekturę maszyny stanów (Finite State Machine), integrując dane z wielu giełd (Binance, Bybit) oraz serwisów analitycznych (TradingView, Coinglass).

## 2. Uruchomienie Systemu
Aby uruchomić program, należy wykonać skrypt główny w środowisku Python:
```bash
python main.py
```
Program uruchomi graficzny interfejs użytkownika (GUI).

## 3. Interfejs Użytkownika (GUI)

### Główny Panel Sterowania
- **▶ START**: Uruchamia główną pętlę decyzyjną bota (Harvest -> Analyze -> Trade).
- **⏹ STOP**: Zatrzymuje działanie bota po zakończeniu obecnego cyklu.
- **⚡ RUN ONCE**: Wykonuje jeden pełny cykl analizy i zatrzymuje się.
- **🛠 KALIBRACJA**: Otwiera kreator kalibracji współrzędnych ekranowych (patrz sekcja 5).
- **⏱️ TIMING**: Otwiera zaawansowaną konfigurację czasów oczekiwania (patrz sekcja 6).

### Menu Opcji
W pasku menu dostępne są dodatkowe ustawienia:
- **File > Exit**: Bezpieczne zamknięcie aplikacji.
- **Control & Logs**:
    - **ENABLE AGENT 3 (EXECUTION)**: Włącza/wyłącza moduł wykonawczy (Agent 3). Jeśli odznaczone, bot tylko analizuje, ale nie składa zleceń (tryb "Paper Trading").
    - **Enable Text Scraping (JSON)**: Włącza pobieranie danych tekstowych ze stron WWW.
    - **Enable Screenshots**: Włącza wykonywanie zrzutów ekranu ze stron WWW do analizy wizualnej.
    - **Run Web PoC (Test)**: Uruchamia testowy skrypt pobierania danych webowych.

### Okno Logów
Centralna część okna wyświetla logi systemowe na żywo. Kolor zielony na czarnym tle ułatwia czytelność. Logi są również zapisywane do pliku `system_log.txt`.

## 4. Funkcje Bezpieczeństwa (Kill Switch)
W razie awarii lub nieoczekiwanego zachowania bota, dostępny jest globalny skrót klawiszowy:
- **F3**: Natychmiastowe zatrzymanie wszystkich procesów bota ("Emergency Stop").

## 5. Kalibracja Systemu
Przycisk **🛠 KALIBRACJA** otwiera okno, w którym definiuje się pozycje przycisków i obszarów na ekranie. Jest to kluczowe dla działania modułu wizyjnego (Vision).

### Dostępne Kategorie Kalibracji:
- **PLATFORMY**:
    - **Gemini**: Kalibracja interfejsu czatu Gemini (Master AI).
    - **Binance (Browser/Deep Dive)**: Lokalizacja przycisków kupna/sprzedaży i pól tekstowych na Binance.
    - **TradingView**: Lokalizacja wykresów i narzędzi.
    - **Coinglass / Bitmex**: Kalibracja podglądu danych rynkowych.
- **AI**: Kalibracja okien czatu dla modeli pomocniczych: GROK, COPILOT, DEEPSEEK, QWEN.
- **WEB INDICATORS**: Kalibracja zakładek dla wskaźników (Open Interest, L/S Ratio, Liquidation Heatmap itp.).

**Instrukcja Kalibracji:**
1. Kliknij przycisk odpowiadający danemu elementowi (np. "Gemini").
2. Postępuj zgodnie z instrukcjami w terminalu/oknie (zazwyczaj najechanie myszką i wciśnięcie klawisza).
3. Nowe współrzędne zostaną zapisane w `intel_config_v33.ini`.

## 6. Konfiguracja Czasu (Chronos Settings)
Przycisk **⏱️ TIMING** pozwala dostosować szybkość działania bota do wydajności komputera i łącza internetowego.

**Kluczowe Parametry:**
- **Loop Interval**: Odstęp między pełnymi cyklami analizy (minuty).
- **Gemini Think / AI Wait**: Czas oczekiwania na odpowiedź modeli AI.
- **Vision Load / Page Load Wait**: Czas na załadowanie stron i wykonanie zrzutów ekranu.
- **Mouse Speed**: Szybkość ruchu kursora (0 = natychmiastowy, >0 = ruch ludzki).
- **Clipboard Wait**: Czas oczekiwania na operacje Schowka (Ctrl+C/V).

Zaleca się zwiększenie wartości "Wait", jeśli komputer działa wolno lub AI nie zdąży wygenerować odpowiedzi.

## 7. Rozwiązywanie Problemów
- **Bot nie klika w przyciski**: Sprawdź kalibrację (**🛠 KALIBRACJA**). Upewnij się, że okna przeglądarki są w tym samym miejscu co podczas kalibracji (nieprzesuwane).
- **Błędy "Vision Fail"**: Zwiększ parametr `Vision Load` w ustawieniach Timing. Sprawdź, czy strony nie zmieniły wyglądu (tryb ciemny/jasny).
- **System zawiesza się**: Użyj **F3**, aby wymusić zatrzymanie. Sprawdź `system_log.txt` oraz plik `crash_dump.txt` w poszukiwaniu błędów krytycznych.
- **Agent 3 nie zawiera transakcji**: Sprawdź w menu `Control & Logs`, czy opcja "ENABLE AGENT 3" jest zaznaczona.

---
*Autor: Zespół Antigravity dla projektu EPIC AGENT.*
