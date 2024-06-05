import os
import pandas as pd
import numpy as np

def read_full_data():

    current_directory = f"extract_features_from_data\\all_csv_file"
    # nối đường dẫn với tên file
    files = os.listdir(current_directory)
    # join directory with file name
    files = [f"{current_directory}\\{file}" for file in files]

    df = pd.read_csv(files[0], sep = "\t")

    for i in range(1, len(files)):
        df_tmp = pd.read_csv(files[i], sep = "\t")
        df = pd.concat([df, df_tmp])
    df["Description"] = df["Description"].apply(lambda x : str(x))
    ad_pattern = r"Google|Facebook|Cửa\wgỗ|Cửa\wnhựa|Cửa\wsắt|Ad|Max|Marketing|Email|SMS" # tìm các từ khóa để lọc ra tin quảng cáo, rác

    df = df[~df['Description'].str.contains(ad_pattern,case=False,regex=True)]
    df = df[~df['Title'].str.contains(ad_pattern,case=False,regex=True)]


    df["index"] = np.arange(0, len(df))
    df = df.drop_duplicates()
    df = df.set_index("index")
    print("Số dòng: " + str(len(df)))

    df.to_csv("extract_features_from_data\\final_extracted_data.csv", index = False, sep = "\t")

if __name__ == "__main__":
    read_full_data()
