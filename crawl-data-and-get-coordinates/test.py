from crawler import Crawler
import os
from selenium import webdriver

os.environ['PATH'] += r"/usr/local/bin/" # Path to driver
driver = webdriver.Firefox() 
driver.maximize_window()

crawler = Crawler(driver=driver,url='https://batdongsan.vn/ban-nha/',n_page=1)
crawler.crawl()
crawler.report.to_csv('crawl-data-and-get-coordinates/output.csv',sep='\t',index=False)
