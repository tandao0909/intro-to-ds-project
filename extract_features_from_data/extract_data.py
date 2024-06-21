# requirement
# !pip install pandas numpy requests

import pandas as pd
import numpy as np
import datetime
import re
from features_prompt import extract_features # import file bắt đầu sử dụng LLM APi
import threading
import os
import time

pd.options.mode.copy_on_write = True



# ------------------------------------------------ Các hàm hỗ trợ trích xuất --------------------------------------------------
def get_max_string(strings):
    """Return a string which has the maximum length in a list of strings
    Parameters:
    - strings: a list of strings
    """
    return max(strings, key = lambda x : len(x))

def to_float(val):
    """Convert a string to float. If the string is not a number, return np.nan
    Parameters:
    - val: a string
    """
    try:
        return float(val)
    except:
        return np.nan

def extract_data_from_df(df): # hàm trích xuất thông tin từ dataframe
    """
    Main function to extract features from a dataframe. This function will extract features from Title and Description of each row in the dataframe.
    Each row will be extracted 5 times to get more accurate results.
    Parameters:
    - df: a dataframe which contains Title and Description columns
    """
    # tạo dataframe mới để lưu trữ thông tin trích xuất
    extend_frame = pd.DataFrame(columns=["Số PN", "Số WC", "Số tầng", "ExtractedTitle"])
    limit = 5 # giới hạn số lần thử trích xuất
    # Với mỗi dòng trong df lấy ra Title và Description để trích xuất thông tin
    # gán lại index
    df["index"] = np.arange(0, len(df))
    df = df.set_index("index")
    for i in range(len(df)):
        # lấy ra title và description từ dataframe
        title = df["Title"][i]
        description = df["Description"][i]

        # trích xuất thông tin từ title và description
        features = [extract_features(description, title) for _ in range(limit)]
        # lấy ra các giá trị không rỗng
        features = [feature for feature in features if feature != []]
        # nếu không có giá trị nào thì thêm vào dataframe một dòng toàn giá trị nan (thay = 0 cho đỡ báo lỗi)
        if len(features) == 0:
            extend_frame.loc[i] = [0, 0, 0, ""]
            print("No features extracted")
        else:
            # cột address là cột cuối cùng trong features tôi cần lấy ra chuỗi dài nhất
            try:
                address = get_max_string([feature[3] for feature in features])
            except:
                address = ""
            num_val = [feature[:3] for feature in features] # lấy ra 3 giá trị đầu tiên
            num_val = [[to_float(val) for val in num] for num in num_val] # đảm bảo các giá trị là số
            # lấy mean theo từng cột
            num_val = np.mean(num_val, axis = 0)
            # nối num_val và address thành một dòng mới
            print([num_val[0], num_val[1], num_val[2], address])
            # nối vào extend_frame
            extend_frame.loc[i] = [num_val[0], num_val[1], num_val[2], address]
    print("Extract complete")
    return extend_frame


# nối dataframe ban đầu với các features mới và tinh chỉnh thêm các features
def concat_dataframe(df, extend_frame, path):
    """
    Concatenate the original dataframe with the extracted features dataframe and do some additional processing.
    Parameters:
    - df: the original dataframe
    - extend_frame: the extracted features dataframe
    - path: the path to save the final dataframe
    """
    df = pd.concat([df, extend_frame], axis=1) 

    convert0_to_NAN = lambda x : np.nan if x == 0 else x
    convertNAN_to_0 = lambda x : 0 if x == np.nan else x
    # combine các cột "Số phòng ngủ" và "Số phòng WC" với nhau
    df["Số phòng ngủ"] = df["Số phòng ngủ"].apply(convertNAN_to_0) # với giá trị là nan thay bằng 0 de so sanh
    df["Số phòng WC"] = df["Số phòng WC"].apply(convertNAN_to_0)
    df["Số phòng ngủ"] = df["Số phòng ngủ"].astype(float)
    df["Số phòng WC"] = df["Số phòng WC"].astype(float)

    df["Số PN"] = df["Số PN"].apply(convertNAN_to_0) # với giá trị là nan thay bằng 0 de so sanh
    df["Số WC"] = df["Số WC"].apply(convertNAN_to_0)
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
    df["Số phòng WC"] = df["Số phòng WC"].apply(convert0_to_NAN) 
    df["Số phòng ngủ"] = df["Số phòng ngủ"].apply(convert0_to_NAN)

    # Combine cột Địa chỉ va ExtractedTitle
        # ưu tiên Địa chỉ hơn
    df["Address1"] = np.where(df["Địa chỉ"].notna(), df["Địa chỉ"], np.where(df["ExtractedTitle"].notna(), df["ExtractedTitle"], np.NAN))
        # ưu tiên ExtractedTitle hơn
    df["Address2"] = np.where(df["ExtractedTitle"].notna(), df["ExtractedTitle"], np.where(df["Địa chỉ"].notna(), df["Địa chỉ"], np.NAN))

    # Lưu lại dataframe sau khi xử lý
    stamp = str(datetime.datetime.now()).replace(":", "-").replace(" ", "_") # tạo ra một thời gian để lưu file
    print("Đã lưu vào lúc: " + stamp) # in ra thời gian để lưu file
    stamp += str(np.random.randint(0, 1000)) # thêm một số ngẫu nhiên vào tên file
    path = os.path.join(path, f"{stamp}.csv")
    df.to_csv(path, sep="\t", index=False) # lưu lại file csv sau khi xử lý xong
    return df

