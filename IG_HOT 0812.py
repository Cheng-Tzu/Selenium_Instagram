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


# In[2]:


browser = webdriver.Chrome()

# ------ #台北美食 ------
frist_url = 'https://www.instagram.com/explore/tags/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F/'

browser.get(frist_url) 


# In[3]:


time.sleep(2)
browser.find_elements(by=By.CLASS_NAME, value='_acan._acap._acas')[0].click()
time.sleep(2)

# ------ 填入帳號與密碼 ------
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
username_input = browser.find_elements(by=By.NAME, value='username')[0]
password_input = browser.find_elements(by=By.NAME, value='password')[0]
print("inputing username and password...")

time.sleep(3)
username_input.send_keys('scu08170000')
print('username finish')
time.sleep(2)
password_input.send_keys('08170000')
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

browser.get(frist_url) 


# In[4]:


# ------ 抓貼文網址 ------
post_url = []
i=0
for i in range(10):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    soup = Soup(browser.page_source,"lxml")

    for elem in soup.select('article div div div div a'):
        if elem['href'] not in post_url:
            post_url.append(elem['href'])
    time.sleep(5) 
    
    i+=1


# In[5]:


# ------ 存貼文網址 ------
url_df = pd.DataFrame(columns = ['date','url']) 
webs = []
for url_p in post_url:
    url_np = 'https://www.instagram.com' + url_p
    webs.append(url_np)


# In[6]:


# wurl = pd.DataFrame(columns = ['url']) 
# wurl['url'] = webs
# wurl.to_excel('C:/Users/Jessie_Cheng/畢專/eachday_url/0815.xlsx')


# In[6]:


content_df = pd.DataFrame(columns = ['a_id']) 
ht_df = pd.DataFrame(columns = ['a_id'])
like_df = pd.DataFrame(columns = ['a_id'])
pic_df = pd.DataFrame(columns = ['a_id'])

# ----------------------------------------------(post_start)----------------------------------------
try:
    x = 0
    for x in range(10):
        url = webs[x] 
        browser.get(url)
    
        # 找到貼文的網頁元素(class)
        time.sleep(3)
        post_user = browser.find_element(by=By.CLASS_NAME, value="oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl._acan._acao._acat._acaw._a6hd")
        post_content_element = browser.find_element(by=By.CLASS_NAME, value="_aacl._aaco._aacu._aacx._aad7._aade")
        post_hashtag = browser.find_elements(by=By.CLASS_NAME, value="oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl._aa9_._a6hd")

    
# ----------------------------------------------(content_df)----------------------------------------
        try:
            post_location = browser.find_element(by=By.CLASS_NAME, value="oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl._aaqk._a6hd")
            content_df = content_df.append({
                'a_id' : str(x+1),
                'u_id' : post_user.text,
                'location' : post_location.text,
                'content' : post_content_element.text,
                'url' : url,
                'createddatetime' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            } , ignore_index=True)
        except:
            content_df = content_df.append({
                'a_id' : str(x+1),
                'u_id' : post_user.text,
                'location' : 'None',
                'content' : post_content_element.text,
                'url' : url,
                'createddatetime' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            } , ignore_index=True)
        
# ----------------------------------------------(ht_df)----------------------------------------
        for t in range(len(post_hashtag)):
            ht_df = ht_df.append({
                'a_id' : str(x+1),
                'hashtag' : post_hashtag[t].text,
                'sum_of_hashtag' : 1
            } , ignore_index=True)

