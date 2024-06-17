"""Train simple models, including:
linear regression, Ridge regression, Lasso regression, decision tree, random forest"""

from pathlib import Path

from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

FilePath = Path() / "../data/housing.csv"

# TODO: Add train decision tree and random forest functions

def grid_search_cv(model:BaseEstimator, 
                   X:pd.DataFrame, 
                   y:pd.DataFrame, 
                   param_grid: dict, 
                   k_fold_num: int) -> BaseEstimator:
    """Return the best model, given the parameter search dictionary."""
    grid_search = GridSearchCV(model, param_grid, cv=k_fold_num)
    grid_search.fit(X, y)
    return grid_search.best_estimator_

def train_linear_regression(X:pd.DataFrame, y:pd.DataFrame) -> LinearRegression:
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    return lin_reg

def train_ridge_regression(X:pd.DataFrame, y:pd.DataFrame, k_fold_num:int) -> BaseEstimator:
    ridge_reg = Ridge()
    param_grid = {'alpha': [0.001, 0.01, 0.1, 1]}
    return grid_search_cv(ridge_reg, X, y, param_grid, k_fold_num)


def train_lasso_regression(X:pd.DataFrame, y:pd.DataFrame, k_fold_num:int) -> BaseEstimator:
    ridge_reg = Lasso()
    param_grid = {'alpha': [0.001, 0.01, 0.1, 1]}
    return grid_search_cv(ridge_reg, X, y, param_grid, k_fold_num)


def train_models(X:pd.DataFrame, y:pd.DataFrame, k_fold_num:int) -> list[BaseEstimator]:
    """
    Train several simple models, and return all these trained models.
    """
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.25)
    models = []
    models.append(train_linear_regression(X_train, y_train))
    models.append(train_ridge_regression(X_train, y_train, k_fold_num))
    models.append(train_lasso_regression(X_train, y_train, k_fold_num))
    return models

def return_vif(X: pd.DataFrame) -> pd.DataFrame:
    """
    Return a pandas Dataframe, which has two columns: 
    - The first indicates the columns in the passed Dataframe
    - The second indicates the VIF associated with that column, rounded to 5 numbers after decimal
    """
    vif = pd.DataFrame()
    vif["Features"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["VIF"] = vif["VIF"].round(5)
    vif.sort_values(by="VIF", ascending=True)
    return vif

def calculate_r_squared(df:pd.DataFrame, column:pd.Series) -> np.float64:
    """
    Return the R^2 factor of the column in the passed DataFrame.    
    """
    X = df.drop(columns=column)
    y = df[column]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return model.rsquared

def scale_data(df:pd.DataFrame) -> pd.DataFrame:
    """
    
    """
    std_scaler = StandardScaler()
    values = std_scaler.fit_transform(df.values)
    return pd.DataFrame(values, columns=df.columns)

if __name__ == "__main__":
    data = pd.read_csv(FilePath)
    # I want to set aside 500 instances for validation
    k_fold_num = len(data) / 500
    label = ['Price']
    X = data[label]
    y = data.drop(labels=label)
    models = train_models(X, y, k_fold_num)
