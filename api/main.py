from fastapi import FastAPI
import pandas as pd
import numpy as np
import keras
from sklearn.preprocessing import MinMaxScaler


app = FastAPI()

df_data = pd.read_csv('../Data/stock_data.csv')


@app.get("/")
def read_root():
    print(df_data)
    return {"Hello": "World"}
