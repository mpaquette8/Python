# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 10:30:26 2021

@author: mpaquette
"""

import krakenex

class kraken_executor(object):

    def __init__(self,pair,direction,order_type,volume,cle_api,cle_privee):
        
        self.cle_api = cle_api
        self.cle_privee = cle_privee
        kraken_executor.init_kraken_spot_api(self)
        kraken_executor.create_order(self,pair,direction,order_type,volume)
        
    def create_order(self,pair,direction,order_type,volume):
        
        if order_type == 'market':
            order = self.kraken_spot_api.query_private('AddOrder',
                                {'pair': pair,
                                'type': direction,
                                'ordertype': order_type,
                                'volume': volume})     
        if order['error'] != []:
            result = order['error'][0]
        else:
            result = order['result']['txid'][0]
        print(result)
        
        return result
    
    
    def init_kraken_spot_api(self):        #api-ta-strat

        self.kraken_spot_api = krakenex.API(self.cle_api,self.cle_privee)

class sma_reversing(object):
    
    def __init__(self,pair,last_data,invest,sma,standard_dev_spread,coef_std_spread,print_mode,mode_buy,buy_status,in_price,cle_api,cle_privee):
        
        import pandas as pd
        from executor import kraken_executor
        from mail_sender import mail_sender
        
        self.mode_sell = False
        self.invest_by_udl = invest

        results_details = {}
        results_details[pair] = {}
    
        df = last_data.copy()
        df.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close','volumefrom':'Volume'},inplace=True)
        
        print (df)
        
        df2 = {}
        df2['G_D_Below'] = []
        df2['close'] = []
        df2['date'] = []
        df2['spread_SMA_{}_close'.format(str(sma))] = []
        df2['Gamma_SMA_{}'.format(str(sma))] = []
        
        for data in df['G_D_Below']:
            df2['G_D_Below'].append(data)
        
        for data in df['spread_SMA_{}_close'.format(str(sma))]:
            df2['spread_SMA_{}_close'.format(str(sma))].append(data)
            
        for data in df['Gamma_SMA_{}'.format(str(sma))]:
            df2['Gamma_SMA_{}'.format(str(sma))].append(data)
    
        for data in df['Close']:
            df2['close'].append(data)
        
        for index in df.index:
            df2['date'].append(index)
            
        df2 = pd.DataFrame(df2)
        
        print('STD_SPREAD: ' + str(standard_dev_spread))
        
        self.buy = buy_status
        self.sell = False
        self.in_price = in_price
        self.in_out_return = 0
        
        for row in df2.iterrows():
            
            self.buy_signal = False
            self.sell_signal = False
            
            if self.buy == True:
                self.in_out_return = (row[1]['close'] / self.in_price) -1
            
            if row[1]['G_D_Below'] == 'Signal' and row[1]['spread_SMA_{}_close'.format(str(sma))] <= -(standard_dev_spread*coef_std_spread) : #-2*std
                self.buy_signal = True
                print('buy_signal = True')
            
            #CONDITIONS DE VENTE
            elif (row[1]['spread_SMA_{}_close'.format(str(sma))] >= 0) or (row[1]['spread_SMA_{}_close'.format(str(sma))] >= -(standard_dev_spread)) or self.in_out_return >= 0.006:
                self.sell_signal = True
            
            if self.buy_signal == True and mode_buy == True and self.buy == False:
                self.buy = True
                self.in_price = row[1]['close']
                self.in_date = row[1]['date']
                kraken_executor(pair,'buy','market',invest,cle_api,cle_privee)
                
                #mail
                msgbody = "Buy " + pair + " @ " + str(self.in_price) + " / " + str(self.in_date)
                mail_sender("Admin","maxime.fm.paquette@gmail.com;thomasbs17@yahoo.fr",msgbody,"[ALGO] SMA_REVERSION")
                
                
            elif self.buy == True and self.sell_signal == True:
                
                self.out_price = row[1]['close']
                self.out_date = row[1]['date']
                
                kraken_executor(pair,'sell','market',invest,cle_api,cle_privee)
            
                #mail
                msgbody = "Sell " + pair + " @ " + str(self.out_price) + " / " + str(self.out_date) + " / Return: " + str(self.in_out_return)
                mail_sender("Admin","maxime.fm.paquette@gmail.com;thomasbs17@yahoo.fr",msgbody,"[ALGO] SMA_REVERSION")    
            
                print('sell_signal = True')
                
                self.buy = False
            
            elif self.buy_signal == False and self.sell_signal == False:
                print('Buy and Sell signal are false')
        
        self.df = df
        self.dataset = df2