Analiza endpointów Coinglass API dla bota tradingowego
Plan Hobbyist - 70 endpointów

✅ Weryfikacja dostępności wymaganych danych
1. Price BTC/USD (Baza) ✅ DOSTĘPNE
Potrzebne endpointy:

/api/price/ohlc-history - Price OHLC history (świece + OHLC)
/futures/price-change-list - Price change list (zmiana ceny)
/api/futures/pairs-markets - Futures pair markets (aktualna cena rynkowa)

Status: ✅ W pełni dostępne

Wszystkie 3 endpointy są w kategorii Market/Price
Otrzymasz: OHLC (Open, High, Low, Close), volume, zmiana %


2. Avg Funding Rate (Sentyment) ✅ DOSTĘPNE
Potrzebne endpointy:

/api/futures/fundingRate/ohlc-history - Funding rate OHLC history
/api/futures/fundingRate/oi-weight-ohlc-history - OI-weighted funding rate (ważony OI)
/api/futures/fundingRate/vol-weight-ohlc-history - Volume-weighted funding rate (ważony volume)
/api/futures/fundingRate/exchange-list - Funding rate by exchange list
/api/futures/fundingRate/accumulated-exchange-list - Cumulative funding rate

Status: ✅ W pełni dostępne

Dostęp do funding rate z wszystkich giełd
Możliwość obliczenia średniej ważonej
Dane historyczne i aktualne


3. Long/Short Ratio (Pozycje ulicy) ✅ DOSTĘPNE
Potrzebne endpointy:

/api/futures/global-long-short-account-ratio/history - Global L/S account ratio
/api/futures/top-long-short-account-ratio/history - Top trader L/S ratio
/api/futures/top-long-short-position-ratio/history - Top trader position ratio
/api/futures/taker-buy-sell-volume/exchange-list - Exchange Taker Buy/Sell Ratio

Status: ✅ W pełni dostępne

Globalny L/S ratio (retail traders)
Top traders L/S ratio (wieloryby)
Taker buy/sell volume ratio
Pełny obraz pozycjonowania rynku


4. Open Interest (Paliwo do ruchu) ✅ DOSTĘPNE
Potrzebne endpointy:

/api/futures/openInterest/ohlc-history - Open interest OHLC history
/api/futures/openInterest/ohlc-aggregated-history - Aggregated OI OHLC
/api/futures/openInterest/ohlc-aggregated-stablecoin - Stablecoin margin OI
/api/futures/openInterest/ohlc-aggregated-coin-margin-history - Coin margin OI
/api/futures/openInterest/exchange-list - OI by exchange list
/api/futures/openInterest/exchange-history-chart - OI chart by exchange

Status: ✅ W pełni dostępne

Open Interest agregowany i per giełda
Podział na stablecoin margin vs coin margin
Dane historyczne OHLC
Możliwość porównania OI między giełdami


5. Liquidations (Poziom "bólu") ✅ DOSTĘPNE
Potrzebne endpointy:

/api/futures/liquidation/history - Pair Liquidation History
/api/futures/liquidation/aggregated-history - Coin Liquidation History
/api/futures/liquidation/coin-list - Liquidation Coin List
/api/futures/liquidation/exchange-list - Liquidation Exchange List
/api/futures/liquidation/order - Liquidation Order (real-time)

Status: ✅ W pełni dostępne

Historia likwidacji (agregowana i per para)
Lista likwidacji per giełda
Real-time liquidation orders
Możliwość analizy "pain levels"


6. Heatmapa Liquidacji Coinglass (Wizja lokalna) ✅ DOSTĘPNE
Potrzebne endpointy:

/api/futures/liquidation/heatmap/model1 - Pair Liquidation Heatmap Model1
/api/futures/liquidation/heatmap/model2 - Pair Liquidation Heatmap Model2
/api/futures/liquidation/heatmap/model3 - Pair Liquidation Heatmap Model3
/api/futures/liquidation/aggregated-heatmap/model1 - Coin Liquidation Heatmap Model1
/api/futures/liquidation/aggregated-heatmap/model2 - Coin Liquidation Heatmap Model2
/api/futures/liquidation/aggregated-heatmap/model3 - Coin Liquidation Heatmap Model3
/api/futures/liquidation/map - Pair Liquidation Map
/api/futures/liquidation/aggregated-map - Coin Liquidation Map

Status: ✅ W pełni dostępne

3 modele heatmap (różne metodologie)
Wersje dla par i agregowane dla coinów
Liquidation maps (wizualizacja klastrów)
UWAGA: To są dane numeryczne (JSON), nie screenshoty obrazków


7. Orderbook Bitmex (Weryfikacja ścian) ⚠️ CZĘŚCIOWO DOSTĘPNE
Dostępne endpointy:

/api/futures/orderbook/ask-bids-history - Pair Orderbook Bid&Ask(±range)
/api/futures/orderbook/aggregated-ask-bids-history - Coin Orderbook Bid&Ask(±range)
/api/futures/orderbook/history - Orderbook Heatmap
/api/futures/orderbook/large-limit-order - Large Orderbook (duże zlecenia)
/api/futures/orderbook/large-limit-order-history - Large Orderbook History

Status: ⚠️ API nie dostarcza screenshotów

Coinglass API nie dostarcza screenshotów z orderbooka
Dostarcza dane numeryczne: bid/ask levels, volumes, duże zlecenia
Musisz sam zwizualizować dane lub użyć bezpośrednio API Bitmex

Alternatywa dla SS z orderbooka:

Użyj danych z Coinglass API:

Large limit orders - wykrywa duże "ściany"
Orderbook heatmap data - dane do własnej wizualizacji


Lub połącz z API Bitmex:

Bitmex WebSocket: wss://www.bitmex.com/realtime
Subscribe: orderBookL2:XBTUSD
Otrzymasz raw orderbook data




📊 Podsumowanie dostępności
WymaganieStatusEndpointyUwagi1. Price BTC/USD✅ 100%3 endpointyPełne dane OHLC2. Avg Funding✅ 100%5 endpointówWażone OI i volume3. L/S Ratio✅ 100%4 endpointyGlobal + top traders4. Open Interest✅ 100%6 endpointówAgregowane + per giełda5. Liquidations✅ 100%5 endpointówHistoria + real-time6. Heatmapy✅ 100%8 endpointów3 modele + mapy7. Orderbook⚠️ 80%5 endpointówDane, nie screenshoty
Suma użytych endpointów: 36 z 70 dostępnych

🎯 Rekomendacje implementacji
Dla punktu 7 (Orderbook visualization):
Opcja A: Wykorzystaj dane z Coinglass
python# Pobierz large orders z Coinglass
large_orders = get_large_orderbook()
# Zwizualizuj sam w matplotlib/plotly
plot_orderbook_walls(large_orders)
Opcja B: Dodaj WebSocket Bitmex
pythonimport websocket
ws = websocket.create_connection("wss://www.bitmex.com/realtime")
ws.send('{"op": "subscribe", "args": ["orderBookL2:XBTUSD"]}')
# Real-time orderbook updates
Opcja C: Użyj REST API Bitmex (bez screenshotów)
python# GET https://www.bitmex.com/api/v1/orderBook/L2?symbol=XBTUSD&depth=25
# Zwraca JSON z poziomami orderbooka

🔥 Dodatkowe endpointy warte uwagi (zostało 34 slotów)
Skoro masz 70 endpointów, a używasz tylko 36, polecam dodać:
Sentyment i makro:

/api/index/fear-greed-history - Fear & Greed Index
/api/coinbase-premium-index - Coinbase Premium (retail FOMO)
/api/bitfinex-margin-long-short - Bitfinex margin positions

Dodatkowe sygnały:

/api/futures/taker-buy-sell-volume/history - Taker buy/sell volume
/api/hyperliquid/whale-alert - Whale movements
/api/futures/basis/history - Futures basis (contango/backwardation)

On-chain (early warning):

/api/exchange/assets - Exchange reserves
/api/exchange/balance/chart - Exchange balance changes


✅ Końcowa weryfikacja
TAK, plan Hobbyist (70 endpointów) w pełni pokrywa Twoje potrzeby:

✅ Wszystkie kluczowe dane dostępne
✅ 36 endpointów wykorzystane (51% limitu)
✅ Pozostało 34 sloty na rozszerzenia
⚠️ Jedyny kompromis: orderbook jako dane JSON, nie screenshoty

Dla screenshotów orderbooka będziesz potrzebować:

Własnej wizualizacji danych z Coinglass API, LUB
Bezpośredniego połączenia z WebSocket/API Bitmex (darmowe)
---
CoinGlass API is a powerful and comprehensive API system designed to aggregate real-time and historical data from major cryptocurrency exchanges across futures, spot, options, ETF, and on-chain markets.

Originally known for its robust futures data aggregation, CoinGlass API provides reliable access to key metrics such as contract trading volume, open interest, funding rates, liquidation events, liquidation heatmaps, liquidation maps, and long/short ratios. Today, the platform has expanded its coverage to include a wide array of critical market indicators spanning spot order books, whale positions, ETF net asset flows, on-chain reserves, and macro sentiment indexes.

As a professional-grade data platform, CoinGlass API supports thousands of trading pairs and hundreds of digital assets across multiple market types. It is trusted by quantitative traders, institutions, data analysts, and developers to power research, strategy, and monitoring infrastructure.

✅ Key Highlights: Aggregated data from leading futures and spot exchanges including Binance, OKX, Bybit, Coinbase, and more

Coverage of over 2000+ crypto derivatives and global options products

Fine-grained historical and real-time access to funding rates, OI, price OHLC, open interest, whale metrics, long/short ratios, and liquidation flows

Enhanced visibility into ETF flows, on-chain reserves, ERC20 transfers, and macro market indexes such as Crypto Fear & Greed, S2F, and Rainbow Chart

Developer-friendly RESTful interface with pagination, filtering, and scalable response structures

CoinGlass API empowers users to monitor market trends, identify strategic opportunities, and quantitatively analyze crypto markets with precision and speed.


Some endpoints will require an API Key. Please refer to this page.

1.Register your coinglass account

2.Log in

3.Check API Key

The base endpoinpus: <https://open-api-v4.coinglass.com>

All endpoints return either a JSON object or array.
---
All requests to the CoinGlass API require authentication using a unique, user-specific API Key.

Requests without a valid API Key or missing headers will be rejected with an authentication error.


🧾 How to Get an API Key

To get started, log in to your account and generate your API Key from your API Key Dashboard.

✅ Example Usage

curl

curl -X GET "https://open-api-v4.coinglass.com/api/futures/supported-coins" \
  -H "accept: application/json" \
  -H "CG-API-KEY: YOUR_API_KEY"

📦 Header Requirement

Every request must include the following HTTP header:

CG-API-KEY: your_api_key_here

If this header is missing or the API Key is invalid, the request will be denied with a 401 Unauthorized error. ❗


Response Headers:


API-KEY-MAX-LIMIT: Indicates the maximum allowed request limit for your API key (per minute).
API-KEY-USE-LIMIT: Shows the current usage count of your API key (requests made in the current time period).
---
Errors & Rate Limits

📡 API Response Status Codes

