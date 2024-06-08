"""Train simple models, including:
linear regression, Ridge regression, Lasso regression, decision tree, random forest"""

from pathlib import Path

from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

FilePath = Path() / "../data/housing.csv"

# TODO: Add train decision tree and random forest functions

def grid_search_cv(model, X, y, param_grid: dict, k_fold_num: int) -> BaseEstimator:
    """Return the best model, given the parameter search dictionary."""
    grid_search = GridSearchCV(model, param_grid, cv=k_fold_num)
    grid_search.fit(X, y)
    return grid_search.best_estimator_

def train_linear_regression(X, y) -> LinearRegression:
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    return lin_reg

def train_ridge_regression(X, y, k_fold_num:int):
    ridge_reg = Ridge()
    param_grid = {'alpha': [0.001, 0.01, 0.1, 1]}
    return grid_search_cv(ridge_reg, X, y, param_grid, k_fold_num)


def train_lasso_regression(X, y, k_fold_num:int):
    ridge_reg = Lasso()
    param_grid = {'alpha': [0.001, 0.01, 0.1, 1]}
    return grid_search_cv(ridge_reg, X, y, param_grid, k_fold_num)


def train_models(X, y, k_fold_num:int):
    """
    Train several simple models, and return all these trained models.
    """
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.25)
    models = []
    models.append(train_linear_regression(X_train, y_train))
    models.append(train_ridge_regression(X_train, y_train, k_fold_num))
    models.append(train_lasso_regression(X_train, y_train, k_fold_num))
    return models


if __name__ == "__main__":
    data = pd.read_csv(FilePath)
    # I want to set aside 500 instances for validation
    k_fold_num = len(data) / 500
    label = ['Price']
    X = data[label]
    y = data.drop(labels=label)
    models = train_models(X, y, k_fold_num)
