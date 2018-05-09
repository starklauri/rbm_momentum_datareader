#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 20:23:54 2018

@author: juhahellen
"""

import pandas
import numpy
from   scipy import stats
from   copy import deepcopy


def delta(data,N,sigma):
    
    T     = N/250.0
    print(T)
    

    ratio = data.div(data.shift(N))
    
    s     = 2*stats.norm.cdf((np.log(ratio)+0.5*sigma**2*T)/(sigma*np.sqrt(T)))-1
    
    df    = pd.DataFrame(data = s, index = data.index, columns = data.columns)
    
    return df
    
used_data = pd.read_csv('../data.csv')

frames = []
for symbol in used_data:
    
  
    S      = np.exp(used_data.fillna(0)).cumprod()
    
    ret    = used_data[symbol].fillna(0).to_frame()
    signal = delta(S[symbol].to_frame(),180,1)
    
    signal = (signal.div(signal.ewm(150).std())).clip(0,5)
    
    lev    = (0.05/(ret.ewm(60).std()*np.sqrt(250))).clip(0,5)
    
    r      = ret.mul(signal.shift(1)).mul(lev.shift(1))
    
    frames.append(deepcopy(r))


m = pd.concat(frames,axis=1)


m.cumsum().plot(figsize=(10,7.5))
plt.show()

m.mean(axis=1).cumsum().plot(figsize=(10,7.5),color='blue')
plt.show()