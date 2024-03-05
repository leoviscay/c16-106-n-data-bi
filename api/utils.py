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