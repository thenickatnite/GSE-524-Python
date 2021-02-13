#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 21:22:37 2020

@author: NickBrown
"""

# Assignment 3: Colley
import pandas as pd
import numpy as np
x = pd.read_pickle("ncaa.pkl")

#creating a function that generates the Colley Rank, primarily used with College Football teams. This was heavily used before the College football playoff
def colley_rank(x):
    A = np.zeros((len(x), len(x)))
    B = np.zeros((len(x)))
    for i in range(len(x.team)):
        A[i,i] = 2 + (x.wins[i] + x.losses[i])
        B[i] = 1 + (x.wins[i] - x.losses[i])/2
        for j in x.opponents[i]:
            A[i,j] = A[i,j] - 1
    colley_score = np.matmul(np.linalg.inv(A), B)
    C = pd.DataFrame({"team": x.team, "score": colley_score})
    C = C.sort_values(by='score', ascending= False)
    return [C,A,B]

colley_rank(x)


