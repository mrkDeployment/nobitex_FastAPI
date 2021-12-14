from fastapi import FastAPI
from pydantic import BaseModel

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