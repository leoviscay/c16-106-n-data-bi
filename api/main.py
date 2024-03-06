from fastapi import FastAPI
import pandas as pdcd 
import numpy as np
import keras
from fastapi.middleware.cors import CORSMiddleware


from services import get_stock_predictions_today
app = FastAPI()

origins = [
    "https://finanalytica.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