The CoinGlass API uses standard HTTP status codes to indicate the success or failure of your requests. Refer to the table below for a quick understanding of common response codes:
Status Code	Description
0	Successful Request
400	Missing or invalid parameters
401	Invalid or missing API key
404	The requested resource does not exist
405	Unsupported HTTP method
408	The request took too long to complete
422	Parameters valid but not acceptable
429	Rate limit exceeded
500	An unexpected error occurred on the server

---

Endpoint Overview
CoinGlass API provides a rich set of endpoints that cover a wide range of crypto market data, including Futures, Spot, Options, ETF, On-Chain, and Index data. Below is a categorized overview of all available endpoints to help you navigate and integrate efficiently.

Endpoints	Description
Market	
/futures/supported-coins	Get supported futures coins
/futures/supported-exchange-pairs	Get supported exchanges and pairs
/api/futures/pairs-markets	Futures pair markets
/api/futures/coins-markets	Futures coin markets
/futures/price-change-list	Price change list
/api/price/ohlc-history	Price OHLC history
Open Interest	
/api/futures/openInterest/ohlc-history	Open interest OHLC history
/api/futures/openInterest/ohlc-aggregated-history	Aggregated OI OHLC history
/api/futures/openInterest/ohlc-aggregated-stablecoin	Aggregated stablecoin OI OHLC
/api/futures/openInterest/ohlc-aggregated-coin-margin-history	Aggregated coin margin OI OHLC
/api/futures/openInterest/exchange-list	OI by exchange list
/api/futures/openInterest/exchange-history-chart	OI chart by exchange
Funding Rate	
/api/futures/fundingRate/ohlc-history	Funding rate OHLC history
/api/futures/fundingRate/oi-weight-ohlc-history	OI-weighted funding rate OHLC
/api/futures/fundingRate/vol-weight-ohlc-history	Volume-weighted funding rate OHLC
/api/futures/fundingRate/exchange-list	Funding rate by exchange list
/api/futures/fundingRate/accumulated-exchange-list	Cumulative funding rate list
/api/futures/fundingRate/arbitrage	Funding arbitrage opportunities
Long/Short Ratio	
/api/futures/global-long-short-account-ratio/history	Global long/short account ratio
/api/futures/top-long-short-account-ratio/history	Top trader long/short ratio
/api/futures/top-long-short-position-ratio/history	Top trader position ratio
/api/futures/taker-buy-sell-volume/exchange-list	Exchange Taker Buy/Sell Ratio
Liquidation	
/api/futures/liquidation/history	Pair Liquidation History
/api/futures/liquidation/aggregated-history	Coin Liquidation History
/api/futures/liquidation/coin-list	Liquidation Coin List
/api/futures/liquidation/exchange-list	Liquidation Exchange List
/api/futures/liquidation/order	Liquidation Order
/api/futures/liquidation/heatmap/model1	Pair Liquidation Heatmap Model1
/api/futures/liquidation/heatmap/model2	Pair Liquidation Heatmap Model2
/api/futures/liquidation/heatmap/model3	Pair Liquidation Heatmap Model3
/api/futures/liquidation/aggregated-heatmap/model1	Coin Liquidation Heatmap Model1
/api/futures/liquidation/aggregated-heatmap/model2	Coin Liquidation Heatmap Model2
/api/futures/liquidation/aggregated-heatmap/model3	Coin Liquidation Heatmap Model3
/api/futures/liquidation/map	Pair Liquidation Map
/api/futures/liquidation/aggregated-map	Coin Liquidation Map
Order Book	
/api/futures/orderbook/ask-bids-history	Pair Orderbook Bid&Ask(±range)
/api/futures/orderbook/aggregated-ask-bids-history	Coin Orderbook Bid&Ask(±range)
/api/futures/orderbook/history	Orderbook Heatmap
/api/futures/orderbook/large-limit-order	Large Orderbook
/api/futures/orderbook/large-limit-order-history	Large Orderbook History
Whale Postions	
/api/hyperliquid/whale-alert	Hyperliquid Whale Alert
/api/hyperliquid/whale-position	Hyperliquid Whale Position
Taker Buy/Sell	
/api/futures/taker-buy-sell-volume/history	Pair Taker Buy/Sell History
/api/futures/aggregated-taker-buy-sell-volume/history	Coin Taker Buy/Sell History
Spots	
/api/spot/supported-coins	Supported Coins
/api/spot/supported-exchange-pairs	Suported Exchange and Pairs
/api/spot/coins-markets	Coins Markets
/api/spot/pairs-markets	Pairs Markets
/api/spot/price/history	Price OHLC History
Order Book	
/api/spot/orderbook/ask-bids-history	Pair Orderbook Bid&Ask(±range)
/api/spot/orderbook/aggregated-ask-bids-history	Coin Orderbook Bid&Ask(±range)
/api/spot/orderbook/history	Orderbook Heatmap
/api/spot/orderbook/large-limit-order	Large Orderbook
/api/spot/orderbook/large-limit-order-history	Large Orderbook History
Taker Buy/Sell	
/api/spot/taker-buy-sell-volume/history	Pair Taker Buy/Sell History
/api/spot/aggregated-taker-buy-sell-volume/history	Coin Taker Buy/Sell History
Options	
/api/option/max-pain	Option Max Pain
/api/option/info	Options Info
/api/option/exchange-oi-history	Exchange Open Interest History
/api/option/exchange-vol-history	Exchange Volume History
On-Chain	
/api/exchange/assets	Exchange Assets
/api/exchange/balance/list	Exchange Balance List
/api/exchange/balance/chart	Exchange Balance Chart
/api/exchange/chain/tx/list	Exchange On-chain Transfers (ERC-20)
ETF	
/api/etf/bitcoin/list	Bitcoin ETF List
/api/hk-etf/bitcoin/flow-history	Hong Kong ETF Flows History
/api/etf/bitcoin/net-assets/history	ETF NetAssets History
/api/etf/bitcoin/flow-history	ETF Flows History
/api/etf/bitcoin/premium-discount/history	ETF Premium/Discount History
/api/etf/bitcoin/history	ETF History
/api/etf/bitcoin/price/history	ETF Price History
/api/etf/bitcoin/detail	ETF Detail
/api/etf/ethereum/net-assets-history	ETF NetAssets History
/api/etf/ethereum/list	Ethereum ETF List
/api/etf/ethereum/flow-history	ETF Flows History
/api/grayscale/holdings-list	Holdings List
/api/grayscale/premium-history	Premium History
Indic	
/api/futures/rsi/list	RSI List
/api/futures/basis/history	Futures Basis
/api/coinbase-premium-index	Coinbase Premium Index
/api/bitfinex-margin-long-short	Bitfinex Margin Long/Short
/api/index/ahr999	AHR999
/api/index/puell-multiple	Puell-Multiple
/api/index/stock-flow	Stock-to-Flow Model
/api/index/pi-cycle-indicator	Pi Cycle Top Indicator
/api/index/golden-ratio-multiplier	Golden-Ratio-Multiplier
/api/index/bitcoin/profitable-days	Bitcoin Profitable Days
/api/index/bitcoin/rainbow-chart	Bitcoin-Rainbow-Chart
/api/index/fear-greed-history	Crypto Fear & Greed Index
/api/index/stableCoin-marketCap-history	StableCoin MarketCap History
/api/index/bitcoin/bubble-index	Bitcoin Bubble Index
/api/bull-market-peak-indicator	Bull Market Peak Indicators
/api/index/2-year-ma-multiplier	Tow Year Ma Multiplier
/api/index/200-week-moving-average-heatmap	200-Week Moving Avg Heatmap
/api/borrow-interest-rate/history	Borrow Interest Rate
---
🎯 Główne wnioski:
✅ 6 z 7 wymagań w pełni dostępnych w planie Hobbyist (70 endpointów)
Stan dostępności:

Price BTC/USD: ✅ 100%
Avg Funding: ✅ 100%
L/S Ratio: ✅ 100%
Open Interest: ✅ 100%
Liquidations: ✅ 100%
Heatmapy Coinglass: ✅ 100%
Orderbook Bitmex: ⚠️ 80% (dane dostępne, ale API nie daje screenshotów)

💡 Dla orderbooka masz 3 opcje:

Użyj danych z Coinglass + własna wizualizacja (Python/plotly)
WebSocket Bitmex (darmowy, real-time)
REST API Bitmex (darmowy, dla snapshots)

Wykorzystujesz tylko 36 z 70 endpointów - zostaje Ci 34 sloty na dodatkowe wskaźniki (Fear & Greed, whale alerts, exchange reserves, etc.)
Czy chcesz, żebym przygotował przykładowy kod do pobierania tych danych lub pokazał jak zwizualizować orderbook z danych Coinglass?Napisz kod i pokaż jak zwizualizować orderbook z coinglass. Nie chcemy pobierać danych częściej niż 1 minuta. Wypisz dla tych naszych wskaźników bez bitmex.00:21Bot tradingowy - Coinglass API IntegrationCode """
Bot tradingowy - Integracja z Coinglass API v4
Limit zapytań: 1 minuta między requestami
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import time
import jsStworzyłem kompletny kod bota z integracją Coinglass API!
🎯 Co zawiera:
✅ Wszystkie 6 wskaźników (bez Bitmex):

Price BTC/USD - aktualna cena + OHLC świece
Avg Funding Rate - ważony po OI + interpretacja sentymentu
Long/Short Ratio - retail vs wieloryby
Open Interest - agregowany + per giełda + zmiana 24h
Liquidations - total + podział long/short + poziom bólu
Liquidation Heatmap - magnesy cenowe (top 10 klastrów)
Orderbook - ściany BID/ASK + whale walls + wizualizacja

🔒 Rate Limiting:

Automatyczne 60s między requestami do tego samego endpointa
Dashboard ~6-7 minut na pełny cykl
Tracking czasu per endpoint

📊 Wizualizacje:

Liquidation Heatmap - scatter plot z top 3 poziomami
Orderbook Depth - styl Bitmex (kumulatywny volume)
Whale Walls - duże zlecenia jako bar chart

💡 Dodatkowe features:

Interpretacje wskaźników (np. "Retail FOMO - rozważyć SHORT")
Export do JSON
Pandas DataFrames dla historii
Error handling

🚀 Jak użyć:
python# 1. Ustaw API key
API_KEY = "your_api_key"

# 2. Inicjalizuj
bot = CoinglassBot(API_KEY)

# 3. Pojedyncze wskaźniki (szybkie)
price = bot.get_btc_price_current()
funding = bot.get_funding_rate()

# 4. Lub pełny dashboard (6-7 min)
dashboard = bot.get_full_dashboard()
bot.save_dashboard(dashboard)
---
Przykładowy kod od Cloud Sonet 4.5:
"""
Bot tradingowy - Integracja z Coinglass API v4
Limit zapytań: 1 minuta między requestami
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional
import numpy as np

# Konfiguracja
API_KEY = "your_api_key_here"
BASE_URL = "https://open-api-v4.coinglass.com"
MIN_REQUEST_INTERVAL = 60  # 60 sekund między requestami

