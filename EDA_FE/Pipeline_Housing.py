"""
Provides wrapper estimator classes for functions in the CleanProcess.py, VisualizeLog.py, and OutliersScale.py files.
"""

import numpy as np
import pandas as pd
from folium import Map

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

from CleanProcess import handle_lat_long
from VisualizeLog import check_coordinates_in_vietnam, visualize_clusters # for visualizing the data
from OutliersScale import drop_outliers, transform_housing_data

# Handle latitude and longitude
class HandleLatLong(BaseEstimator, TransformerMixin):
    """
    Handle Latitude and Longitude attributes
    """
    def __init__(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Drop duplicates and NaN values from the 'Latitude' and 'Longitude' columns from the passed DataFrame.

        Parameters:
            X (pandas.DataFrame): The input DataFrame

        Returns:
            pandas.DataFrame: The DataFrame with duplicates and NaN values removed from the 'Latitude' and 'Longitude' columns
        """
        X = handle_lat_long(X)
        return X
    
class DropColumns(BaseEstimator, TransformerMixin):
    """
    Drop columns from the DataFrame

    Parameters:
        columns (list): The list of columns to drop

    Returns:
        pandas.DataFrame: The DataFrame with the specified columns dropped
    """
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns from the DataFrame

        Parameters:
            X (pandas.DataFrame): The input DataFrame

        Returns:
            pandas.DataFrame: The DataFrame with the specified columns dropped
        """
        return X.drop(self.columns, axis=1)
   
class CheckCoordinatesInVietnam(BaseEstimator, TransformerMixin):
    """
    Check if the coordinates are in Vietnam

    Parameters:
        shapefile_path (str): The path to the shapefile

    Returns:
        pandas.DataFrame: The DataFrame with the coordinates checked
    """
    def __init__(self, shapefile_path:str):
        self.shapefile_path = shapefile_path

    def fit(self, X, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        X = check_coordinates_in_vietnam(shapefile_path=self.shapefile_path, housing_df=X)
        return X
    
class VisualizeData(BaseEstimator, TransformerMixin):
    """
    Visualize the data

    Returns:
        pandas.DataFrame: The DataFrame with the data visualized
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Visualize the data

        Parameters:
            X (pandas.DataFrame): The input DataFrame
        
        Returns:
            folium.Map: The map with the data visualized
        """
        # We don't need to return the map, just visualize it
        visualize_clusters(X)
        return X
    
class ApplyLogTransformation(BaseEstimator, TransformerMixin):
    """
    Apply log transformation to specific columns of a DataFrame

    Parameters:
        columns (list): The columns to apply log transformation

    Returns:
        pandas.DataFrame: The DataFrame with log transformation applied to specific columns
    """

    def __init__(self, columns:list[str]):
        self.columns = columns
    def fit(self, X, y=None):
        return self
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Apply log transformation to specific columns of a DataFrame

        Parameters:
            X (pandas.DataFrame): The input DataFrame

        Returns:
            pandas.DataFrame: The DataFrame with log transformation applied to specific columns
        """
        for column in self.columns:
            X[column] = np.log(X[column])
        return X
    
class DropOutliers(BaseEstimator, TransformerMixin):
    """
    Drop outliers from the DataFrame using the box plot method

    Parameters:
        column (str): The column to drop outliers from  

    Returns:
        pandas.DataFrame: The DataFrame without outliers
    """
    
    def __init__(self, column:str):
        self.column = column
    def fit(self, X, y=None):
        return self
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Drop outliers from the DataFrame using the box plot method

        Parameters:
            X (pandas.DataFrame): The input DataFrame

        Returns:
            pandas.DataFrame: The DataFrame without outliers
        """
        X = drop_outliers(X, self.column)
        return X
    
class ConvertBooleanToNumeric(BaseEstimator, TransformerMixin):
    """
    Convert boolean columns to numeric

    Parameters:
        columns (list[str]): The columns to convert

    Returns:
        pandas.DataFrame: The DataFrame with boolean columns converted to numeric
    """
    def __init__(self, columns:list[str]):
        self.columns = columns

    def fit(self, X, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Convert boolean columns to numeric

        Parameters:
            X (pandas.DataFrame): The input DataFrame

        Returns:
            pandas.DataFrame: The DataFrame with boolean columns converted to numeric
        """
        for column in self.columns:
            X[column] = X[column].astype(int)
        return X

class TransformHousingData(BaseEstimator, TransformerMixin):
    """
    Transform the housing data

    Returns:
        pandas.DataFrame: The DataFrame with the housing data transformed
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Transform the housing data

        Parameters:
            X (pandas.DataFrame): The input DataFrame

        Returns:
            pandas.DataFrame: The DataFrame with the housing data transformed
        """
        X = transform_housing_data(X)
        return X

class StandardizeData(BaseEstimator, TransformerMixin):
    """
    Standardize the data

    Returns:
        pandas.DataFrame: The DataFrame with the data standardized
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        """
        Standardize the data

        Parameters:
            X (pandas.DataFrame): The input DataFrame

        Returns:
            pandas.DataFrame: The DataFrame with the data standardized
        """
        scaler = StandardScaler()
        values = scaler.fit_transform(X)
        X = pd.DataFrame(values, columns=X.columns, index=X.index)
        return X
    
# Pipeline for numerical attributes
num_pipeline = Pipeline([
    ('handle_lat_long', HandleLatLong()),
    ('drop_columns', DropColumns(['Title', 'Links', 'Địa chỉ', 'Description', 'ExtractedTitle', 'Address.1'])),
    ('check_coordinates_in_vietnam', CheckCoordinatesInVietnam(shapefile_path='/home/letruongzzio/Documents/Data Science/EDA_FE/vietnam_Vietnam_Country_Boundary/extracted_files/vietnam_Vietnam_Country_Boundary.shp')),
    ('visualize_data', VisualizeData()),
    ('log_transformation', ApplyLogTransformation(['Price', 'Diện tích (m2)', 'Diện tích sử dụng'])),
    ('drop_outliers', DropOutliers('Price')),
    ('convert_boolean_to_numeric', ConvertBooleanToNumeric(['Chỗ để xe hơi', 'Đang cho thuê', 'CSVC xung quanh', 'Mặt tiền'])),
    ('transform_housing_data', TransformHousingData()),
    ('standardize_data', StandardizeData())
])
