from fastapi import FastAPI
import pandas as pd
import numpy as np
import keras
from data import getLastMonthData
from predict import loadAndPredict

app = FastAPI()

@app.get("/{stock}")
def read_root(stock):
    try:
        data = getLastMonthData(stock)
        print("data.shape")
        print(data.shape)
        print("data.shape before reshaping:", data.shape)

        # Reshape the data to match the expected input shape of the model
        data_reshaped = data.reshape(1, 30, 7)

        print("data.shape after reshaping:", data_reshaped.shape)
        predictions = loadAndPredict(stock, data)
        print(predictions)
        return {"Stock": stock, "Predictions": predictions}

    except Exception as e:
        print(e)
        return {"Error": e, "keras": keras. __version__
}


