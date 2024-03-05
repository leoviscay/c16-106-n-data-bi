from datetime import datetime
import pandas as pd
from supabase import Client, create_client
import os
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')


def create_supabase_client():
    supabase: Client = create_client(api_url, key)
    return supabase

def calculate_pct_change(predictions, last_day):
    last_day = float(last_day)
    predictions  = float(predictions)
    pct_change = ((predictions - last_day) / last_day) * 100
    return pct_change

def check_and_convert_prediction(predictions):
            if predictions:
                prediction_str = str(predictions[0])
                return prediction_str
            else:
                return "No prediction"
            

def check_last_row(last_row):
    today = pd.Timestamp.now().normalize().date()
    print(last_row.name.date())
    return last_row.name.date() == today