import pandas as pd

def handle_lat_long(df):
    df.drop_duplicates(subset=['Latitude', 'Longitude'],inplace = True)  
    df.dropna(subset=['Latitude', 'Longitude'], inplace = True)
    return df

def drop_columns(df, columns_to_drop):
    return df.drop(columns=columns_to_drop, axis = 1, inplace = True)