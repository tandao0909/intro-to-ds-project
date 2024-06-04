import os
import requests
import re

s = requests.Session()

# Sử dụng model
title_model = "meta-llama/Meta-Llama-3-70B-Instruct"
feature_model = "meta-llama/Meta-Llama-3-8B-Instruct"
api_base = "https://api.endpoints.anyscale.com/v1"
url = f"{api_base}/chat/completions"

token = "esecret_6crjtwnbanh5wzlt1fcehx2cfl"


# Đọc prompt từ file prompt.txt
with open("features_prompt.txt", "r", encoding="utf-8") as f:
    features_prompt = f.read()

with open("title_prompt.txt", "r", encoding="utf-8") as f:
    title_prompt = f.read()

# Lấy ra kết quả từ model
def extract_features(description, token = token):
    body = {
        "model": feature_model,
        "messages": [
            {
            "role": "user",
            "content": features_prompt
            },
            {
            "role": "user",
            "content": description
            }
        ],
        "temperature": 1,
        "max_tokens": 256,
        "top_p": 1,
        "frequency_penalty": 0
    }

    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        all_content = resp.json()["choices"][0]["message"]["content"] # đây là câu trả lời chính
        # tìm Python list trong câu trả lời
        open_key = all_content.find("[") 
        end_key = all_content.find("]")
        try:
            ans = eval(all_content[open_key:end_key+1])
            # đây là đoạn bị lỗi, tự động trả về mảng rỗng để bên phía extract_data.py xử lý đưa vào index error
        except:
            ans = []
        return ans


def extract_title(title, token = token):
    body = {
        "model": title_model,
        "messages": [
            {
            "role": "user",
            "content": title_prompt
            },
            {
            "role": "user",
            "content": title
            }
        ],
        "temperature": 1,
        "max_tokens": 256,
        "top_p": 1,
        "frequency_penalty": 0
    }

    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        all_content = resp.json()["choices"][0]["message"]["content"]
        # ans = resp.json()

        return ans, all_content


if __name__ == "__main__":
    print(extract_features("""Mô tả:
+ Thông số cực đẹp 5 x 30m (150m2)
+ Nhà cấp 4, 2PN, toilet, phòng khách, bếp, sân sau trồng cây.
+ Nhà gần sát Mặt tiền, hẻm nhựa xe hơi tránh.
+ Khu vực tập trung nhiều Khu dân cư, các Dự án lớn, thu hút đông đảo các Nhà Đầu Tư lớn, Huyện Nhà Bè hướng đến mục tiêu trở thành Thành phố trực thuộc TP.Hồ Chí Minh.
+ Giá chưa tới 30tr/m2 bao đầu tư.
+ Sổ đang vay bank 2.2 tỷ, pháp lý chuẩn, chủ cần bán gấp.
Thiện chí alo em Hiền gặp chính chủ thương lượng, miễn trung gian.
"""))