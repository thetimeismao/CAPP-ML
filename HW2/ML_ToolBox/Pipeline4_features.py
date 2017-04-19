# 4. Generate Features/Predictors: For this assignment, you should 
# write one function that can discretize a continuous variable and 
# one function that can take a categorical variable and create binary/dummy 
# variables from it. Apply them to at least one variable each in this data.
    
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import pylab as pl

def display_importance(df, label, features):
    '''
    Given dataframe, label, and list of features,
    plot a graph to rank variable importance
    '''
    clf = RandomForestClassifier()
    clf.fit(df[features], df[label])
    importances = clf.feature_importances_
    sorted_idx = np.argsort(importances)
    padding = np.arange(len(features)) + 0.5
    pl.xlabel("Relative Importance")
    pl.title("Variable Importance")
    pl.barh(padding, importances[sorted_idx], align='center')
    pl.yticks(padding, features[sorted_idx])
    
def discretize(df, col, n, cut='quantile'):
    '''
    Discretizes certain given column into equal n count of bins.
    
    Given dataframe, specific column to be discretized and n categories to create,
    updates dataframe accordingly    
    '''
    if cut == 'quantile':
        df[col + '_bucket'] = pd.cut(df[col], n)
    else:
        raise ValueError('cut format not currently available')


def gen_dummies(df, col):
    '''
    Given a dataframe and certain column, returns a set of dummies
    '''
    return pd.get_dummies(df[col], prefix = [col])
