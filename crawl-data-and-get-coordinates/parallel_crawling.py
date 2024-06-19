import os
import re
import numpy as np
from selenium import webdriver
import pandas as pd
import numpy as np
from time import sleep
import threading
import os
from queue import Queue
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

#Set đường dẫn
os.environ['PATH'] += r"/usr/local/bin/"
path = "/home/tiamo/Documents/code/Intro to DS 2024/Project1/intro-to-ds-project/crawl-data-and-get-coordinates/dataset"

#Trang web cần cào dữ liệu
base_url = "https://batdongsan.vn/ban-nha/"

#Số trang bắt đầu cào dữ liệu trong từng luồng
num_pages = [650,660,670,680,690]
# Số trang cần phải cào trong từng lường (step của numpages ở trên)
n_iter = 10

def openMultiBrowser(n):
    '''
    Vai trò: Mở đồng loạt n trình duyệt để tiến hành chạy đa luồng
    Arg:
        - n là số trình duyệt muốn chạy đồng thời
    Return
        - list n driver - đại diện n trình duyệt muốn chạy trong n luồng
    '''
    drivers = []
    for i in range(n):
        # setting option cho Chrome Driver để nó chạy ngầm, không hiện GUI để tiết kiệm tài nguyên
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        driver = webdriver.Chrome(options=chrome_options)
        # set up thời gian chờ tối đa của web là 5s -  tránh tình trạng chờ quá lâu
        driver.set_page_load_timeout(5) 
        drivers.append(driver)
    return drivers

def loadMultiPages(driver,i):
    '''
    Vai trò: Ứng với một driver, sẽ load đến đường dẫn cần crawl dữ liệu đầu tiên
    Arg:
        - driver - một driver trong list driver ta khơi tạo trước đó để thực hiện mở link đơn lẻ
        - i - số trang bắt đầu tương ứng với driver này (ex:1,5,10,15,20...etc)
    Return: None
    '''
    try:
        print("------Loading thread------")
        driver.get(f"{base_url}p{i}")
    except TimeoutException: #try except để tránh trình trạng load quá lâu
        pass
   

def loadMultiBrowsers(drivers_rx): 
    '''
    Vai trò: Tiến hành chạy đa luồng với danh sách các driver đã khởi tạo
    Arg:
        - drivers_rx: danh sách các driver đã khởi tạo ở hàm openMultiBrowser
    Return: None
    '''
    for i,driver in enumerate(drivers_rx):
        '''
        target - là hàm muốn chạy trong luồng
        args là các đối số cần thiết cho hàm đó - ở đây là driver tương ứng với luồng,
                                                num_pages[i] là số trang bắt đầu cào dữ liệu như đã đề cập trước đó
        '''
        t = threading.Thread(target=loadMultiPages,args=(driver,num_pages[i]))
        t.start()

def get_params(text):
    '''
    Vai trò: Trích xuất thông tin cần thiết từ mục params trên bài đăng bán nhà
    Arg: đoạn văn bản chứa những thông tin trên được khai thác từ webelement
    Return: một list các chỉ số theo định dạng [Diện tích (m2),Số phòng ngủ,Số WC, Địa chỉ] -> được trích xuất từ text
    '''
    reg_template = {"Area":'Diện tích:\s*(\d+)',
                "Room":'Phòng ngủ:\s*(\d+)',
                "WC":'Phòng WC:\s*(\d+)',
                "Location":'Địa chỉ:\s*(.+)'}
    list_params = []
    for name in reg_template:
        x = re.search(r'{}'.format(reg_template[name]),text)
        if x:
            list_params.append(x.group(1))
        else:
            #nếu chỉ số k đc đề cập trong đoạn text thì trả về NaN
            list_params.append(np.nan)
    return list_params

