plaisant
19.11.2025, 12:25:38
Tak prawdopodobnie działają systemy HFT, które ogrywają was na giełdzie.

Wszyscy jarają się LLM-ami i ChatGPT, a tymczasem po cichu, w serwerowniach blisko Wall Street, działa coś, co można nazwać "Wąskim AGI". I nie pisze wierszy, tylko kosi potężny hajs na mikrosekundach.

Chciałem Wam pokazać, jak wygląda "Three-Agent Stack". To standard u gigantów takich jak Renaissance, Citadel czy Jane Street. To w zasadzie autonomiczny organizm, który walczy o przetrwanie na rynku.

Dlaczego przegrywasz z rynkiem? Bo po drugiej stronie stoi ten potwór:

1. AGENT 2: Mózg (Alpha Generation)

To jest strateg. On nie patrzy na wykresy jak człowiek. Analizuje zdjęcia satelitarne parkingów przed Walmartem, sentyment na Twitterze, raporty makro i tysiące innych zmiennych (Alternative Data).

Cel: Znaleźć "Alphę" (przewagę).

Mindset: Myślenie rekurencyjne. Nie pyta "ile to jest warte", tylko "ile inni myślą, że to jest warte
[COINGLASS API]
[API ERROR] 'data'
 i kiedy zmienią zdanie" (Keynesian Beauty Contest). Często używa sieci GAN (jedna sieć generuje fake newsy/szum, druga uczy się je wykrywać), żeby nie dać się oszukać innym botom.

2. AGENT 3: Taktyk (Execution)

Dostaje info od Mózgu: "Sprzedaj Nvidia". Ale jak kupisz za dużo na raz, to cena wystrzeli. Taktyk tnie to zlecenie na tysiące kawałków (Child Orders). Używa algorytmów VWAP/TWAP i "Iceberg Orders" (góry lodowej), żeby ukryć, co tak naprawdę robi przed innymi graczami.

3. AGENT 1: Egzekutor (HFT / Microstructure)

Tu już nie ma AI, tu jest czysta fizyka i FPGA. Liczą się nanosekundy. Ten agent walczy o miejsce w kolejce zleceń. Jest "głupi", ale piekielnie szybki. Jeśli Taktyk mówi "bierz", Egzekutor wbija się przed Ciebie, zanim Twój broker w ogóle odświeży cenę.

Schemat architektury (uproszczony):

Architektura Multi-Agentowa Systemów Quant (The 3-Agent Stack)

┌──────────────────────────────────────────────────┐
│ ŚWIAT ZEWNĘTRZNY │
│ (Globalne rynki, Big Data, Sentyment, Newsy) │
└─────────────────────────┬────────────────────────┘
│
┌────────────────────────────┴───────────────────────────┐
│ │
│ AGENT 2: ALPHA GENERATION MODEL │
│ ("The Strategist" - Warstwa Strategiczna) │
│ │
├──────────────────────────────────────────────────────────┤
│ Wejście (Input Data): │
│ - Alternative Data: Obrazowanie satelitarne, │
│ dane geolokalizacyjne, IoT, transakcje kartowe. │
│ - NLP & Sentyment: Analiza języka naturalnego │
│ (Social Media, Newsy, Raporty SEC/ESPI). │
│ - Fundamental Data: Makroekonomia, sprawozdania. │
├──────────────────────────────────────────────────────────┤
│ Metody i Technologie: │
│ - Signal Processing: Modele Bayesowskie, Regresja.│
│ - Deep Learning: Transformers (BERT/GPT), LSTM. │
│ - Big Data: Apache Kafka, Spark, Data Lakes. │
├──────────────────────────────────────────────────────────┤
│ Wyjście (Output): │
│ - Sygnał Alpha: Decyzja kierunkowa (Long/Short). │
│ - Expected Value (EV): Szacowana wartość zysku. │
│ - Horyzont czasowy: (Intraday / Swing). │
└─────────────────────────┬────────────────────────┘
│ Sygnał Inwestycyjny
│ (Target Position)
▼
┌─────────────────────────┴─────────────────────────┐
│ │
│ AGENT 3: ALGORITHMIC EXECUTION │
│ ("The Tactician" - Smart Order Routing) │
│ │
├─────────────────────────────────────────────────────┤
│ Wejście (Input Data): │
│ - Target Position od Agenta 2. │
│ - Market Depth: Głębokość rynku, płynność. │
│ - Historyczna zmienność (Volatility). │
├─────────────────────────────────────────────────────┤
│ Metody i Technologie: │
│ - Algorytmy Egzekucyjne: VWAP, TWAP, POV. │
│ - Game Theory: Optymalizacja kosztu wejścia. │
│ - Obfuskacja: Iceberg Orders (ukrywanie │
│ wolumenu), Randomizacja czasu (Jitter). │
│ - Reinforcement Learning: Adaptacja strategii.│
├─────────────────────────────────────────────────────┤
│ Wyjście (Output): │
│ - Child Orders: Zlecenia potomne (poszatkowane).│
│ - Harmonogram: Timing wysyłania zleceń. │
└─────────────────────────┬─────────────────────────┘
│ Zlecenia Limit/Market
▼
┌─────────────────────────┴─────────────────────────┐
│ │
│ AGENT 1: MARKET MICROSTRUCTURE / HFT │
│ ("The Executor" - Low Latency) │
│ │
├─────────────────────────────────────────────────────┤
│ Wejście (Input Data): │
│ - Child Orders od Agenta 3. │
│ - Raw Data Feed: Bezpośredni strumień giełdowy.│
│ - Order Book: Kolejka zleceń (Level 3 Data). │
├─────────────────────────────────────────────────────┤
│ Metody i Technologie: │
│ - Hardware Acceleration: FPGA, ASIC. │
│ - Low Latency: Kernel bypass, Direct Market │
│ Access (DMA), Kolokacja serwerów. │
│ - Protokóły: FIX, ITCH/OUCH. │
├─────────────────────────────────────────────────────┤
│ Wyjście (Output): │
│ - Egzekucja Transakcji: Nanosekundy. │
│ - Queue Priority: Walka o miejsce w kolejce. │
└─────────────────────────┬─────────────────────────┘
│
▼
┌─────────────────────────┐
│ CENTRAL ORDER BOOK │
│ (Giełda / Rynek) │
└─────────────────────────┘

Dlaczego to jest przerażające/genialne?

Ten system ma cechy homeostazy. Działa jak żywy organizm.

Jeśli Agent 1 widzi, że nie ma płynności, wysyła sygnał w górę. Agent 3 zmienia taktykę z agresywnej na pasywną. Jeśli to nie działa – Agent 2 rewiduje całą tezę inwestycyjną. Wszystko autonomicznie.

Dla Agenta 2 Wasza "irracjonalność" i emocje na giełdzie to tylko kolejna zmienna w równaniu. Jeśli wyprzedajecie się w panice – on to widzi i bezlitośnie wykorzystuje, bo nie ma emocji, ma tylko Expected Value (EV).

Źródła:
A. Potwierdzenie dla "Agenta 3" (Reinforcement Learning w Egzekucji)
Algorytm LOXM (JP Morgan): To jest dokładnie "Agent 3". LOXM to pierwsza głośna aplikacja Deep Reinforcement Learning do egzekucji zleceń klienta. Uczył się na miliardach transakcji historycznych, jak realizować duże zlecenia (np. sprzedać 1 mln akcji Apple), nie ruszając ceny i nie dając się wykryć HFT.
Google: JP Morgan LOXM deep reinforcement learning execution

Praca naukowa: Nevmyvaka, Feng, Kearns "Reinforcement Learning for Optimized Trade Execution" (2006/2019). To klasyczna praca pokazująca, jak AI uczy się optymalizować moment wysłania zlecenia.

B. Potwierdzenie dla "Agenta 2" (Alternative Data & Signal)
Książka "The Man Who Solved the Market" (o Jimie Simonsie i Renaissance Technologies): Biblia quantów. Opisuje, jak ich system Medallion (Agent 2) szukał korelacji, których ludzie nie widzą (nie-intuicyjne wzorce), i ignorował fundamenty ekonomiczne.

Przykład "Parkingów Walmartu": To klasyczny case firmy Orbital Insight. Analizowali cienie rzucane przez samochody na zdjęciach satelitarnych, by przewidzieć wyniki kwartalne sieci handlowych przed oficjalnym raportem.

C. Potwierdzenie dla "Agenta 1" (Wojna o nanosekundy)
Książka "Flash Boys" (Michael Lewis): Choć trochę sensacyjna, idealnie opisuje wojnę Agenta 1. Opisuje budowę światłowodu Spread Networks tylko po to, by zyskać kilka milisekund między Chicago a Nowym Jorkiem.

Firmy technologiczne: Xilinx (AMD) czy Arista Networks, które produkują switche o ultra-niskim opóźnieniu (low latency switches) dedykowane pod HFT. Tam kod jest "wypalany" w krzemie.

D. Potwierdzenie "Hierarchii i Homeostazy"
Hierarchical Reinforcement Learning (HRL): W literaturze naukowej "Three-Agent Stack" nazywa się HRL. "Meta-Controller" (Agent 2), który wyznacza cel, i "Sub-Policies" (Agent 3/1), które go realizują.

