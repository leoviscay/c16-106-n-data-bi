import os
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def loadAndPredict(stock_name, data):
    # Construct the path to the model file
    model_path = f"./models/{stock_name}.h5"
    
    # Check if the model file exists
    if not os.path.exists(model_path):
        print(f"Model file for {stock_name} not found.")
        return None
    
    # Load the Keras model
    model = load_model(model_path)
    
    # Make predictions based on the data
    predictions = model.predict(data)
    
    # Scale the predictions using MinMaxScaler
    scaler = MinMaxScaler()
    scaler.fit(predictions)
    scaled_predictions = scaler.transform(predictions)
    
    # Inverse transform the scaled predictions
    inverse_predictions = scaler.inverse_transform(scaled_predictions)
    
    return inverse_predictions

