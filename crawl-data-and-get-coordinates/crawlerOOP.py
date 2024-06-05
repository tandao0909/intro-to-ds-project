import os
import re
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time
from selenium.webdriver.remote.webdriver import WebDriver


os.environ['PATH'] += r"/usr/local/bin/"
driver = webdriver.Firefox()
driver.maximize_window()

class Crawler:
    def __init__(self,driver:WebDriver,url,n_page : int):
        self.driver = driver
        self.url = url
        self.n_page = n_page
        self.report = pd.DataFrame(columns=['Title', 'Price', 'Links',\
            'Diện tích (m2)', 'Số phòng ngủ','Số phòng WC', 'Địa chỉ'\
            ,'Description'])
    
    def get_params(self,text):
        reg_template = {"Area":'Diện tích:\s*(\d+)',
                "Room":'Phòng ngủ:\s*(\d+)',
                "WC":'Phòng WC:\s*(\d+)',
                "Location":'Địa chỉ:\s*(.+)'}
        list_params = []
        for i,name in enumerate(reg_template):
            x = re.search(r'{}'.format(reg_template[name]),text)
            if x:
                list_params.append(x.group(1))
            else:
                list_params.append(np.nan)
        return list_params
    
    def crawl(self):
        page = self.n_page
        for i in range(page):
            url = self.url + "p{}".format(i+1)
            self.driver.get(url)
            self.driver.implicitly_wait(1)
            try:
                elements = self.driver.find_elements('css selector'\
                    ,'.uk-width-medium-7-10 .name [href]')
                elements_price = self.driver.find_elements('css selector',\
                    '.price')
            except:
                continue
            
            title = [element.text for element in elements]
            
            links = [element.get_attribute('href') for element in elements]
            
            price = [element.text for element in elements_price]
            
            df1 = pd.DataFrame(zip(title,price,links),columns=['Title','Price','Links']) 

            data = []
            
            n = len(df1) #number of links
            
            for j in range(n):
                try:
                    self.driver.get(links[j])
                    params = self.driver.find_element('css selector','.param')
                    content = self.driver.find_element('css selector','.content')
                except:
                    df1.drop(j,axis=0,inplace=True)
                    continue
                params_ = self.get_params(params.text)
                params_.append(content.text)
                data.append(params_)
                
            tmp = np.vstack([item for item in data])
            
            df2 = pd.DataFrame(tmp,columns=['Diện tích (m2)','Số phòng ngủ','Số phòng WC','Địa chỉ', "Description"])
            df1 = pd.concat([df1,df2],axis=1)
            
            self.report = pd.concat([self.report,df1],axis=0)
            self.report.set_index(np.arange(len(self.report)),inplace=True)
            self.report.to_csv('next_turn.csv',sep="\t",index=False)
            
            
crawler = Crawler(driver=driver,url='https://batdongsan.vn/ban-nha/',n_page=1)
crawler.crawl()
crawler.report

    