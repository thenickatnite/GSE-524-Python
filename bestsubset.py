#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 15:35:23 2020

@author: NickBrown
"""

import itertools
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
import pandas as pd


def bestsubset(X,y): 
    mse=np.empty(0)
    size = np.empty(0)
    cs=[]
    for k in range(X.shape[1]):
        for c in itertools.combinations(range(X.shape[1]),k+1):
            Xc=X.iloc[:,list(c)]
            model1=LinearRegression()
            model1.fit(Xc,y)
            y_pred=model1.predict(Xc)
            mse1=mean_squared_error(y,y_pred)
            mse=np.append(mse,mse1)
            size = np.append(size, Xc.shape[1])
            cs.append(c)
        
    train = pd.DataFrame({'mse': mse, 'size': size, 'cs': cs})
    train = train.sort_values(by =['mse'])
    by_variable = train.groupby("size").agg({"mse": "min", 'cs': "first"}).reset_index()
    d = []
    mse2 = np.empty(0)
    for i in range(len(by_variable)):
        Xc = X.iloc[:, list(by_variable.cs[i])]
        scores=cross_val_score(LinearRegression(),Xc,y,cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
        mse2=np.append(mse2,np.mean(scores))
        d.append(by_variable.cs[i])
    i=np.argmax(mse2)
    Xc=X.iloc[:,list(d[i])]
    model=LinearRegression()
    model.fit(Xc,y)
    model.coef_
    ret = [list(d[i]),model.coef_]
    return ret


#Auto = pd.read_csv('Auto.csv')
#y=Auto.mpg
#X=Auto[["horsepower","cylinders","displacement","weight","acceleration"]] 
#bestsubset(X, y)

def forwardsubset(X,y):
    # used the set type here, could have probably just as easily used a list
    # the get_loc function returns the index position for each column, other this would return their string names
    remaining = set([X.columns.get_loc(c) for c in X.columns])
    # empty, will fill as we go through the loop and fins the lowest MSE
    selected = []
    mse = np.empty(0)
    cs = []
    # using tuples, similar method we briefly used in class
    current_score, new_score = float('inf'), float('inf')
    while remaining:
        # putting this here in the loop cleans out the MSEs and variables for each iteration
        scores_w_c = []
        for variable in remaining:
            Xc = X.iloc[:, list(selected) + [variable]]
            Xc = pd.DataFrame(Xc)
            model1=LinearRegression()
            model1.fit(Xc,y)
            y_pred=model1.predict(Xc)
            mse1=mean_squared_error(y,y_pred)
            scores_w_c.append((mse1, variable))
        # using sort will put the smallest MSE first. Can then use the [0] to return it, obviously wouldn't work if your were using some other method
        scores_w_c.sort()
        new_score, new_candidate = scores_w_c[0]
        # recording the best variable combo and score before the next loop.
        if new_score < current_score:
            remaining.remove(new_candidate)
            selected.append(new_candidate)
            mse = np.append(mse, new_score)
            cs.append(selected.copy())
            current_score = new_score
    
    train = pd.DataFrame({"mse": mse, "cs": cs})
    train = train.sort_values(by =['mse'])
    d = []
    mse2 = np.empty(0)
    for i in range(len(train)):
        Xc = X.iloc[:, list(train.cs[i])]
        scores=cross_val_score(LinearRegression(),Xc,y,cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
        mse2=np.append(mse2,np.mean(scores))
        d.append(train.cs[i])
    i=np.argmax(mse2)
    Xc=X.iloc[:,list(d[i])]
    model=LinearRegression()
    model.fit(Xc,y)
    model.coef_
    ret = [list(d[i]),model.coef_]
    return ret
  
#Auto = pd.read_csv('Auto.csv')
#y=Auto.mpg
#X=Auto[["horsepower","cylinders","displacement","weight","acceleration"]] 
#bestsubset(X,y)
#forwardsubset(X,y)


#crime = pd.read_csv('london_crime.csv')
#y = crime.crime
#X = crime[["population", "police", "emp", "un", "ymale", "white"]]
#%timeit oldbestsubset(X,y)
#%timeit bestsubset(X, y)
#%timeit forwardsubset(X, y)
