import os
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def loadAndPredict(stock_name, data, min_max_scaler):
    # Construct the path to the model file
    model_path_h5 = f"./models/{stock_name}.h5"
    model_path_keras = f"./models/{stock_name}.keras"

    # Check if the model file exists with .h5 extension
    if os.path.exists(model_path_h5):
        model_path = model_path_h5
    # Check if the model file exists with .keras extension
    elif os.path.exists(model_path_keras):
        model_path = model_path_keras
    else:
        print(f"Model file for {stock_name} not found.")
        return None
    
    # Load the Keras model
    model = load_model(model_path)

    # Make predictions based on the data

    try:
         # Predict using the model
        pred = model.predict(data)
        print("Predictions before scaling:")
        print(pred)
        prediction = min_max_scaler.inverse_transform(pred)
        print("Predictions after inverse scaling:")
        print(prediction)
        return prediction[0]

    except Exception as e:
        print(e)
        return e 
    

