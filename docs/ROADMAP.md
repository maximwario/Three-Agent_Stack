# PERCEPTRON ROADMAP & DEVELOPMENT JOURNAL

> "Stability > Functionality. System musi przetrwać błąd operatora i awarię sieci."

## ✅ UKOŃCZONE KAMIENIE MILOWE (v0.3.3)
- [x] **HUD v1 (Command Bar)**: Działający pasek z danymi o PnL i Pozycji.
- [x] **Deep Dive Parsing**: Przejście z "szumu" na Regex (wyciąganie Entry Price/Size).
- [x] **Vision Search**: Bot widzi przyciski, nie klika na ślepo.
- [x] **Async Harvest**: Rozdzielenie zadawania pytań od odbierania odpowiedzi.
- [x] **Immortal Loop**: Podstawowa pętla `try...except` z autorestartem.
- [x] **Main.py Fixes**: Dodano Error Modal, Menu (File > Exit) i poprawiono zatrzymywanie (Kill Switch / Stop Button).

---

## 📅 AKTUALNY CEL: v0.6.3 "THE HAMILTON CORE"

### 1. Rozbudowa HUD (Mission Control v2)
Prawa strona paska jest zbyt uboga.
- [ ] **Live Action Log**: Zamiast statycznego "HARVESTING", pasek ma wyświetlać przewijane logi (np. `[GROK] Data Copied`, `[BN] PnL Update`).
- [ ] **Visual Heartbeat**: Migająca kropka (zielona/czerwona) oznaczająca, że wątek orkiestratora żyje.
- [ ] **Agent Status**: Małe ikony (kwadraciki) dla każdego AI. Zielony = Sukces, Czerwony = Vision Fail.


### 2. Prawdziwa Architektura Hamiltona (Software Engineering)
Obecna pętla to tylko `while True` z obsługą błędów. Potrzebujemy inżynierii.
- [ ] **The Executive (Kolejka Priorytetów)**:
    - Zamiast liniowego kodu, zadania (`CheckPrice`, `Analyze`, `Trade`) trafiają do kolejki.
    - Jeśli system jest przeciążony, porzuca zadania *Background* (np. screenshoty), a wykonuje *Critical* (sprawdzenie Stop Loss). To jest trudne do wdrorzenia
- [ ] **Watchdog (Niezależny Proces)**:
    - Osobny skrypt `.py`, który sprawdza plik `heartbeat.txt`.
    - Jeśli główny `main.py` się zawiesi (brak aktualizacji pliku przez 30s), Watchdog zabija proces i uruchamia go ponownie ("BAILOUT").

### 3. API Coinglass (Full Integration)
- [x] Zakup i wpięcie klucza API Coinglass.
- [x] Zastąpienie mocka w `api_collector.py` prawdziwymi danymi (OI, Liq Heatmap data).

Od teraz 13 grudzień 2025 roku, pomijamy cele, które są do wykonania powyżej. Są one na uwadze, ale zajmujemy się czymś ważniejszym w 0.6.6. To duża zmiana w naszym projekcie. 
---

## 🔮 KONCEPCJE PRZYSZŁOŚCIOWE (v0.6.4)

- **Poprawki konieczne w main.py** : 
- [x] modal (messagebox na crash?); dodaj menu (File > Exit). Notatka Manie: # Skrypt teraz działa tak, że po kliknięciu w stop a nawet wyłączeniu programu, program nadal dzoiała i klika. Dopiero wyłączenie cmd terminala powoduje zatrzymanie działania.

- **## 📅 AKTUALNY CEL: v0.6.5** : Natatka Maniek: Zapisanie jako gotowy "Perceptron_v34_Modular_loop" (Epic_Agent_1_v0_6_5) do obsługi API coinglass. OK

- **## 📅 AKTUALNY CEL: v0.6.6** : 
Zaprogramować dodatkowe ruchy np. dwiedzanie dodatkowych zakładek (stron internetowych). Trzeba na tych stronach internetowych zrobić coś co będzie zwracać dane np. screen shoty wybranych elementów strony internetowej. Te dane będą używane do zrobienia raportów. Będzie to dokładane jako SS do raportów. Będzie to zrobione w formie obrazka z danymi np. "Vision: capture PNG (temp_vision/) → copy_to_clipboard" i dołączone do naszego raportu dokładnie tak samo jak teraz to robi z headmap i bitmex. "...- API: api_collector.get_market_report() → full_report
  ↓ (wait: active_wait_cycle(scroll tabs))