# Trích xuất thông tin từ dataframe
def process(df, start, end, path):
    """
    Extract features from a dataframe. This function take a part of the dataframe and extract features from it. It is good for multi-threading.
    Parameters:
    - df: the dataframe
    - start: the start index
    - end: the end index
    - path: the path to save the final dataframe
    """
    # Chia nhỏ data thành các mini-batch với size = 100
    end = min(end, len(df))
    mini_batch = df[start: end]
    mini_batch["index"] = np.arange(0, len(mini_batch))
    mini_batch = mini_batch.set_index("index")
    extend_frame = extract_data_from_df(mini_batch)
    mini_batch = concat_dataframe(mini_batch, extend_frame, path)
    print(f"Complete {start} to {end}")
# Nối tất cả các data đã được xử lý thành 1 dataframe

def read_full_data(path_in, path_out):
    """
    Read all data in a folder and concatenate them into a single dataframe.
    Parameters:
    - path_in: the folder path which contains all data files
    - path_out: the path to save the final dataframe
    """
    current_directory = path_in
    # nối đường dẫn với tên file
    files = os.listdir(current_directory)
    # join directory with file name
    files = [os.path.join(current_directory, file) for file in files]

    # nối tất cả data trong folder vào 1 dataframe
    df = pd.concat([pd.read_csv(file, sep = "\t") for file in files])
    df = df.drop_duplicates(subset = ["Description"], keep = "first") # xóa đi các dòng trùng lặp
    df.drop(["index"], axis = 1, inplace=True) # bỏ đi cột index
    df["Số tầng"] = df["Số tầng"].apply(lambda x : 1 if x < 1 else x) # nếu số tầng nhỏ hơn 1 thì gán bằng 1
    df["Diện tích sử dụng"] = df["Diện tích (m2)"] * df["Số tầng"] # tính diện tích sử dụng
    df.to_csv(path_out, index = False, sep = "\t")
    # print(df)

