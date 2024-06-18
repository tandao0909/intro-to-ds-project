# About this data
## 1. Features
Data mà nhóm thu thập được bao gồm có 17 features, bao gồm:
- **Title** : tiêu đề của bài đăng bán nhà
- **Price** : giá bán của căn nhà - đơn vị **tỷ đồng**
- **Diện tích (m2)**
- **Số phòng ngủ**
- **Số phòng WC**
- **Địa chỉ**
- **Description** : nội dung mô tả về căn nhà của người môi giới
- **Chỗ để xe hơi**
- **Đang cho thuê** : cho biết căn nhà đó có đang được sử dụng để cho thuê hay không
- **CSVC xung quanh** : các tiện ích như trường học, bệnh viện, trung tâm thương mại...etc
- **ExtractedTitle** : địa chỉ được trích xuất từ tiêu đề của bài đăng
- **Address1** : địa chỉ được crawl từ mục thông số trong bài đăng bán nhà
- **Address2** : địa chỉ được trích xuất từ tiêu đề của bài đăng
- **lat1** : vĩ độ được trích xuất từ address1 
- **lon1** : kinh độ được trích xuất từ address1
- **lat2** : vĩ độ được trích xuất từ address2 
- **lon2** : kinh độ được trích xuất từ address2 

## 2. Instances
Bộ dataset bao gồm **3358** instances - đã lọc ra những mẫu bị trùng lặp và mẫu không hợp lệ (bài đăng quảng cáo, bán cửa..etc)

## 3. Toolkits
1. Python (pandas,regex...etc)
2. Selenium
3. LLMs produced by [AnyScale](https://www.anyscale.com/)
4. Google Maps API produced by [Google Cloud Platform](https://cloud.google.com/?_gl=1*r24ouv*_up*MQ..&gclid=667652e9cf68194ded6b3488bfd2ad4c&gclsrc=3p.ds)

# About data used for complex models (can be found in [train_complex](../train_complex/) directory)
## Features
- **Log price**: The logarithm of price (which is previously measured in billion VND)
- **Log area (square meters)**: The logarithm of area (measured in squared meters)
- **Distance to center 2**: The distance to the centroid of the second cluster
- **Distance to center 4**: The distance to the centroid of the fourth cluster
- **Log WC**: The logarithm of the number of WC
- **Log Floors**: The logarithm of the number of floors
## Instances
Contains 1548 instances, derives from the [train_set.csv](./train_set.csv) file.