[Gemini Synteza]: paste report + images → wait(gemini_think) → copy response"

Chcę dodać do naszego projektu obsługę tych dodatkowych stron internetowych. Powinny być pełne kroki w kalibracji tak jak to jest teraz dla headmap i bitmex.

Tych stron internetowych jest tyle co wych wskaźników pięciu (5):

## Lista Wskaźników z Coinglass API (A-E)

A. OPEN INTEREST (Zmiana 24h): Całkowity wolumen otwartych pozycji + % zmiana w 24h.
B. LONG/SHORT RATIO (Divergence Check): Proporcja long/short (retail vs. whales) + analiza dywergencji.
C. LIQUIDATIONS (Pain Level): Suma likwidacji long/short w 24h + poziom "bólu" (wartość strat).
D. HEATMAP (Liquidation Magnets): Mapa ciepła z kluczowymi poziomami cenowymi likwidacji (top 3 magnesy).
E. ORDERBOOK WALLS (Whale Walls): Duże ściany zleceń (buy/sell walls) z wolumenem i cenami.

## 📅 AKTUALNY CEL: omówienie wstępne dokładne:

Trzeba dodać obsługę pięciu stron internetowych na które się wejdzie i zrobi SS (screenschot). Trzeba przedyskutować te wdrarzanie tych pięciu wskaźników jako SS ze stron internetowych. To są specyficzne strony internetowe. Trzeba tam wejść w zakładkę tej strony i zrobić SS. Przed zrobieniem tego SS trzeba wykonać specyficzne ruchy np. scrolowanie delikatnie w dół w miejsce strony internetowej na której są dane które chcemy mieć na tym SS.

Poza zrobieniem SSrzeba potszeba tam wejść i również zaznaczyć cały tekst ze strony internetowei (Ctrl+A) i skopiować go (Ctrl+c) i dodać do oddzielnego pliku tekstowego lub json aby po chwili go parsować lub tylko skompletować z tych pięciu stron internetpowych tych pięciu wskaźników. Wklejać całość z tego json do naszego raportu dla Gemini i sprawdzić czy Gemini chce parsowania tego lub czy dobrze radzi sobie z odsiewaniem danych i wyłapywaniem tego co realnie daje ten wskaźnik.

W ten sposób będziemy mieć pięć wskaźników z coinglass API i pięć wskaźników z stron internetowych w formie Screen shot i danych txt które możemy parsować i dodać do naszego raportu lub nie parsować i dodać do naszego raportu. Jeśli parsowac to nie usuwać takich rad z tych stron: "Wyjaśnienie dla Funding Rate".

Może te wszystkie 5 Ctrl+a i ctrl+c na tych stronach internetowych które zapisza się w pliku podac AI jako wsad w formacie json aby potem zrobic z tego dodatek json do raportu do Gemini ze strony internetowej gdzie są dane na temat: "## Lista Wskaźników z Coinglass API (A-E)"

**Wyjaśnienie dla Funding Rate**
"""Note: All funding rates are quoted as 8-hour rates. The dYdX rate has been multiplied by 8, as dYdX quotes rates on an hourly basis. When the funding rate is 0.01%, it is displayed in black, representing the baseline rate. When the funding rate is greater than 0.01%, it is shown in red, indicating a bullish market sentiment. When the funding rate is below 0.005%, it appears in green, representing a bearish market sentiment. The stronger the bullish or bearish sentiment, the darker the color.
What is the Funding Rate?

The funding rate is a fee set by cryptocurrency exchanges to maintain balance between the perpetual contract price and the underlying asset price. It applies mainly to perpetual futures contracts and acts as a mechanism for fund exchange between long and short traders. The exchange itself does not collect this fee — it serves to adjust the costs or returns of holding positions so that the contract price remains close to the spot price of the underlying asset.

When the price of a perpetual contract deviates from the underlying asset, the exchange adjusts the funding rate to encourage longs or shorts to pay funds in the opposite direction, bringing the contract price back in line with the underlying asset.

When the market is bullish, the funding rate is typically positive and increases over time — meaning long traders pay the funding fee to short traders.
Conversely, when the market is bearish, the funding rate is usually negative, meaning short traders pay the funding fee to long traders.

If the funding rate is positive, longs pay shorts; if it is negative, shorts pay longs.
When the funding rate is 0.00%, no funding payments are exchanged between longs and shorts.

In general, the maximum upper limit for Bitcoin’s funding rate is 0.375%, and the minimum lower limit is -0.375%, though this may vary slightly across different exchanges."""