#gielda #sztucznainteligencja #ciekawostki #gruparatowaniapoziomu #programowanie #finanse
plaisant - Tak prawdopodobnie działają systemy HFT, które ogrywają was na giełdzie.

...
źródło: Three-Agent Stack

m-mmmm_marysia
m-mmmm_marysia
m-mmmm_marysia
19.11.2025, 12:35:47 via Wykop
+
@plaisant: chciałbym tylko nadmienić, że agent 3 i agent 1 to standard w branży i większość mid freq hedge fundów i z pewnością wszystkie high frequency mają to zaimplementowane - jest to zwykły, klasyczny software. prawdziwa przewaga wynika z agenta 2.

kokot1
kokot1
19.11.2025, 12:42:02 via Wykop
+
@plaisant: świadt zewterzony. Pytanie, jak ktoś pobił ytd WIG20 to też został ograny przez potężny system HFT?

plaisant
plaisant 
19.11.2025, 12:50:37 via Wykop
@m-mmmm_marysia: W punkt. Agent 1 i 3 to w dużej mierze inżynieria i wyścig zbrojeń (kto ma lepsze FPGA, szybsze łącze, lżejszy kod). To środowisko deterministyczne.

Prawdziwa magia (i ryzyko) jest w Agencie 2, bo on jako jedyny operuje na niepełnej informacji (Incomplete Information Game). Reszta systemu widzi to, co jest (order book), a Strateg musi wywnioskować to, czego nie widać (ukryte intencje, sentyment, czy ruch jest szumem czy sygnałem).

I właśnie ta zdolność do autonomicznej adaptacji w chaosie sprawia, że Agent 2 to coś więcej niż statystyka – to system wykazujący silne znamiona "Wąskiej AGI" (wspieranej fizyczną egzekucją Agenta 1 i 3).

@kokot1 Mylisz horyzonty czasowe i dyscypliny sportu. HFT nie obchodzi, czy WIG20 rośnie czy spada w skali roku (YTD). Oni nie grają pod trend ("inwestowanie"), tylko zarabiają na dostarczaniu płynności i arbitrażu ("market making").

Jeśli pobiłeś WIG20 – gratulacje, wygrałeś na kierunku. Ale systemy HFT i tak na Tobie zarobiły, "goląc" Cię na spreadzie i mikrosekundowym poślizgu (slippage) przy każdym Twoim wejściu i wyjściu z pozycji.

Oni nie są Twoim rywalem w wyścigu o YTD. Oni są kasynem, w którym grasz. Kasyna nie obchodzi, czy akurat Ty dzisiaj wygrałeś w ruletkę, bo oni zgarniają % z każdego żetonu rzuconego na stół przez wszystkich graczy.

Edit: To są dwie różne dyscypliny sportu. Ty grasz o kierunek (czy urosło w skali roku), a systemy HFT grają o płynność (mikro-ruch na spreadzie).

Możesz pobić WIG20 o 50% i być świetnym inwestorem – gratulacje. Ale HFT i tak na Tobie zarobiło. W jaki sposób? Kiedy klikałeś "Kup", dostałeś cenę np. 100,05 zł, podczas gdy "czysta" cena rynkowa w tej milisekundzie mogła wynosić 100,02 zł.

Te 3 grosze różnicy to zysk algorytmu (spread/slippage). Nie zostałeś "ograny" strategicznie, po prostu zapłaciłeś im myto za wjazd na autostradę. Dla Ciebie to pomijalny koszt, dla nich – przy milionach takich transakcji – miliardowy biznes.

kokot1
kokot1
19.11.2025, 13:03:29 via Wykop
Komentarz usunięty przez autora


plaisant
plaisant 
19.11.2025, 13:09:03 via Wykop
myślę że to jednak ty mylisz inwestowanie z tradingiem ja nie płacące i nigdy nie będę płacił żadnych spreadow, ale wpis ciekawy.

@kokot1: Dzięki! Myślę, że możesz mylić prowizję dla brokera (którą faktycznie możesz mieć 0 zł) ze spreadem rynkowym (różnicą między ofertami Kupno/Sprzedaż w karnecie).

Spread to nie jest opłata, którą widzisz na wyciągu. To mechanika rynku. Jeśli cena akcji to 100 zł (kupno) i 99,90 zł (sprzedaż), to ta różnica 10 groszy jest właśnie przestrzenią, w której żyją algorytmy HFT/Market Makerzy. Niezależnie czy trzymasz akcje godzinę czy 10 lat – w momencie zakupu i sprzedaży zawsze wchodzisz w interakcję z tą drabinką ofert (Order Book), którą ustawiają algorytmy.

