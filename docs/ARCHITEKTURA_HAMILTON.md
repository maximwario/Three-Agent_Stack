ARCHITEKTURA_HAMILTON.md

"Nie chodziło tylko o to, by program działał. Chodziło o to, by system działał nawet wtedy, gdy program, sprzęt lub człowiek zawiodą." — Margaret Hamilton

1. Wstęp: Dziedzictwo "Stosu Kartek"
Ten dokument stanowi techniczną analizę rozwiązań zastosowanych w oprogramowaniu Apollo Guidance Computer (AGC), stworzonym przez zespół MIT. Słynne zdjęcie Hamilton stojącej obok stosu wydruków symbolizuje narodziny Software Engineering – dyscypliny, która traktuje kod jak system krytyczny, od którego zależy życie (w naszym przypadku: kapitał).

Celem jest adaptacja tych zasad do autonomicznego systemu tradingowego Perceptron.

2. THE EXECUTIVE: Asynchroniczny Zarządca (Priority Queue)
Lekcja z Apollo (Błąd 1201/1202)
Podczas lądowania Apollo 11, radar zalewał procesor przerwaniami. System nie zawiesił się, lecz "zrzucił balast". Jądro systemu (The Executive) posiadało kolejkę zadań. Gdy zabrakło zasobów, Executive usunął zadania o niskim priorytecie (ekran), by ratować zadania krytyczne (silnik).

Implementacja w Pythonie (Trading Bot)
Bot nie może działać liniowo. Musi klasyfikować zadania. Jeśli API laguje, bot przestaje rysować wykresy (GUI), ale za wszelką cenę wysyła Stop Loss.

Python

import queue
import time

# Hierarchia Priorytetów (Im mniej, tym ważniej)
PRIORITY_CRITICAL = 1  # Stop Loss, Zamknięcie pozycji, Margin Call
PRIORITY_MISSION  = 2  # Analiza sygnału, Otwarcie pozycji
PRIORITY_BACKGROUND = 3 # Logowanie, Screenshoty, Aktualizacja GUI

class HamiltonExecutive:
    def __init__(self):
        self.task_queue = queue.PriorityQueue()

    def add_task(self, priority, task_name, function):
        self.task_queue.put((priority, task_name, function))

    def run_cycle(self):
        # Symulacja przeciążenia (Błąd 1201):
        # Jeśli kolejka jest zapchana (>10 zadań), usuń śmieci (Low Priority)
        if self.task_queue.qsize() > 10:
            print("[ALARM 1201] EXECUTIVE OVERLOAD! Dropping background tasks.")
            self._flush_low_priority()

        while not self.task_queue.empty():
            priority, name, func = self.task_queue.get()
            print(f"Wykonuję: {name} [Prio: {priority}]")
            func()

    def _flush_low_priority(self):
        """Usuwa wszystko co nie jest CRITICAL"""
        temp_list = []
        while not self.task_queue.empty():
            item = self.task_queue.get()
            if item[0] == PRIORITY_CRITICAL:
                temp_list.append(item)
        for item in temp_list:
            self.task_queue.put(item)
3. RESTART PROTECTION: Pamięć Fazowa i "Hot Start"
Lekcja z Apollo (Ferrytowa Pamięć)
AGC resetował się w locie. Nie startował jednak od zera ("Cold Start"). Kluczowe zmienne (faza lotu, wektory) były zapisywane w pamięci nieulotnej. Po restarcie system sprawdzał: "Czy mam zapisaną fazę?". Jeśli tak, wykonywał Hot Start – wznawiał pracę dokładnie w miejscu przerwania.

Implementacja w Pythonie (Persistence)
Bot po restarcie (lub crashu) musi wiedzieć, czy ma otwartą pozycję, czytając plik mission_status.json, a nie zgadując z ekranu.

Python

import json
import os

STATUS_FILE = "mission_status.json"

def save_checkpoint(phase, position_data):
    """Zapisuje stan misji (odpowiednik zapisu na rdzeniach ferrytowych)"""
    state = {
        "PHASE": phase,  # np. "MONITORING", "IN_POSITION", "PANIC_SELL"
        "DATA": position_data, 
        "TIMESTAMP": time.time()
    }
    with open(STATUS_FILE, 'w') as f:
        json.dump(state, f)