def get_data(driver,start_page):
    '''
    Vai trò: thực hiện cào dữ liệu trong từng luồng
    Arg:
        - driver : driver tương ứng trong từng luồng
        - start_page: số trang bắt đầu cào dữ liệu trong luồng này (ex: 1,5,10,15,20...etc)
    Return: trả về một dataframe là dữ liệu thu thập được sao khi duyệt qua n_page ứng với mỗi luồng
    '''
    report =  pd.DataFrame(columns=['Title', 'Price', 'Links',\
            'Diện tích (m2)', 'Số phòng ngủ','Số phòng WC', 'Địa chỉ'\
            ,'Description'])

    for i in range(start_page,start_page+n_iter):
        print(f"------Start crawl page {i}------")
        
        try:
            # Lấy ra element để tiến sang trang tiếp theo - sử dụng ở cuối vòng lặp
            next = driver.find_element('css selector','.uk-pagination [rel="next"]').get_attribute('href')
             # Lấy element là các item trong một page (20 items)
            print("\t------Getting links to 20 items------")
            elements = driver.find_elements('css selector','.uk-width-medium-7-10 .name [href]')
        except TimeoutException:
            pass
        
        # Trích xuất dẫn đến mô tảchi tiết của từng item
        links = [element.get_attribute('href') for element in elements]
        # Duyệt qua từng item
        n = len(links)
        data = []
        print("\t------Start extracting information------")
        for j in range(n):
            # Mở link dẫn đến item
            try:
                driver.get(links[j])
            except TimeoutException:
                pass
            # Lấy ra những thông tin cần thiết (Title, Price, Số Phòng ngủ, Số WC, Diện tích, Description...etc)
            try:
                # Cho page 1s để load những element cần thiết - tránh trường hợp tìm không ra
                sleep(3)
                # Tìm các element chứa những thông tin cần thiết
                title_ele = driver.find_element('css selector','h1.uk-panel-title')
                price_ele = driver.find_element('css selector','.meta .price')
                params_ele = driver.find_element('css selector',".param")
                content_ele = driver.find_element('css selector','.item .body .content')
                # Trích xuất văn bản từ web element
                title = title_ele.text
                price = price_ele.text
                params_ = get_params(params_ele.text)
                params_.append(content_ele.text)
                # Gộp các thông tin thành một list tmp_list theo form la các feature trong data frame report đã khai báo
                tmp_list = [title,price,links[j]]
                tmp_list = tmp_list + params_
                data.append(tmp_list)
            except:
                print("Error!")
                pass
        
        # Xếp chồng các phần tử trong list data trước đó để tạo thành ma trận với mỗi hàng là một mẫu trong bộ dữ liệu
        matrix_data = np.vstack([item for item in data]) 
        # Tạo ra data_page là dataframe chứa dữ liệu của một trang và concat vào dataframe report
        data_page = pd.DataFrame(matrix_data,columns=report.columns)
        
        report = pd.concat([report,data_page],axis=0)
        report.set_index(np.arange(len(report)),inplace=True)
        # Sao lưu lại data vào file output.csv tránh trường hợp bị mất dữ liệu trong quá trình cào
        report.to_csv(f'{path}/page{i}.csv',sep="\t",index=False)
        print(f"------Page{i} - Done!------\n\n")
        # Chuyển sang trang kế tiếp
        try:
            driver.get(next)
        except TimeoutException:
            pass

    return report


def runInParallel(func,drivers_rx):
    '''
    Vai trò: Tiến hành chạy đa luồng
    Arg:
        -func: hàm để crawl data - ở đây sẽ là get_data
        - drivers_rx : danh sách các driver được khai báo trước đó để tiến hành chạy đa luồng
    Return: trả về một danh sách n dataframe (n là số luồng)
    '''
    # Hàng đợi để lưu trữ kết quả từ hàm get_data
    que = Queue()
    for i,driver in enumerate(drivers_rx):
        '''
        target: hàm sẽ thực hiện việc push các dataframe thu được từ get_data vào hàng đợi q
        args:
            - q = que - hàng đợi đã khai báo trước đó
            - arg1 = driver - driver của luồng thứ i
            - start_page = num_page[i] - số trang bắt đầu cào dữ liệu ứng với luồng thứ i
        '''
        t1 = threading.Thread(target= lambda q,arg1,start_page:q.put(func(arg1,start_page)),args=(que,driver,num_pages[i]))
        t1.start()
    ans = []
    for i in range(len(drivers_rx)):
        try:
            tmp = que.get()
            ans.append(tmp)
        except:
            continue
    print("------Done!------")
    return ans

if __name__ == '__main__':
    driver_r5 = openMultiBrowser(5)
    loadMultiBrowsers(driver_r5)
    sleep(5)
    list_report = runInParallel(get_data,driver_r5)
    df = pd.concat([report for report in list_report],axis=0)
    df.to_csv('raw_data_update.csv',sep='\t')
    