# ----------------------------------------------(pic_df)----------------------------------------
        z = 0
        for z in range(10):
            # 找到下一頁按鈕
            but = browser.find_elements(by=By.CLASS_NAME, value='_aahi')
            if but == []:
                time.sleep(5)
                soup = Soup(browser.page_source,"lxml")
                post_img = soup.find_all(class_="_aagt")
                p_url = (post_img[0].get('src'))
                pic_df = pic_df.append({
                    'a_id' : x+1,
                    'u_id' : post_user.text,
                    'pic' : p_url
                } , ignore_index=True)
    
            else:
                button = browser.find_elements(by=By.CLASS_NAME, value='_aahi')[0]
                if button == None:
                    if post_img == None:
                        break
                    else:
                        soup = Soup(browser.page_source,"lxml")
                        post_img = soup.find_all(class_="_aagt")
                        p_url = post_img[0].get('src')
                        pic_df = pic_df.append({
                            'a_id' : x+1,
                            'u_id' : post_user.text,
                            'pic' : p_url,
                        } , ignore_index=True)
                else:
                    # 點擊下一頁按鈕
                    button.click()
                    soup = Soup(browser.page_source,"lxml")
                    time.sleep(2)
                    post_img = soup.find_all(class_="_aagt")
                    p_url = post_img[0].get('src')
                    pic_df = pic_df.append({
                        'a_id' : x+1,
                        'u_id' : post_user.text,
                        'pic' : p_url,
                    } , ignore_index=True)
            z ++ 1

        time.sleep(5)
        post_img = soup.find_all(class_="_aagt")
        p_url = post_img[1].get('src')
        pic_df = pic_df.append({
            'a_id' : x+1,
            'u_id' : post_user.text,
            'pic' : p_url,
        } , ignore_index=True)
# ----------------------------------------------(like_df)----------------------------------------
        time.sleep(5)
        try:
            post_likes = browser.find_element(by=By.CLASS_NAME, value='_aacl._aaco._aacw._aacx._aada._aade')
            post_likes = post_likes.text.split(' ')[0]    
            if post_likes == '其他人':
                browser.get(url + 'liked_by/')
                for lk in range(20):
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(2)
                num_like = browser.find_elements(by=By.CLASS_NAME, value='_ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9-._aba8')
                nlike = len(num_like)
                time.sleep(2)
                browser.get(url)
                time.sleep(2)
                post_content_element = browser.find_element(by=By.CLASS_NAME, value="_aacl._aaco._aacu._aacx._aad7._aade")
                like_df = like_df.append({
                    'a_id' : str(x+1),
                    'sum_of_like' : nlike
                } , ignore_index=True)
            else:
                num_like = int(post_likes)
                like_df = like_df.append({
                    'a_id' : str(x+1),
                    'sum_of_like' : num_like
                } , ignore_index=True)
        except:
            pass

    
# ----------------------------------------------(finish)----------------------------------------

        time.sleep(2)    
        x ++ 1
    
    print('Post Finish')
    
except:
    print('Post Not Finish')
    pass


# In[17]:


content_df


# In[18]:


ht_df


# In[19]:


ht_sum_df = ht_df.groupby('a_id').sum()
ht_sum_df


# In[20]:


like_df


# In[21]:


pic_df['date'] = datetime.date.today().strftime("%Y-%m-%d")
pic_df.reset_index(inplace=True)
pic_df = pic_df.drop('index',axis=1)
pic_df


# ## export CSV

# In[22]:


article_df = pd.merge(content_df,ht_sum_df, on='a_id')
article_df = pd.merge(article_df,like_df, on='a_id')
article_df['a_id'] = article_df['a_id'].astype(int)
article_df = article_df[['a_id','u_id','content','url','sum_of_like','sum_of_hashtag','createddatetime']]
article_df


# In[23]:


hashtag_df = ht_df.drop('sum_of_hashtag',axis=1)
hashtag_df['a_id'] = hashtag_df['a_id'].astype(int)
hashtag_df


# In[24]:


pic_df


# In[15]:


# date = datetime.date.today().strftime("%Y-%m-%d").replace('-','')[4:]
# article_df.to_csv('article'+ date +'.csv')
# hashtag_df.to_csv('hashtag'+ date +'.csv')
# pic_df.to_csv('pic'+ date +'.csv')


# ## download pic

# In[16]:


# i=0
# for i in range(44):
#     urllib.request.urlretrieve(pic_df['pic'][i], pic_df['u_id'][i] + '_' + pic_df['date'][i] + '_' + str(i) + '.jpg')
#     print("download successful")
#     time.sleep(2)
#     i+=1


# In[ ]:





# In[ ]:



d=0
for d in range(2):


time.sleep(5)





d+=1    


# In[ ]:





# In[ ]:





# In[ ]:




