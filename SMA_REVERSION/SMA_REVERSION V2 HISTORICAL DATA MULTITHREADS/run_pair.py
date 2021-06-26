# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:18:26 2020

@author: mpaquette
"""

from websocket_connection import ws_connector
import time
import pandas as pd
from datetime import datetime
from indicators import indicators
from executor import sma_reversing
import threading

def txt_printer(file_name,data_to_print,append_or_write):

    file1 = open(file_name,append_or_write)
    file1.writelines('\n')
    file1.writelines(data_to_print)
    file1.writelines('\n')
    file1.close()

class run_pair(object):

    def __init__(self,invest,coef_std_spread,sma,pair,ws_pair,cle_api,cle_privee,underlying):

        #initiation de la thread websocket kraken
        ws_thread = ws_connector('ws_kraken',ws_pair)
        self.data_ws = ws_thread.data
        time.sleep(3)
        
        #initiation des variables critiques
        self.df_brut = pd.DataFrame()
        self.index = 0
        self.first_run = True
        self.buy_status = False
        self.in_price = 0
        
        #param utilisateurs
        self.invest = invest
        self.coef_std_spread = coef_std_spread
        self.sma = sma
        self.pair = pair
        self.ws_pair = ws_pair
        self.cle_api = cle_api
        self.cle_privee = cle_privee
        self.underlying = underlying
        
        threading.Thread(name='run_pair_' + self.pair,target=self.run).start()
        
    def run(self):

        while True:
            
            #websocket data
            price_data = self.data_ws['raw']['ohlc']
            
            #condition pour traiter les data seulement si ce n'est pas un heartbeat
            if  type(price_data) == list or self.first_run == True:
                
                if self.first_run == True:
                    
                    from historical_data import screener_v1 #to get cryptocommpare historical data
                    
                    df = screener_v1(self.underlying,{'currency':'EUR','historical_data':{'frequence':'histominute',
                                                                                                          'data_number':2000,
                                                                                                          'exchange':'Kraken',
                                                                                                          'aggregate':'1'}}).market_data
                    
                    
                    #retraitement pour etre similaire aux data websocket df
                    df.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close','time':'TS'},inplace=True)
                    df['TS_end'] = ''
                    df = df.drop(columns=['volumefrom', 'volumeto', 'conversionType','conversionSymbol'])
                    
                    self.index =  len(df.index) #incrementation de l'indeex pour les cumul des datas websocket

                    self.df_brut = df
                    
                    
                elif self.first_run == False:
                
                    #récupération des datas ws en variables pour ensuite créer un dict puis une DF pandas
                    TS_start = int(float(price_data[1][0]))
                    TS_end = int(float(price_data[1][1]))
                    open_price = float(price_data[1][2])
                    high_price = float(price_data[1][3])
                    low_price = float(price_data[1][4])
                    close_price = float(price_data[1][5])
                    
                    dico = {'TS':TS_start,'Open':open_price,'High':high_price,'Low':low_price,'Close':close_price,'TS_end':TS_end} 
                    
                    df2 = pd.DataFrame(dico,index=[self.index])
                    self.index += 1 #incrementation de l'index
                    
                    self.df_brut = self.df_brut.append(df2)

                df = self.df_brut.copy()
                
                #retraitement des timestamps
                df['TS'] = [datetime.fromtimestamp(x) for x in df['TS']]
                df['TS'] = df['TS'].dt.floor('Min') #mettre les dates en minutes sans les secondes
                df = df.drop_duplicates(subset='TS', keep="last", inplace=False) #on garde seulement le close minute (derniere data de la minute)
                df = df.set_index('TS')
                is_empty = df.empty
                
                if is_empty == False: #si df est vide alors on passe
                    
                    #calcul des indicateurs sur l'ensemble de la df
                    indicators_list = {'SMA':[self.sma],'EMA':[10],'CMA':{'min_periods':0},'RSI':''}
                    data = indicators(df,indicators_list)
                    
                    #split des indicateurs fixes (std RSI..) et evolutif (moving average etc)
                    df = data['df']
                    txt_printer(self.pair + " dataframe.txt",str(pd.DataFrame.to_json(df)),"w")
                    
                    df_others = data['df_others']

                    std_spread = df_others['std_spread']

                    last_row_df = df.tail(1) #on va analyser seulement la derniere ligne pour voir si il y a signal ou non
                    print(last_row_df)
                    
                    #run du detecteur de signal
                    signal_calculation_and_execution = sma_reversing(self.pair,last_row_df,self.invest,self.sma,std_spread,self.coef_std_spread,True,True,self.buy_status,self.in_price,self.cle_api,self.cle_privee)
                    self.buy_status = signal_calculation_and_execution.buy
                    self.in_price = signal_calculation_and_execution.in_price
                    
            
            self.first_run = False
        
        
