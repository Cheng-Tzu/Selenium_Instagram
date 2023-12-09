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

# 回到指定網頁(#台北美食)
browser.get(frist_url) 

# 抓貼文網址(格式為：'/p/.........../') 
## 設定空List 使用迴圈將資料append進去 並輔以滑動頁面增加爬取到的貼文
## range設定10是因為大約在9~11左右就會出現博弈、詐騙類混淆貼文
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
    
# 輸出正確可讀的網址
webs = []
for url_p in post_url:
    url_np = 'https://www.instagram.com' + url_p
    webs.append(url_np)

# ---------------------------------------------------------------------------------------------------------

# 開始爬取貼文

## 定義四個DataFrame 貼文、標籤、讚數、圖片 並為每篇文章編號(a_id)
content_df = pd.DataFrame(columns = ['a_id']) 
ht_df = pd.DataFrame(columns = ['a_id'])
like_df = pd.DataFrame(columns = ['a_id'])
pic_df = pd.DataFrame(columns = ['a_id'])

# 使用try except語法 避免網頁出錯(非code error)導致運行中斷 
try:
    x = 0
    # range(10)只處理10篇文 可依照所擁有的網址數量做調整
    for x in range(10):
        
        url = webs[x] 
        browser.get(url)
    
        # 找到貼文的網頁元素(class)
        time.sleep(3)
        post_user = browser.find_element(by=By.CLASS_NAME, value="_ap3a._aaco._aacw._aacx._aad7._aade")
        post_content_element = browser.find_element(by=By.CLASS_NAME, value="x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.xt0psk2.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj")
        post_hashtag = browser.find_elements(by=By.CLASS_NAME, value="x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._aa9_._a6hd")

    
# ----------------------------------------------(content_df)----------------------------------------
# 貼文df包含 文章編號、發文者ID、標註店家[有就抓(try) 沒有就補"None"(except)]、內文全文、網址、爬取時間(可有可無)
        try:
            post_location = browser.find_element(by=By.CLASS_NAME, value="x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd")
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
# 標籤df包含 文章編號、標籤、給予int格式的1(後續會使用)
        for t in range(len(post_hashtag)):
            ht_df = ht_df.append({
                'a_id' : str(x+1),
                'hashtag' : post_hashtag[t].text,
                'sum_of_hashtag' : 1
            } , ignore_index=True)

# ----------------------------------------------(pic_df)----------------------------------------
# 照片df包含 文章編號、發文帳號、照片網址
        z = 0
        for z in range(10):
            
            # 找到下一頁按鈕
            but = browser.find_elements(by=By.CLASS_NAME, value='_9zm2')

            # 若沒有下一頁按鈕 直接儲存首張圖片的網址
            if but == []:
                time.sleep(5)
                soup = Soup(browser.page_source,"lxml")
                post_img = soup.find_all(class_="_aagv")[0]
                tag = post_img.find('img')
                p_url = tag.get('src')
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
                        post_img = soup.find_all(class_="_aagv")[0]
                        tag = post_img.find('img')
                        p_url = tag.get('src')
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
                    post_img = soup.find_all(class_="_aagv")[0]
                    tag = post_img.find('img')
                    p_url = tag.get('src')
                    pic_df = pic_df.append({
                        'a_id' : x+1,
                        'u_id' : post_user.text,
                        'pic' : p_url,
                    } , ignore_index=True)
            z ++ 1

        # 由於有出現下一頁按鈕會不斷翻頁 為避免最後一張照片沒有爬取到 需要再補一次code 後續資料處理可刪除重複行
        time.sleep(5)
        post_img = soup.find_all(class_="_aagv")
        tag = post_img[0].find('img')
        pic_df = pic_df.append({
            'a_id' : x+1,
            'u_id' : post_user.text,
            'pic' : p_url,
        } , ignore_index=True)
# ----------------------------------------------(like_df)----------------------------------------
# 讚數df包含 文章編號、讚數(部分貼文不會顯示總讚數 改為進入按讚名單頁面滑動網頁後以帳號數量作為讚數儲存)
        time.sleep(5)
        try:
            post_likes = browser.find_elements(by=By.CLASS_NAME, value='x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.xt0psk2.x1i0vuye.xvs91rp.x1s688f.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')
            if len(post_likes) == 1':
                browser.get(url + 'liked_by/')
                for lk in range(20):
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(2)
                num_like = browser.find_elements(by=By.CLASS_NAME, value='x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3')
                nlike = len(num_like)
                time.sleep(2)
                browser.get(url)
                time.sleep(2)
                like_df = like_df.append({
                    'a_id' : str(x+1),
                    'sum_of_like' : nlike
                } , ignore_index=True)
            else:
                num_like = post_likes[0].text.replace('個讚','')
                like_df = like_df.append({
                    'a_id' : str(x+1),
                    'sum_of_like' : num_like
                } , ignore_index=True)
        except:
            pass

    
# ----------------------------------------------(finish)----------------------------------------

        time.sleep(2)    
        x ++ 1

    # 上方code完成後顯示"Post Finish"
    print('Post Finish')
    
except:
    # 若一開始就失敗則會顯示"Post Not Finish"
    print('Post Not Finish')
    pass

# ---------------------------------------------------------------------------------------------------------

# 處理標籤 > 使用groupby以文章標籤為主 計算標籤數量 
ht_sum_df = ht_df.groupby('a_id').sum()
ht_sum_df

# 處理照片 > 將含時分秒的日期時間格式改為純日期格式 > 使用drop_duplicates刪除重複欄位
pic_df['date'] = datetime.date.today().strftime("%Y-%m-%d")
pic_df = pic_df.drop_duplicates()
pic_df.reset_index(inplace=True)
pic_df = pic_df.drop('index',axis=1)
pic_df


# 合併貼文、標籤數、讚數三個列數相同的dataframe並輸出(含中文檔案還是建議輸出excel檔 csv配上encoding有時還是會有亂碼出現)
article_df = pd.merge(content_df,ht_sum_df, on='a_id')
article_df = pd.merge(article_df,like_df, on='a_id')
article_df['a_id'] = article_df['a_id'].astype(int)
article_df = article_df[['a_id','u_id','content','url','sum_of_like','sum_of_hashtag','createddatetime']]
article_df.to_excel('IG_main_df.xlsx')

# 輸出照片dataframe
pic_df.to_csv('IG_pic_url.csv')