def system_boot():
    """Procedura startowa: Rozróżnia Cold Start od Hot Start"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            last_state = json.load(f)
        
        # HOT START: Wznów, jeśli mieliśmy otwartą pozycję
        if last_state["PHASE"] == "IN_POSITION":
            print("!!! HOT START !!! Wykryto otwartą pozycję. Wznawiam zarządzanie.")
            return TradingEngine(state=last_state)
    
    # COLD START
    print("Cold Start. System czysty. Rozpoczynam nasłuch.")
    return TradingEngine(state=None)
4. HUMAN ERROR PROOFING: Problem "P01" (Verb 37)
Lekcja z Apollo
Córka Hamilton przypadkowo uruchomiła program startowy (P01) w trakcie lotu symulatorem. NASA zignorowała to, ale Hamilton dodała zabezpieczenie. Gdy astronauta Lovell (Apollo 8) popełnił ten błąd w rzeczywistości, kod go uratował. System sprawdzał Kontekst: "Czy jesteśmy w locie? Tak. Czy P01 ma sens? Nie. Ignoruj".

Implementacja w Pythonie (Context & Mouse Guard)
Bot musi bronić się przed Operatorem. Jeśli ruszysz myszką w trakcie pracy bota, bot musi to wykryć i przerwać działanie (PAUSE), zamiast walczyć o kursor.

Python

import pyautogui

def safe_click(x, y):
    # 1. Pobierz pozycję myszy PRZED ruchem bota
    start_pos = pyautogui.position()
    
    # 2. Ruch bota
    pyautogui.moveTo(x, y)
    
    # 3. WERYFIKACJA KONTEKSTU (Czy człowiek walczy?)
    # Jeśli kursor jest w innym miejscu niż bot go zostawił -> BŁĄD CZŁOWIEKA
    current_pos = pyautogui.position()
    if current_pos != (x, y):
        print("[ALARM P01] Wykryto ingerencję operatora! PRZERYWAM AKCJĘ.")
        return False # Nie klikaj!
        
    pyautogui.click()
    return True
5. PROGRAM "P00" (DOOZY): Nieśmiertelna Pętla Bezczynności
Lekcja z Apollo
Gdy komputer nie miał zadań nawigacyjnych, włączał się program P00. Nie "spał". W tle ciągle liczył sumy kontrolne pamięci i sprawdzał spójność systemu. Dzięki temu wiedział o awarii zanim ta wpłynęła na lot.

Implementacja w Pythonie (Active Idle)
Bot w nocy nie robi time.sleep(3600). W czasie "nudnym" powinien diagnozować otoczenie.

Python

def idle_routine():
    """Wykonywane, gdy nie ma sygnałów handlowych"""
    print("[P00] System IDLE. Rozpoczynam autodiagnostykę...")
    
    # 1. Sprawdź ping do giełdy
    latency = check_api_latency()
    if latency > 500:
        log_warning("Wysokie opóźnienie sieci!")
        
    # 2. Sprawdź wolne miejsce na dysku (na screenshoty)
    if disk_space() < 100_MB:
        cleanup_old_logs()
        
    # 3. Heartbeat
    update_heartbeat_file()
6. POODOO i BAILOUT: Hierarchia Błędów
Lekcja z Apollo
POODOO: Błąd miękki (np. złe dane). Ubij proces, jedź dalej.

BAILOUT: Błąd krytyczny (wyciek pamięci, zgubiona orientacja). Twardy restart oprogramowania.

Implementacja w Pythonie (Exception Handling)
Python

def main_loop():
    while True:
        try:
            run_cycle()
        
        except VisionError:
            # POODOO: Nie widzę przycisku. Trudno, spróbuję za chwilę.
            log("[POODOO] Vision Fail - Retrying next frame.")
            time.sleep(1)
            continue
            
        except ApiCriticalError:
            # BAILOUT: Klucz API odrzucony lub brak internetu.
            # Nie ma sensu próbować dalej. Zabij proces, zrestartuj modem/bota.
            log("[BAILOUT] CRITICAL FAILURE. INITIATING RESTART.")
            emergency_save_state()
            os.system("shutdown /r /t 1") # Opcja nuklearna
7. LITTLE OLD LADIES: Symulacja i Weryfikacja
Lekcja z Apollo
Kod był "tkany" ręcznie w fabrykach. Błąd był nieodwracalny. Dlatego testowano go na symulatorach, które udawały cały wszechświat, zanim wgrano go do rakiety.

Implementacja w Pythonie (Dry Run Simulator)
Zanim bot dostanie pieniądze, musi przejść test na "sucho".

Market Recorder: Nagrywaj sesję (ekran + dane API) do pliku.

Replay: Puszczaj nagranie botowi jako "kamera". Niech klika "na sucho". Jeśli przetrwa nagranie krachu – może dostać kapitał.

8. SANITY CHECKS (Filtracja Danych)
Lekcja z Apollo
Dane z sensorów przepuszczano przez filtry (np. Kalmana), by odrzucić odczyty niemożliwe fizycznie.

Implementacja w Pythonie
Jeśli OCR odczyta cenę BTC jako 9.00 (zamiast 90,000), bot nie może sprzedać.

Python

def validate_price(new_price, last_price):
    # Fizyka rynku: Cena nie zmienia się o 50% w 1 sekundę.
    change = abs(new_price - last_price) / last_price
    
    if change > 0.20: 
        print(f"[SANITY CHECK] Odrzucono anomalię: {new_price}. Używam poprzedniej ceny.")
        return last_price 
        
    return new_price
Dokument ten jest techniczną podstawą dla Agenta 1 (Orkiestratora) i Agenta 3 (Egzekutora).

Koniec podstaw które mamy w python.

Wcześniejsze rozwinięcie:

"Nie chodziło tylko o to, by program działał. Chodziło o to, by system działał nawet wtedy, gdy program, sprzęt lub człowiek zawiodą." — Margaret Hamilton

1. Wstęp: Dziedzictwo "Stosu Kartek"
Ten dokument stanowi techniczną analizę rozwiązań zastosowanych w oprogramowaniu Apollo Guidance Computer (AGC), stworzonym przez zespół MIT pod kierownictwem Margaret Hamilton. Słynne zdjęcie Hamilton stojącej obok stosu wydruków kodu źródłowego symbolizuje narodziny nowożytnej Inżynierii Oprogramowania (Software Engineering).

Cel: Adaptacja zasad "Safety-Critical" z misji księżycowych do autonomicznego systemu tradingowego (Projekt Perceptron).

2. THE EXECUTIVE: Asynchroniczny Zarządca Priorytetów
Teoria AGC
Komputer Apollo nie posiadał systemu operacyjnego w dzisiejszym rozumieniu. Posiadał "The Executive" – jądro systemu, które zarządzało ograniczonymi zasobami (czas procesora, 2KB RAM) w oparciu o sztywne priorytety.

Podczas lądowania Apollo 11 wystąpiły słynne błędy 1201 i 1202. Radar rendez-vous (niepotrzebny przy lądowaniu) zalał procesor przerwaniami.

Reakcja Standardowa: Zawieszenie systemu (Blue Screen).

Reakcja Hamilton: System wykrył przeciążenie (overload). Executive natychmiast "zabił" procesy o niskim priorytecie (aktualizacja wyświetlacza DSKY, obsługa radaru), aby zwolnić moc obliczeniową dla procesu o PRIORYTECIE 1 (utrzymanie ciągu silnika i orientacji lądownika).

Implementacja w Pythonie (Trading Bot)
Bot nie może wykonywać zadań liniowo (while True). Musi używać Kolejki Priorytetów. Jeśli API giełdy laguje, bot porzuca aktualizację GUI (Low Priority), by zdążyć wysłać Stop Loss (Critical Priority).

Python

import queue
import time

# Definicje Priorytetów (Im mniejsza liczba, tym ważniejsze)
PRIORITY_CRITICAL = 1  # Stop Loss, Margin Call
PRIORITY_MISSION  = 2  # Analiza rynku, Otwarcie pozycji
PRIORITY_BACKGROUND = 3 # Logi, Screenshoty, GUI update

class HamiltonExecutive:
    def __init__(self):
        self.task_queue = queue.PriorityQueue()

    def add_task(self, priority, task_name, function):
        self.task_queue.put((priority, task_name, function))

    def run_cycle(self):
        # Symulacja przeciążenia: Jeśli kolejka jest pełna, wykonaj tylko Critical
        if self.task_queue.qsize() > 10:
            print("[ALARM 1201] Przeciążenie! Odrzucam zadania tła.")
            self._flush_low_priority()

        while not self.task_queue.empty():
            priority, name, func = self.task_queue.get()
            print(f"Wykonuję: {name} (Priorytet: {priority})")
            func()

    def _flush_low_priority(self):
        # Usuwa wszystko co nie jest CRITICAL
        temp_list = []
        while not self.task_queue.empty():
            item = self.task_queue.get()
            if item[0] == PRIORITY_CRITICAL:
                temp_list.append(item)
        for item in temp_list:
            self.task_queue.put(item)
3. RESTART PROTECTION: Pamięć Fazowa
Teoria AGC
W systemach krytycznych "reset" nie może oznaczać startu od zera. AGC posiadał tzw. Restart Protection. Kod był podzielony na "Fazy" (Phases).

Gdy program wchodził w fazę lądowania, zapisywał numer fazy i kluczowe wektory w pamięci nieulotnej (ferrytowej).

Gdy następował reset (np. zanik napięcia), procedura startowa sprawdzała rejestr fazy. Jeśli był tam zapis, wykonywano "Hot Start" – powrót do ostatniego punktu w milisekundach, bez utraty danych nawigacyjnych.

Implementacja w Pythonie (Mission Persistence)
Bot po restarcie (lub crashu) musi wiedzieć, czy ma otwartą pozycję, czytając plik mission_status.json, a nie analizując ekran (bo ekran może być mylący/zlagowany).

Python

import json
import os

STATUS_FILE = "mission_status.json"

def save_checkpoint(phase, position_data):
    """Zapisuje stan misji do 'pamięci nieulotnej' (dysku)"""
    state = {
        "PHASE": phase,  # np. "MONITORING", "IN_POSITION", "CLOSING"
        "DATA": position_data, # entry_price, size, stop_loss
        "TIMESTAMP": time.time()
    }
    with open(STATUS_FILE, 'w') as f:
        json.dump(state, f)

def system_boot():
    """Procedura startowa (Hot vs Cold Start)"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            last_state = json.load(f)
        
        # HOT START
        if last_state["PHASE"] == "IN_POSITION":
            print("!!! HOT START !!! Wykryto otwartą pozycję. Wznawiam zarządzanie.")
            return TradingEngine(state=last_state)
    
    # COLD START
    print("Cold Start. Inicjalizacja czystego systemu.")
    return TradingEngine(state=None)
