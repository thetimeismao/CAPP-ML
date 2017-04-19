# 3. Pre-Process Data: For this assignment, you can limit this to filling in 
# missing values for the variables that have missing values. You can use any 
# simple method to do it (use mean to fill in missing values).

import pandas as pd

def fill_miss(df, col, fill_val_method = 'mean'):
    '''
    Fill in missing values for a given column in a dataframe
    
    Given a dataframe, specific column, and fill value method, 
    return the same dataframe without missing values.
    '''
  
    if fill_val_method == 'mean':
        df[col] = df[col].fillna(df[col].mean())
    elif fill_val_method == 'median':
        df[col] = df[col].fillna(df[col].median())
    elif fill_val_method == 'drop':
        df[col] = df[col].fillna(0)
    elif fill_val_method == "ffill":
        df[col] = df[col].fillna(method=fill_val_method)
    else: 
        raise ValueError('{fv} not currently valid'.format(fv=fill_val_method))
   
    return df