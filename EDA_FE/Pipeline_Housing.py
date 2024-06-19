import numpy as np
from sklearn.preprocessing import StandardScaler
from CleanProcess import handle_lat_long
from VisualizeLog import check_coordinates_in_vietnam, visualize_clusters # for visualizing the data
from OutliersScale import drop_outliers, transform_housing_data
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

# Handle latitude and longitude
class HandleLatLong(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        handle_lat_long(X)
        return X
    
# Custom transformer to drop columns
class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X.drop(self.columns, axis=1)
    
# Check whether or not the coordinates are in Vietnam
class CheckCoordinatesInVietnam(BaseEstimator, TransformerMixin):
    def __init__(self, shapefile_path):
        self.shapefile_path = shapefile_path
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        check_coordinates_in_vietnam(shapefile_path=self.shapefile_path, housing_df=X)
        return X
    
# Visualize the data
class VisualizeData(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        visualize_clusters(X)
        return X
    
# Custom transformer to apply log transformation
class ApplyLogTransformation(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        for column in self.columns:
            X[column] = np.log(X[column])
        return X
    
# Custom transformer to drop outliers
class DropOutliers(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = drop_outliers(X, self.column)
        return X
    
# Custom transformer to convert boolean to numeric
class ConvertBooleanToNumeric(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        for column in self.columns:
            X[column] = X[column].astype(int)
        return X

# Custom transformer to transform housing data
class TransformHousingData(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = transform_housing_data(X)
        return X

# Standardize the data
class StandardizeData(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
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
