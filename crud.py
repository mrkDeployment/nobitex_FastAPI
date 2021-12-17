import requests
from fastapi import HTTPException


def tether_price():
    response1=requests.get('https://api.nobitex.ir/v2/orderbook/USDTIRT')
    response=response1.json()
    tether=float(response["bids"][0][0])

    return tether

def buy(quantity: int, token: str,
        nobitex_coin: str,
        nobitex_coin_percent:int,
        binance_coin: str,
        coin:str,
        buyPercent: float=10):

    response1=requests.get('https://api.nobitex.ir/v2/orderbook/' + nobitex_coin)
    response= response1.json()
    print("eeeeee",response)

    price_sum_bid = 0

    tether=float(tether_price())

    nobitex_price_bid={}

    for k in range(16):
      price_sum_bid += float(response["bids"][k][0]) * float(response["bids"][k][1])

      if (quantity * 3 < price_sum_bid):
        price_bid = float(response["bids"][k][0]) / tether
        nobitex_price_bid= price_bid / nobitex_coin_percent
        break
      else:
        if (k == 15):
          price_bid = float(response["bids"][15][0]) * 1.03 / tether
          nobitex_price_bid= price_bid / nobitex_coin_percent

    binance_price={}
    print('sssssssssss')
    response1= requests.get("https://api.binance.com/api/v3/ticker/price?symbol="+binance_coin)
    print('dddddddddddddd')
    response=response1.json()
    price= response["price"]
    binance_price= float(price)

    response_buy={}

    if ((binance_price-nobitex_price_bid) / binance_price)*100 > buyPercent:

      allowed_price = tether * 0.9875 * binance_price
      amount = str(quantity / (allowed_price * nobitex_coin_percent))
      config = {"Authorization": "Token " + token}
      buy_data = {
        "type": "buy",
        "execution": "market",
        "srcCurrency": coin,
        "dstCurrency": "rls",
        "amount": amount,
      }

      url="https://api.nobitex.ir/market/orders/add"
      response1 = requests.post(url, headers=config, data=buy_data)
      response_buy=response1.json()


    return response_buy


def sell(quantity: float,
         token: str,
         nobitex_coin: str,
        nobitex_coin_percent: int,
        binance_coin: str,
        coin: str,
        sellPercent: float = 10):

  response1 = requests.get('https://api.nobitex.ir/v2/orderbook/' + nobitex_coin)
  response = response1.json()

  price_sum_ask = 0

  tether = float(tether_price())

  nobitex_price_ask = {}

  for k in range(16):
    price_sum_ask += float(response["asks"][k][0]) * float(response["asks"][k][1])

    if (quantity * 3 * float(response["asks"][0][0]) < price_sum_ask):
      price_ask = float(response["asks"][k][0]) / tether
      nobitex_price_ask = price_ask / nobitex_coin_percent
      break
    else:
      if (k == 15):
        price_ask = float(response["asks"][15][0]) * 1.03 / tether
        nobitex_price_ask= price_ask / nobitex_coin_percent

  binance_price = {}

  try:
    response1 = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + binance_coin)
  except:
    raise HTTPException(status_code=402, detail="binance api don't work because of proxy failed")

  response = response1.json()
  price = response["price"]
  binance_price = float(price)

  response_sell = {}

  if ((nobitex_price_ask - binance_price) / binance_price) * 100 > sellPercent:
    allowed_price = tether * 0.9875 * binance_price
    amount = str(quantity / (allowed_price * nobitex_coin_percent))
    config = {"Authorization": "Token " + token}

    sell_data = {
      "type": "sell",
      "execution": "market",
      "srcCurrency": coin,
      "dstCurrency": "rls",
      "amount": str(quantity),
    }

    url = "https://api.nobitex.ir/market/orders/add"
    response1 = requests.post(url, headers=config, data=sell_data)
    response_sell = response1.json()

  return response_sell



def candle(symbol: str,interval: str='30m',limit: str ='6'):

  changed_percent = 0
  try:
    candle1=requests.get("https://api.binance.com/api/v3/klines?interval=" + interval + "&limit=" + limit + "&symbol=" + symbol)
  except:
    raise HTTPException(status_code=401,detail="sssssss")

  candle=candle1.json()
  changed_percent = (candle[int(limit) - 1][4] - candle[0][1]) / candle[0][1] * 100

  return changed_percent