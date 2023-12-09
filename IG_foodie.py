#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[155]:


fddf = pd.read_excel('foodie.xlsx')
fddf['sum'] =1


# In[ ]:





# In[165]:


fddf = fddf.groupby('NAME').sum()
a = fddf['sum'] >= 4
fddf = fddf[a].sort_values(by='sum', ascending=False)
fddf.reset_index(inplace=True)


# In[166]:


fddf


# In[158]:


web=[]
for i in range(len(fddf)):
    fd_nurl = 'https://www.instagram.com/' + fddf['NAME'][i]
    web.append(fd_nurl)
    print(fd_nurl)


# In[ ]:





# In[5]:


browser = webdriver.Chrome()

# ------ #台北美食 ------
frist_url = 'https://www.instagram.com/explore/tags/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F/'

browser.get(frist_url) 


# In[6]:


time.sleep(2)
browser.find_elements(by=By.CLASS_NAME, value='_acan._acap._acas')[0].click()
time.sleep(2)

# ------ 填入帳號與密碼 ------
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
username_input = browser.find_elements(by=By.NAME, value='username')[0]
password_input = browser.find_elements(by=By.NAME, value='password')[0]
print("inputing username and password...")

time.sleep(3)
username_input.send_keys('instagram.scu.2022@gmail.com')
print('username finish')
time.sleep(2)
password_input.send_keys('08170001')
print('password finish')

# ------ 登入 ------
login_click = browser.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[3]/button/div')
time.sleep(3)
login_click.click()
print('login now')

# ------ 不儲存登入資料 ------
time.sleep(5)
store_click = browser.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/main/div/div/div/div/button')
store_click.click()

print("success!")


# In[162]:


web_df = pd.DataFrame(columns = ['name'])


# In[163]:


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
        
    name = browser.find_element(by=By.CLASS_NAME, value='_aacl._aacs._aact._aacx._aada')
    
    time.sleep(2)
    for url_p in post_url:
        url_np = 'https://www.instagram.com' + url_p
        web_df = web_df.append({
            'name' : name.text,
            'url' : url_np
        } , ignore_index=True)
        
    time.sleep(2)
    t+=1


# In[164]:


web_df


# In[180]:


web_df.to_csv('foodie3409.csv')


# In[ ]:





# In[117]:


# ------ 存貼文網址 ------


# In[179]:


web_df.drop((3157:3200),axis=1)


# In[42]:


len(post_url)


# In[ ]:





# In[ ]:





# In[51]:


href_df = pd.DataFrame(columns = ['id'])


# In[52]:


href_df['']


# In[89]:


name = browser.find_element(by=By.CLASS_NAME, value='_aacl._aacs._aact._aacx._aada')
name.text


# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[76]:


href_df = pd.DataFrame()
for a in range(1):
    browser.get(web[1])
    time.sleep(3)
    
    for i in range(20):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
        time.sleep(3)
        for link in browser.find_elements_by_css_selector(".qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq._a6hd"):
            href = link.get_attribute('href')
            if href.startswith('https://www.instagram.com/p/'):
                href_df.append({
                    'url' : href,
                } , ignore_index=True)
            else:
                href_df.append({
                    'url' : '',
                } , ignore_index=True)
    
#     a+=1


# In[77]:


href_df


# In[93]:


aa = pd.DataFrame()
aa['url'] = h
aa.drop_duplicates()


# In[73]:


# u = browser.find_element(by=By.CLASS_NAME, value='qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq._a6hd')
u = browser.find_elements_by_css_selector(".qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq._a6hd")


# In[72]:


u.get_attribute('href')


# In[75]:


for i in range(len(u)):
    print(u[i].get_attribute('href'))


# In[ ]:




