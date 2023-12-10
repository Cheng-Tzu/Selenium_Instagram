# 套用所需要的套件
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
import pandas as pd
import time

# 載入webdrive 並進入目標網址(GoogleMaps)
browser = webdriver.Chrome()
browser.get('https://www.google.com.tw/maps/@25.0173405,121.5397518,17z?hl=zh-TW') 


# 載入依照食記及標籤所蒐集到有關的資料 並給予每一個文章對應的餐廳一個1值 便於計算數量
foodie = pd.read_excel('foodie.xlsx')['location']
hashtag = pd.read_excel('hashtag.xlsx')['location']
foodie['num'] = 1
hashtag['num'] = 1

# 合併兩個DataFrame 並使用groupby計算餐廳出現次數
loca_df = pd.concat([foodie,hashtag],axis=0)
sum_df = loca_df.groupby('location').sum()

# 選出符合標準的餐廳(認定出現三次以上便是可以推薦的餐廳)
filter = sum_df['num'] >= 3
location_df = sum_df[filter].sort_values(by='num', ascending=False)

# ---------------------------------------------------------------------------------------------------------

# 定義三個DataFrame 評論、一般資歷、連絡電話 
comment_df = pd.DataFrame(columns = ['location','lo_star','comment','cm_star'])
google_df = pd.DataFrame(columns = ['lo_id','location','open_time','address','maps_url'])
tel_df = pd.DataFrame(columns = ['lo_id', 'tel'])

