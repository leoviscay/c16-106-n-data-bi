import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime, timedelta

def getDates():
    # Get today's date
    today = datetime.now().date()

    # Calculate 45 days before today
    days_before = today - timedelta(days=49)

    # Convert dates to strings in the required format
    start_date = days_before.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    return start_date, end_date

def scaleData(data, min_max_scaler):
    data['Pct change'] = data['Adj Close'].pct_change()
    columns_to_scale = ['High', 'Low', 'Open', 'Close', 'Volume', 'Pct change', 'Adj Close']
    
    # Remove NaN values before scaling
    data.dropna(inplace=True)
    
    # Reshape and scale each column
    for col in columns_to_scale:
        data[col] = min_max_scaler.fit_transform(data[col].values.reshape(-1, 1))
        
    return data

def batchData(data):
    data = data.values
    last_30_days_data = data[-30:]
    df = np.array([last_30_days_data])
    return df

def getLastMonthData(stock):
    start_date, end_date = getDates()
    df = yf.download(stock, start = start_date, end=end_date)
    data = df.reindex(['High','Low','Open','Close','Volume','Pct change','Adj Close'], axis=1)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaleData(data, scaler)
    X_data = batchData(scaled_data)

    return X_data[0]
    