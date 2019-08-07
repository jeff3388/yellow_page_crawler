# 格式規範
#  company_infor['company_name'], 
#  company_infor['principal'], 
#  company_infor['phone'], 
#  company_infor['uniform_numbers'], 
#  company_infor['address'], 
#  company_infor['city'], 
#  company_infor['registration_authority'], 
#  company_infor['setting_date'],
#  company_infor['change_date'],
#  company_infor['capital_amount'],
#  company_infor['kind'],
#  company_infor['datetime_str']

from bs4 import BeautifulSoup
import numpy as np
import datetime
import requests
import random
import time
import csv

headers ={
    'Content-Type': 'text/html; charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Host': 'opengovtw.com',
    'Referer': 'https://opengovtw.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

# url_ls = []

# with open("opengovtw.csv","r",encoding="utf-8") as opengovtw_csv:
#     rows = csv.reader(opengovtw_csv)
#     for row in rows:
#         url_ls += [row]

url = "https://opengovtw.com/ban/82910702"
res = requests.get(url=url,headers=headers,timeout=15).content
soup = BeautifulSoup(res, 'html.parser') 
soup.encoding

t = soup.find_all("table",attrs={"class":"table table-striped table-hover table-dl"})
i = [i.text.strip() for i in t]
j = [j.replace("\n","").replace("\xa0\xa0","") for j in i][0].split("\t\t")

limit = 2 # 每組人數
result = [j[k:k + limit] for k in range(0, len(j), limit)]
q = [tuple(q) for q in result]
conpany_dict = dict(q)

company_name = conpany_dict["公司名稱"]
principal = conpany_dict["代表人姓名"]
address = conpany_dict["公司所在地"]
registration_authority = conpany_dict["登記機關"]
capital_amount = conpany_dict["資本總額(元)"]
uniform_numbers = conpany_dict["統一編號"]

datetime_dt = datetime.datetime.today()# 獲得當地時間
datetime_str = datetime_dt.strftime("%Y-%m-%d")  # 格式化日期

company_infor = dict([
                       ('company_name', company_name),
                       ('principal', principal),
                       ('phone', 'Na'),
                       ('uniform_numbers', str(uniform_numbers)),
                       ('address', address),
                       ('city', 'Na'),
                       ('registration_authority', registration_authority),
                       ('setting_date', 'Na'),
                       ('change_date', 'Na'),
                       ('capital_amount', str(capital_amount)),
                       ('kind', 'Na'),
                       ('datetime_str', datetime_str),
                      ])

# 二維表格
csvtable = [
    [company_infor['company_name'], 
     company_infor['principal'], 
     company_infor['phone'], 
     company_infor['uniform_numbers'], 
     company_infor['address'], 
     company_infor['city'], 
     company_infor['registration_authority'], 
     company_infor['setting_date'],
     company_infor['change_date'],
     company_infor['capital_amount'],
     company_infor['kind'],
     company_infor['datetime_str'],
    ]
]

with open('opengovtw_content.csv', 'a', newline='',encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csvtable)