# 
p = 0
for p in range(len(location_df)):

    # 定位搜尋框及搜索鍵 並將餐廳依序代入
    place_input = browser.find_elements(by=By.ID, value='searchboxinput')[0]
    search_click = browser.find_element(by=By.ID, value='searchbox-searchbutton')
    
    place_input.send_keys(location_df['location'][p])
    time.sleep(2)
    search_click.click()
    time.sleep(3)

    #-------------------------複製網址-------------------------                 
    try:
        try:
            # 有時會出現相似餐廳名稱的選項 默認選擇第一項           
            browser.find_elements(by=By.CLASS_NAME, value='hfpxzc')[0].click()        
        except:    
            pass

        # 點擊分享彈出小視窗 複製網址後關閉小視窗
        time.sleep(2)
        share_b = browser.find_elements(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[4]/div[5]/button')
        time.sleep(2)
        share_b.click()
        time.sleep(2)
        
        url = browser.find_element(by=By.CLASS_NAME, value='vrsrZe').get_attribute('value')
        close_b = browser.find_element(by=By.CLASS_NAME, value='AmPKde')
        time.sleep(2)
        close_b.click()
    
    #-------------------------電話.營業時間.地址、加入df-------------------------
        time.sleep(2)

        # 定位包含電話、地址的部分
        place_number = browser.find_elements(by=By.CLASS_NAME, value='Io6YTe')
        address = browser.find_elements(by=By.CLASS_NAME, value='Io6YTe')[0].text
        
        time.sleep(3)

        # 若有營業時間 將下拉式選單展開並依照一周七天儲存營業時間 若無 則將營業時間代入"NO"
        try:
            browser.find_element(by=By.CLASS_NAME, value='ZDu9vd').click()
            time.sleep(3)
                    
            x=0
            for x in range(7):
                opentime = browser.find_elements(by=By.CLASS_NAME, value='mWUh3d')[x].get_attribute('data-value')
                google_df = google_df.append({
                    'lo_id' : 'L' + str(p+1),
                    'location' : location_df['location'][p],
                    'open_time' : opentime,
                    'address' : address,
                    'maps_url' : url,
                }, ignore_index=True)
           
                x+=1
        except:
            google_df = google_df.append({
                'lo_id' : 'L' + str(p+1),
                'location' : location_df['location'][p],
                'open_time' : 'NO',
                'address' : address,
                'maps_url' : url,
            }, ignore_index=True)

        # 前項定位電話時是將該CLASSNAME全部暫存 (因為每個餐廳的基本資料數量有差異 唯一相同就是第一項為地址)
        # 使用迴圈及startwith將電話開頭為02或09的篩選出來
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

        # 跳轉至評論分頁
        all_comment = browser.find_elements(by=By.CLASS_NAME, value='Gpq6kf')[1]
        all_comment.click()
        time.sleep(3)

        # 依照所需評論數量去修改a的range
        a=0
        for a in range(5):
            pane = browser.find_element(by=By.CLASS_NAME, value='m6QErb.DxyBCb.kA9KIf.dS8AEf')
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
            time.sleep(3)
            a+=1

        # 取得店家總評分
        lo_star = browser.find_element(by=By.CLASS_NAME, value='fontDisplayLarge')
        time.sleep(3)

        # 定位評論內文、評論對應的星等、「全文」鍵
        comment = browser.find_elements(by=By.CLASS_NAME, value='wiI7pd')
        cm_star = browser.find_elements(by=By.CLASS_NAME, value='kvMYJc')
        whole = browser.find_elements(by=By.CLASS_NAME, value='w8nwRe.kyuRq')

        # 設定需要的貼文數量 以20為範例 有全文鍵就打開後抓資料 無就直接抓資料
        c=0
        for c in range(len(20):
                    
            try:
                whole[c].click()
                time.sleep(3)

                comment_df = comment_df.append({
                    'lo_id' : 'L' + str(p+1),
                    'location' : location_df['location'][p],
                    'lo_star' : lo_star.text,
                    'comment' : comment[c].text,
                    'cm_star' : cm_star[c].get_attribute('aria-label')
                } , ignore_index=True)
                
                time.sleep(3)
            
            except:
                comment_df = comment_df.append({
                    'lo_id' : 'L' + str(p+1),
                    'location' : location_df['location'][p],
                    'lo_star' : lo_star.text,
                    'comment' : comment[c].text,
                    'cm_star' : cm_star[c].get_attribute('aria-label')
                } , ignore_index=True)
                
                time.sleep(3)
                                    
        
            c+=1

        # 回到首頁
        back_to_first_page = browser.find_element(by=By.CLASS_NAME, value='VfPpkd-icon-LgbsSe.yHy1rc.eT1oJ.mN1ivc')    
        back_to_first_page.click()
        time.sleep(3)
    
    # 若Google沒資料 則除了餐廳名稱、編號外都代入"None"    
    except:
        google_df = google_df.append({
            'lo_id' : 'L' + str(p+1),
            'location' : location_df[p],
            'open_time' : 'None',
            'address' : 'None',
            'maps_url' : 'None',
        }, ignore_index=True)
        tel_df = tel_df.append({
            'lo_id' : 'L' + str(p+1),
            'tel' : 'None',
        }, ignore_index=True)
        comment_df = comment_df.append({
            'lo_id' : 'L' + str(p+1),
            'location' : 'None',
            'lo_star' : 'None',
            'comment' : 'None',
            'cm_star' : 'None'
        } , ignore_index=True)
    
    # 清空搜尋欄
    browser.find_element(by=By.CLASS_NAME, value='lSDxNd').click()

    p += 1

# ---------------------------------------------------------------------------------------------------------

# 處理營業時間 使用gruopby.agg合併文字 後將原先欄位刪除 並去重
time_df = google_df.groupby(by=['lo_id']).agg({'open_time': ' '.join})
info_df = google_df.drop('open_time',axis=1)

# 用find()將非台北市的地址篩掉
for i in range(len(info_df)):
    str = info_df['address'][i]
    find_str = str.find('台北市')
    
    if find_str == -1:
        info_df['address'][i] = ' '
    else:
        info_df['address'][i] = info_df['address'][i]

info_df = info_df[info_df.address != ' ']
info_df.reset_index().drop('index',axis=1)

# 合併除了評論外的DataFrame
final_df = pd.merge(info_df, time_df, how='outer', on='lo_id').drop_duplicates()
final_df = pd.merge(final_df, tel_df, how='outer', on='lo_id')

# 輸出餐廳資料、評論dataframe
final_df.to_excel('googlemaps_info.xlsx')
comment_df.to_excel('googlemaps_comt.xlsx')



