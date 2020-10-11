#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 13:06:37 2020

@author: NickBrown
"""

# Assignment 1
# Question 1 (Exercise 1-2)
# import math just in case
import math
a = 60*42 + 42
b = 10*(1/1.61)
c = [int((a//b)//60), int((a/b)%60), (b*60)/42.7]

# Question 2 (Exercise 2-2)
d = (4/3)*math.pi*5**3
e = ((.6)*24.95)*60 + (3 + 59*(.75))
f = [7,30]

# Question 3
import numpy as np
g = np.arange(1,101,1)**2

# Question 4
n = np.arange(1,21,1)
h = np.array(n*(n+1)/2, dtype=int)
# Will see if this works, may have to go back to the drawing board

# Question 5
i = h%3==0

# Question 6
# j = h[i==True] # doesn't work even though k is correct, think I read the question wrong
n = np.arange(0,20,1)
j = n[i==True]

# Question 7
o = h[i==True]
k = o[::-1]
