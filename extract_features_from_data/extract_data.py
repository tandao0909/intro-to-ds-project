# requirement
# !pip install pandas numpy requests

import pandas as pd
import numpy as np
import datetime
import re
from features_prompt import extract_features # import file bắt đầu sử dụng LLM APi
import threading
import os

pd.options.mode.copy_on_write = True



# ------------------------------------------------ Các hàm hỗ trợ trích xuất --------------------------------------------------

def extract_data_from_df(df): # hàm trích xuất thông tin từ dataframe
    # tạo dataframe mới để lưu trữ thông tin trích xuất
    extend_frame = pd.DataFrame(columns=["Chỗ để xe hơi", "Đang cho thuê", "CSVC xung quanh", "Số PN", "Số WC", "ExtractedTitle"])
    limit = 9 # giới hạn số lần thử trích xuất
    # Với mỗi dòng trong df lấy ra Title và Description để trích xuất thông tin
    for i in range(len(df)):
        for j in range(limit + 1): # sau 10 lần thử thì thoát khỏi vòng lặp
            if j == limit:
                print("Failed to extract")
                extend_frame.loc[i] = [False, False, False, False, False, False]
                break
            print(i, end = "\t")
            features = extract_features(df["Description"][i], title = df["Title"][i]) # trích xuất thông tin trả về list
            try:
                extend_frame.loc[i] = features # gán list vào dataframe mới
                print("Complete") # nếu thành công in ra "Complete"
                break # thoát khỏi vòng lặp sớm
            except Exception as e:
                print(e)

    print("Extract complete")
    return extend_frame


# nối dataframe ban đầu với các features mới và tinh chỉnh thêm các features
def concat_dataframe(df, extend_frame):
    df = pd.concat([df, extend_frame], axis=1) 

    # combine các cột "Số phòng ngủ" và "Số phòng WC" với nhau
    df["Số phòng ngủ"] = df["Số phòng ngủ"].apply(lambda x: 0 if x == np.NAN else x) # với giá trị là nan thay bằng 0 de so sanh
    df["Số phòng WC"] = df["Số phòng WC"].apply(lambda x: 0 if x == np.NAN else x)
    df["Số phòng ngủ"] = df["Số phòng ngủ"].astype(float)
    df["Số phòng WC"] = df["Số phòng WC"].astype(float)

    df["Số PN"] = df["Số PN"].apply(lambda x: 0 if x == np.NAN else x) # với giá trị là nan thay bằng 0 de so sanh
    df["Số WC"] = df["Số WC"].apply(lambda x: 0 if x == np.NAN else x)
    df["Số PN"] = df["Số PN"].astype(float)
    df["Số WC"] = df["Số WC"].astype(float)

    def max_two_columns_PN(row): # sẽ lấy max giữa 2 cột "Số phòng ngủ" và "Số PN"
        return max(row['Số phòng ngủ'], row['Số PN'])
    def max_two_columns_WC(row):
        return max(row['Số phòng WC'], row['Số WC'])

    df['Số phòng ngủ'] = df.apply(max_two_columns_PN, axis=1)
    df['Số phòng WC'] = df.apply(max_two_columns_WC, axis=1)

    df = df.drop(["Số PN", "Số WC"], axis = 1) # bỏ đi 1 cột sau khi đã lấy max

    # nếu giá trị là 0 thì thay bằng nan
    df["Số phòng WC"] = df["Số phòng WC"].apply(lambda x : np.nan if x == 0 else x) 
    df["Số phòng ngủ"] = df["Số phòng ngủ"].apply(lambda x : np.nan if x == 0 else x)

    # Combine cột Địa chỉ va ExtractedTitle
        # ưu tiên Địa chỉ hơn
    df["Address1"] = np.where(df["Địa chỉ"].notna(), df["Địa chỉ"], np.where(df["ExtractedTitle"].notna(), df["ExtractedTitle"], np.NAN))
        # ưu tiên ExtractedTitle hơn
    df["Address2"] = np.where(df["ExtractedTitle"].notna(), df["ExtractedTitle"], np.where(df["Địa chỉ"].notna(), df["Địa chỉ"], np.NAN))

    # Lưu lại dataframe sau khi xử lý
    stamp = str(datetime.datetime.now())[:19].replace(":", "-").replace(" ", "_") # tạo ra một thời gian để lưu file
    print("Đã lưu vào lúc: " + stamp) # in ra thời gian để lưu file
    df.to_csv(f"extract_features_from_data\\data_2\\{stamp}.csv", sep="\t", index=False) # lưu lại file csv sau khi xử lý xong
    return df