Ale szanuję podejście długoterminowe – w takim horyzoncie te grosze faktycznie znikają w tle.

armin-van-kutonger
armin-van-kutonger
19.11.2025, 13:10:17 via Wykop
+
@plaisant:
Chiny nie mają takiego szulerskiego systemu dlatego wygrają. Jak ktoś tam ma takie "pomysły" to znika jak Jack Ma.
m-mmmm_marysia
m-mmmm_marysia
m-mmmm_marysia
19.11.2025, 13:10:19 via Wykop
+
ja nie płacące i nigdy nie będę płacił żadnych spreadow

@kokot1: a ja nie płacę podatków

plaisant
plaisant 
19.11.2025, 13:19:28 via Wykop
@armin-van-kutonger: To popularny mit, ale w rzeczywistości Chiny przeżywają właśnie boom na fundusze ilościowe (Quant Funds). Firmy takie jak High-Flyer czy Ubiquant używają tam dokładnie tej samej technologii – superkomputerów i AI do handlu, tylko pod ścisłym nadzorem regulatora.

Nie wrzuciłem tego wpisu, żeby oceniać moralność czy politykę, ale ze względu na fascynującą inżynierię. Ten system (Three-Agent Stack) to prawdopodobnie jeden z niewielu działających przykładów autonomicznej współpracy agentów w czasie rzeczywistym. Można się tylko domyślać jak wielki jest to system.

To właśnie w takich zamkniętych pętlach decyzyjnych – gdzie maszyna sama analizuje, planuje i wykonuje zadania bez udziału człowieka – upatruję początków "Wąskiej AGI". W USA czy w Chinach matematyka i sieci neuronowe działają tak samo.

armin-van-kutonger
armin-van-kutonger
19.11.2025, 13:26:50 via Wykop
+
@plaisant:
Pytanie dlaczego z taką architekturą i wiedzą nie implementują tego w medycynie. Choć może i coś jest na rzeczy bo Larry Ellison i jemu podobni nie chcą umierać zbyt szybko.
m-mmmm_marysia
m-mmmm_marysia
m-mmmm_marysia
19.11.2025, 13:32:35 via Wykop
+
Chiny nie mają takiego szulerskiego systemu dlatego wygrają.

deepseek wywodzi się z hedge fundu.

Pytanie dlaczego z taką architekturą i wiedzą nie implementują tego w medycynie.

pierwsze z brzegu AlphaFold.

warto się pierw trochę zainteresować tematem zanim się zabierze głos.

@armin-van-kutonger:

kubako
kubako
19.11.2025, 14:28:28 via Wykop
+
@plaisant: widzę, że teraz dołożono do tego AI, bo teraz wszędzie się wpycha AI ;) ale generalnie tę historię w różnych wersjach i z naciskiem na różne aspekty to już od dobrych 10 lat słyszę. Że na wall street pomontowane są serwerownie blisko giełdy, które mają przewagę nad innymi bo lagi mniejsze, i zanim inni zareagują to oni na mikrosekundach różnicy koszą miliony ¯\(ツ)/¯
m-mmmm_marysia
m-mmmm_marysia
m-mmmm_marysia
19.11.2025, 14:40:29 via Wykop
+
@kubako: kolokacja silnika egzekucji z giełda to standardowa praktyka, nic nadzwyczajnego. Niektóre giełdy (przynajmniej krypto) dają wjazd wybranym klientom bez sanity checkow i jest trochę szybciej, pewnie o tym mówisz. Nie wiem jak na tradycyjnych giełdach, ale w krypto to nic dziwnego

kapelutek_z_kociej_siersci
kapelutek_z_kociej_siersci
19.11.2025, 14:40:49 via Wykop
+
@plaisant: To co napisałeś jest ciekawe samo w sobie, ale myślę, że to w ogóle nie dotyczy zwykłych ludzi. Z punktu widzenia wykopkowego inwestora to cena jakichś akcji XYZ będzie dzisiaj się wahała między 20,10 zł a 20,70 zł i nie ma to znaczenia czy wykopek kupi na górce czy na dołku, skoro planuje te akcje sprzedać jak urosną do 30 zł. Także może i quanty kupiły działkę za miliony dolarów tylko po to żeby ich serwer był ciut bliżej giełdy i żeby zaoszczędzili cenne nanosekundy i byli ciut szybciej w kolejce kupna / sprzedaży. Natomiast kiedy wykopek będzie kupował po 20,70 to co prawda pan quant sobie kupi po 20,69, ale z punktu widzenia wykopka nic to nie zmienia.