def data_cleaning(df):
    """
    Clean the data before extracting features. This function will remove unnecessary columns, remove duplicates, and filter out ads.
    Then it will create new features for the dataframe: "Chỗ để xe hơi", "Đang cho thuê", "CSVC xung quanh", "Mặt tiền".
    Parameters:
    - df: the dataframe
    """
    df = df.drop_duplicates() # xóa đi các trùng lặp

    df["Description"] = df["Description"].apply(lambda x : str(x).lower()) # chuyển tất cả các giá trị trong cột Description thành string và chuyển về chữ thường
    df["Title"] = df["Title"].apply(lambda x : str(x).lower()) # chuyển tất cả các giá trị trong cột Title thành string và chuyển về chữ thường

    ad_pattern = r"google|facebook|cửa\wgỗ|cửa\wnhựa|cửa\wsắt|ad|max|marketing|email|sms" # tìm các từ khóa để lọc ra tin quảng cáo, rác
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
    df["Price"] = df["Price"].astype(float) # chuyển về kiểu float
    df = df[df["Price"] < 100]

    df["index"] = np.arange(0, len(df)) # set lại index mới cho dataframe 
    df = df.set_index("index")
 

    # ------------------------------------------------ Tạo các features mới --------------------------------------------------
    # Chỗ để xe hơi
    gara_pattern = r"\bgara\b|\bđỗ ô tô\b|\bxe hơi\b|\bô tô tránh\b|\bhầm xe\b|\bhầm\b|\bnhà xe\b|\bđỗ\b|\bô tô\b|\bôtô\b|\bsân đỗ\b"
    df["Chỗ để xe hơi"] = df["Description"].str.contains(gara_pattern,case=False,regex=True)

    # Đang cho thuê
    in_lease_pattern = r"\btriệu/tháng\b|\btr/tháng\b|\bdòng tiền\b|\bđang cho thuê\b|\bdoanh thu\b"
    df["Đang cho thuê"] = df["Description"].str.contains(in_lease_pattern,case=False,regex=True)

    # Tiện ích xung quanh
    extension_pattern=r"trường\shọc|bệnh\sviện|bv|trung\stâm\sthương\smại|mall|aeon|siêu\sthị|đh|đại\shọc|học\sviện|tiện\sích|chợ|thpt|thcs|sầm\suất|vị\strí\sđắc\sđịa|trường|mart|bigc|y tế"
    df["CSVC xung quanh"]=df["Description"].str.contains(extension_pattern,case=False,regex=True)

    # Mặt tiền
    money_face_pattern = r"mặt tiền|mặt phố|mặt đường"
    except_pattern = r"cách mặt tiền|cách mặt phố|sát mặt tiền" # loại bỏ các từ khóa không phải mặt tiền
    tmp = df["Description"].str.contains(money_face_pattern,case=False,regex=True)
    tmp2 = ~df["Description"].str.contains(except_pattern,case=False,regex=True)

    df["Mặt tiền"] = tmp & tmp2 # lọc ra các dòng chứa từ khóa "mặt tiền" và không chứa từ khóa except_pattern
    return df


def solve(read_path, path_in, path_out, save_path, folder = False):
    """
    Main function to extract features from a dataframe. This function will extract features from a dataframe and save the final dataframe.
    Parameters:
    - read_path: the path to the data file
    - path_in: the folder path which contains all data files
    - path_out: the path to save the final dataframe
    - save_path: the path to save the extracted data
    - folder: if True, read all files in the folder. If False, read only one file
    """
    if folder:
        # concat all csv file in folder path
        files = os.listdir(read_path)
        files = [os.path.join(read_path, file) for file in files]
        df = pd.concat([pd.read_csv(file, sep = "\t") for file in files])
        print("Folder = True")
    else:
        df = pd.read_csv(read_path, sep = '\t')

    df = data_cleaning(df)
    print(f"Len(df) = {len(df)}")
    start_time = time.time()
    threads = []

    step = int(len(df) / 10) + 10 # chia nhỏ data thành 10 phần dành cho 10 thread
    print(f"Step for each thread: {step}")

    for i in range(0, len(df), step):
        threads.append(threading.Thread(target=process, args=(df,i, i + step, save_path)))

    for thread in threads:
        try:
            thread.start()
        except Exception as e:
            print(e)

    # sau khi tất cả các thread đã hoàn thành thì join lại
    for thread in threads:
        thread.join()

    read_full_data(path_in, path_out)
    print("Time: ", time.time() - start_time)
    print("Done")


if __name__ == "__main__":
    # folder chứa data cần xử lý
    read_path = os.path.join("extract_features_from_data", "data_to_solve")
    # trong quá trình xử lý do tách nhỏ ra thành 10 phần nên cần lưu vào 1 thư mục
    save_path = os.path.join("extract_features_from_data", "solved_data")
    # path_in: path chứa tất cả các file đã xử lý
    path_in = os.path.join("extract_features_from_data", "solved_data")
    # path_out: path để lưu file cuối cùng sau khi xử lý
    path_out = os.path.join("extract_features_from_data", "final_extracted_data.csv")

    # gọi hàm xử lý
    solve(read_path, path_in, path_out, save_path, folder = True)

