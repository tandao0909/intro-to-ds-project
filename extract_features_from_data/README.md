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



## 2. Các tập tin chính

### 2.1. extract_data.py

Tập tin chính để chạy extract data. Trả về data với nhiều features hơn.

Chỉ cần sử dụng file này. Cung cấp đường dẫn đến dữ liệu cào được từ web, nó tự động hoàn toàn và trả về file `final_extracted_data`.

Trong file hãy cung cấp đường dẫn đến file dữ liệu thô và bấm chạy.

### 2.2. features_prompt.py

Là tập tin python script lưu quá trình sử dụng LLM API từ [anyscale](https://www.anyscale.com/). 

Về vấn đề lỗi khi trả về không đúng format khi được dạy là điều dễ hiểu. Mô hình ngôn ngữ sẽ trả lời sai vài lần trong khoảng 100 lần được hỏi. Khi trả lời sai lập tức gửi về mảng rỗng nhầm thông báo cho extract_data.py hiểu. Nên lỗi bên tập tin chính sẽ là `cannot set a row with mismatched columns`.

### 2.3 features_prompt.txt

Là tập tim prompt huấn luyện mô hình LLM để trả về các đặc trưng cần thiết.

### 2.4 private_docu.txt

Người dùng cần tạo một file txt `private_docu.txt` và điền vào đó anyscale API key để LLM có thể hoạt động.