4. ODPORNOŚĆ NA BŁĄD LUDZKI (Human Error Proofing)
Teoria AGC
Inspiracją była córka Hamilton, Lauren, która w symulatorze uruchomiła program startowy P01 w trakcie lotu, co spowodowało awarię. NASA zignorowała to ryzyko ("astronauci są wyszkoleni"). W rzeczywistości, podczas misji Apollo 8, astronauta Jim Lovell popełnił ten błąd.

Rozwiązanie Hamilton: Kod sprawdzał kontekst. Jeśli statek jest w locie (mierzyły to akcelerometry), komenda P01 (Start) była ignorowana lub wymagała potwierdzenia "Verb 50 Noun 25" (Please Perform/Check).

Implementacja w Pythonie (Context Validation)
Bot nie może ufać kliknięciom w ciemno. Przed każdą akcją musi sprawdzić Kontekst.

Python

def execute_order(action):
    # 1. Sprawdź KONTEKST RYNKU (Czy giełda działa? Czy dane są świeże?)
    if not is_data_fresh():
        print("[ERROR] Dane starsze niż 5s. BLOKADA ZLECENIA.")
        return

    # 2. Sprawdź KONTEKST PORTFELA (Zabezpieczenie P01)
    # Jeśli mamy już pozycję, a komenda to "OPEN LONG" -> Ignoruj (Chronione przed dublowaniem)
    current_state = load_mission_state()
    if current_state["active_position"] and action == "OPEN_LONG":
        print("[SAFETY] Odrzucono OPEN_LONG: Pozycja już otwarta!")
        return

    # 3. Wykonaj
    tactician.click(action)
5. POODOO i BAILOUT: Hierarchia Błędów
Teoria AGC
AGC miał zdefiniowane procedury radzenia sobie z błędami:

ALARM / POODOO: Błąd "miękki" (np. złe dane z radaru). System ubijał tylko wadliwy proces, reszta działała.

BAILOUT: Błąd krytyczny (np. wyciek pamięci, utrata wątku). System wykonywał natychmiastowy restart oprogramowania, porzucając wszystko oprócz zmiennych krytycznych.

Implementacja w Pythonie (Exception Handling)
Bot nie może po prostu zrobić print("Error"). Musi rozróżnić błąd odczytu OCR od błędu API.

Python

def main_loop():
    while True:
        try:
            # Próba wykonania cyklu
            run_cycle()
        
        except VisionError:
            # POODOO: Błąd miękki (nie widzę przycisku). Pomiń ten cykl, spróbuj za chwilę.
            log("Vision Fail - Retrying...")
            time.sleep(1)
            continue
            
        except ApiCriticalError:
            # BAILOUT: Błąd krytyczny (API odrzuciło klucze / brak neta).
            # Wymusza restart modułu sieciowego lub całego bota.
            log("!!! API FAILURE - BAILOUT !!!")
            emergency_save_state()
            restart_program()
6. SANITY CHECKS: Filtracja Danych (Kalman Style)
Teoria AGC
Dane z sensorów w kosmosie bywają błędne. AGC nie przyjmował ich "na wiarę". Używano filtrów (np. Kalmana), by ocenić, czy odczyt jest fizycznie możliwy.

Implementacja w Pythonie (Input Sanitation)
OCR często myli cyfry (np. 8 z B). Bot musi odrzucić odczyt, który nie ma sensu rynkowego.

Python

def validate_price(new_price, last_price):
    # Zasada: Bitcoin nie zmienia ceny o 50% w ciągu 1 sekundy.
    change_pct = abs(new_price - last_price) / last_price
    
    if change_pct > 0.20: # Jeśli zmiana > 20%
        print(f"[SANITY CHECK] Odrzucono cenę {new_price}. Zbyt duża zmiana.")
        return last_price # Zwróć starą (bezpieczną) cenę
        
    return new_price
7. WNIOSKI KOŃCOWE DLA PROJEKTU PERCEPTRON
Stosując Architekturę Hamilton, Twój system przestaje być "skryptem", a staje się "autonomicznym systemem sterowania".

Immortal Loop: Główna pętla nigdy nie gaśnie (chyba że fizycznie padnie zasilanie).

State Persistence: Bot zawsze wie, co robił przed resetem.

Active Defense: Bot aktywnie broni się przed błędnymi danymi (OCR) i błędnymi komendami (Human Error).

Dokument sporządzony przez Agenta 2 na podstawie analizy historycznej kodu LUMINARY.

Koniec wcześniejszego rozwinięcia.

Wpis PLAISANT na ten temat na forum wykop.pl
https://wykop.pl/ludzie/plaisant
https://wykop.pl/wpis/84202857/chce-zaglebic-sie-w-software-engineering-mam-w-pam

@plaisant 6 godz. i 17 min temu 06:63 10/12/2025
Chcę zagłębić się w Software Engineering. Mam w pamięci Panią Margaret Hamilton która trzyma stos kartek papieru.. Pomyślałem, że przyjrzę się temu co jest w tym kodzie.

Napisałem prosty program który działa w pętli a wypadałby by wprowadzić "Maszynę Stanów" z priorytetami, wzorowana na AGC.

Z dwóch działających prototypów powstał wczoraj projekt który ma teraz 12 skryptów w .py 50 funkcji, działa poprawnie. Teraz dużo łatwiej zapanować nad kodem. To moje pierwsze użycie Antigravity i to wynosi programowanie na inny level. Gdy myślę o wprowadzaniu ulepszeń to widzę to zdjęcie, bo pamiętam dlaczego zatrudniono tą Panią w MIT.

Kod, który uratował lądowanie na Księżycu. Jak Margaret Hamilton wymyśliła inżynierię oprogramowania.

Wszyscy znamy to zdjęcie. Margaret Hamilton stojąca obok sterty wydruków kodu źródłowego, która jest wyższa od niej. Ale mało kto wie, co było W ŚRODKU tego kodu. A to, co tam było, to genialna architektura, której dzisiaj brakuje w 90% nowoczesnych aplikacji.

1. "Zrób tak, żeby się nie dało zepsuć" (Human Error) Margaret dołączyła do projektu, gdy software był traktowany po macoszemu. Jej pierwsze zadanie? Napisać program, który wykrywa błędy. Legenda głosi, że inspiracją była jej córka, Lauren. Podczas zabawy w symulatorze Lauren nacisnęła przycisk "P01" (start przed startem) w trakcie lotu. System się wywalił. Szefostwo NASA powiedziało: "Astronauci są wyszkoleni, nie zrobią tego". Margaret mimo to dodała zabezpieczenie: "Jeśli jesteś w locie, ignoruj komendę P01". Podczas misji Apollo 8, astronauta Jim Lovell... przez pomyłkę nacisnął P01. Dzięki kodowi Hamilton, system nie zresetował nawigacji, a jedynie pozwolił na szybkie przywrócenie danych.

2. Asynchroniczny Egzekutor (The Executive) To jest najważniejsza rzecz. Komputer Apollo (AGC) miał zaledwie 4KB pamięci RAM (Erasable Memory) i 72KB ROM (Rope Memory). Nie mógł robić wszystkiego naraz. Hamilton i jej zespół (m.in. Hal Laning) zaprojektowali system operacyjny oparty na priorytetach.

Wyobraź sobie lądowanie Apollo 11. Słynny alarm "1201" i "1202". Co się stało? Radar dokujący (niepotrzebny przy lądowaniu) był włączony i zalewał procesor tysiącami przerwań na sekundę. Procesor był przeciążony w 100%. Normalny komputer (jak Windows Blue Screen) by się zawiesił. Lądownik by się rozbił. Ale kod Hamilton działał inaczej. Miał "The Executive". Program powiedział: "Nie mam zasobów na wszystko. Wywalam zadania o niskim priorytecie (aktualizacja wyświetlacza, obsługa radaru), ale za wszelką cenę utrzymuję zadania o PRIORYTECIE 1 (utrzymanie silnika, sterowanie lotem)".

Alarm 1201 nie oznaczał "Zepsułem się". Oznaczał: "Jestem przeciążony, więc resetuję rzeczy nieistotne, żebyś przeżył".

#programowanie #ciekawostki #softwareengineering

---
plaisant - Chcę zagłębić się w Software Engineering. Mam w pamięci Panią Margaret Ham...

źródło: AGC_Software_Engineering_Margaret_Hamilton

Hellicon
Hellicon
6 godz. i 7 min temu via Android
@plaisant Przecież Armstrong musiał wyłączyć to gówno i lądować ręcznie xD

plaisant
plaisant
6 godz. i 1 min temu via Wykop
@Hellicon: poważnie? :D Jeśli to wystąpiło to natkne się na to, bo zamierzam o tym poczytać. A czy to nie było tak, że system przeciążył się i zredukował wszystko by oddać moc procesora do obliczanie ciągu silników?

Hellicon
Hellicon
5 godz. i 53 min temu via Android
@plaisant System się przeciążył od danych i ocipiał. Zwyczajnie wyłączyli i lądowanie bylo reczne bo nie było czasu, paliwa mieli na sekundy. Na kanale ToJakiśKosmos Kuba kiedyś opowiadał. Ogólnie to twoja opowieść o tej pani jest trochę naiwna. Każdy programista musi przewidywać błędy ale przy skomplikowanym kodzie to jest po prostu niemożliwe i możesz tylko wypisywać kody bledów na serialu.

plaisant
plaisant
5 godz. i 47 min temu via Wykop
@Hellicon: dzięki za ten komentarz. Nie zanam się na programowaniu a mam bardzo dobry swój przykład kodu który ze spagetti przerodził się w 12 plików w Py i jest dużo bardziej czytelny i łatwiej o zmiany. Zainteresował mnie sam kod tej Pani. Ona to napisała tak by było odporne na wszystko. Nastąpił błąd ludzi który ona przewidziała w kodzie i uwzględniła to. To pasuje idealnie do mojego projektu. W jej kodzie jest podanych bardzo dużo przykłądów na "serce" i w moim przypadku maszyna stanów to ciągłe działanie, a teraz skrypt śpi ¯\(ツ)/¯ szukam jakiejś inspiracji i jej kod dobrze się tu wpisuje w teorii.

plaisant
plaisant
5 godz. i 36 min temu via Wykop
@Hellicon: Np. AI w moim projekcie potrzebuje od czasu do czasu inspiracji, motywacji, można ją wspomagać, lub bardziej inspirować ale też np przeszkadzać i musi być na to odporna. Zastanawiam się jak włożyć to w mój projekt, by integracja w system niczego nie spieprzyła. Samo dotknięcie klawiatury gdy bot działa to już dużo się dzieje. To musi być w zasadzie sysyem który ciągle pracuje na pewnych twardych danych tak jak w przypadku kodu AGC po za tym co dzieje się w kodzie teraz.

https://wykop.pl/wpis/84202857/chce-zaglebic-sie-w-software-engineering-mam-w-pam

Margaret Hamilton i lądowanie na Księżycu
Utworzono za pomocą modelu 3 Pro 9 grudnia 2025 10:48
Opublikowano: 10 grudnia 2025 01:46
Znasz historię pewnej pani która napisała w asemblerze bardzo dużo kartek papieru do jakiejś sondy kosmicznej. Czy możesz mi to streścić?

Tak, z pewnością chodzi Ci o Margaret Hamilton i jej kluczową rolę w programie Apollo.

To jedna z najbardziej ikonicznych historii w dziejach informatyki. Choć nie była to "sonda" w sensie bezzałogowym, lecz lądownik załogowy (Apollo 11), to opis idealnie pasuje do słynnego zdjęcia i jej pracy.

Oto streszczenie tej historii:

1. Kim jest Margaret Hamilton?
W latach 60. Margaret Hamilton była dyrektorką działu inżynierii oprogramowania w MIT Instrumentation Laboratory. Jej zespół był odpowiedzialny za stworzenie oprogramowania pokładowego dla Apollo Guidance Computer (AGC) – komputera, który miał zabrać ludzi na Księżyc i bezpiecznie sprowadzić ich z powrotem.

2. Słynne zdjęcie "stosu kartek"
Obraz, który masz w głowie, to prawdopodobnie słynna fotografia z 1969 roku.

Co na nim widać: Margaret stoi obok stosu wydruków papierowych, który jest równy jej wzrostowi (a nawet nieco wyższy).

Co to za papier: To nie notatki, ale wydruk kodu źródłowego systemu operacyjnego i aplikacji dla modułu dowodzenia oraz lądownika księżycowego.

Język: Kod był napisany w asemblerze AGC. W tamtych czasach programy były "tkane" w pamięci (tzw. Core Rope Memory) – fizycznie przewlekano druty przez rdzenie magnetyczne: drut przechodzący przez rdzeń to 1, a omijający go to 0.

Ciekawostka: Hamilton ukuła termin "Inżynieria Oprogramowania" (Software Engineering), aby nadać swojej dziedzinie taki sam prestiż i rygor, jaki miały inżynieria sprzętowa czy lotnicza.

3. Jak ten kod uratował lądowanie na Księżycu?
Najważniejszy moment tej historii wydarzył się podczas lądowania Apollo 11, zaledwie 3 minuty przed dotknięciem powierzchni Księżyca.

Problem: Komputer pokładowy nagle zaczął wyświetlać błędy 1201 i 1202. Oznaczało to, że procesor był przeciążony (dostawał za dużo danych z radaru rendez-vous, który został omyłkowo włączony).

Reakcja oprogramowania: System zaprojektowany przez zespół Hamilton był genialny w swojej odporności. Zamiast się zawiesić (co oznaczałoby przerwanie misji i potencjalną śmierć astronautów), oprogramowanie wykryło przeciążenie.

Rozwiązanie: System zaczął "zabijać" procesy o niskim priorytecie (np. odświeżanie wyświetlacza dla astronautów), aby zachować moc obliczeniową dla zadań krytycznych – czyli sterowania silnikami i utrzymania lądownika w poziomie.

Dzięki temu kodowi kontrola lotu w Houston mogła wydać komendę "GO", a Neil Armstrong i Buzz Aldrin wylądowali bezpiecznie.

Podsumowując
Pani ze zdjęcia to Margaret Hamilton. Stos papieru to kod w asemblerze dla programu Apollo. Jej praca nie tylko pozwoliła ludziom wylądować na Księżycu, ale zdefiniowała nowoczesne podejście do tworzenia niezawodnego oprogramowania.

Czy chciałbyś, abym wyjaśnił dokładniej, na czym polegała specyfika pamięci "tkanej" (Core Rope Memory), której używano w tamtych komputerach?

Tak i wyjaśnij jeszcze odporność tego kodu. Mamy projekt bota tradingowwgo który klika na ekranie i robi Screen shoty. Chcemy by był odporny jak ten kod w asemblerze. Opowiedz mi o tym więcej jonkonstruowalem również bardzo odpornego bota do pokera.

To fascynujące wyzwanie. Skoro zbudowałeś odpornego bota do pokera, to znaczy, że rozumiesz już koncepcję zarządzania stanem gry (state management). Trading jest jednak o tyle trudniejszy, że – w przeciwieństwie do pokera – jest systemem czasu rzeczywistego, gdzie błędy "zewnętrzne" (lagi, zmiany UI, błędy OCR) są normą, a nie wyjątkiem.

Oto jak działała "niezniszczalność" kodu Margaret Hamilton i jak możesz przenieść te zasady do architektury swojego bota tradingowego.

1. Pamięć tkana (Core Rope Memory) – Sprzętowa niezniszczalność
Zacznijmy od tego, o co pytałeś. Kod w AGC nie był zapisany na dysku magnetycznym, który mógłby się rozmagnesować, ani w pamięci RAM, którą błąd programu mógłby nadpisać.

Jak to działało: Programy były dosłownie "wdziergane" w rdzenie ferrytowe. Jeśli drut przechodził przez pierścień, było to 1. Jeśli przechodził obok, było to 0.

Efekt: Pamięć była fizycznie tylko do odczytu (ROM). Żaden błąd w kodzie ("wyciek pamięci", "buffer overflow") nie mógł zepsuć systemu operacyjnego, bo fizyka na to nie pozwalała. Aby zmienić kod, trzeba było fizycznie spleść nowy moduł.

Wniosek dla Twojego bota: W nowoczesnym systemie nie będziesz "tkał drutów", ale możesz zastosować zasadę Immutability (Niezmienności).

Niech Twój bot działa w kontenerze (np. Docker), który jest "czysty" przy każdym starcie.

Logika decyzyjna powinna być oddzielona od stanu. Jeśli bot się zawiesi, restartujesz go, a on pobiera stan z zewnętrznej bazy (nie z własnej pamięci RAM).

2. Architektura "The Executive" – Asynchroniczność i Priorytety
To jest klucz do sukcesu Apollo 11 (błędy 1201/1202). System operacyjny Hamilton nie był prostą pętlą while(true). Był to planista zadań (scheduler) oparty na priorytetach.

Kiedy radar zaczął zalewać komputer śmieciowymi danymi, "Executive" zauważył, że brakuje mu czasu procesora (cykli) na wykonanie wszystkiego.

Co zrobił system: "Okej, nie mam czasu na odświeżanie ekranu dla Neila Armstronga (niski priorytet). Przestaję to robić. Ale muszę obliczać ciąg silnika, żeby się nie rozbili (krytyczny priorytet)."

Zasada Graceful Degradation: System działał dalej, "porzucając" mniej ważne funkcje, zamiast się zawiesić (Blue Screen of Death).

Wniosek dla Twojego bota (Bot vs. GUI/OCR): Twój bot tradingowy operujący na zrzutach ekranu jest podatny na "zalanie danymi" (np. szybkie ruchy rynku, wyskakujące okienka).

Zastosuj kolejkę priorytetów:

CRITICAL: Obsługa otwartej pozycji (Stop Loss / Take Profit).

HIGH: Wykrycie sygnału wejścia.

LOW: Logowanie statystyk, robienie ładnych screenów dla użytkownika.

Jeśli bot wykryje, że OCR (rozpoznawanie tekstu) zajmuje za dużo czasu (lag), powinien pominąć analizę nowych wykresów, a skupić się tylko na sprawdzeniu, czy nie trzeba awaryjnie zamknąć pozycji.

3. Restartability (Ochrona przed resetem)
Kod Apollo był zaprojektowany tak, że mógł się zrestartować w ułamku sekundy i "wiedział", gdzie jest. Miał tzw. "Restart Protection". Kluczowe zmienne (pozycja, prędkość) były zapisywane w specjalnej pamięci kasowalnej przy każdej zmianie. Gdy komputer się resetował (co zdarzyło się kilka razy podczas misji!), wstawał i mówił: "Okej, jestem w fazie lądowania, mam taką prędkość, lecimy dalej". Nie zaczynał od "Start Windows".

Wniosek dla Twojego bota: Boty "klikające" często gubią się, gdy np. platforma tradingowa się zawiesi lub zminimalizuje.

Stateless logic: Twój bot po restarcie musi umieć odczytać stan z ekranu i zrozumieć sytuację bez pamiętania "co robił przed chwilą".

Zadaj sobie pytanie: Gdybym wyłączył prąd i włączył go za 10 sekund, czy bot otworzy drugą pozycję (błąd), czy rozpozna, że jedna już jest otwarta?

4. Weryfikacja danych (Kalman Filtering / Sanity Checks)
W Apollo dane z radarów nie były przyjmowane "na wiarę". Były filtrowane przez Filtr Kalmana, który estymował, czy odczyt ma sens fizyczny.

Wniosek dla Twojego bota (OCR jest omylny): OCR często myli 8 z B, 0 z O albo 1 z 7. Jeśli Twój bot odczyta cenę Bitcoina jako 900,000 zamiast 90,000, może podjąć fatalną decyzję.

Sanity Check: Jeśli cena zmieniła się o 50% w ciągu 1 sekundy – to prawdopodobnie błąd odczytu, a nie krach giełdowy. Ignoruj taką klatkę.

Redundancja: Nie podejmuj decyzji na podstawie 1 screenshota. Decyzja = "Buy" tylko jeśli 2 z 3 ostatnich klatek pokazują ten sam sygnał.

Podsumowanie – Jak zbudować "Pancernego Bota"?
Skoro robiłeś bota do pokera, wiesz, że tam stan jest dyskretny (są tury). W tradingu stan jest płynny. Aby uzyskać odporność klasy Apollo:

Odseparuj "Oczy" (OCR/Screen) od "Mózgu" (Logika) i "Rąk" (Klikanie). Awaria OCR nie powinna wywalać logiki zarządzania kapitałem.

Zaimplementuj "Heartbeat" (Bicie serca). Proces nadrzędny (Watchdog), który zabija i restartuje bota, jeśli ten nie odpowie w ciągu 200ms.

Idempotentność akcji: Upewnij się, że jeśli bot spróbuje kliknąć "Sprzedaj" 5 razy z rzędu (bo ma laga), to system nie sprzeda 5 razy więcej, niż posiadasz.

To podejście inżynieryjne, a nie "skrypciarskie". Właśnie to odróżniało zespół Margaret Hamilton od ówczesnych "koderów".

Opowiedz mi więcej, jak najwięcej o tym kodzie. Chciałbym wiedzieć dużo więcej.

To fascynujący temat. Kod, o którym mowa, to oprogramowanie dla Apollo Guidance Computer (AGC). Program dla lądownika księżycowego (LM) nosił nazwę kodową LUMINARY, a dla modułu dowodzenia (CM) – COLOSSUS.

Aby zbudować bota tradingowego o takiej odporności, musisz zrozumieć filozofię inżynierii, która stała za tym kodem. To nie była tylko kwestia "dobrego napisania funkcji", ale architektury przetrwania.

Oto głęboka analiza techniczna rozwiązań z Apollo i ich przełożenie na Twojego bota.

1. Architektura "The Executive" (Zarządca Czasu)
AGC nie posiadał systemu operacyjnego w dzisiejszym rozumieniu (jak Windows czy Linux). Posiadał coś, co nazywano The Executive. Był to hybrydowy system zarządzania zadaniami, który łączył dwa podejścia:

Cooperative Multitasking (Wielozadaniowość kooperacyjna): Zadania długotrwałe (np. obliczanie orbity) dobrowolnie oddawały procesor, gdy kończyły pewien etap obliczeń.

Priority-Interrupt Driven (Sterowanie przerwaniami): Zadania krytyczne (np. sygnał "silnik włączony/wyłączony" lub naciśnięcie klawisza przez astronautę) przerywały wszystko inne natychmiast.

Jak to działało (Mechanizm Job Area): Pamięć RAM była mikroskopijna (2KB). Executive dzielił zadania na "Jobs". Każdy Job miał przypisany priorytet. Gdy pojawił się błąd 1202 (przeciążenie), Executive spojrzał na kolejkę zadań i zobaczył:

Obliczanie wektora lądowania (Priorytet: WYSOKI)

Obsługa radaru rendez-vous (Priorytet: ŚREDNI - to generowało spam danych)

Aktualizacja wyświetlacza DSKY (Priorytet: NISKI)

System bezlitośnie wyrzucił zadania 2 i 3 z kolejki, zwalniając pamięć i czas procesora dla zadania nr 1. To nie był "crash". To było świadome odrzucenie balastu.

Lekcja dla Twojego bota: Twój bot nie powinien przetwarzać wszystkiego "jak leci". Podziel logikę na wątki o różnych priorytetach.

Thread A (Critical): Obsługa API giełdy (wysyłanie zleceń). Jeśli CPU skacze do 100%, ten wątek ma pierwszeństwo.

Thread B (Normal): Analiza obrazu (OCR). Jeśli są lagi, pomiń klatki.

Thread C (Low): UI, logi, zapisywanie screenshotów na dysk. W razie problemów – zabij ten wątek.

2. Wirtualna Maszyna w 1969 roku (Interpreter)
To jeden z najbardziej niesamowitych faktów. AGC był komputerem 15-bitowym (plus bit parzystości). Instrukcje asemblera były bardzo proste (dodaj, odejmij, skocz). Były świetne do sterowania przekaźnikami, ale beznadziejne do skomplikowanej matematyki wektorowej potrzebnej w kosmosie (nawigacja trójwymiarowa).

Co zrobił zespół Hamilton? Napisali wirtualną maszynę. Stworzyli zestaw "pseudokodu" zwanego INTERPRETER. Programiści pisali skomplikowane równania w specjalnym języku wyższego poziomu, a kod maszynowy AGC tłumaczył je w locie na proste instrukcje. Było to wolniejsze, ale pozwalało upchnąć niesamowicie złożoną logikę w małej pamięci.

Lekcja dla Twojego bota: Oddziel warstwę "wykonawczą" (klikacza) od warstwy "analitycznej" (mózgu). Niech Twój "Mózg" operuje na wysokim poziomie abstrakcji (np. "Strategia: Bearish Engulfing"), a "Interpreter" (Driver) tłumaczy to na konkretne koordynaty myszki (X: 1240, Y: 800). Jeśli zmieni się rozdzielczość ekranu lub interfejs giełdy, zmieniasz tylko Driver, a Mózg pozostaje ten sam.

3. Restart Protection (Ochrona przed resetem)
Wspomniałem o tym wcześniej, ale wejdźmy w szczegóły. AGC miał mechanizm Checkpointów. Każdy długi program był podzielony na etapy (Phases). Gdy program wchodził w "Fazę 5: Podejście końcowe", zapisywał numer 5 w specjalnym rejestrze pamięci ferrytowej (nieulotnej).

Gdy komputer się resetował (trwało to około 1 sekundy), procedura startowa sprawdzała ten rejestr:

Czy rejestr jest pusty? -> Uruchom procedurę startową "na zimno" (Cold Start).

Czy jest tam numer 5? -> Uruchom procedurę "na gorąco" (Hot Start) i skocz natychmiast do Fazy 5, przywracając ostatnie znane zmienne wektorów.

Dlatego astronauci widzieli, jak ekran gaśnie i zapala się ponownie, ale silnik nie przestawał działać, a nawigacja wracała dokładnie tam, gdzie była.

Lekcja dla Twojego bota: Twój bot musi być bezstanowy (stateless) lub posiadać trwały stan (persistent state). Zapisuj stan każdej transakcji w lokalnej bazie danych (np. SQLite) zanim wyślesz kliknięcie.

Sekwencja:

Decyzja: KUP.

Zapis do DB: "Status: PRÓBA KUPNA".

Kliknięcie myszką.

Weryfikacja ekranu.

Zapis do DB: "Status: KUPIO NO". Jeśli bot padnie po punkcie 3, po restarcie odczyta z bazy "PRÓBA KUPNA", sprawdzi na ekranie, czy pozycja jest otwarta i zaktualizuje status, zamiast klikać "KUP" drugi raz.

4. DSKY i Interfejs Czasownik-Rzeczownik (Verb-Noun)
Astronauci komunikowali się z komputerem za pomocą panelu DSKY (Display and Keyboard). Używali składni: VERB (Co zrobić) + NOUN (Na czym).

Przykłady:

Verb 16 (Monitoruj dziesiętnie) Noun 20 (Kąty IMU - inercyjne).

Verb 37 (Zmień program) Noun 01 (Pre-launch).

To narzucało żelazną strukturę komunikacji. Nie było miejsca na niejednoznaczność.

Lekcja dla Twojego bota: Skoro Twój bot "patrzy" na ekran, musi rozumieć interfejs w sposób ustrukturyzowany. Zdefiniuj "Gramatykę" interfejsu Twojej platformy tradingowej. Zamiast szukać "jakiegokolwiek zielonego przycisku", niech bot szuka konkretnych par:

Kontekst (Noun): Okno zlecenia.

Akcja (Verb): Przycisk zatwierdź. Jeśli bot widzi przycisk "Zatwierdź", ale nie widzi "Okna zlecenia" (kontekstu), nie wolno mu kliknąć. To chroni przed klikaniem w reklamy czy pop-upy.

5. Obsługa błędów sprzętowych: Hard-wired Logic
W AGC istniały pewne funkcje, które nie były programem, ale były "wdrutowane" na sztywno. Np. jeśli oprogramowanie weszło w nieskończoną pętlę i nie wysłało sygnału "żyję" do specjalnego układu w ciągu określonego czasu, układ sprzętowy automatycznie resetował komputer. To słynny Watchdog Timer.

Lekcja dla Twojego bota: Napisz oddzielny, malutki skrypt (Watchdog), który monitoruje głównego bota. Główny bot musi co 5 sekund aktualizować plik heartbeat.txt obecną datą. Jeśli Watchdog zauważy, że plik jest starszy niż 15 sekund -> Zabija proces bota, robi screenshota (do debugowania) i uruchamia go ponownie.

Podsumowanie techniczne "Stylu Apollo" dla Twojego projektu:
Defensive Programming: Zakładaj, że dane wejściowe (OCR) są błędne, dopóki nie zostaną zweryfikowane (np. średnia z 3 klatek).

Fail-Fast & Recovery: Lepiej, żeby bot się zrestartował i wczytał stan z dysku, niż żeby działał w niestabilnym stanie pamięci.

Graceful Degradation: Przy braku zasobów (lagi), odcinaj funkcje pomocnicze (wykresy), ratuj funkcje krytyczne (Stop Loss).

Audit Logs: Kod Apollo logował wszystko. Twój bot powinien zapisywać nie tylko co zrobił, ale dlaczego (zrzut zmiennych decyzyjnych).

Czy chcesz, abym napisał dla Ciebie pseudokod takiej struktury "Main Loop" z obsługą priorytetów i Watchdoga?

Nie. Chcę jeszcze więcej posłuchać o tym.

To fantastycznie. Skoro chcesz wejść w "trzewia" tego systemu, zanurkujmy głębiej. To, co zaraz przeczytasz, to czysta inżynieria ekstremalna. Kod Apollo to nie tylko algorytmy nawigacji, to podręcznik przetrwania dla maszyn.

Oto szczegóły, o których rzadko się mówi poza kręgami pasjonatów retro-computingu i inżynierii systemów krytycznych.

1. Program "P00" (P-Zero) i pętla bezczynności
Większość programistów piszących boty myśli: "Jak nie ma nic do roboty, to sleep(100)". W Apollo marnowanie cykli było grzechem.

Gdy komputer nie miał żadnych zadań nawigacyjnych (np. podczas spokojnego lotu na orbitę), włączał się program P00 (Doozy).

Co robił: Nie spał. W tle wykonywał ciągłą autodiagnostykę.

Sumy kontrolne: Przeliczał sumy kontrolne banków pamięci stałej (ROM), aby sprawdzić, czy któryś z rdzeni ferrytowych nie uległ uszkodzeniu pod wpływem promieniowania kosmicznego.

Ratchet (Zapadka): Jeśli wykrył błąd, zapalał lampkę ostrzegawczą "Operator Error" lub "Restart".

Lekcja dla Twojego bota: Twój bot, gdy "nic nie robi" (np. w nocy, gdy giełda jest spokojna), nie powinien spać. Powinien:

Sprawdzać spójność bazy danych.

Pingować API giełdy, by mierzyć opóźnienia.

Sprawdzać ilość wolnego miejsca na dysku (na screenshoty). Bot musi wiedzieć, że jest "chory", zanim przyjdzie moment krytyczny.

2. Słynne procedury błędów: POODOO i BAILOUT
To nie żart. Tak nazywały się oficjalne etykiety (labels) w kodzie źródłowym Asemblera AGC do obsługi błędów krytycznych. Pokazują one hierarchię radzenia sobie z katastrofą.