class CoinglassBot:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "coinglassSecret": api_key
        }
        self.last_request_time = {}
        
    def _rate_limit(self, endpoint: str):
        """Zapewnia minimum 60s między requestami do tego samego endpointa"""
        current_time = time.time()
        if endpoint in self.last_request_time:
            elapsed = current_time - self.last_request_time[endpoint]
            if elapsed < MIN_REQUEST_INTERVAL:
                sleep_time = MIN_REQUEST_INTERVAL - elapsed
                print(f"⏱️  Rate limit: czekam {sleep_time:.1f}s przed {endpoint}")
                time.sleep(sleep_time)
        self.last_request_time[endpoint] = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Wykonuje request z rate limiting"""
        self._rate_limit(endpoint)
        url = f"{BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error requesting {endpoint}: {e}")
            return None

    # ==========================================
    # 1. PRICE BTC/USD (BAZA)
    # ==========================================
    
    def get_btc_price_current(self) -> Dict:
        """Aktualna cena BTC z futures markets"""
        print("\n📊 1. Pobieranie aktualnej ceny BTC...")
        data = self._make_request(
            "/api/futures/coins-markets",
            params={"symbol": "BTC"}
        )
        if data and data.get("success"):
            price_data = data["data"][0] if data["data"] else {}
            result = {
                "price": price_data.get("price"),
                "change_24h": price_data.get("priceChangePercent"),
                "volume_24h": price_data.get("volUsd"),
                "timestamp": datetime.now().isoformat()
            }
            print(f"   💰 Cena: ${result['price']:,.2f}")
            print(f"   📈 Zmiana 24h: {result['change_24h']:.2f}%")
            return result
        return None
    
    def get_btc_ohlc(self, interval: str = "1h", limit: int = 100) -> pd.DataFrame:
        """Historia cen OHLC (świece)
        
        Args:
            interval: '1m', '5m', '15m', '30m', '1h', '4h', '1d'
            limit: ilość świec (max 2000)
        """
        print(f"\n📊 1. Pobieranie OHLC {interval}...")
        data = self._make_request(
            "/api/price/ohlc-history",
            params={
                "symbol": "BTC",
                "interval": interval,
                "limit": limit
            }
        )
        if data and data.get("success"):
            df = pd.DataFrame(data["data"])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            print(f"   ✅ Pobrano {len(df)} świec")
            return df
        return pd.DataFrame()

    # ==========================================
    # 2. AVG FUNDING RATE (SENTYMENT)
    # ==========================================
    
    def get_funding_rate(self) -> Dict:
        """Aktualny funding rate ze wszystkich giełd"""
        print("\n💸 2. Pobieranie Funding Rate...")
        data = self._make_request(
            "/api/futures/fundingRate/exchange-list",
            params={"symbol": "BTC"}
        )
        if data and data.get("success"):
            exchanges = data["data"]
            
            # Oblicz średnią ważoną po OI
            total_oi = sum(ex.get("openInterest", 0) for ex in exchanges)
            if total_oi > 0:
                weighted_fr = sum(
                    ex.get("fundingRate", 0) * ex.get("openInterest", 0) 
                    for ex in exchanges
                ) / total_oi
            else:
                weighted_fr = np.mean([ex.get("fundingRate", 0) for ex in exchanges])
            
            result = {
                "weighted_avg": weighted_fr,
                "simple_avg": np.mean([ex.get("fundingRate", 0) for ex in exchanges]),
                "min": min(ex.get("fundingRate", 0) for ex in exchanges),
                "max": max(ex.get("fundingRate", 0) for ex in exchanges),
                "exchanges_data": exchanges,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"   💰 Średnia ważona: {result['weighted_avg']:.4f}%")
            print(f"   📊 Zakres: {result['min']:.4f}% - {result['max']:.4f}%")
            
            # Interpretacja
            if result['weighted_avg'] > 0.01:
                print(f"   🔴 LONG dominują (płacą SHORT)")
            elif result['weighted_avg'] < -0.01:
                print(f"   🟢 SHORT dominują (płacą LONG)")
            else:
                print(f"   ⚪ Rynek zbalansowany")
            
            return result
        return None
    
    def get_funding_rate_history(self, interval: str = "1h", limit: int = 168) -> pd.DataFrame:
        """Historia funding rate (domyślnie 7 dni przy 1h)"""
        print(f"\n💸 2. Pobieranie historii Funding Rate...")
        data = self._make_request(
            "/api/futures/fundingRate/ohlc-history",
            params={
                "symbol": "BTC",
                "interval": interval,
                "limit": limit
            }
        )
        if data and data.get("success"):
            df = pd.DataFrame(data["data"])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            print(f"   ✅ Pobrano {len(df)} punktów")
            return df
        return pd.DataFrame()

    # ==========================================
    # 3. LONG/SHORT RATIO (POZYCJE ULICY)
    # ==========================================
    
    def get_long_short_ratio(self) -> Dict:
        """Globalny Long/Short ratio + Top traders"""
        print("\n⚖️  3. Pobieranie Long/Short Ratio...")
        
        # Global ratio (retail)
        global_data = self._make_request(
            "/api/futures/global-long-short-account-ratio/history",
            params={
                "symbol": "BTC",
                "interval": "1h",
                "limit": 1
            }
        )
        
        time.sleep(1)  # Dodatkowa przerwa między requestami
        
        # Top traders ratio
        top_data = self._make_request(
            "/api/futures/top-long-short-account-ratio/history",
            params={
                "symbol": "BTC",
                "interval": "1h",
                "limit": 1
            }
        )
        
        result = {}
        
        if global_data and global_data.get("success"):
            latest = global_data["data"][0] if global_data["data"] else {}
            result["retail_long_ratio"] = latest.get("longRatio", 0)
            result["retail_short_ratio"] = latest.get("shortRatio", 0)
            print(f"   👥 Retail - Long: {result['retail_long_ratio']:.2f}% | Short: {result['retail_short_ratio']:.2f}%")
        
        if top_data and top_data.get("success"):
            latest = top_data["data"][0] if top_data["data"] else {}
            result["whale_long_ratio"] = latest.get("longRatio", 0)
            result["whale_short_ratio"] = latest.get("shortRatio", 0)
            print(f"   🐋 Wieloryby - Long: {result['whale_long_ratio']:.2f}% | Short: {result['whale_short_ratio']:.2f}%")
        
        # Interpretacja
        if result.get("retail_long_ratio", 0) > 60:
            print(f"   ⚠️  Retail FOMO - rozważyć SHORT")
        elif result.get("retail_short_ratio", 0) > 60:
            print(f"   💚 Retail panic - rozważyć LONG")
        
        result["timestamp"] = datetime.now().isoformat()
        return result

    # ==========================================
    # 4. OPEN INTEREST (PALIWO DO RUCHU)
    # ==========================================
    
    def get_open_interest(self) -> Dict:
        """Open Interest agregowany + per giełda"""
        print("\n🔥 4. Pobieranie Open Interest...")
        
        # OI agregowany
        agg_data = self._make_request(
            "/api/futures/openInterest/ohlc-aggregated-history",
            params={
                "symbol": "BTC",
                "interval": "1h",
                "limit": 24  # Ostatnie 24h
            }
        )
        
        time.sleep(1)
        
        # OI per giełda
        exchange_data = self._make_request(
            "/api/futures/openInterest/exchange-list",
            params={"symbol": "BTC"}
        )
        
        result = {}
        
        if agg_data and agg_data.get("success"):
            df = pd.DataFrame(agg_data["data"])
            current_oi = df.iloc[-1]["openInterest"] if len(df) > 0 else 0
            oi_24h_ago = df.iloc[0]["openInterest"] if len(df) > 0 else 0
            oi_change = ((current_oi - oi_24h_ago) / oi_24h_ago * 100) if oi_24h_ago > 0 else 0
            
            result["current_oi"] = current_oi
            result["oi_change_24h"] = oi_change
            result["oi_history"] = df
            
            print(f"   💰 Aktualny OI: ${current_oi:,.0f}")
            print(f"   📊 Zmiana 24h: {oi_change:+.2f}%")
        
        if exchange_data and exchange_data.get("success"):
            result["exchanges"] = exchange_data["data"]
            top_3 = sorted(exchange_data["data"], 
                          key=lambda x: x.get("openInterest", 0), 
                          reverse=True)[:3]
            print(f"   🏆 Top giełdy:")
            for ex in top_3:
                print(f"      {ex['exchangeName']}: ${ex.get('openInterest', 0):,.0f}")
        
        # Interpretacja
        if result.get("oi_change_24h", 0) > 5:
            print(f"   ⚠️  Wzrost OI +5% - nowe pozycje, potencjalna zmienność")
        elif result.get("oi_change_24h", 0) < -5:
            print(f"   ✅ Spadek OI -5% - zamykanie pozycji, konsolidacja")
        
        result["timestamp"] = datetime.now().isoformat()
        return result

    # ==========================================
    # 5. LIQUIDATIONS (POZIOM BÓLU)
    # ==========================================
    
    def get_liquidations(self, time_range: str = "24h") -> Dict:
        """Dane o likwidacjach"""
        print(f"\n💀 5. Pobieranie Liquidations ({time_range})...")
        
        data = self._make_request(
            "/api/futures/liquidation/aggregated-history",
            params={
                "symbol": "BTC",
                "interval": "1h",
                "limit": 24 if time_range == "24h" else 168
            }
        )
        
        if data and data.get("success"):
            df = pd.DataFrame(data["data"])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            
            total_long_liq = df["longLiquidationUsd"].sum()
            total_short_liq = df["shortLiquidationUsd"].sum()
            total_liq = total_long_liq + total_short_liq
            
            result = {
                "total_liquidations": total_liq,
                "long_liquidations": total_long_liq,
                "short_liquidations": total_short_liq,
                "long_liq_ratio": (total_long_liq / total_liq * 100) if total_liq > 0 else 0,
                "history": df,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"   💰 Całkowite likwidacje: ${total_liq:,.0f}")
            print(f"   🔴 Long: ${total_long_liq:,.0f} ({result['long_liq_ratio']:.1f}%)")
            print(f"   🟢 Short: ${total_short_liq:,.0f} ({100-result['long_liq_ratio']:.1f}%)")
            
            # Interpretacja
            if result['long_liq_ratio'] > 70:
                print(f"   ⚠️  Dominacja likwidacji LONG - rynek spadał")
            elif result['long_liq_ratio'] < 30:
                print(f"   ⚠️  Dominacja likwidacji SHORT - rynek rósł")
            
            return result
        return None

    # ==========================================
    # 6. HEATMAPA LIQUIDACJI (MAGNESY CENY)
    # ==========================================
    
    def get_liquidation_heatmap(self) -> Dict:
        """Pobiera dane heatmapy likwidacji (3 modele)"""
        print("\n🔥 6. Pobieranie Liquidation Heatmap...")
        
        # Model 1 - podstawowy
        data = self._make_request(
            "/api/futures/liquidation/heatmap/model1",
            params={"symbol": "BTC"}
        )
        
        if data and data.get("success"):
            heatmap_data = data["data"]
            
            # Znajdź największe klastry likwidacji
            clusters = []
            for item in heatmap_data:
                clusters.append({
                    "price": item.get("price"),
                    "liquidation_volume": item.get("volume"),
                    "side": item.get("side")  # long/short
                })
            
            # Sortuj po volume
            clusters = sorted(clusters, key=lambda x: x["liquidation_volume"], reverse=True)[:10]
            
            result = {
                "top_clusters": clusters,
                "full_data": heatmap_data,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"   🎯 Top 5 poziomów likwidacji:")
            for i, cluster in enumerate(clusters[:5], 1):
                print(f"      {i}. ${cluster['price']:,.0f} - ${cluster['liquidation_volume']:,.0f} ({cluster['side']})")
            
            return result
        return None
    
    def visualize_liquidation_heatmap(self, heatmap_data: Dict):
        """Wizualizuje heatmapę likwidacji"""
        if not heatmap_data or "full_data" not in heatmap_data:
            print("❌ Brak danych do wizualizacji")
            return
        
        data = heatmap_data["full_data"]
        df = pd.DataFrame(data)
        
        # Oddziel long i short
        df_long = df[df['side'] == 'long'].copy()
        df_short = df[df['side'] == 'short'].copy()
        
        plt.figure(figsize=(14, 8))
        
        # Plot heatmap
        plt.scatter(df_long['price'], df_long['volume'], 
                   c='red', alpha=0.6, s=df_long['volume']/1e6, 
                   label='Long Liquidations')
        plt.scatter(df_short['price'], df_short['volume'], 
                   c='green', alpha=0.6, s=df_short['volume']/1e6,
                   label='Short Liquidations')
        
        plt.xlabel('Cena BTC (USD)', fontsize=12)
        plt.ylabel('Wolumen likwidacji (USD)', fontsize=12)
        plt.title('🔥 Liquidation Heatmap - Magnesy cenowe', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ticklabel_format(style='plain', axis='y')
        
        # Dodaj linie dla top 3 klastrów
        top_3 = heatmap_data["top_clusters"][:3]
        for i, cluster in enumerate(top_3, 1):
            plt.axvline(x=cluster['price'], color='orange', linestyle='--', alpha=0.5)
            plt.text(cluster['price'], plt.ylim()[1]*0.9, 
                    f"#{i}: ${cluster['price']:,.0f}", 
                    rotation=90, va='top')
        
        plt.tight_layout()
        plt.savefig('liquidation_heatmap.png', dpi=300, bbox_inches='tight')
        print("   ✅ Zapisano: liquidation_heatmap.png")
        plt.show()

    # ==========================================
    # 7. ORDERBOOK (ŚCIANY I WSPARCIA)
    # ==========================================
    
    def get_orderbook(self) -> Dict:
        """Pobiera dane orderbooka (bid/ask levels)"""
        print("\n📖 7. Pobieranie Orderbook...")
        
        data = self._make_request(
            "/api/futures/orderbook/ask-bids-history",
            params={
                "symbol": "BTC",
                "exchange": "Binance",  # Możesz zmienić
                "range": 1000  # ±1000 USD od aktualnej ceny
            }
        )
        
        if data and data.get("success"):
            orderbook = data["data"]
            
            bids = orderbook.get("bids", [])
            asks = orderbook.get("asks", [])
            
            # Oblicz "ściany" (duże zlecenia)
            bid_volumes = [b["volume"] for b in bids]
            ask_volumes = [a["volume"] for a in asks]
            
            bid_wall_threshold = np.percentile(bid_volumes, 90) if bid_volumes else 0
            ask_wall_threshold = np.percentile(ask_volumes, 90) if ask_volumes else 0
            
            bid_walls = [b for b in bids if b["volume"] > bid_wall_threshold]
            ask_walls = [a for a in asks if a["volume"] > ask_wall_threshold]
            
            result = {
                "bids": bids,
                "asks": asks,
                "bid_walls": bid_walls,
                "ask_walls": ask_walls,
                "total_bid_volume": sum(bid_volumes),
                "total_ask_volume": sum(ask_volumes),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"   📊 Bid levels: {len(bids)} | Ask levels: {len(asks)}")
            print(f"   💰 Bid volume: ${result['total_bid_volume']:,.0f}")
            print(f"   💰 Ask volume: ${result['total_ask_volume']:,.0f}")
            print(f"   🧱 Bid walls: {len(bid_walls)} | Ask walls: {len(ask_walls)}")
            
            return result
        return None
    
    def get_large_orderbook(self) -> Dict:
        """Pobiera duże zlecenia (whale walls)"""
        print("\n🐋 7. Pobieranie Large Orderbook...")
        
        data = self._make_request(
            "/api/futures/orderbook/large-limit-order",
            params={"symbol": "BTC"}
        )
        
        if data and data.get("success"):
            large_orders = data["data"]
            
            # Grupuj per cenę i stronę
            bid_orders = [o for o in large_orders if o.get("side") == "bid"]
            ask_orders = [o for o in large_orders if o.get("side") == "ask"]
            
            result = {
                "bid_orders": bid_orders,
                "ask_orders": ask_orders,
                "total_bid_orders": len(bid_orders),
                "total_ask_orders": len(ask_orders),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"   🐋 Duże BID: {len(bid_orders)} zleceń")
            print(f"   🐋 Duże ASK: {len(ask_orders)} zleceń")
            
            if bid_orders:
                top_bid = max(bid_orders, key=lambda x: x.get("volume", 0))
                print(f"   💰 Największy BID: ${top_bid.get('price'):,.0f} (${top_bid.get('volume'):,.0f})")
            
            if ask_orders:
                top_ask = max(ask_orders, key=lambda x: x.get("volume", 0))
                print(f"   💰 Największy ASK: ${top_ask.get('price'):,.0f} (${top_ask.get('volume'):,.0f})")
            
            return result
        return None
    
    def visualize_orderbook(self, orderbook_data: Dict):
        """Wizualizuje orderbook z 'ścianami'"""
        if not orderbook_data:
            print("❌ Brak danych orderbooka")
            return
        
        bids = orderbook_data.get("bids", [])
        asks = orderbook_data.get("asks", [])
        
        if not bids or not asks:
            print("❌ Puste dane bids/asks")
            return
        
        # Przygotuj dane
        bid_prices = [b["price"] for b in bids]
        bid_volumes = [b["volume"] for b in bids]
        ask_prices = [a["price"] for a in asks]
        ask_volumes = [a["volume"] for a in asks]
        
        # Kumulatywne volume
        bid_cumsum = np.cumsum(bid_volumes[::-1])[::-1]
        ask_cumsum = np.cumsum(ask_volumes)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Panel 1: Orderbook depth
        ax1.fill_between(bid_prices, 0, bid_cumsum, color='green', alpha=0.3, label='Bids')
        ax1.fill_between(ask_prices, 0, ask_cumsum, color='red', alpha=0.3, label='Asks')
        ax1.set_xlabel('Cena (USD)', fontsize=12)
        ax1.set_ylabel('Kumulatywny Volume', fontsize=12)
        ax1.set_title('📖 Orderbook Depth - Bitmex Style', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Panel 2: Whale walls (duże zlecenia)
        bid_walls = orderbook_data.get("bid_walls", [])
        ask_walls = orderbook_data.get("ask_walls", [])
        
        if bid_walls:
            wall_prices = [w["price"] for w in bid_walls]
            wall_volumes = [w["volume"] for w in bid_walls]
            ax2.bar(wall_prices, wall_volumes, color='green', alpha=0.6, width=50, label='Bid Walls')
        
        if ask_walls:
            wall_prices = [w["price"] for w in ask_walls]
            wall_volumes = [w["volume"] for w in ask_walls]
            ax2.bar(wall_prices, wall_volumes, color='red', alpha=0.6, width=50, label='Ask Walls')
        
        ax2.set_xlabel('Cena (USD)', fontsize=12)
        ax2.set_ylabel('Volume', fontsize=12)
        ax2.set_title('🧱 Whale Walls - Duże zlecenia', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('orderbook_visualization.png', dpi=300, bbox_inches='tight')
        print("   ✅ Zapisano: orderbook_visualization.png")
        plt.show()

    # ==========================================
    # DASHBOARD - Wszystkie wskaźniki naraz
    # ==========================================
    
    def get_full_dashboard(self) -> Dict:
        """Pobiera wszystkie wskaźniki z respektowaniem rate limits (6-7 minut)"""
        print("\n" + "="*60)
        print("🚀 URUCHAMIANIE PEŁNEGO DASHBOARDU")
        print("⏱️  Szacowany czas: ~6-7 minut (rate limiting 60s)")
        print("="*60)
        
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "indicators": {}
        }
        
        # 1. Price (1 request)
        dashboard["indicators"]["price"] = self.get_btc_price_current()
        
        # 2. Funding Rate (1 request)
        dashboard["indicators"]["funding_rate"] = self.get_funding_rate()
        
        # 3. Long/Short Ratio (2 requests z 1s przerwą)
        dashboard["indicators"]["long_short"] = self.get_long_short_ratio()
        
        # 4. Open Interest (2 requests z 1s przerwą)
        dashboard["indicators"]["open_interest"] = self.get_open_interest()
        
        # 5. Liquidations (1 request)
        dashboard["indicators"]["liquidations"] = self.get_liquidations()
        
        # 6. Heatmap (1 request)
        dashboard["indicators"]["heatmap"] = self.get_liquidation_heatmap()
        
        # 7. Orderbook (1 request dla large orders jest lepsze)
        dashboard["indicators"]["orderbook"] = self.get_large_orderbook()
        
        print("\n" + "="*60)
        print("✅ DASHBOARD GOTOWY")
        print("="*60)
        
        return dashboard
    
    def save_dashboard(self, dashboard: Dict, filename: str = "dashboard.json"):
        """Zapisuje dashboard do pliku JSON"""
        with open(filename, 'w') as f:
            json.dump(dashboard, f, indent=2, default=str)
        print(f"💾 Dashboard zapisany: {filename}")


# ==========================================
# PRZYKŁAD UŻYCIA
# ==========================================

if __name__ == "__main__":
    # Inicjalizacja bota
    bot = CoinglassBot(API_KEY)
    
    # OPCJA 1: Pojedyncze wskaźniki (szybkie testy)
    print("\n" + "="*60)
    print("📊 PRZYKŁAD: Pojedyncze wskaźniki")
    print("="*60)
    
    # Cena
    price = bot.get_btc_price_current()
    
    # Funding rate
    funding = bot.get_funding_rate()
    
    # Long/Short
    ls_ratio = bot.get_long_short_ratio()
    
    # OPCJA 2: Pełny dashboard (6-7 minut z rate limiting)
    print("\n" + "="*60)
    print("🎯 OPCJA: Uruchomić pełny dashboard? (6-7 min)")
    print("="*60)
    
    run_full = input("Uruchomić pełny dashboard? (y/n): ").lower()
    
    if run_full == 'y':
        dashboard = bot.get_full_dashboard()
        bot.save_dashboard(dashboard)
        
        # Wizualizacje
        if dashboard["indicators"].get("heatmap"):
            bot.visualize_liquidation_heatmap(dashboard["indicators"]["heatmap"])
        
        if dashboard["indicators"].get("orderbook"):
            # Dla large orderbook potrzebujemy normalnego orderbooka do wizualizacji
            print("\n📊 Pobieranie pełnego orderbooka dla wizualizacji...")
            orderbook = bot.get_orderbook()
            if orderbook:
                bot.visualize_orderbook(orderbook)
    
    print("\n✅ Gotowe!")