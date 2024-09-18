import pandas as pd
import numpy as np



def preprocessor(df,region_df):

    # filltering of summer olymics
    df = df[df['Season']== 'Summer']

    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')

    # droping duplicates
    df.drop_duplicates(inplace = True)

    # one hot encoding model
    # pd.get_dummies(df['Medal']).astype(int)
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df





