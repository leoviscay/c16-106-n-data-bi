from fastapi import FastAPI
import pandas as pdcd 
import numpy as np
import keras

from services import get_stock_predictions_today
app = FastAPI()



@app.get("/prediction/{stock}")
def read_root(stock):
    try:
        print(stock)
        db_data, updated = get_stock_predictions_today(stock)
        print(db_data, updated)
        return {"stock": stock, "predictions": db_data["prediction"], "last_day": db_data["last_day"], "pct_change":db_data["pct_change"]  }

    except Exception as e:
        print(e)
        return {"Error": e.__cause__, "keras": keras. __version__}


