import requests

def tether_price():
    response1=requests.get('https://api.nobitex.ir/v2/orderbook/USDTIRT')
    response=response1.json()
    tether=float(response["bids"][0][0])

    return tether

async def buy(quantity: int, token: str, buyPercent: float=10):

    coin_list = [
      "btc",
      "eth",
      "ltc",
      "shib",
      "xlm",
      "trx",
      "doge",
      "etc",
      "bnb",
      "eos",
      "xrp",
      "uni",
      "link",
      "dot",
      "aave",
      "ada"
    ]

    nobitex_coin_list = [
      ["BTCIRT",1],
      ["ETHIRT",1],
      ["LTCIRT",1],
      ["SHIBIRT",1000],
      ["XLMIRT",1],
      ["TRXIRT",1],
      ["DOGEIRT",1],
      ["ETCIRT",1],
      ["BNBIRT",1],
      ["EOSIRT",1],
      ["XRPIRT",1],
      ["UNIIRT",1],
      ["LINKIRT",1],
      ["DOTIRT",1],
      ["AAVEIRT",1],
      ["ADAIRT",1]
    ]

    binance_coin_list = [
      "BTCUSDT",
      "ETHUSDT",
      "LTCUSDT",
      "SHIBUSDT",
      "XLMUSDT",
      "TRXUSDT",
      "DOGEUSDT",
      "ETCUSDT",
      "BNBUSDT",
      "EOSUSDT",
      "XRPUSDT",
      "UNIUSDT",
      "LINKUSDT",
      "DOTUSDT",
      "AAVEUSDT",
      "ADAUSDT"
    ]

    for i in range(1,len(nobitex_coin_list)+1):
      j=i-1

      response1=await requests.get('https://api.nobitex.ir/v2/orderbook/' + nobitex_coin_list[i - 1][0])
      response= response1.json()
      print("eeeeee",response)

      price_sum_bid = 0

      tether=float(tether_price())

      nobitex_price_bid={}

      for k in range(16):
        price_sum_bid += float(response["bids"][k][0]) * float(response["bids"][k][1])

        if (quantity * 3 < price_sum_bid):
          price_bid = float(response["bids"][k][0]) / tether
          nobitex_price_bid[j]= price_bid / nobitex_coin_list[j][1]
          break
        else:
          if (k == 15):
            price_bid = float(response["bids"][15][0]) * 1.03 / tether
            nobitex_price_bid[j]: price_bid / nobitex_coin_list[j][1]

      binance_price={}
      print('sssssssssss')
      response1=await requests.get("https://api.binance.com/api/v3/ticker/price?symbol="+binance_coin_list[j])
      print('dddddddddddddd')
      response=response1.json()
      price= response["price"]
      binance_price[j]= float(price)

      response_buy={}

      if ((binance_price[j]-nobitex_price_bid[j]) / binance_price[j])*100 > buyPercent:

        allowed_price = tether * 0.9875 * binance_price[j]
        amount = str(quantity / (allowed_price * nobitex_coin_list[j][1]))
        config = {"Authorization": "Token " + token}
        buy_data = {
          "type": "buy",
          "execution": "market",
          "srcCurrency": coin_list[j],
          "dstCurrency": "rls",
          "amount": amount,
        }

        url="https://api.nobitex.ir/market/orders/add"
        response1 = await requests.post(url, headers=config, data=buy_data)
        response_buy[j]=response1.json()


    return response_buy




async def sell(quantity: int, token: str, sellPercent: float = 10):
  coin_list = [
    "btc",
    "eth",
    "ltc",
    "shib",
    "xlm",
    "trx",
    "doge",
    "etc",
    "bnb",
    "eos",
    "xrp",
    "uni",
    "link",
    "dot",
    "aave",
    "ada"
  ]

  nobitex_coin_list = [
    ["BTCIRT", 1],
    ["ETHIRT", 1],
    ["LTCIRT", 1],
    ["SHIBIRT", 1000],
    ["XLMIRT", 1],
    ["TRXIRT", 1],
    ["DOGEIRT", 1],
    ["ETCIRT", 1],
    ["BNBIRT", 1],
    ["EOSIRT", 1],
    ["XRPIRT", 1],
    ["UNIIRT", 1],
    ["LINKIRT", 1],
    ["DOTIRT", 1],
    ["AAVEIRT", 1],
    ["ADAIRT", 1]
  ]

  binance_coin_list = [
    "BTCUSDT",
    "ETHUSDT",
    "LTCUSDT",
    "SHIBUSDT",
    "XLMUSDT",
    "TRXUSDT",
    "DOGEUSDT",
    "ETCUSDT",
    "BNBUSDT",
    "EOSUSDT",
    "XRPUSDT",
    "UNIUSDT",
    "LINKUSDT",
    "DOTUSDT",
    "AAVEUSDT",
    "ADAUSDT"
  ]

  for i in range(1, len(nobitex_coin_list) + 1):
    j = i - 1

    response1 = await requests.get('https://api.nobitex.ir/v2/orderbook/' + nobitex_coin_list[i - 1][0])
    response = response1.json()
    print("eeeeee", response)

    price_sum_bid = 0

    tether = float(tether_price())

    nobitex_price_bid = {}

    for k in range(16):
      price_sum_bid += float(response["bids"][k][0]) * float(response["bids"][k][1])

      if (quantity * 3 < price_sum_bid):
        price_bid = float(response["bids"][k][0]) / tether
        nobitex_price_bid[j] = price_bid / nobitex_coin_list[j][1]
        break
      else:
        if (k == 15):
          price_bid = float(response["bids"][15][0]) * 1.03 / tether
          nobitex_price_bid[j]: price_bid / nobitex_coin_list[j][1]

    binance_price = {}
    print('sssssssssss')
    response1 = await requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + binance_coin_list[j])
    print('dddddddddddddd')
    response = response1.json()
    price = response["price"]
    binance_price[j] = float(price)

    response_sell = {}

    if ((nobitex_price_bid[j]-binance_price[j]) / binance_price[j]) * 100 > sellPercent:
      allowed_price = tether * binance_price[j]
      amount = str(quantity / (allowed_price * nobitex_coin_list[j][1]))
      config = {"Authorization": "Token " + token}
      sell_data = {
        "type": "sell",
        "execution": "market",
        "srcCurrency": coin_list[j],
        "dstCurrency": "rls",
        "amount": amount,
      }

      url = "https://api.nobitex.ir/market/orders/add"
      response1 = requests.post(url, headers=config, data=sell_data)
      response_sell[j] = response1.json()

  return response_sell
