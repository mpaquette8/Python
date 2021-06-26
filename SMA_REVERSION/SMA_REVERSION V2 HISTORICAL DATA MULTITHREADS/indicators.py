
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 17:16:43 2020
@author: mpaquette
"""

def indicators(df,indicators):
    
    import numpy as np
    
    #other indicator dict creation
    df_other = {}
    
    df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','volumefrom':'Volume'},inplace=True)
    
    df['log_returns'] = np.log(df['close']/df['close'].shift(1))
                
    #simple moving averages (SMA)
    name = 'SMA'
    for window in indicators[name]:
        df[name+'_'+str(window)] = df['close'].rolling(window=window).mean()
        #spread %
        df['spread_'+name+'_'+str(window)+'_close'] = df['close'] - df[name+'_'+str(window)]
        df['spread_'+name+'_'+str(window)+'_close'+'_diff'] = df['spread_'+name+'_'+str(window)+'_close'] - df['spread_'+name+'_'+str(window)+'_close'].shift(1)
        
        df.loc[df['spread_'+name+'_'+str(window)+'_close'] >= 0, 'Close Price Position'] = 'Above' 
        df.loc[df['spread_'+name+'_'+str(window)+'_close'] < 0, 'Close Price Position'] = 'Below'
        
        #standard deviation
        df_other['std_spread'] = np.std(df['spread_'+name+'_'+str(window)+'_close'])
    
    
    #exponential moving averages (EMA)
    name = 'EMA'
    for window in indicators[name]:
        df[name+'_'+str(window)] = df['close'].ewm(span=window,min_periods=window).mean()
        #spread %
        df['spread_'+name+'_'+str(window)+'_close'] = df['close'] - df[name+'_'+str(window)]
    
    #cumulative moving averages (CMA)
    min_periods = indicators['CMA']['min_periods']
    df['CMA_'+str(min_periods)] = df['close'].expanding(min_periods=min_periods).mean()

    #Delta
    name = 'Delta_SMA'
    rolling = 3
    for window in indicators['SMA']:
        df[name+'_'+str(window)] = df['SMA'+'_'+str(window)] - df['SMA'+'_'+str(window)].shift(1)
        df[name+'_'+str(window)+'_rolling_'+str(rolling)] = df[name+'_'+str(window)].rolling(window=rolling).mean()
    
    #Gamma
    name = 'Gamma_SMA'
    for window in indicators['SMA']:
        df[name+'_'+str(window)] = df['Delta_SMA'+'_'+str(window)] - df['Delta_SMA'+'_'+str(window)].shift(1)
    
    #Gamma- Delta- et Below
    df['G_D_Below'] = 'No_signal'
    for window in indicators['SMA']:
        df.loc[(df['Gamma_SMA'+'_'+str(window)] < 0) & (df['Delta_SMA'+'_'+str(window)] < 0) & (df['Close Price Position'] == 'Below'), 'G_D_Below'] = 'Signal'
    
    df['TS'] = df.index
    
    #RSI
    mean_up_returns = df['log_returns'].agg(lambda x: x[x>0].mean())
    mean_down_returns = df['log_returns'].agg(lambda x: x[x<0].mean())
    rs = abs(mean_up_returns) / abs(mean_down_returns) #relative strength
    rsi = 100-100/(1+rs)
    df_other['rsi'] = rsi
    
    data = {}
    data['df'] = df.copy()
    data['df_others'] = df_other.copy()
    
    return data