from fastapi import FastAPI
import crud

app=FastAPI()

@app.post("/buy/")
def buy(quantity:int,token:str, buyPercent:float):
    nobitex_buy=crud.buy(quantity=quantity,token=token,buyPercent=buyPercent)

    return nobitex_buy


@app.post("/sell/")
def buy(quantity:int,token:str, sellPercent:float):
    nobitex_sell=crud.sell(quantity=quantity,token=token,sellPercent=sellPercent)

    return nobitex_sell