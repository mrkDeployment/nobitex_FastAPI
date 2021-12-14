from fastapi import FastAPI
from pydantic import BaseModel
import requests

import crud

app=FastAPI()


class Buy(BaseModel):
    quantity: int
    token: str
    buyPercent: float

class Sell(BaseModel):
    quantity: int
    token: str
    sellPercent: float

@app.post("/buy/")
def buy(buy:Buy):
    nobitex_buy=crud.buy(quantity=buy.quantity,token=buy.token,buyPercent=buy.buyPercent)

    return nobitex_buy


@app.post("/sell/")
def sell(sell:Sell):
    nobitex_sell=crud.sell(quantity=sell.quantity,token=sell.token,sellPercent=sell.sellPercent)

    return nobitex_sell

@app.get("/sedssd/")
def cdd():
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
  print('aaaaaaaaaa')
  response1 = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + binance_coin_list[0])
  response=response1.json()
  return response