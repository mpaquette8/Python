# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 23:50:05 2021

@author: mpaquette
"""

from run_pair import run_pair
import time

#global parameters
coef_std_spread = 2
sma = 120
timesleep = 5

#threads activation
bitcoin = True
ethereum = True
ripple = False
dogecoin = False

#BITCOIN
if bitcoin == True:
    invest = 0.0155 #min: 0.0001 ; 0.0155 (500€)
    pair = 'XXBTZEUR'
    ws_pair = 'XBT/EUR'
    cle_api_kraken = '+ekkeLKC7q7krZFPStFmLq2Eyy1ARnXJtBozMe03suQ+Vd7bjCD7006N'
    cle_privee_kraken = 'EmK/sI614xWzDYRT9mo4QdXzIvI7i2QLtXL47IFzm8Y1/kqaDETFBwKl1i66nRPIyQSPbU3xLrmkeYclDRF6+A=='
    underlying = 'BTC'
    run_pair(invest,coef_std_spread,sma,pair,ws_pair,cle_api_kraken,cle_privee_kraken,underlying)
    time.sleep(timesleep)

#ETHEREUM
if ethereum == True:
    invest = 0.3 #min: 0.004 ; 0.25 (500€)
    pair = 'XETHZEUR'
    ws_pair = 'ETH/EUR'
    cle_api_kraken = 'PvtGgpQzxpVdIxNFVGHShdUeLR2nznzFb5b5HVIES6rh/l0moTu3FqCG'
    cle_privee_kraken = 'NaCs1DTr01U33q0vUeU7c9h2q637Qxi47bqn4iw5L6Payydxzqn3mEmhLd4h4i35sZV3HzyuJLsegsN4Wu+BKA=='
    underlying = 'ETH'
    run_pair(invest,coef_std_spread,sma,pair,ws_pair,cle_api_kraken,cle_privee_kraken,underlying)
    time.sleep(timesleep)

#XRP
if ripple == True:
    invest = 350 #min: 5 ; 730 (500€)
    pair = 'XXRPZEUR'
    ws_pair = 'XRP/EUR'
    cle_api_kraken = 'VRiKYZMr8h2lOQmNVf1x+FP3A6V6Gc1AoiDO7Z/bV1BIYXOyak+HTB1z'
    cle_privee_kraken = 'LbKewqc8wDPnjuT2YBwtWFrvtqYtOk2ypifGbFzkzJiqIvrD+xxG4B2zumqLuRQYP/BHUrd+KAyb5KAD8l/PlA=='
    underlying = 'XRP'
    run_pair(invest,coef_std_spread,sma,pair,ws_pair,cle_api_kraken,cle_privee_kraken,underlying)
    time.sleep(timesleep)
    
#DOGECOIN
if dogecoin == True:
    invest = 1000 #min: 50 ; 2000 (500€)
    pair = 'XDGEUR'
    ws_pair = 'DOGE/EUR'
    cle_api_kraken = 'u1UBmcNHwEX0QjrYuGwynDJL4eCKVfIAkiS/qzo7S89UhqxP1F7Ymlpl'
    cle_privee_kraken = 'wTEE7dhKqYpEn+qge0Xva9uVibB6X1Lc/YL6XOn22icCNbDWca4DRBuaAnf9fpxy3WtquwjxsKrVBv7kE9KDJg=='
    underlying = 'DOGE'
    run_pair(invest,coef_std_spread,sma,pair,ws_pair,cle_api_kraken,cle_privee_kraken,underlying)
    time.sleep(timesleep)