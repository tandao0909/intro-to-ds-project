import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def drop_outliers(df:pd.DataFrame, field_name:str) -> pd.DataFrame:
    """
    Drop outliers from a DataFrame based on a specific field, using box plot method.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        field_name (str): The field name to drop outliers.
    
    Returns:
        pd.DataFrame: The DataFrame without outliers.
    """
    # Calculate the first and third quartile 
    q1 = df[field_name].quantile(0.25)
    q3 = df[field_name].quantile(0.75)

    # Calculate the IQR
    iqr = q3 - q1

    # Calculate the lower and upper bound
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Return the DataFrame within the lower and upper bound
    return df[(df[field_name] > lower_bound) & (df[field_name] < upper_bound)]

def apply_log_transformation(df:pd.DataFrame, columns:list[str]) -> pd.DataFrame:
    """
    Apply log transformation to specific columns of a DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (str): The columns to apply log transformation.

    Returns:
        pd.DataFrame: The DataFrame with log transformation applied to specific columns.
    """
    df[columns] = np.log(df[columns])
    return df

def convert_boolean_to_numeric(df:pd.DataFrame, columns:list[str]) -> pd.DataFrame:
    """
    Convert boolean values to numeric values in specific columns of a DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (str): The columns to convert boolean values to numeric values.
    
    Returns:
        pd.DataFrame: The DataFrame with boolean values converted to numeric values in specific columns.
    """
    df[columns] = df[columns].astype(int)
    return df

def apply_floor(df:pd.DataFrame, columns:list[str]) -> pd.DataFrame:
    """
    Apply floor function to specific columns of a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (str): The columns to apply floor function.

    Returns:
        pd.DataFrame: The DataFrame with floor function applied to specific columns.
    """
    df[columns] = np.floor(df[columns])
    return df

def compute_rooms(df:pd.DataFrame) -> pd.DataFrame:
    """
    Compute the total number of rooms based on the number of bedrooms and bathrooms.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with the number of rooms computed.
    """
    df['Rooms'] = df['Số phòng ngủ'] + df['Số phòng WC']
    return df

def compute_features(df:pd.DataFrame) -> pd.DataFrame:
    """
    Compute the total number of features based on the number of parking spaces, rooms for rent, infrastructure, and facade.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with the number of features computed.
    """
    df['Features'] = df['Chỗ để xe hơi'] + df['Đang cho thuê'] + df['CSVC xung quanh'] + df['Mặt tiền']
    return df

def transform_housing_data(df:pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns, add ID column, select specific columns, and return the transformed DataFrame.

    Parameters:
        pd.DataFrame: The input DataFrame.
    
    Returns:
        pd.DataFrame: The transformed DataFrame.
    """
    # Rename columns
    df.rename(columns={
        'Price': 'Log price (1 billion VND)', 
        'Diện tích (m2)': 'Log area (square meters)', 
        'Diện tích sử dụng': 'Log usable area (square meters)',
        'Chỗ để xe hơi': 'Parking', 
        'Đang cho thuê': 'For rent', 
        'Mặt tiền': 'Facade', 
        'CSVC xung quanh': 'Infrastructure', 
        'Số tầng': 'Number of floors',
        'Số phòng ngủ': 'Bedrooms',
        'Số phòng WC': 'WC',
    }, inplace=True)
    
    # Add ID column and set it as index
    df['ID'] = range(1, df.shape[0] + 1)
    df = df[['ID'] + [col for col in df.columns if col != 'ID']]
    
    # Select specific columns
    selected_columns = ['ID', 'Cluster', 'Log price (1 billion VND)', 'Log area (square meters)',
                        'Log usable area (square meters)', 'Rooms', 'Bedrooms', 'WC', 'Number of floors', 
                        'Parking', 'For rent', 'Facade', 'Infrastructure', 'Features', 
                        'Latitude', 'Longitude', 'Distance to center']
    df = df[selected_columns]
    
    return df

def scale_data(data:pd.DataFrame) -> pd.DataFrame:
    """
    Scale the input data using StandardScaler.

    Parameters:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The scaled DataFrame.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data.values)
    scaled_data = pd.DataFrame(scaled_data, columns=data.columns)
    return scaled_data