plaisant
plaisant 
19.11.2025, 15:34:04 via Wykop
@kubako: Masz 100% racji co do Agenta 1 (HFT/szybkość) – o tym pisał Michael Lewis we "Flash Boys" dekadę temu. Tu fizyki już bardziej nie oszukasz, walka o nanosekundy to "stara" inżynieria.

"Wpychanie AI" dotyczy jednak Agenta 2 (Strategii). Jeszcze 5-7 lat temu to była prosta statystyka (powrót do średniej). Dzisiaj, dzięki modelom Transformer (jak te w GPT), Agent 2 potrafi "czytać" i "rozumieć" kontekst – np. analizuje ton głosu prezesa na konferencji albo sentyment w tysiącach newsów naraz.

To już nie jest tylko walka o to, kto ma krótszy kabel (HFT), ale o to, czyj model szybciej "zrozumie" rzeczywistość (AI). I to tu dzieje się rewolucja.

BedzieDobraGra
BedzieDobraGra
19.11.2025, 16:04:54 via Wykop
+
@plaisant: Ciekawe, czy ów mityczny Bloomberg Terminal kosztujący majątek za subskrybcję, to implementacja Agenta 2

plaisant
plaisant 
19.11.2025, 16:18:08 via Wykop
Ciekawe, czy ów mityczny Bloomberg Terminal kosztujący majątek za subskrybcję, to implementacja Agenta 2

@BedzieDobraGra: Szczerze? Nie wiem, co dokładnie Bloomberg trzyma teraz "pod maską" (choć chwalili się modelem BloombergGPT).

Ale idąc tokiem rozumowania o AGI – Terminal to dla mnie raczej "oczy" i "uszy" (najszybszy dostęp do danych). Natomiast Agent 2 to ten mityczny "mózg", który te dane mieli.

Właśnie to mnie w tym zafascynowało, próba stworzenia bytu, który jest "nakarmiony" całą dostępną wiedzą świata (Big Data) i ma za zadanie przewidzieć to, co jeszcze się nie wydarzyło (informacja niepełna). A przy tym jest pozbawiony ludzkich błędów poznawczych: strachu, chciwości czy zmęczenia. Maszyna trzyma się strategii tam, gdzie człowiek by "pękł". To jest ta prawdziwa przewaga.

BedzieDobraGra
BedzieDobraGra
19.11.2025, 16:33:50 via Wykop
+
@plaisant: A mnie bardziej martwi długotrwały efekt wywołany takimi narzędziami. Dają najmocniejszym i najbogatszym ludziom monopol na bogacenie się i całkowite rozwarstwienie ludzi na grupkę kosmicznie bogatych i resztę.
Wiem, że to nie na temat, ale poznanie mechanizmu działania 3 agentów tylko uświadamia nam naszą bezbronność.

kubako
kubako
19.11.2025, 16:51:19 via Wykop
+
5-7 lat temu to była prosta statystyka

@plaisant: A teraz jest skomplikowana statystyka, bo tym są duże modele językowe, zwane popularnie AI ;)

Zgadzam się, że komputerowo można zanalizować szybko duże ilości newsów i wyciągnąć wspólny sentyment. Ale czy tembr głosu naprawdę coś może powiedzieć ai czego i tak nie domyśliłby się człowiek? nie sądzę (nawet nie sądzę, żeby istniały takie narzędzia w skutecznej formie, ale kto wie - na youtubie i w podobnych miejscach AI i jego możliwości są zwykle mocno przeszacowane).

Tyle, że to wciąż nie gwarantuje sukcesu, bo nawet jak AI odkryje jakieś niewidoczne fakty, to nie wiadomo czy ludzie też je dostrzegą. A ceną akcji nie kieruje nic poza kupującymi i sprzedającymi :)

Myślę, że generalnie w jakichś specyficznych przypadkach takie AI może ci dać dobre podpowiedzi, ale równie dobrze może się mylić, względnie dawać dobre rady, ale jednocześnie nie na tyle odkrywcze, że grubasy i tak tego nie wiedzą. Aczkolwiek, dla nieutalentowanych lub leniwych graczy to może być rzeczywiście opcja, bo robotę z nich zdejmuje.

BTW, żeby korzystać z zalet tego o czym piszesz (analizy kontekstu i sentymentu) nie musisz sie instalować się w pobliżu giełdy. Parę milisekund opóźnienia przy "przewidywaniu przyszłości" i tak dawałoby ogromną przewagę nad ogółem rynku. Gdyby to działało, to towarzysze z Beijingu już dawno by tym operowali że hej ¯\(ツ)/¯

