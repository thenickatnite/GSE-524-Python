#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 09:32:11 2020

@author: NickBrown
"""

# Assignment 2
# import needed modules 
import numpy as np
import pandas as pd
# Import the data set
fulldata = pd.read_csv('london_crime.csv')

# Part 1 - Log log model
# Create a column called 'crimerate', consisting of total number of crimes
# per borough divided by population of the borough
fulldata["crimerate"] = fulldata.crime / fulldata.population

# create 'policerate' variable
fulldata["policerate"] = fulldata.police / fulldata.population

# create log variables
fulldata["lcrime"] = np.log(fulldata.crimerate)
fulldata["lpolice"] = np.log(fulldata.policerate)
fulldata["lemp"] = np.log(fulldata.emp)
fulldata["lun"] = np.log(fulldata.un)
fulldata["lymale"] = np.log(fulldata.ymale)
fulldata["lwhite"] = np.log(fulldata.white)


# import stats module
import statsmodels.formula.api as smf
# run regression with lcrime as the dependent variable and get summary
model1 = smf.ols("lcrime ~ lpolice + lemp + lun + lymale + lwhite", data = fulldata).fit()
model1.summary()

# Part 2 Differences model
# Create differences variables in differences data set named 'diffdata'
x = fulldata.week > 52
n = np.arange(0,3328,1)
j = n[x == True]

# could be a potential issue due to index. Will see.
dlcrime = np.array(fulldata.lcrime[j]) - np.array(fulldata.lcrime[j-52])
dlpolice = np.array(fulldata.lpolice[j]) - np.array(fulldata.lpolice[j-52])
dlun = np.array(fulldata.lun[j]) - np.array(fulldata.lun[j-52])
dlemp = np.array(fulldata.lemp[j]) - np.array(fulldata.lemp[j-52])
dlymale = np.array(fulldata.lymale[j]) - np.array(fulldata.lymale[j-52])
dlwhite = np.array(fulldata.lwhite[j]) - np.array(fulldata.lwhite[j-52])
diffdata = pd.DataFrame({"dlcrime": dlcrime, "dlpolice": dlpolice, "dlun": dlun,
                        "dlemp": dlemp, "dlymale": dlymale, "dlwhite": dlwhite })

model2 = smf.ols("dlcrime ~ dlpolice + dlemp + dlun + dlymale + dlwhite", data = diffdata).fit()
model2.summary()


# Part 3 Natural Experiment model
diffdata["weeks"] = np.array(fulldata.week[j])
diffdata["borough"] = np.array(fulldata.borough[j])


# Set up bool for weeks 80-85, change type to int so it's in 1s and zeros
# instead of being in True or False
diffdata["sixweeks"] = np.array((diffdata.weeks >= 80) & (diffdata.weeks < 86), dtype = int)

# Take a similar approach for the treatment, using the "or" instead of the 
# "and" vectorized operation for bool
diffdata["sixweeks_treat"] = np.array((diffdata.sixweeks == 1) &
                                     ((diffdata.borough == 1) | 
                                     (diffdata.borough == 2) |
                                     (diffdata.borough == 3) |
                                     (diffdata.borough == 6) |
                                     (diffdata.borough == 14)), dtype = int)

diffdata=diffdata.drop("weeks",1)
diffdata=diffdata.drop("borough",1)


model3 = smf.ols("dlcrime ~ sixweeks + sixweeks_treat + dlemp + dlun + dlymale + dlwhite", data = diffdata).fit()
model3.summary()