ALARM / POODOO: Uruchamiane, gdy zadanie nie mogło zostać wykonane (np. dzielenie przez zero, błędne dane wejściowe).

Działanie: Ubij tylko ten konkretny proces, wyślij kod błędu na wyświetlacz (np. 1202), ale pozwól reszcie systemu działać. To jest "miękki błąd".

BAILOUT: To była opcja nuklearna. Uruchamiana, gdy przepełniła się pamięć albo system zgubił wątek.

Działanie: Natychmiastowy restart oprogramowania. Zapomnij o tym, co robiłeś w pamięci operacyjnej, wczytaj "Core Set" (najważniejsze zmienne) i wstań od nowa.

Lekcja dla Twojego bota: Stwórz hierarchię błędów.

Jeśli OCR źle odczyta cenę -> POODOO (zignoruj klatkę, loguj błąd).

Jeśli bot nie może kliknąć przycisku "Zamknij pozycję" przez 10 sekund -> BAILOUT (Zabij proces przeglądarki, zabij proces bota, uruchom wszystko od zera). Czasem tylko twardy reset ratuje kapitał.

3. "Little Old Ladies" – Kompilacja fizyczna
To jest aspekt sprzętowy, który determinował jakość kodu. Kod Margaret Hamilton po zatwierdzeniu był wysyłany do fabryki Raytheon.

Tam pracowały tkaczki (nazywane pieszczotliwie LOL – Little Old Ladies), często byłe pracownice przemysłu tekstylnego.

Dostawały one wydruk binarny.

Używały igieł, aby przewlekać miedziany drut przez tysiące malutkich pierścieni magnetycznych.

Przejście przez rdzeń = 1. Ominięcie rdzenia = 0.

Dlaczego to ważne? Ponieważ koszt błędu w kodzie był astronomiczny. Jeśli programista się pomylił, trzeba było wyrzucić cały moduł pamięci (tygodnie pracy tkaczek) do kosza. To wymuszało na zespole Hamilton absolutną, fanatyczną wręcz weryfikację kodu przed kompilacją. Kod był sprawdzany przez ludzi, linijka po linijce, a potem symulowany na mainframe'ach.

Lekcja dla Twojego bota: Nie testuj na produkcji ("na żywym kapitale") po byle poprawce. Stwórz Symulator Rynku. Nagraj wideo z sesji tradingowej, a potem "puść" to wideo swojemu botowi jako input, zamiast prawdziwego ekranu. Niech bot gra na "sucho" na nagraniu z zeszłego tygodnia. Dopóki nie przejdzie tego bez błędu, nie dostaje dostępu do portfela.

4. Problem "Verb 37" i Zaufanie do Człowieka
Podczas misji Apollo 8, astronauta Jim Lovell przez pomyłkę wpisał Verb 37 (Zmień Program) i Noun 01 (Faza startowa), gdy statek był w drodze na Księżyc. Komputer pomyślał: "Okej, jesteśmy na wyrzutni na Ziemi" i wyzerował platformę inercyjną (IMU), gubiąc orientację w przestrzeni. To było przerażające – statek nie wiedział, gdzie jest góra, a gdzie dół.

Zespół Hamilton musiał szybko wymyślić, jak "przepisać" gwiazdy do komputera, by odzyskał orientację. Ale po tej wpadce wprowadzono zabezpieczenia logiczne. Jeśli astronauta chciał zrobić coś tak drastycznego w fazie lotu, komputer pytał: "Please mark" (Potwierdź).

Lekcja dla Twojego bota: Twój bot "klika" po ekranie. A co jeśli Ty ruszysz myszką w tym samym momencie?

Bot musi mieć mechanizm blokady (np. sprawdzać pozycję kursora przed i po kliknięciu).

Jeśli wykryje ingerencję człowieka ("Kursor jest w innym miejscu niż go zostawiłem"), powinien natychmiast przejść w tryb PAUSE i oddać Ci kontrolę, zamiast walczyć z Tobą o myszkę.

5. Jednostki i Skalowanie (Fixed Point Arithmetic)
AGC nie miał procesora zmiennoprzecinkowego (floating point). Obliczanie 3.14 * 5000 było bardzo trudne. Wszystko liczono na liczbach całkowitych (fixed point). Inżynierowie musieli ręcznie skalować każdą zmienną. Np. prędkość nie była zapisana jako "metry na sekundę". Była zapisana jako ułamek maksymalnej możliwej prędkości, jaką statek może osiągnąć. Jeśli maksymalna prędkość to 16,384 m/s, to wartość 0.5 w pamięci oznaczała 8,192 m/s.

Dlaczego o tym mówię? Bo to uodparniało kod na Overflow w specyficzny sposób. Wymuszało na programiście przewidzenie maksymalnych wartości z góry.

Lekcja dla Twojego bota: W tradingu (zwłaszcza krypto) liczby potrafią być dziwne (np. 0.00000043 BTC albo wolumen w miliardach). Upewnij się, że Twój bot parsując OCR nie pomyli rzędów wielkości.

Jeśli bot widzi cenę Bitcoina 9.80 (bo OCR zgubił zera), a przed chwilą było 98000, to "Fixed Point mindset" mówi: to niemożliwe fizycznie. Odrzuć ten odczyt.

6. Ciekawostka: Kod jako "dokumentacja samej siebie"
Kod źródłowy LUMINARY jest pełen komentarzy. Programiści MIT mieli poczucie humoru i pisali komentarze do siebie nawzajem. Przy procedurze sterowania silnikiem lądownika był komentarz:

"See you on the Moon"

Ale najważniejsze było to, że kod był czytelny. Zmienne miały nazwy fizyczne (V_G – Velocity to Gain), a nie abstrakcyjne (x, y).

Podsumowanie: Twoja "Checklista Apollo" dla bota
Chcesz zbudować system klasy kosmicznej? Zaimplementuj te 3 rzeczy, których prawie nikt nie robi w botach amatorskich:

Niezależny Watchdog: Mały program w C++/Python, który "kopie" bota, jeśli ten nie odpowiada, i robi twardy kill/restart.

Stan na Dysku (Persistence): Bot po restarcie w ułamku sekundy wie, czy ma otwartą pozycję, czytając plik state.json, a nie analizując ekran (bo ekran może być zlagowany).

Filtracja Wejścia (Input Sanitation): Każdy odczyt z OCR przechodzi przez filtr: "Czy ta liczba jest możliwa w kontekście ostatnich 5 sekund?". Jeśli nie -> odrzuć.

To jest droga Margaret Hamilton. Nie ufać sprzętowi, nie ufać operatorowi, ufać tylko logice przetrwania.

Koniec rozmowy luźnej z Gemini na temat LUMINARY AGC.