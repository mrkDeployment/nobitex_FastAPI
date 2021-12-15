import requests

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
          nobitex_price_bid: price_bid / nobitex_coin_percent

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


def sell(quantity: int, token: str,
        nobitex_coin: str,
        nobitex_coin_percent: int,
        binance_coin: str,
        coin: str,
        sellPercent: float = 10):
  response1 = requests.get('https://api.nobitex.ir/v2/orderbook/' + nobitex_coin)
  response = response1.json()
  print("eeeeee", response)

  price_sum_bid = 0

  tether = float(tether_price())

  nobitex_price_bid = {}

  for k in range(16):
    price_sum_bid += float(response["bids"][k][0]) * float(response["bids"][k][1])

    if (quantity * 3 < price_sum_bid):
      price_bid = float(response["bids"][k][0]) / tether
      nobitex_price_bid = price_bid / nobitex_coin_percent
      break
    else:
      if (k == 15):
        price_bid = float(response["bids"][15][0]) * 1.03 / tether
        nobitex_price_bid: price_bid / nobitex_coin_percent

  binance_price = {}
  print('sssssssssss')
  response1 = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + binance_coin)
  print('dddddddddddddd')
  response = response1.json()
  price = response["price"]
  binance_price = float(price)

  response_sell = {}

  if ((nobitex_price_bid - binance_price) / binance_price) * 100 > sellPercent:
    allowed_price = tether * 0.9875 * binance_price
    amount = str(quantity / (allowed_price * nobitex_coin_percent))
    config = {"Authorization": "Token " + token}
    sell_data = {
      "type": "sell",
      "execution": "market",
      "srcCurrency": coin,
      "dstCurrency": "rls",
      "amount": amount,
    }

    url = "https://api.nobitex.ir/market/orders/add"
    response1 = requests.post(url, headers=config, data=sell_data)
    response_sell = response1.json()

  return response_sell
