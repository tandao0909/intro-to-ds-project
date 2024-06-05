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
with open("features_prompt_copy.txt", "r", encoding="utf-8") as f:
    features_prompt = f.read()

with open("title_prompt.txt", "r", encoding="utf-8") as f:
    title_prompt = f.read()

# Lấy ra kết quả từ model
def extract_features(description, title, token = token):
    body = {
        "model": feature_model,
        "messages": [
            {
            "role": "user",
            "content": features_prompt
            },
            {
            "role": "user",
            "content": "Mô tả" + description + "\nTiêu đề: " + title
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

        return all_content


if __name__ == "__main__":
    dsr = """
Bán nhà HXH Âu Cơ Phường 9 Tân Bình, 51m2 3 Tầng, giá 5 tỷ nhỉnh
+ DT 51m2 cực to cứng nhất khu
+ Kết cấu: 3 Tầng đẹp nhứt nách
+ Hẻm xe hơi mát mẻ an ninh
+ Sổ đẹp hoàn công đủ
+ Hẻm Âu Cơ thông Trần Văn Quang tiện di chuyển đường Bàu Cát, đường Ni Sư Huỳnh Liên, đường Hồng Lạc, Đường Lạc Long Quân, 1 phút ra chợ vải Tân Bình, 5 phút đi qua cư xá Lữ Gia, cư xá Bắc Hải, Quận 10, Quận 1.
    """
    title = "Tiêu đề: Bán nhà HXH Âu Cơ Phường 9 Tân Bình, 51m2 3 Tầng, giá 5 tỷ nhỉnh"
    print(extract_features(dsr, title))