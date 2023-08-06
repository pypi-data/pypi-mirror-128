import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
class Dataclean():
    """The library has 3 functions:- replacing null values, standardization and finding the variance_inflation_factor value column wise.

       The base minimum parameter which it expects is either a numpy array or a DataFrame.

       The only things we need to keep in mind is make sure there is no column in date format if so once you have preprocessed it then use these functions.
       if any column has values in dataformat then it may give error.
       Also in case of a DataFrame kindly ensure the first column is target column or dependent column. only then start using this function.

    """
    def __init__(self, x):
        self.x=x
    def null(self):

        if type(self.x)==np.ndarray:
            df=self.x.flatten()
            x = df[np.logical_not(np.isnan(df))]
            df= np.nan_to_num(df,copy =True,nan=x.mean())

        elif type(self.x)==pd.core.frame.DataFrame:
            df=self.x
            num_f = [feature for feature in df.columns if df[feature].dtypes != 'O']
            for x in num_f:
                if df[x].isnull().sum() > 0:
                    df[x] = df[x].mean()
   
        return df

    def standardize(self):
        if type(self.x) == np.ndarray:
            df = self.x.flatten()
            scaler = StandardScaler()
            df = scaler.fit_transform(df)
        elif type(self.x)==pd.core.frame.DataFrame:
            df=self.x
            scaler = StandardScaler()
            df1 = pd.DataFrame(scaler.fit_transform(df), columns = df.columns) 
        return df1

#VIF
    def vif(self):
        df=self.x
        vif_df = pd.DataFrame()
        x = df.iloc[:,1:]
        #y = df.iloc[:,0]
        vif_df['vif'] = [variance_inflation_factor(df,i) for i in range(df.shape[1])]
        vif_df['feature']  = x.columns
        return vif_df