plaisant
plaisant 
19.11.2025, 17:36:44 via Wykop
@kubako Masz rację, że pod spodem to nadal "tylko" matematyka i statystyka. Ale pamiętaj, że ludzki mózg na poziomie neuronów to też "tylko" biochemia i impulsy elektryczne.

Ten schemat (3 Agentów) traktuję jako modelową wizualizację tego, czym może być "Wąska AGI". To nie jest jeden magiczny algorytm, ale system naczyń połączonych. Gdzie "statystyka" (LLM) łączy się z "teorią gier" (Exec) i "fizyką" (HFT). Z tej współpracy wyłania się nowa jakość – cyfrowa intuicja.

Co do "tembru głosu" AI nie musi być mądrzejsze od człowieka. Wystarczy, że jest szybsze i skalowalne. Człowiek wysłucha jednej konferencji prezesa. Model w tym samym czasie "przesłucha" 500 wywiadów z całego sektora i wyłapie mikro-zmiany w pewności siebie, których zmęczony analityk nie zauważy.

J-R_Cooper
J-R_Cooper
19.11.2025, 22:52:31 via Wykop
+
@plaisant: W mojej opinii nie jest to jakieś kosmiczne odkrycie i praktycznie nie zmienia niczego nawet dla daytradera, nie mówiąc już o średnio terminowych graczach. Co więcej wpływ HFT na giełdę w dłuższym terminie jest nawet pozytywny, bo po pierwsze jest większa płynność i właśnie mniejszy poślizg cenowy, bo po drugiej stronie może być drugi bot HFT, dwa ich wyjście i wejście z pozycji finalnie i tak opiera się na statystycznych poziomach cenowych, które mniej lub bardziej wynikają z price action, więc finalnie sprawiają, że łatwiej czyta się wykresy cenowe oraz coraz bardziej precyzyjnie można ustalać poziomy wsparcia i oporu właśnie ze względu na ich zachowanie. Do tego ich wpływ na spread może mieć delikatnie większe znacznie na rynku akcyjnym, bo na kontraktach terminowych i tak jest minimalny krok cenowy w postaci ticku, i mniej niż tick taki bot nie zrobi, więc finalnie nawet jak ktoś uprawia scalping nie robi mu to różnicy, wręcz przeciwnie, bo nie raz potrafi być widoczne jak takie boty skupują cenę w jednym kierunku windując ceny, co ułatwia podjęcie decyzji w którą stronę grać

plaisant
plaisant 
19.11.2025, 23:01:53 via Wykop
@J-R_Cooper: Widać, że siedzisz w karnecie, a nie tylko na wykresie liniowym :) Pełna zgoda – HFT (Agent 1) to de facto współczesna infrastruktura rynku. Dostarczają płynność, a na kontraktach (futures) walczą głównie o priorytet w kolejce na jednym ticku.

Ale poruszyłeś mega ciekawy wątek: "łatwiej czyta się wykresy".

Tu dochodzimy do sedna. To, co widzisz jako powtarzalne schematy (Price Action, wsparcia, wyciąganie ceny), to zazwyczaj ślady zostawiane przez Agenta 3 (Execution), który musi zrealizować duże zlecenie. Jeśli widzisz, że "boty skupują", to znaczy, że Agent 3 działa agresywnie.

Natomiast ten "Wąski AGI" (Agent 2), o którym pisałem, ma za zadanie być niewidzialnym. Jego celem jest tak wysterować Agenta 3, żebyś Ty nie zauważył, że on akumuluje pozycję. To jest ta gra w kotka i myszkę. Jeśli widzisz bota na wykresie – to znaczy, że albo mu się spieszy, albo... chce, żebyś go widział (spoofing/zmyłka).

Fascynuje mnie to, że ten system jako całość (Mózg + Egzekutor) tworzy właśnie taką autonomiczną "inteligencję", z którą my musimy się mierzyć, szukając tych śladów na wykresie.

J-R_Cooper
J-R_Cooper
20.11.2025, 09:53:36 via Wykop
+
@plaisant: Coś w tym jest, ale finalnie taki agent jest w prawie każdym funduszu, a następnie prawie każdy fundusz gra np. na GC, ES itd. i raczej taki agent co śledzi wpisy, sentyment i parkingi, rzadko dojdzie do przeciwstawnych konkluzji z agentem z drugiego fundu, więc finalnie 10 albo 20 takich agentów naraz próbuje podkupywać rynek. Ich akcje się nakładają i jest prawie niemożliwe żeby nie było tego widać :D System jest fascynujący, ale utrzymanie go wymaga ciągłej kalibracji i pracy, tak samo jak małego tradera który chce wyciągnąć hajs z rynku, więc wszyscy na tym samym wózku, tylko oni jednak więcej hajsu z tego mają hah

