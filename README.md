Dự án là dự án của nhóm làm về bài tập lớn môn Nhập môn Khoa học dữ liệu. Nội dung dự án là cào dữ liệu từ trang https://batdongsan.vn/ban-nha/, sau đó thực hiện phân tích và đánh giá giá nhà sử dụng các mô hình cơ bản.

# Introduce to Data Science - Project 1
## 1. Timeline

| Tuần/Ngày     | Công Việc                        | Người Thực Hiện    | Ghi Chú                            |
| ------------- | -------------------------------- | ------------------ | --------------------------------- |
| 02/06 - 05/06 | Phát triển script scrape dữ liệu | Vinh               |                                    |
| 06/06 - 07/06 | Kiểm tra và làm sạch dữ liệu     | Thang Q            |                                    |
| 08/06 - 09/06 | EDA                              | Le Truong          | Outlier, Distribution, Tuong quan  |
| 10/06 - 14/06 | Feature Engineer                 | Hoa Ho             | Chuẩn bị dữ liệu cho mô hình hóa   |
| 15/06         | Huấn luyện các mô hình           | Tan Dao            | Linear/Ridge/Lasso Regression, v.v |
| 16/06         | Đánh giá mô hình                 | Vinh, Thang Quang  | So sánh hiệu suất các mô hình      |
| 17/06-19/06   | Tinh chỉnh mô hình tốt nhất      | Le Truong, Hoa Ho  | Hyper Tuning                       |
| 20/06-21/06   | Hoàn thiện báo cáo               | Tan Dao, Le Truong | Mô tả quá trình, phương pháp luận  |
| 21/06         | Đóng gói dữ liệu và nộp báo cáo  | Tất cả             | Kiểm tra lại toàn bộ dự án         |

## Project Structure

- Thư mục [raw-data-and-get-coordinates](./craw-data-and-get-coordinates/) chứa các file cào dữ liệu và biên dịch ra các biến tọa độ dựa trên địa chỉ cào được.
- Thư mực [extract_features_from_data](./extract_features_from_data/) chứa các biến được trích xuất từ dữ liệu thô
- Thư mục [data](./data/) chứa dữ liệu sẽ được sử dụng.