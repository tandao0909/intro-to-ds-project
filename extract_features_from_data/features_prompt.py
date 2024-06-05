import os
import requests
import re

s = requests.Session()

# Sử dụng model
title_model = "meta-llama/Meta-Llama-3-70B-Instruct"
feature_model = "meta-llama/Meta-Llama-3-8B-Instruct"
api_base = "https://api.endpoints.anyscale.com/v1"
url = f"{api_base}/chat/completions"


with open("extract_features_from_data\\private_docu.txt") as f:
    token = f.read()

# Đọc prompt từ file prompt.txt
with open("extract_features_from_data\\features_prompt.txt", "r", encoding="utf-8") as f:
    features_prompt = f.read()


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