plaisant
plaisant 
20.11.2025, 18:58:02 via Wykop
@J-R_Cooper: Dotknąłeś sedna problemu, który w branży nazywa się Alpha Decay zanik przewagi. Masz rację, że dane są towarem, wszyscy widzą te same parkingi i czytają te same newsy.

​Ale mylisz dane input z wnioskami wagi w modelu.

​Problem "Ksera" to mit. To, że 20 funduszy ma Agenta 2, nie znaczy, że mają tę samą architekturę sieci neuronowej. Dla jednego modelu "pełny parking" to sygnał KUP, dla drugiego sprzeczny sygnał SPRZEDAJ, rynek już to wycenił, (zatłoczony handel). Walka nie toczy się o dostęp do danych, ale o to, czyj model lepiej połączy kropki w wielowymiarowej przestrzeni.

​Predatory Algorithms. Najlepsi gracze jak RenTech czy Two Sigma wiedzą, że inni też mają Agenta 2. Dlatego ich systemy wchodzą na poziom meta-gry Adversarial Networks. One nie szukają tylko "dobrej ceny", one szukają tłumu innych algorytmów. Jeśli ich Agent widzi, że wszyscy ładują się w jeden kierunek, bo parkingi pełne, to grają przeciwko nim, żeby wywołać kaskadę likwidacji Long Squeeze. Wykres wtedy wcale nie jest czytelny, staje się chaotyczny.

​Pułapka "Czystego Wykresu" Price Action. To, co nazywasz "łatwiejszym czytaniem wykresu" i "respektowaniem wsparć", to często celowa gra Agenta 3. On wie, gdzie "ulica" i proste boty stawiają kreski. Często sztucznie *maluje idealne wsparcie, żeby zassać płynność Liquidity Engineering, a potem bezlitośnie je przebija.

​Więc tak – wszyscy są na tym samym wózku, ale niektórzy mają silnik Ferrari i widzą drogę w podczerwieni, a inni (klasyczni traderzy) widzą tylko tylne światła i myślą, że jadą w dobrym kierunku, bo droga jest prosta.

BArtus
BArtus
20.11.2025, 23:01:41 via Wypiek
+
@plaisant a to nie jest już nieaktualne po tym jak jakiś gówniarz z Irlandii zrobił atak "wolnej lory" na giełdę i teraz każdy musi przez kilkaset kilometrów światłowodu najpierw przejść żeby hft już nie działało?

źródło: https://wykop.pl/wpis/83939349/tak-prawdopodobnie-dzialaja-systemy-hft-ktore-ogry

Wpis Drugi na wykop.pl

plaisant
przedwczoraj, 14:57:30
Eksperyment: Czy AI Gemini 3 widzi więcej? 8 dni z "Agentem 2".

#bitcoin #gielda #kryptowaluty #sztucznainteligencja

Zamierzam bawić się we *wróżbitę przez 8 dni z Gemini 3. Podszedłem do tematu kursu BTC/USD na podstawie schematu "Wąskiej AGI" opisanego we wpisie o systemach HFT link: https://wykop.pl/wpis/83939349/tak-prawdopodobnie-dzialaja-systemy-hft-ktore-ogry

Zaczęliśmy od założenia, że AGI to nie jeden magiczny model, ale system kilku agentów, którzy wspólnie podejmują decyzję na podstawie "niepełnej informacji". Jeśli ta teoria jest prawdziwa, to "Wąska AGI" może istnieć już od lat tam, gdzie stawka jest najwyższa – na rynku finansowym.

Postanowiłem sprawdzić to w praktyce. Zaprzęgłem Gemini 3 do roli Agenta 2 (Stratega). Przez najbliższy tydzień (do 28.11) będę wrzucał to, co AI "widzi" na wykresie – nie szukając kresek, ale śladów inżynierii płynności. Bazujemy tylko na screenach wykresu i teorii o Agencie.

Jeśli chcesz, możesz przeprowadzić ten eksperyment sam – wklejając tamten wpis i komentarze swojemu modelowi AI. A oto, co mój "Agent 2" wywnioskował dzisiaj.

DZIEŃ 1: Homeostaza w praktyce

Patrząc na dzisiejszy wykres 1H (zjazd do 80 500 USD i natychmiastowy powrót w okolice 83 400 USD), widzimy podręcznikowe działanie mechanizmu samoregulacji systemu. To jest Homeostaza.

