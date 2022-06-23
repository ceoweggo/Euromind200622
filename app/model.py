from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import os
import json
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
# process the data 
def ProcessData(path):
    f = open(path, 'r').read()
    data = json.loads(f)
    f.close()
    df = pd.DataFrame(columns=['data', 'low', 'high', 'close', 'open'])
    for k,v in data.items():
        date = dt.datatime.strptime(k, '%Y-%m-%d')
        data_row = [date.date(), float(v['3. low']),float(v['2. high']),
                            float(v['4. close']),float(v['1. open'])]
        df.loc[-1,:] = data_row
        df.index = df.index + 1
    print('Data saved to : ',path)
    df.to_json(path)
    df = df.sort_values('Date')
    df.head()

