from bs4 import BeautifulSoup
import numpy as np
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

area_ls =[
      '%E8%87%BA%E5%8C%97%E5%B8%82', # 台北
      '%E6%96%B0%E5%8C%97%E5%B8%82', # 新北
      '%E8%87%BA%E4%B8%AD%E5%B8%82', # 台中
      '%E6%A1%83%E5%9C%92%E5%B8%82', # 桃園
      '%E9%AB%98%E9%9B%84%E5%B8%82', # 高雄
      '%E8%87%BA%E5%8D%97%E5%B8%82', # 台南
      '%E6%96%B0%E7%AB%B9%E7%B8%A3', # 新竹縣
      '%E6%96%B0%E7%AB%B9%E5%B8%82', # 新竹市
      '%E5%BD%B0%E5%8C%96%E7%B8%A3', # 彰化
      '%E5%8D%97%E6%8A%95%E7%B8%A3', # 南投
      '%E5%B1%8F%E6%9D%B1%E7%B8%A3', # 屏東
      '%E8%8B%97%E6%A0%97%E7%B8%A3', # 苗栗
      '%E5%AE%9C%E8%98%AD%E7%B8%A3', # 宜蘭
      '%E9%9B%B2%E6%9E%97%E7%B8%A3', # 雲林
      '%E5%98%89%E7%BE%A9%E5%B8%82', # 嘉義市
      '%E5%98%89%E7%BE%A9%E7%B8%A3', # 嘉義縣
      '%E5%9F%BA%E9%9A%86%E5%B8%82', # 基隆市
      '%E8%8A%B1%E8%93%AE%E7%B8%A3', # 花蓮
      '%E8%87%BA%E6%9D%B1%E7%B8%A3', # 台東
      '%E6%BE%8E%E6%B9%96%E7%B8%A3', # 澎湖
      '%E9%87%91%E9%96%80%E7%B8%A3', # 金門
      '%E9%80%A3%E6%B1%9F%E7%B8%A3', # 連江
      ]
    
    
for area in area_ls:
    for p in range(1,250):
        try:
            t = random.randint(5,7)
            time.sleep(t)
            url = 'https://opengovtw.com/ban?q='+ area +'&page='+ str(p)
            res = requests.get(url=url,headers=headers,timeout=15).content
            soup = BeautifulSoup(res, 'html.parser') 
            soup.encoding

            tbody = soup.find_all('table',attrs={'class','table table-striped table-hover table-condensed'})
            string = soup.find_all('div',attrs={'class','panel-body'})

             ### 判斷是否為空的頁面 ###
            s = [s.text.find("Your search did not match any entities.") for s in string]
            c = [c for c in s if c != -1]
            ########################

            url_ls = []

            if c == []:
                for i in tbody:
                    i = i.find_all('a')
                    for u in i:
                        u = u.get('href')
                        url_ls += [u]

                num_ls = list(np.unique(url_ls)) # num_ls 排序不變

                limit = 1
                urls_ls = [num_ls[i:i + limit] for i in range(0, len(num_ls), limit)]

                with open('opengovtw_url.csv', 'a', newline='',encoding = 'utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(urls_ls)

            else:
                break
        except Exception as e:
            print(e)