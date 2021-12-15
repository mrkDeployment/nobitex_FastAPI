from fastapi import FastAPI
from pydantic import BaseModel
import requests

import crud

app=FastAPI()

class Buy(BaseModel):
    quantity: int
    token: str
    nobitex_coin: str
    nobitex_coin_percent: int
    binance_coin: str
    coin: str
    buyPercent: float

class Sell(BaseModel):
    quantity: int
    token: str
    nobitex_coin: str
    nobitex_coin_percent: int
    binance_coin: str
    coin: str
    sellPercent: float

@app.post("/buy/")
def buy(buy:Buy):
    nobitex_buy=crud.buy(quantity=buy.quantity,
                         token=buy.token,
                         buyPercent=buy.buyPercent,
                         nobitex_coin=buy.nobitex_coin,
                         binance_coin=buy.binance_coin,
                         coin=buy.coin,
                         nobitex_coin_percent=buy.nobitex_coin_percent)

    return nobitex_buy


@app.post("/sell/")
def sell(sell:Sell):
    nobitex_sell=crud.sell(quantity=sell.quantity,
                         token=sell.token,
                         sellPercent=sell.sellPercent,
                         nobitex_coin=sell.nobitex_coin,
                         binance_coin=sell.binance_coin,
                         coin=sell.coin,
                         nobitex_coin_percent=sell.nobitex_coin_percent)
    return nobitex_sell