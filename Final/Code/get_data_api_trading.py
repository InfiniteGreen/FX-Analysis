import requests
import pandas as pd
from pandas.io.json import json_normalize
import json
import os
import datetime
from datetime import date


fx_list = ["AUD_USD","EUR_USD","GBP_USD","NZD_USD","USD_CAD","USD_CHF","USD_JPY"]

for fx in fx_list:
    url = f"https://api-fxtrade.oanda.com/v1/candles?instrument={fx}&candleFormat=midpoint&granularity=D&start=1999-12-31&end=2005-01-01"
    response = requests.get(url)

    # Printing the text from the responses
    results= json.loads(response.text)    

    # setup dictionary to later convert to a df
    fx_dict = {'FX':[],
                'Time':[],
                'Open':[],
                'High':[],
                'Low':[],
                'Close':[], 
                'Volume':[]}

    # start loop to exctract values from the json calls and append to dictionary
    for r in range(len(results['candles'])):
            fx_dict['FX'].append(fx)
            fx_dict['Time'].append(results['candles'][r]['time'])
            fx_dict['Open'].append(results['candles'][r]['openMid'])
            fx_dict['High'].append(results['candles'][r]['highMid'])
            fx_dict['Low'].append(results['candles'][r]['lowMid'])
            fx_dict['Close'].append(results['candles'][r]['closeMid'])
            fx_dict['Volume'].append(results['candles'][r]['volume'])

    # Turn the dictionary in to a data frame
    fx_df = pd.DataFrame(fx_dict)

    # Convert Time column to DateTime data type, then to Date
    fx_df['Time'] = pd.to_datetime(fx_df['Time'])
    fx_df['Time'] = fx_df['Time'].dt.date
    
    # Write to csv
    td = datetime.date.today()
    fx_df.to_csv(f"{fx}-{td}.csv",index=False)
