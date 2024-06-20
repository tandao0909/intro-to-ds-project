import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def drop_outliers(df, field_name):
    q1 = df[field_name].quantile(0.25)
    q3 = df[field_name].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df = df[(df[field_name] > lower_bound) & (df[field_name] < upper_bound)]
    return df

def apply_log_transformation(df, columns):
    df[columns] = np.log(df[columns])
    return df

def convert_boolean_to_numeric(df, columns):
    for col in columns:
        df[col] = df[col].replace({True: 1, False: 0})
    return df

def apply_floor_and_compute_rooms(df, columns):
    df[columns] = np.floor(df[columns])
    # df['Rooms'] = df['Số phòng ngủ'] + df['Số phòng WC']
    return df

def compute_features(df):
    df['Features'] = df['Chỗ để xe hơi'] + df['Đang cho thuê'] + df['CSVC xung quanh'] + df['Mặt tiền']
    return df

def transform_housing_data(df):
    # Rename columns
    df.rename(columns={
        'Price': 'Log price (1 billion VND)', 
        'Diện tích (m2)': 'Log area (square meters)', 
        'Diện tích sử dụng': 'Log usable area (square meters)',
        'Số phòng ngủ': '(Log) Bedrooms',
        'Số phòng WC': '(Log) WC',
        'Số tầng': '(Log) Number of floors',
        'Chỗ để xe hơi': 'Parking', 
        'Đang cho thuê': 'For rent', 
        'Mặt tiền': 'Facade', 
        'CSVC xung quanh': 'Infrastructure', 
    }, inplace=True)
    
    # Add ID column and set it as index
    df['ID'] = range(1, len(df) + 1)
    df = df[['ID'] + [col for col in df.columns if col != 'ID']]
    
    # Select specific columns
    # selected_columns = ['ID', 'Cluster', 'Log price (1 billion VND)', 'Log area (square meters)', 
    #                     'Log usable area (square meters)', 'Bedrooms', 'WC', 'Number of floors', 
    #                     'Parking', 'For rent', 'Facade', 'Infrastructure', 
    #                     'Latitude', 'Longitude', 'Distance to center']
    # df = df[selected_columns]
    
    return df

def scale_data(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data