# Trích xuất thông tin từ dataframe
def process(df, start, end):
    # Chia nhỏ data thành các mini-batch với size = 100
    end = min(end, len(df))
    mini_batch = df[start: end]
    mini_batch["index"] = np.arange(0, len(mini_batch))
    mini_batch = mini_batch.set_index("index")
    extend_frame = extract_data_from_df(mini_batch)
    mini_batch = concat_dataframe(mini_batch, extend_frame)
    print(f"Complete {start} to {end}")
# Nối tất cả các data đã được xử lý thành 1 dataframe
def read_full_data(path):
    current_directory = f"extract_features_from_data\\data_2"
    # nối đường dẫn với tên file
    files = os.listdir(current_directory)
    # join directory with file name
    files = [f"{current_directory}\\{file}" for file in files]

    # nối tất cả data trong folder vào 1 dataframe
    df = pd.concat([pd.read_csv(file, sep = "\t") for file in files])

    df.to_csv(path, index = False, sep = "\t")
    print(df)
# Nối các cột lon, lat vào dataframe
def concat_lon_lat(address1_path, address2_path, path_to_save, push_to_database = False):
    data = pd.read_csv("final_extracted_data.csv", sep = "\t")
    lon_lat1 = pd.read_csv(address1_path, sep = "\t")
    lon_lat1.rename(columns = {"Latitude":"lat1", "Longitude":"lon1"}, inplace = True)
    lon_lat1 = lon_lat1.drop(["Unnamed: 0", "Address1"], axis = 1)

    lon_lat2 = pd.read_csv(address2_path, sep = "\t")
    lon_lat2.rename(columns = {"Latitude":"lat2", "Longitude":"lon2"}, inplace = True)
    lon_lat2 = lon_lat2.drop(["Unnamed: 0", "Address2"], axis = 1)
    data = pd.concat([data, lon_lat1, lon_lat2], axis = 1)
    data.to_csv("final_extracted_data_has_lon_lat.csv", sep = "\t", index = False)
    if push_to_database:
        data.to_csv(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "data\\housing.csv"), sep = "\t", index = False)

if __name__ == "__main__":
    # ------------------------------------------------ Xử lý dữ liệu --------------------------------------------------
    df = pd.read_csv("crawl-data-and-get-coordinates\\next_1000(1).csv", sep="\t")
    origin = df # giữ lại bản gốc của data
    # Bỏ đi các cột bị thừa
    df = df.drop(['Links', 'Unnamed: 0'], axis=1)
    df = df.drop_duplicates() # xóa đi các trùng lặp

    # data ban đầu những giá trị không phải số được điền là "na" -> thay bằng np.NAN
    replace_na_with_NaN = lambda x : np.NAN if (x == "na" or x == 0) else x

    columns = list(df.columns) # Không chuyển Decription vì nó sẽ được xử lý riêng
    columns.remove("Description")

    for column in columns:
        df[column] = df[column].apply(replace_na_with_NaN)

    ad_pattern = r"Google|Facebook|Cửa\wgỗ|Cửa\wnhựa|Cửa\wsắt|Ad|Max|Marketing|Email|SMS" # tìm các từ khóa để lọc ra tin quảng cáo, rác
    df["Title"] = df["Title"].apply(lambda x : str(x))
    df = df[~df['Title'].str.contains(ad_pattern,case=False,regex=True)] # xóa đi các dòng chứa từ khóa quảng cáo
    df["Description"] = df["Description"].apply(lambda x : str(x)) # chuyển tất cả các giá trị trong cột Description thành string
    df = df[~df['Description'].str.contains(ad_pattern,case=False,regex=True)] # xóa đi các dòng chứa từ khóa quảng cáo
    df["Price"] = df["Price"].apply(lambda x : str(x))
    price_pattern = r"tỷ" # lọc ra các dòng chứa giá bán hợp lệ: "tỷ"
    enter_pattern = r"\n" # giá bán không thể chứa ký tự xuống dòng nên lọc bỏ đi

    df = df[df["Price"].str.contains(price_pattern,case=False,regex=True)] # giữ lại giá có "tỷ"
    df = df[~df["Price"].str.contains(enter_pattern,case=False,regex=True)] # xóa đi giá có ký tự xuống dòng
    df["Price"] = df["Price"].apply(lambda x : x[:-3]) # bỏ đi chữ "tỷ"

    df["index"] = np.arange(0, len(df)) # set lại index mới cho dataframe 
    df = df.set_index("index")

    print(len(df))
    # ------------------------------------------------ Trích xuất dữ liệu --------------------------------------------------
    threads = []

    for i in range(0, len(df), 100):
        threads.append(threading.Thread(target=process, args=(df,i, i + 100)))

    for thread in threads:
        thread.start()

    # after all threads are done print "Done"
    for thread in threads:
        thread.join()
    
    path = "extract_features_from_data\\final_extracted_data.csv"
    read_full_data(path)
    print("Done")