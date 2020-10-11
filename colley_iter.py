#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:52:10 2020

@author: NickBrown
"""

import pandas as pd
import numpy as np
x = pd.read_pickle("ncaa.pkl")

def colley_iter(x, t):
    n = 0
    r = np.array((1+x.wins)/(2+(x.wins+x.losses)))
    x['r'] = r
    p = np.copy(r)
    sum_opponents = np.zeros(len(x))
    while np.amax(p) >= t:
        n = n+1
        m = np.copy(x.r)
        for i in range(len(x.team)): # issue is likely in the sum of opponents r 
            sum_opponents[i] = np.sum(x.r[x.opponents[i]])
        effwins = ((x.wins-x.losses)/2) + sum_opponents
        x.r = (1+effwins)/(2+(x.wins+x.losses))
        p = np.abs(x.r-m)
    colley_score = x.r
    C = pd.DataFrame({"team": x.team, "score": colley_score})
    C = C.sort_values(by='score', ascending= False)
    return [C,n]
           
colley_iter(x, 0.0001) 

# issue with speed when t is very small.
