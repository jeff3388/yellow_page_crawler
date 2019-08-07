# Chrome瀏覽器 selenium 作法
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import requests
import time
import re
import csv

# 解析工商登記廠商資料
def parse_web(driver):
    datetime_dt = datetime.datetime.today()# 獲得當地時間
    datetime_str = datetime_dt.strftime("%Y-%m-%d")  # 格式化日期

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find("table",attrs={"class","table table-striped"})
    t = table.find_all("td")
    content = [i.text.strip().replace("\t","").replace("\n","").replace("\xa0","") for i in t]
    content = "".join(content)

#     # 統一編號
#     uniform_numbers = (content.split("統一編號")[1]).split("公司狀況")[0]
#     company_name = (content.split("公司名稱")[1]).split("Google搜尋")[0]

#     try:
#         principal = (content.split("代表人姓名")[1]).split("公司所在地")[0]
#     except:
#         try:
#             principal = (content.split("在中華民國境內負責人")[1]).split("分公司所在地")[0]
#         except:
#             principal = (content.split("在中華民國境內代表人")[1]).split("辦事處所在地")[0]

#     try:
#         address = (content.split("公司所在地")[1]).split("電子地圖")[0]
#     except:
#         address = (content.split("辦事處所在地")[1]).split("電子地圖")[0]


#     c1 = content.find("核准設立日期")
#     if c1 != -1:
#         registration_authority =  (content.split("登記機關")[1]).split("核准設立日期")[0]
#     else:
#         registration_authority =  (content.split("登記機關")[1]).split("核准登記日期")[0]

#     try:
#         setting_date = (content.split("核准設立日期")[1]).split("最後核准變更日期")[0]
#     except:
#         setting_date = (content.split("核准登記日期")[1]).split("最後核准變更日期")[0]

#     try:
#         c2 = content.find("實收資本額(元)")
#         if c2 != -1:
#             capital_amount = (content.split("資本總額(元)")[1]).split("實收資本額(元)")[0]
#         else:
#             capital_amount = 'Na'
            
#         c2 = content.find("代表人姓名")
#         if c2 != -1:
#             capital_amount = (content.split("資本總額(元)")[1]).split("代表人姓名")[0]
#         else:
#             capital_amount = 'Na'
#     except:
#         try:
#             capital_amount = (content.split("在中華民國境內營運資金")[1]).split("在中華民國境內負責人")[0]
#         except:
#             pass

#     if company_name == '':
#         company_name = 'Na'

#     if principal == '':
#         principal ='Na'

#     if uniform_numbers == '':
#         uniform_numbers ='Na'

#     if address == '':
#         address ='Na'

#     if registration_authority == '':
#         registration_authority ='Na'

#     if setting_date == '':
#         setting_date ='Na'

#     company_infor = dict([
#                        ('company_name', company_name),
#                        ('principal', principal),
#                        ('phone', 'Na'),
#                        ('uniform_numbers', str(uniform_numbers)),
#                        ('address', address),
#                        ('city', 'Na'),
#                        ('registration_authority', registration_authority),
#                        ('setting_date', setting_date),
#                        ('change_date', 'Na'),
#                        ('capital_amount', str(capital_amount)),
#                        ('kind', 'Na'),
#                        ('datetime_str', datetime_str),
#                       ])
    
#     # 二維表格
#     csvtable = [
#         [company_infor['company_name'], 
#          company_infor['principal'], 
#          company_infor['phone'], 
#          company_infor['uniform_numbers'], 
#          company_infor['address'], 
#          company_infor['city'], 
#          company_infor['registration_authority'], 
#          company_infor['setting_date'],
#          company_infor['change_date'],
#          company_infor['capital_amount'],
#          company_infor['kind'],
#          company_infor['datetime_str'],
#         ]
#     ]

        # 二維表格
    csvtable = [[content + "," + datetime_str]]
    
    with open('findbiz.csv', 'a', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csvtable)
        
    # return company_infor

############################## main program ####################################
def main(city_name):
    
    options = webdriver.ChromeOptions()
    #關閉瀏覽器跳出訊息
    prefs = {
        'profile.default_content_setting_values' :
            {
            'notifications' : 2
             }
    }
    options.add_experimental_option('prefs',prefs) # 關閉瀏覽器跳出訊息
    options.add_argument("--incognito")           #開啟無痕模式
    options.add_argument("--disable-notifications") # 取消網頁允許跳出訊息警告
    options.add_argument("--disable-infobars") # 取消 "Chrome 目前受到自動測試軟體控制" 警語

    # # 也可使用以下這種寫法
    # options.add_argument("--incognito","--start-maximized","--headless")
    path = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path = path ,options = options)
    driver.get("https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do")
    driver.find_element_by_css_selector("#infoAddr").click()
    driver.find_element_by_css_selector("#isAliveY").click()


    driver.find_element_by_css_selector("#qryCond").send_keys(city_name)
    driver.find_element_by_css_selector("#qryCond").send_keys(Keys.ENTER)

    # 解析頁面
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title_class = soup.find_all("div",attrs={"class","panel panel-default"})
    number = len(title_class) + 1

    while True:
        try:
            for q in range(3,12):
                for n in range(1 , number):
                    driver.find_element_by_css_selector("#vParagraph > div:nth-child(" + str(n) + ") > div.panel-heading.companyName > a").click()
                    time.sleep(4)
                    parse_web(driver)

                    driver.back() # 回上一頁
                    time.sleep(4)


                driver.find_element_by_css_selector("#QueryList_queryList > div > div > div > div > nav > ul > li:nth-child("+ str(q) +") > a").click()
                time.sleep(3)
            driver.find_element_by_css_selector("#QueryList_queryList > div > div > div > div > nav > ul > li:nth-child(12) > a").click() # next page

        except Exception as e:
            print(e)
            break
            
    
city_name = '新北市'
main(city_name)