**Wyjaśnienia jak to widzimy w programie:**
To powinno być do zaznaczenia ptaszkiem w menu przed uruchomieniem programu te 5 wskaźników z coinglass API i te 5 wskaźników z stron internetowych. Zaznaczenie ptaszkiem lub zaznaczenie w inny sposób pozwala na działanie aby wykonał się krok wejścia w zakładkę na tę stronę internetową i zrobienie SS i Ctrl+A i Ctrl+C i zapisanie do pliku tekstowego lub json aby potem zrobic z tego dodatek json do raportu do Gemini ze strony internetowej gdzie są dane na temat: "## Lista Wskaźników z Coinglass API (A-E)".

**Dlaczego zaznaczanie ptaszkiem do aktywacji lub zezaktywacji?**

Bo wtedy zrobimy z tego systemu automatyczny system do zrobienia raportów z giełdy. Będziemy mieli możliwośc parsowania tekstu z tej strony o naszych wszystkich wskaźnikach. Potrzebne są do tego osobne parsery dla każdego z osobna z tych wskaźników. Zapis do json lub do pliku tekstowego. Podanie tych danych do gemini jako dane przetworzone do json ale wewnątrz cała strona internetowa zrobione przez ctrl+a i ctrl+c.

Dodatkowo robią się już dwa SS na stronach bitmex i coinglass "headmap" to nasze nowe SS niech się zapisaują i podają do Gemini dokładnie tak jak teraz SS z bitmex i SS z coinglass headmapa.

Więc możemy tekst TXT ze stron:
1. nie parsować i zapisywać Ctrl+a i Ctrl+C do json pliku i podawać w raporcie do Gemini całość 5 stron internetowych zapisanych w json.
2. parsowac i podawać wyszczególnione dane jako txt data a nie API data tych samych wskaźników.
3. Podawać te 5 wskaźników jako SS screen shot.

Wszystkie te dane powinny być w raporcie do Gemini.

**Notatki o Exchange Liq... zrobiony copy paste tekst zaznaczony.:**

1. Exchange Liquidations
Exchanges
Liquidations
Long
Short
Rate
Rate
All
$6.15M
$2.57M
$3.59M
100%
58.28%Short
Binance
Binance
$2.86M
$1.29M
$1.58M
46.51%
55.08%Short
Hyperliquid
Hyperliquid
$868.61K
$406.59K
$462.02K
14.11%
53.19%Short
OKX
OKX
$855.03K
$398.25K
$456.78K
13.89%
53.42%Short
Bybit
Bybit
$839.58K
$323.21K
$516.37K
13.64%
61.5%Short
HTX
HTX
$418.45K
$31.97K
$386.47K
6.8%
92.36%Short
Gate
Gate
$286.31K
$112.06K
$174.25K
4.65%
60.86%Short
CoinEx
CoinEx
$23.92K
$9.82K
$14.10K
0.39%
58.93%Short
Bitmex
Bitmex
$0.09
$0.09
$0
0%
100%Long
Bitfinex
Bitfinex
$0
$0
$0
0%
0%Long
---------------------------

Zastanawiamy się czy obsługa tego będzie mogła postępować po za główną pętlą w czasie kiedy mamy SLIPPING spanie. Wtedy może być odwiedzanie tych stron i pilonowanie tego by dane były zbierane dokładnie z tych 5 stron internetowych. Mam tu na myśli tylko dane TXT, bo dane SS to przejście tak jak zawsze robimy. Ss bitmex i SS headmap i doszło by kilka SS z tych stron (te strony musiałby być do wybierania "SS pięciu wskaźników" zaznaczane ptaszkiem w menu przed uruchomieniem programu pętli.)

