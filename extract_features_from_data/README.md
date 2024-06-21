## 1. Task:

Trích xuất dữ liệu phi cấu trúc từ cột "Description" và cột "Title" thành dữ liệu có cấu trúc. Ví dụ:

```
+ Thông số cực đẹp 5 x 30m (150m2)
+ Nhà cấp 4, 2PN, toilet, phòng khách, bếp, sân sau trồng cây.
+ Nhà gần sát Mặt tiền, hẻm nhựa xe hơi tránh.
+ Khu vực tập trung nhiều Khu dân cư, các Dự án lớn, thu hút đông đảo các Nhà Đầu Tư lớn, Huyện Nhà Bè hướng đến mục tiêu trở thành Thành phố trực thuộc TP.Hồ Chí Minh.
+ Giá chưa tới 30tr/m2 bao đầu tư.
+ Sổ đang vay bank 2.2 tỷ, pháp lý chuẩn, chủ cần bán gấp.
☎️ Thiện chí alo em Hiền gặp chính chủ thương lượng, miễn trung gian."

Tiêu đề: Bạch Đằng, Quận 1
```

Thành các tính năng như sau: "Số PN", "Số WC", "Số tầng", "ExtractedTitle". Trong đó ExtractedTitle: nghĩa là địa chỉ được trích xuất từ TItle lẫn Description.

```
Kết quả trả về sẽ là một Python list như: [2, 1, 0, "Bạch Đằng, Quận 1"]
```

Giải thích: 

```
- Đề cập "2PN" nên số phòng ngủ là 2 và 1 từ toilet nên số phòng ngủ là 2 và số toilet là 1
- Không đề cập đến số tầng
- Tiêu đề thể hiện địa chỉ
```

Với mỗi một hàng dữ liệu, ta trích xuất 5 lần vì LLM model chưa xử lý tốt được thông tin. Sau đó 3 cột đầu là số phòng ngủ, wc và số tầng sẽ được lấy trung bình. Cột cuối cùng là địa chỉ sẽ được chọn bởi địa chỉ dài nhất trong 5 lần trích xuất.

## 2. Các tập tin chính

### 2.1. extract_data.py

Tập tin chính để chạy extract data. Trả về data với nhiều features hơn.

Chỉ cần sử dụng file này. Cung cấp đường dẫn đến dữ liệu cào được từ web, nó tự động hoàn toàn và trả về file `final_extracted_data`.

Trong file hãy cung cấp đường dẫn đến file dữ liệu thô, đường dẫn lưu, đường dẫn xuất là chạy được.

Cụ thể trong hàm main:

```

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

```

Lưu ý: Nếu chỉ cần xử lý 1 file đơn lẻ thì `read_path` là đường dẫn đến file và hàm solve hãy truyền tham số `folder` = False hoặc không truyền, mặc định đã là False. Còn cần xử lý nhiều file trong một thư mục hãy để `read_path` là đường dẫn đến thư mục như code block trên và đặt tham số `folder=True` trong hàm solve.

### 2.2. features_prompt.py

Là tập tin python script lưu quá trình sử dụng LLM API từ [anyscale](https://www.anyscale.com/). 

Về vấn đề lỗi khi trả về không đúng format khi được dạy là điều dễ hiểu. Mô hình ngôn ngữ sẽ trả lời sai vài lần trong khoảng 100 lần được hỏi. Khi trả lời sai lập tức gửi về mảng rỗng nhầm thông báo cho extract_data.py hiểu. Nên lỗi bên tập tin chính sẽ là `cannot set a row with mismatched columns`.

### 2.3 features_prompt.txt

Là tập tin prompt huấn luyện mô hình LLM để trả về các đặc trưng cần thiết.

### 2.4 private_docu.txt

Người dùng cần tạo một file txt `private_docu.txt` và điền vào đó anyscale API key để LLM có thể hoạt động.