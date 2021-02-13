#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:01:05 2020

@author: NickBrown
"""

import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from scipy.stats import chi2
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import GroupKFold
from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

b = pd.read_csv("boston.csv")
y = b.MEDV
X = b.iloc[:, np.arange(0,13)]

Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.75,random_state=0)

# Practice using Machine Learning methods in Python, using the sklearn library

# 1 Linear Regression
model1=LinearRegression()
model1.fit(Xtrain,ytrain)
ytest_pred=model1.predict(Xtest)
mse1=mean_squared_error(ytest,ytest_pred)

# 2 Linear Regression with quadratic terms and interactions
y = b.MEDV
X= pd.DataFrame(PolynomialFeatures(degree = 2).fit_transform(X))
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.75,random_state=0)
model2=LinearRegression(fit_intercept= False)
model2.fit(Xtrain,ytrain)
ytest_pred=model2.predict(Xtest)
mse2=mean_squared_error(ytest,ytest_pred)

# 3 Ridge Regression
ridge = RidgeCV(alphas=np.linspace(0.001,1,1000),normalize=True,cv = KFold(10,shuffle=True,random_state=0))
ridge.fit(Xtrain, ytrain)
ridge.alpha_

ridge_model=Ridge(alpha=ridge.alpha_,normalize=True)
ridge_model.fit(Xtrain,ytrain)
ytest_pred = ridge_model.predict(Xtest)
mse3 = mean_squared_error(ytest, ytest_pred)


# 4 Bagging regression
LR = LinearRegression(fit_intercept= False)
bag = BaggingRegressor(LR, n_estimators=100, random_state=0)
bag.fit(Xtrain, ytrain)
pred = bag.predict(Xtest)
mse4 = mean_squared_error(ytest, pred)

# 5 Decision Tree
y = b.MEDV
X = b.iloc[:, np.arange(0,13)]
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.75,random_state=0)

model5 = DecisionTreeRegressor(criterion = "mse", random_state = 0)
model5.fit(Xtrain, ytrain)
pred = model5.predict(Xtest)
mse5 = mean_squared_error(ytest, pred)

# 6 Decision Tree with Limits on Tree Size
grid = {"max_depth": np.arange(3,7), "min_samples_leaf": np.array([2,5,10,15,20])}
grid_tree = GridSearchCV(model5, grid, cv = KFold(10,shuffle=True,random_state=0))
grid_tree.best_params_
grid_tree.fit(Xtrain, ytrain)
model6 = DecisionTreeRegressor(criterion = "mse", max_depth = 6, min_samples_leaf=15, random_state=0)
model6.fit(Xtrain, ytrain)
pred = model6.predict(Xtest)
mse6 = mean_squared_error(ytest, pred)

# 7 Decision Tree with Cost Complexity Pruning
model5.fit(Xtrain, ytrain)
path = model5.cost_complexity_pruning_path(Xtrain, ytrain)
ccp_alphas, impurities = path.ccp_alphas, path.impurities

mse = []
for ccp_alpha in ccp_alphas:
    scores=cross_val_score(DecisionTreeRegressor(random_state=0,ccp_alpha=ccp_alpha),Xtrain,ytrain,cv=KFold(10,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
    mse.append(np.mean(scores))
alpha=ccp_alphas[np.argmax(mse)]

model7 = DecisionTreeRegressor(criterion = "mse", ccp_alpha= alpha, random_state= 0)
model7.fit(Xtrain, ytrain)
pred = model7.predict(Xtest)
mse7 = mean_squared_error(ytest, pred)

# 8 Random Forest 
rf = RandomForestRegressor(random_state=0)
rf.fit(Xtrain, ytrain)
pred = rf.predict(Xtest)
mse8 = mean_squared_error(ytest, pred)