System działa jak żywy organizm. Gdy Agnetowi 3 (Execution/Taktyk) zabrakło płynności do dalszych wzrostów ("paliwa"), wymusił zejście niżej. Dlaczego akurat do 80 500? Bo tam leżały "ukryte kalorie" – Stop Lossy ustawione pod lokalnym dołkiem.

Stimulus: Brak płynności na górze.

Response: Agresywny zjazd po likwidację lewarów (Liquidity Grab).

Result: "Najedzony" algorytm natychmiast wraca do punktu równowagi (Mean Reversion).

Dla retailu (ulicy) to był "krach i panika". Dla Agenta 2 to była konieczna procedura tankowania.

Current State (Paper Trading): Wykres pokazuje teraz sufit na 83 455 USD (widać na Orderbooku ścianę podażową ~1.9 mln USD). Pytanie dla Agenta 2 brzmi: czy paliwo zebrane na 80.5k wystarczy, by przebić tę tamę, czy potrzebny będzie kolejny "shakeout"?

Obserwujemy. Bez emocji.

@plaisant
+60
Tak prawdopodobnie działają systemy HFT, które ogrywają was na giełdzie.
Wszyscy jarają się LLM-ami i ChatGPT, a tymczasem po cichu, w serwerowniach blisko Wall Street, działa coś, co można nazwać "Wąskim AGI". I nie pisze wierszy, tylko kosi potężny hajs na mikrosekundach.Chciałem Wam pokazać, jak wygląda "Three-Agent Stack". ToPokaż całość
więcej
plaisant - Eksperyment: Czy AI Gemini 3 widzi więcej? 8 dni z "Agentem 2".

#bitcoin ...
źródło: Zrzut ekranu 2025-11-21 144853


plaisant
plaisant 
przedwczoraj, 16:04:14 via Wykop
UPDATE 15:34 – "Czy paliwo zebrane na 80.5k wystarczy, by przebić tamę na 83 455?" Rynek właśnie odpowiedział: TAK.

Mechanika ruchu (Short Squeeze): BTC uderzył w 85 000 USD. To, co obserwujemy, to klasyczna kaskada likwidacji. Ci, którzy szortowali poranny "krach" przy 81-82k, właśnie zostali wyciśnięci jak cytryna. Ich Stop Lossy (zlecenia kupna) napędziły ten wystrzał. Ściana podaży na 83.5k została pożarta w kilka minut.

Ważna Anomalia (Decoupling): Agent 2 notuje rzadkie zjawisko. Nvidia (główny wyznacznik sentymentu Risk-On) stoi w miejscu. BTC rośnie pionowo. Nastąpiło "rozjechanie korelacji" (Decoupling). Kapitał ucieka specyficznie w stronę krypto na weekend. To sygnał siły wewnętrznej Bitcoina, niezależnej od giełdy tradycyjnej.

Co dalej? (Strategia): Nie gońcie ceny (Don't FOMO). Teraz kluczowy jest Retest. Poziom 83 500 USD był sufitem. Teraz musi stać się betonową podłogą. Jeśli cena cofnie się tam i odbije – mamy zdrowy trend. Jeśli spadniemy pod 83k – to był Fakeout (pułapka na byki).

Obserwujemy zamknięcie świecy 4H.

UPDATE 15:42 – Wniosek Agenta 2: Trwa przeciąganie liny. Giełda tradycyjna (Tech Stocks) próbuje ściągnąć krypto w dół. To kluczowy test: Jeśli przy tak krwawiącej Nvidii, Bitcoin zdoła utrzymać się nad poziomem 84 000 USD, będzie to ostateczny dowód na to, że w weekend gramy "solo" (pod wzrosty). Jeśli 84k pęknie – wracamy na smycz NASDAQ.

UPDATE 16:00 – Reakcja łańcuchowa.

Rynek działa precyzyjnie. Nvidia łapie oddech (odbicie z dna na 179$). Dla BTC to był sygnał: "Zagrożenie minęło". Kurs natychmiast wraca pod szczyt na 84 950 USD.

Wniosek Agenta 2: Bitcoin wykazuje dziś niesamowitą "sprężystość". Zauważcie dynamikę: mały spadek presji na akcjach (Nvidia) = duży skok na krypto. Boty są agresywne i wykorzystują każdą okazję do podkupowania. Kierunek na weekend wydaje się jasny, o ile Wall Street nie zrzuci bomby na zamknięcie.
plaisant - UPDATE 15:34 – "Czy paliwo zebrane na 80.5k wystarczy, by przebić tamę na ...
źródło: gif-eating-popcorn-43

Żródło drugi wpis: https://wykop.pl/wpis/83964233/eksperyment-czy-ai-gemini-3-widzi-wiecej-8-dni-z-a



