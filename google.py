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


# In[2]:


browser = webdriver.Chrome()
browser.get('https://www.google.com.tw/maps/@25.0173405,121.5397518,17z?hl=zh-TW') 


# In[136]:


df1 = pd.read_excel("filiter_location_all.xlsx")
df1


# In[179]:


comment_df = pd.DataFrame(columns = ['location','lo_star','comment','cm_star'])
google_df = pd.DataFrame(columns = ['lo_id','location','open_time','address','maps_url'])
comment_df = pd.DataFrame(columns = ['location','lo_star','comment','cm_star'])
tel_df = pd.DataFrame(columns = ['lo_id', 'tel'])
open_times = {}


# In[195]:


p = 0
for p in range(72,81):

    place_input = browser.find_elements(by=By.ID, value='searchboxinput')[0]
    search_click = browser.find_element(by=By.ID, value='searchbox-searchbutton')
    
    place_input.send_keys(df1['location'][p])
    time.sleep(2)
    search_click.click()
    time.sleep(3)

    #-------------------------複製網址-------------------------                 
    try:
        try:
            time.sleep(3)
            browser.find_elements(by=By.CLASS_NAME, value='hfpxzc')[0].click()
            
            time.sleep(2)
            share_b = browser.find_elements(by=By.CLASS_NAME, value='S9kvJb')[8]
            time.sleep(2)
            share_b.click()
            time.sleep(2)
            url = browser.find_element(by=By.CLASS_NAME, value='vrsrZe').get_attribute('value')
            close_b = browser.find_element(by=By.CLASS_NAME, value='AmPKde')
            time.sleep(2)
            close_b.click()
        
        except:        
            time.sleep(2)
            share_b = browser.find_elements(by=By.CLASS_NAME, value='S9kvJb')[8]
            time.sleep(2)
            share_b.click()
            time.sleep(2)
            url = browser.find_element(by=By.CLASS_NAME, value='vrsrZe').get_attribute('value')
            close_b = browser.find_element(by=By.CLASS_NAME, value='AmPKde')
            time.sleep(2)
            close_b.click()
    
    #-------------------------電話.營業時間.地址、加入df-------------------------
        time.sleep(2)
        place_number = browser.find_elements(by=By.CSS_SELECTOR, value='.Io6YTe')
        address = browser.find_elements(by=By.CSS_SELECTOR, value='.rogA2c')[0].text
        time.sleep(3)
        
        try:
            browser.find_element(by=By.CLASS_NAME, value='ZDu9vd').click()
            time.sleep(3)
                    
            x=0
            for x in range(7):
                opentime = browser.find_elements(by=By.CLASS_NAME, value='mWUh3d')[x].get_attribute('data-value')
                google_df = google_df.append({
                    'lo_id' : 'L' + str(p+1),
                    'location' : df1['location'][p],
                    'open_time' : opentime,
                    'address' : address,
                    'maps_url' : url,
                }, ignore_index=True)
           
                x+=1
        except:
            google_df = google_df.append({
                'lo_id' : 'L' + str(p+1),
                'location' : df1['location'][p],
                'open_time' : 'NO',
                'address' : address,
                'maps_url' : url,
            }, ignore_index=True)
            
        for a in range(len(place_number)):
            if place_number[a].text.startswith('02'):
                tel_df = tel_df.append({
                    'lo_id' : 'L' + str(p+1),
                    'tel' : place_number[a].text,
                }, ignore_index=True)
            elif place_number[a].text.startswith('09'):
                tel_df = tel_df.append({
                    'lo_id' : 'L' + str(p+1),
                    'tel' : place_number[a].text,
                }, ignore_index=True)
            else:
                continue
                    
            a+=1
        
        time.sleep(4)
    
    #-------------------------評論加入df-------------------------
        
        all_comment = browser.find_element(by=By.CLASS_NAME, value='DkEaL')
        all_comment.click()
        time.sleep(3)
    
        a=0
        for a in range(2):
            pane = browser.find_element(by=By.CLASS_NAME, value='m6QErb.DxyBCb.kA9KIf.dS8AEf')
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
            time.sleep(3)
            a+=1

        lo_star = browser.find_element(by=By.CLASS_NAME, value='fontDisplayLarge')
        time.sleep(3)
            
        c=0
        for c in range(20):
        
            comment = browser.find_elements(by=By.CLASS_NAME, value='wiI7pd')
            cm_star = browser.find_elements(by=By.CLASS_NAME, value='kvMYJc')
            
            try:
                each = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div[' +  str((1+3*c)) + ']/div/div[3]/div[4]/jsl/button'
                whole_content_bt = browser.find_elements_by_xpath(each)
                whole_content_bt[0].click()
                time.sleep(3)
                
                comment_df = comment_df.append({
                    'location' : df1['location'][p],
                    'lo_star' : lo_star.text,
                    'comment' : comment[c].text,
                    'cm_star' : cm_star[c].get_attribute('aria-label')
                } , ignore_index=True)
        
                time.sleep(3)
            
            except:
                comment_df = comment_df.append({
                    'location' : df1['location'][p],
                    'lo_star' : lo_star.text,
                    'comment' : comment[c].text,
                    'cm_star' : cm_star[c].get_attribute('aria-label')
                } , ignore_index=True)
                
                time.sleep(3)
                                    
        
            c+=1
    
        back_to_first_page = browser.find_element(by=By.CLASS_NAME, value='VfPpkd-icon-LgbsSe.yHy1rc.eT1oJ.mN1ivc')    
        back_to_first_page.click()
        time.sleep(3)
    
    
    
    
    except:
        google_df = google_df.append({
            'lo_id' : 'L' + str(p+1),
            'location' : df1[p],
            'open_time' : 'except',
            'address' : 'except',
            'maps_url' : 'except',
        }, ignore_index=True)
        tel_df = tel_df.append({
            'lo_id' : 'L' + str(p+1),
            'tel' : 'except',
        }, ignore_index=True)
        comment_df = comment_df.append({
            'location' : 'except',
            'lo_star' : 'except',
            'comment' : 'except',
            'cm_star' : 'except'
        } , ignore_index=True)
    
    
    browser.find_element(by=By.CLASS_NAME, value='gsst_a').click()

    p += 1


