from datetime import datetime, date
from utils import calculate_pct_change, check_and_convert_prediction, check_last_row, create_supabase_client
from data import getLastMonthData
from predict import loadAndPredict

supabase = create_supabase_client()


def get_stock_predictions_today(stock_symbol):
   
    today = date.today()
    print("stock_symbol")            
    print(today) 
    if isinstance(stock_symbol, str):
        print("The object is of type str.")
    else:
        print("The object is not of type str.")           
    # Execute query
    data = supabase.table('predictions').select('*').eq('stock', stock_symbol).eq("created_at",today ).execute()
    print(data)
   
    current_time = datetime.now()
    print("stock_symbol")            
    print(current_time)
    # Assuming len(data) == 0 or data[0].updated_at
    if len(data.data) == 0:
        # Predict and create a new record in the database
        # Make predictions here...
        final_prediction, last_day, pct_change = get_final_prediction(stock_symbol) 
        # Assuming you have a function to insert the prediction into the database
        prediction = insert_into_database(stock_symbol, final_prediction, last_day, pct_change)
        return prediction, True
    elif ((current_time - datetime.strptime(data.data[0]["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")).total_seconds() / 3600 < 1) or data.data[0]["definitive"] == True:
        # Return existing data
        return data.data[0], False
    else:
        # Predict, update the record, and return data
        # Make predictions here...
        final_prediction, last_day, pct_change = get_final_prediction(stock_symbol)  
        # Assuming you have a function to update the prediction in the database
        print("data.data[0].id")
        print(data.data[0])
        prediction = update_database(data.data[0]["id"], final_prediction, last_day, pct_change, stock_symbol)
        print("prediction")
        print(prediction)
        return prediction, True

   
def insert_into_database(stock_symbol, final_prediction, last_day, pct_change):
    """
    Function to insert prediction data into the database.
    """
    # Assuming 'predictions' is the table name in your database
    prediction_data = {
        'stock': stock_symbol,
        'prediction': final_prediction,
        'last_day': last_day,
        'pct_change': pct_change,
        "definitive": True

    }
    
    # Assuming you're using Supabase to insert data
    # Replace 'predictions' with your actual table name
    # Also, replace 'supabase' with your actual Supabase client object
    data = supabase.table('predictions').insert(prediction_data).execute()

    return data.data[0]


def update_database(prediction_id, final_prediction, last_day, pct_change, stock):
    """
    Function to update prediction data in the database.
    """
    current_time = datetime.now()

    # Assuming 'predictions' is the table name in your database
    updated_prediction_data = {
        'id': prediction_id,
        'prediction': final_prediction,
        'last_day': last_day,
        'pct_change': pct_change,
        "stock": stock,
        "updated_at":str(current_time),
        "definitive": True

    }
    
    # Assuming you're using Supabase to update data
    # Replace 'predictions' with your actual table name
    # Also, replace 'supabase' with your actual Supabase client object
    data = supabase.table('predictions').upsert(updated_prediction_data).execute()

    return data.data[0]


   


def get_final_prediction(stock):
    """
    Function to get the final prediction for a given stock.
    """
    data, min_max_scaler, last_day = getLastMonthData(stock)
    print("check_last_row(last_day)")
    print(check_last_row(last_day))
    
    
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
    return final_prediction, last_day, pct_change
