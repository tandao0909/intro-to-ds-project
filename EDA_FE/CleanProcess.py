import pandas as pd

def handle_lat_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop duplicates and NaN values from the 'Latitude' and 'Longitude' columns from the passed DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame

    Returns:
        pandas.DataFrame: The DataFrame with duplicates and NaN values removed from the 'Latitude' and 'Longitude' columns
    """
    df.drop_duplicates(subset=['Latitude', 'Longitude'],inplace = True)  
    df.dropna(subset=['Latitude', 'Longitude'], inplace = True)
    return df
