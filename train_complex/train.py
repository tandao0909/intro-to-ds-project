from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class LogTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        X["Log Bedrooms"] = np.log(X["Bedrooms"])
        X["Log WC"] = np.log(X["WC"])
        X["Log Floors"] = np.log(X["Number of floors"])
        X = X.drop(columns=["Bedrooms", "WC", "Number of floors", "Latitude", "Longitude", 'Log usable area (square meters)'])
        return X

class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop) -> None:
        self.columns_to_drop = columns_to_drop

    def fit(self, X, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        return X.drop(columns=self.columns_to_drop)
