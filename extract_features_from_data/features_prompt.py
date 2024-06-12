import os
import requests
import re

s = requests.Session()
current_file_path = os.path.abspath(__file__)

# Sử dụng model
feature_model = "meta-llama/Meta-Llama-3-70B-Instruct"
# feature_model = "mistralai/Mixtral-8x22B-Instruct-v0.1"
api_base = "https://api.endpoints.anyscale.com/v1"
url = f"{api_base}/chat/completions"





with open(os.path.join(os.path.dirname(current_file_path), "private_docu.txt"), encoding="utf-8", mode = "r") as f:
    token = f.read()

# Đọc prompt từ file prompt.txt
with open(os.path.join(os.path.dirname(current_file_path), "features_prompt.txt"), "r", encoding="utf-8") as f:
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
        try:
            all_content = resp.json()["choices"][0]["message"]["content"] # đây là câu trả lời chính
        except Exception as e:
            print(e)
            return [0, 0, 0, ""]
        # tìm Python list trong câu trả lời
        open_key = all_content.find("[") 
        end_key = all_content.find("]")
        try:
            ans = eval(all_content[open_key:end_key+1])
            # đây là đoạn bị lỗi, tự động trả về mảng rỗng để bên phía extract_data.py xử lý đưa vào index error
        except:
            ans = [0, 0, 0, ""]
        return ans
