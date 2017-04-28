# 2. Explore Data: You can use the code you wrote for assignment 1 here to generate 
# distributions and data summaries.

def explore(df, col, ignore=[]):
    '''
    Generate summary statisitcs and list of features(exclude dependent var)
    for the whole dataset
    
    Given a dataframe and column, return a short summary describing the column
    '''
    print("-"*40)
    print('Describe Column: {}'.format(col))
    print(df[col].describe())
    print('Unique values: {}'.format(len(df[col].value_counts())))
