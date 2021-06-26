# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 22:35:22 2021

@author: mpaquette
"""
class crypto_compare(object):
    
    def __init__(self,underlying,user_parameters):
       
        crypto_compare.get_data(self,underlying,user_parameters)
        crypto_compare.market_data_cleaner(self)

    def get_data(self,underlying,user_parameters): #only cryptos here
        
        #list of crypto to screen
            
        historical_data_frequence = str(user_parameters['historical_data']['frequence'])
        historical_data_number = str(user_parameters['historical_data']['data_number']) #-1 because 0 is the beginning
        exchange = str(user_parameters['historical_data']['exchange'])
        aggregate = str(user_parameters['historical_data']['aggregate'])
        quote = user_parameters['currency']
        
        query_data_brut = {}
        
        #REQUEST
        query_data_brut[underlying] = crypto_compare.ohlc_query(underlying,quote,historical_data_frequence,historical_data_number,exchange,aggregate)
  
        self.query_data_brut = query_data_brut
            
    def ohlc_query(base,quote,frequence,data_number,exchange,aggregate): #OK
        
        import requests
        
        url = 'https://min-api.cryptocompare.com/data/v2/' + str(frequence) + '?fsym=' + str(base) + '&tsym=' + str(quote) + '&limit=' + str(data_number) + '&aggregate=' + str(aggregate) + '&e=' + str(exchange)
        rq = requests.get(url)
        
        return rq.json()
    
    def market_data_cleaner(self):
        
        '''Get price ohlc dictionnary from ohlc_query brut data'''
        
        import pandas as pd
        
        market_data = {}
        
        for underlying in self.query_data_brut:
            
            market_data[underlying] = pd.DataFrame.from_dict(self.query_data_brut[underlying]['Data']['Data'])
        
        self.market_data = market_data
        
class screener_v1(object):
    
    def __init__(self,underlying,user_parameters):
        
        #market data
        crypto_compare_data = crypto_compare(underlying,user_parameters)
        self.market_data = crypto_compare_data.market_data[underlying]


