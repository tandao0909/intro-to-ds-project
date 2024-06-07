import os
import pandas as pd
import numpy as np

def read_full_data():

    current_directory = f"extract_features_from_data\\data_2"
    # nối đường dẫn với tên file
    files = os.listdir(current_directory)
    # join directory with file name
    files = [f"{current_directory}\\{file}" for file in files]

    df = pd.read_csv(files[0], sep = "\t")

    for i in range(1, len(files)):
        df_tmp = pd.read_csv(files[i], sep = "\t")
        df = pd.concat([df, df_tmp])

    df.to_csv("extract_features_from_data\\final_extracted_data_test.csv", index = False, sep = "\t")

if __name__ == "__main__":
    read_full_data()

    
