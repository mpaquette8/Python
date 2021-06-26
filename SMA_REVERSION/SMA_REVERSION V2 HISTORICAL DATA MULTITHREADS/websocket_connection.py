# -*- coding: utf-8 -*-
"""
Created on Thu May  7 21:07:21 2020

@author: mpaquette
"""

import json
from websocket import create_connection
import threading

class ws_connector(object):

    def __init__(self,ws_name,ws_pair):
        
        self.ws_name = ws_name
        self.ws_pair = ws_pair
        self.data = {}
        self.data[ws_name] = {}
        self.data["raw"] = {}
        
        if ws_name == 'ws_cc':ws_connector.StartWS_cryptocompare(self)
        elif ws_name == 'ws_kraken':ws_connector.StartWS_kraken(self)
        
        threading.Thread(name='websocket_' + self.ws_pair, target=self.LiveStream).start()

    def StartWS_kraken(self):
        
        ws = create_connection('wss://ws.kraken.com/') #,enable_multithread=True
        subscription = '{"event":"subscribe", "subscription":{"name":"ohlc"}, "pair":%(symbol)s}' % {
            "symbol":[self.ws_pair]}
        subscription = subscription.replace("'","\"")
        self.data['ws_kraken']['ohlc'] = ws
        self.data['ws_kraken']['ohlc'].send(subscription)
    
    def StartWS_cryptocompare(self):
            
        api_key = "7f63b7f13e658bdd5755058e3279d79653854fa73d24ee763587d84066f26a7a"
        url = "wss://streamer.cryptocompare.com/v2?api_key=" + api_key
        ws = create_connection(url)
        subscription = json.dumps({
                "action": "SubAdd",
                "subs": ["24~Kraken~ETH~EUR~m"],
            })
        self.data['ws_cc']['ohlc'] = ws
        self.data['ws_cc']['ohlc'].send(subscription)
    
    def ReceiveRaw(self):
        while True:
            raw = self.data[self.ws_name]['ohlc'].recv()
            
            try:
                raw = json.loads(raw)
            except ValueError:
                print('Personal comment: Decoding JSON has failed')
                raw = ''

            self.data['raw']['ohlc'] = raw
            
    def LiveStream(self):
        while True:
            self.ReceiveRaw()
            #self.Threads()