# In[196]:


google_df


# In[197]:


tel_df


# In[226]:


comment_df


# In[216]:


time_df = google_df.groupby(by=['lo_id']).agg({'open_time': ' '.join})
info_df = google_df.drop('open_time',axis=1)
g_df = pd.merge(info_df, time_df, how='outer', on='lo_id').drop_duplicates()
f_df = pd.merge(g_df, tel_df, how='outer', on='lo_id')
f_df


# In[224]:


f_df.to_excel('google0911.xlsx')
comment_df.to_excel('comment0911.xlsx')


# In[ ]:





# In[ ]:


# lo = pd.read_excel('google0911.xlsx').drop('Unnamed: 0',axis=1)
# lo


# In[217]:


lo = f_df
lo


# In[ ]:





# In[219]:


for i in range(len(lo)):
    s = lo['address'][i]
    f = s.find('台北市')
    
    if f == -1:
        lo['address'][i] = ' '
    else:
        lo['address'][i] = lo['address'][i]


# In[233]:


loct_df = lo[lo.address != ' ']
loct_df.reset_index(inplace=True)


# In[235]:


loct_df = loct_df.drop('index',axis=1)
loct_df


# In[ ]:





# In[245]:


lo_id_df = loct_df[['lo_id','location']]
f_comment_df = pd.merge(lo_id_df, comment_df, how='inner', on='location')
f_comment_df


# In[ ]:





# In[248]:


f_comment_df.drop_duplicates()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[247]:


loct_df.to_excel('taipei_filter_location.xlsx')
f_comment_df.to_excel('taipei_filter_comment.xlsx')


# In[20]:


a = pd.read_excel('taipei_filter_location.xlsx').drop('Unnamed: 0',axis=1)
b = pd.read_excel('taipei_filter_comment.xlsx').drop('Unnamed: 0',axis=1)


# In[33]:


a.to_csv('taipei_filter_location.csv')
b.to_csv('taipei_filter_comment.csv')


# In[22]:


a['district'] = a['address']


# In[28]:


for f in range(len(a)):
    a['district'][f] = a['district'][f][6:9]


# In[31]:


a = a[['lo_id','location','address','district','maps_url','open_time','tel']]


# In[4]:


import pandas as pd

df = pd.read_excel('taipei_filter_location.xlsx')[['lo_id','location']]
df


# In[6]:


for i in range(65):
    print(df['location'][i])
    print(len(df['location'][i]))


# In[10]:


for i in range(65):
    if (len(df['location'][i])) > 10:
           print(df['location'][i])


# In[82]:


import re
len(re.findall(en, df['location'][20]))
# print(str(re.findall(en, df['location'][20])[0]) + str(re.findall(en, df['location'][20])[1]))


# In[67]:


for i in range(65):
    if (len(name[i])) > 10:
        print(name[i])


# In[70]:


import re
zh = '[\u4e00-\u9fa5]+'
en = '[\u0041-\u005a|\u0061-\u007a]+'
name = df['location']

for i in range(65):
    if (len(name[i])) > 10:
        if name[i][0].isupper() == True:
            print(str(re.findall(en, name[i])[0:]).replace('[','').replace(']','').replace(',',''))
            print()
        elif re.match(zh, name[i]) != None:
            print(str(re.findall(zh, name[i])[0:]).replace('[','').replace(']','').replace(',',''))
    else:
        pass


# In[ ]:





# In[ ]:




