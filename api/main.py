from fastapi import FastAPI
import pandas as pdcd 
import numpy as np
import keras
from data import getLastMonthData
from predict import loadAndPredict
from utils import  calculate_pct_change,  check_and_convert_prediction
app = FastAPI()



@app.get("/{stock}")
def read_root(stock):
    try:
        data,  min_max_scaler, last_day  = getLastMonthData(stock)
        last_day = last_day["Close"]
        print("last_day")
        print(last_day)

        print("data.shape")
        print(data.shape)
        print("data.shape before reshaping:", data.shape)
        data_reshaped = data.reshape(1, 30, 7)
        
        predictions = loadAndPredict(stock, data_reshaped, min_max_scaler)

        

        final_prediction = check_and_convert_prediction(predictions)
        pct_change = calculate_pct_change(final_prediction, last_day)
        print("Percentage Change:", pct_change)


        print(final_prediction)
        return {"stock": stock, "predictions": final_prediction, "last_day": last_day, "pct_change": pct_change }

    except Exception as e:
        print(e)
        return {"Error": e, "keras": keras. __version__
}


