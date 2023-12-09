# 套用所需要的套件
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
import pandas as pd
import time
import urllib.request
import datetime

# ---------------------------------------------------------------------------------------------------------

# 在此之前先使用多部(測試使用5部)手機在Instagram搜尋"台北食記" 並將前15個與foodie有關的帳號名稱列出來
# 使用groupby計算每個帳號出現次數 大於等於4的帳號留下
foodie_df = pd.read_excel('foodie.xlsx')
foodie_df['sum'] =1
fddf = fddf.groupby('NAME').sum()
a = fddf['sum'] >= 4
fddf = fddf[a].sort_values(by='sum', ascending=False)
fddf.reset_index()

# 將帳號名稱與Instagram前網址合併 產出list
web=[]
for i in range(len(fddf)):
    fd_nurl = 'https://www.instagram.com/' + fddf['NAME'][i]
    web.append(fd_nurl)
    print(fd_nurl)

# 載入webdrive
browser = webdriver.Chrome()

# 設定並進入目標網址(#台北美食)
frist_url = 'https://www.instagram.com/explore/tags/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F/'
browser.get(frist_url) 

time.sleep(2)
browser.find_elements(by=By.CLASS_NAME, value='_acan._acap._acas')[0].click()
time.sleep(2)

# 定位帳號、密碼框(開始前必須等到webdriver抓到帳號框的定位 以防網速不足出現error)
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
username_input = browser.find_elements(by=By.NAME, value='username')[0]
password_input = browser.find_elements(by=By.NAME, value='password')[0]
print("inputing username and password...")

# 輸入帳號密碼 需停頓 躲避防爬蟲機制+避免網速過慢出現error
time.sleep(3)
username_input.send_keys('XXXXXXXX')
print('username finish')
time.sleep(2)
password_input.send_keys('YYYYYYYY')
print('password finish')

# 登入
login_click = browser.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[3]/button/div')
time.sleep(3)
login_click.click()
print('login now')

# 選擇不儲存登入資料(稍後再說)
time.sleep(5)
store_click = browser.find_element(by=By.CLASS_NAME, value='_ac8f')
store_click.click()
print("success!")

# 取得每個foodie帳號下數百篇文章的網址 並輸出成csv
web_df = pd.DataFrame(columns = ['u_id'])
t=0
for t in range(len(web)):
    browser.get(web[t]) 
    time.sleep(3)
    
    post_url = []
    i=0
    for i in range(30):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        soup = Soup(browser.page_source,"lxml")

        for elem in soup.select('article div div div div a'):
            if elem['href'] not in post_url:
                post_url.append(elem['href'])
        time.sleep(2) 
    
        i+=1
        
    post_user = browser.find_element(by=By.CLASS_NAME, value="_ap3a._aaco._aacw._aacx._aad7._aade")
    
    time.sleep(2)
    for url_p in post_url:
        url_np = 'https://www.instagram.com' + url_p
        web_df = web_df.append({
            'name' : post_user.text,
            'url' : url_np
        } , ignore_index=True)
        
    time.sleep(2)
    t+=1

web_df.to_csv('foodie3409.csv')


# 後續可依照IG_byhashtag.py中「爬取貼文」的部分操作
