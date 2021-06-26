# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 18:42:23 2021

@author: mpaquette
"""

import pandas as pd
import json
from datetime import datetime

sma = 120

with open('XXBTZEUR dataframe.txt') as f:
    json_data = json.load(f)

df = pd.DataFrame(json_data)

# df['TS'] = df['TS'] / 1000 + (-2*60*60)

# df['TS'] = [datetime.fromtimestamp(x) for x in df['TS']]
# df.set_index('TS',inplace=True)

# import matplotlib.pyplot as plt
# plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

# #plt.hist(df_marketdata['Delta_SMA_{}'.format(str(sma))], bins=50)
# #plt.hist(df['Gamma_SMA_{}'.format(str(sma))], bins=50)
# plt.hist(df['spread_SMA_{}_close'.format(str(sma))], bins=50)
# plt.gca().set(title='distribution Histogram', ylabel='distribution');

# data_desc = df.describe(include='all',datetime_is_numeric=True)