**# Perspektywy. Perspective**

Notatka Maniek: jeśli jest SLIPPING spanie to działać będzie inaczej niż jeśli nie jest SLIPPING spanie. Teraz chcemy to w pętli odwzorować. jeśli nie śpi to kolekcjonuje dane z tych pięciu stron internetowych i zapisuje do pliku tekstowego i do json. Ma być to wsad json z danych pochodzących z 30 minut zbierania ostatnich aktualnych wiadomości. To będzie podawane gdy pętla się wybudzi i będzie szła zadawać nowe pytania do wszystkich AI a następnie idzie robić SS headmap i SS bitmex i idzie po odpowiedzi do tych stron AI i idzie wkleić raport do gemini to niech załącza do raportu w formacie json dane z tych 30 min "co się działo na tych pięciu wskaźnikach w ostatnich 30 minutach?". Myślę, że taki komplet danych byłby łatwy do rzetworzenia dla Gemini. To byłby komplet danych z 30 minut.

Te zmiany pozwoliłby działać skryptowi w czasie gdy śpi. Zbierałby najważniejsze dane. Można to rozbudować by te dane zebrane wstępnie posortować by to przypominało wersję API za 99 $. Trudne do napisania. Bany na IP od operatora coinglass. Można to obchodzić ale lepiej wykupić API. Wersja Z API coinglass działająca to C:\Users\maxim\all_doc_pro\ALL-TradingAgent\Epic_v8_4_et_v33\EPIC_Agent_1_v0_6_5_stop_ok poprzedni katalog.

**# Proof of Concept**
1. dyt folderu projektu
Lokalizacja: .../Epic_Agent_1_v0_6_6_web_info_hunters

Przegląd struktury katalogów
agents/: Zawiera logikę „mózgu” (
strategist.py
,
consultants.py
). Dobre rozdzielenie zagadnień.
sensors/: Zawiera moduły wejściowe (
api_collector.py
,
vision.py
).
U

2. Uwaga:
api_collector.py
obecnie w dużym stopniu opiera się na strukturze API Coinglass. Konieczne będzie napisanie nowego adaptera (np. web_collector.py), aby zastąpić go bez naruszania
main.py

3. ore/: Zawiera
orchestrator.py
. Sugeruje to przejście w kierunku „architektury Hamiltona” wspomnianej w dokumentacji.
utils/: Funkcje pomocnicze.
json_cleaner.py
i
parsers.py
będą kluczowe dla podejścia scrapingowego.
utils/logger.py
: Niezbędne do debugowania nieuniknionych błędów scrapingowych.
Kluczowe obserwacje
Zgodność z planem działania: Struktura kodu (czujniki, rdzeń) jest zgodna z celami modułowości „Hamiltona” w
ROADMAP.md

4. Konfiguracja:
intel_config_v33.ini
i
config_manager.py
są dobrze skonfigurowane do obsługi przełączania między „trybem API” a „trybem scrapingowym” (zgodnie z sugestią w planie działania „zaznaczenie ptaszkiem”).
Trwałość danych:
market_data_latest.json
służy do przesyłania danych. To dobry punkt „interfejsu” — jeśli Twój nowy Scraper zapisuje w tym samym formacie JSON, reszta bota nie zauważy różnicy.

----------------
00:25 14/12/2025 udało się zrobić wiele poprawek i działa.
Zostało ustalić timingi dla przechodzenia na binance.

===============================================================================
===============================================================
=============================================
==========================
=======
=== 08/01/2026 === Zrobione opisy z Grok dla wersji v0.9.2 ===
=======
==========================
=============================================
===============================================================
===============================================================================
# PERCEPTRON ROADMAP & DEVELOPMENT JOURNAL

> "Stability > Functionality. System musi przetrwać błąd operatora i awarię sieci." – Doktryna Hamilton.

## ✅ UKOŃCZONE (do v0.9.2)
- HUD v1-2, FSM Core, Data Harvest (API/web/vision), Agents (full stack), Utils (parsers/signal), Tests (strategist/verify), Docs (architecture/prompts).

## 📅 v0.9.5 "HAMILTON STABLE" (Q1 2026)
- [ ] HUD v3: AI diodes, log panel.
- [ ] Signal v2: Emojis/multi-line.
- [ ] Scraping Fixes: Dynamic timing, error fallback.
- [ ] Persistence: Crash recovery from json.

## 🚀 v1.0 "AGI TRADER" (Q1-Q2 2026)
- [ ] Full API: Binance ccxt migration (no browser risks).
- [ ] Local ML: DeepSeek/Qwen dla EV/offline.
- [ ] Backtester: Simulate on history.jsonl (pandas).
- [ ] X Search: Real-time sentiment via tool.
- [ ] Risk: Auto-validation, dynamic TP/SL.

## v1.1 "MULTI-ASSET" (Q2 2026)
- [ ] Altcoins: ETH/SOL support.
- [ ] Multi-Exchange: Bybit/Bitmex.
- [ ] UI: Web dashboard (Flask).

## v2.0 "AUTONOMOUS AGI" (Q3-Q4 2026+)
- [ ] Self-Learning: Prompt updates via EV feedback.
- [ ] Cloud: AWS 24/7, watchdog.
- [ ] Community: Custom AI endpoints.

## Notatki Dev
- Audyty: Focus error handling/threading (Grok/Gemini).
- Inspiracje: Hamilton (watchdog), HFT (liquidity).
- Timeline: Monthly, 24h stability tests.

=====================================================
10:30 09/01/2026 poprawki w helpers.py

Calibration Logic Fix Plan
Problem
The ValidationWizard in 
utils/helpers.py
 has a mismatch with the execution logic in 
agents/agent_3.py
.

Missing Limit Buttons: 
agent_3.py
 tries to click bin_buy_limit and bin_sell_limit for Limit orders, but these keys are never calibrated.
Incorrect Market Buttons: 
agent_3.py
 uses bin_buy and bin_sell for Market orders. However, ValidationWizard calibrates these keys after switching to the Limit tab. If the layout differs between Market and Limit tabs, the clicks will miss or be inaccurate.
Solution
Modify 
utils/helpers.py
 -> 
CalibrationWizard
 class -> BINANCE_CONTROLS list.

New Step Sequence
... (Steps 1-9 unchanged) ...
Market Section:
bin_market (Tab)
bin_market_qty
bin_market_tp
bin_market_sl
[MOVE HERE] bin_buy (Market Buy Button) - Renamed description to indicate Market
[MOVE HERE] bin_sell (Market Sell Button) - Renamed description to indicate Market
Limit Section:
bin_limit (Tab)
bin_limit_price
bin_limit_qty
bin_limit_tp
bin_limit_sl
[ADD NEW] bin_buy_limit (Limit Buy Button)
[ADD NEW] bin_sell_limit (Limit Sell Button)
Total steps: 22 (was 20).

Verification
Review 
utils/helpers.py
 to ensure the list structure is correct.
The user will need to re-run calibration (which they seem to be doing anyway).

---

Naprawione. Zaktualizowałem utils/helpers.py.

Nowa sekwencja kalibracji (22 kroki):

Kroki 1-9 (bez zmian)
Sekcja MARKET:
Zakładka Market, Ilość, TP, SL
KUP (Market)
SPRZEDAJ (Market)
Sekcja LIMIT:
Zakładka Limit, Cena, Ilość, TP, SL
KUP (Limit) (Nowe!)
SPRZEDAJ (Limit) (Nowe!)
Teraz możesz bezpiecznie ponownie przeprowadzić kalibrację dla "Binance (Browser Tab)", a program zapisze poprawne koordynaty dla obu trybów LIMIT i MARKET. Otwórz kalibrację ponownie by dodać nowe koordynaty dla LIMIT i MARKET button. Do 10:30 09/01/2026 były dodane ręcznie w config_v33.ini

Koniec poprawek w helpers.py

Dla przypomnienia: tekst z setup.md:
- **[BINANCE_CONTROLS] etc.**: For A3 (Agent_3) on/off to function properly:
1. Ensure you are on the Binance FUTURES tab. 1920x1080 Zoom 50%
2. Enable/check the TP/SL button.
3. In "Cancel all orders", select "All" from the dropdown (options: "All", "LIMIT", "Stop-Limit"). Note: There is no default selection, but Binance remembers the choice after the first manual selection.
=========================================================

Feedback? Issue!
