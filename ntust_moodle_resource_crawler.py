#from selenium import webdriver as wd
#from selenium.webdriver.common.keys import Keys
from time import time
import pandas as pd
from modules.ex_AutoLogin_NTUST_Moodle import auto_login_moodle #, get_new_driver
from modules.file_helper import save_json, load_json

def get_moodle_resources():
    with open("./res/link.txt") as fp:
        link = fp.readline().strip()
    if link is None or link == "":
        print("[WARNING] link is unavailable!")
    else:
        # auto login NTUST Moodle
        driver = auto_login_moodle()
        
        # redirect to the link
        driver.get(link)
        
        # get instance names
        except_list = ["公佈欄", "討論區"]
        xpath = "//span[@class='instancename']"
        
        resources = dict()
        res_titles = [e.text for e in driver.find_elements_by_xpath(xpath)]
        #for res_title in res_titles:
            #print(res_title)
        for i, res_title in enumerate(res_titles): 
            resources.setdefault(i, dict())
            resources[i]["title"] = res_title
            if any((except_list[0] in res_title,\
                    except_list[1] in res_title)):
                resources[i]["flag"] = False
            else:
                resources[i]["flag"] = True
        
        '''
        # print out `resources` for test
        print("resources:")
        for k, v in resources.items():
            print(f'({k}) {v["title"]} \nis-available: {v["flag"]}')
        #print(len(resources)) # 93
        '''
        
        # get links of instance names
        xpath = "//span[@class='instancename']/.."
        res_links = [e.get_attribute("href") for e in driver.find_elements_by_xpath(xpath)]
        #print(len(res_links)) # 93 <-- 說明 link 數量 和 資源標題總數 是相等的 (=> 可用索引對應)
        for i, res_info in resources.items():
            if res_info["flag"]:
                resources[i]["link-tier1"] = res_links[i]
            else:
                resources[i]["link-tier1"] = "unknown"
        '''
        # print out `resources` for test
        print("resources:")
        for k, v in resources.items():
            print(f'({k}) {v["title"]} \nis-available: {v["flag"]} \nlink-tier1: {v["link-tier1"]}')
        #print(len(resources)) # 93
        '''
        
        '''
        [result]
        (91) 2020 期中考解答 
        is-available: True 
        link-tier1: https://moodle.ntust.edu.tw/mod/resource/view.php?id=354292
        (92) 期中考注意事項（4/13 發放） 
        is-available: True 
        link-tier1: https://moodle.ntust.edu.tw/mod/resource/view.php?id=354295
        '''
        driver.quit()
        return resources

def get_json_filepath_tier_i(i):
    return f"./res/resoueces_tier{i}.txt"

def get_csv_filepath(i):
    return f"./res/resoueces_tier{i}.csv"

# =============================================================================
# 1. 自動登入Moodle，並獲取所有資源(含「Moodle 內嵌連結」)，
#    並以 txt 暫時保存 json 格式資料。
#    [註] Moodle 內嵌連結需登入才可用
# =============================================================================
def exec_get_res_and_save_json():
    t0 = time()
    print("execute: `exec_get_res_and_save_json`")
    # [config] Setting path to place json file
    json_filepath = get_json_filepath_tier_i(1)
    resources = get_moodle_resources()
    save_json(resources, json_filepath)
    print("execute func: `exec_get_res_and_save_json`")
    print(f"time consumed: {time()-t0} seconds")

# =============================================================================
# 2. 載入所有資源(含 Moodle 內嵌連結)，
#    並獲取外部連結(不須登入 Moodle 即可訪問)，
#    並以 txt 暫時保存 json 格式資料。
# =============================================================================
def exec_load_json_and_get_vid_links():
    t0 = time()
    print("execute: `exec_load_json_and_get_vid_links`")
    # [config] Setting path to place json file
    json_filepath = get_json_filepath_tier_i(2)
    
    # auto login NTUST Moodle
    driver = auto_login_moodle()
    resources = load_json(get_json_filepath_tier_i(1))
    #print(resources)
    keyword = "影音連結"
    #limit = 0
    for i, res_info in resources.items():
        if res_info["flag"] and keyword in res_info["title"]:
            # visit `link-tier1`
            res_link = res_info["link-tier1"]
            print(f'影音資源: {res_info["title"]}')
            print(f"正在造訪資源連結: {res_link}")
            driver.get(res_link)
            
            # switch to frame
            driver.switch_to.frame(0)
            xpath = "//div[@class='ytp-title-text']/a"
            vid_link = driver.find_element_by_xpath(xpath).get_attribute("href")
            print(f"vid_link: {vid_link}")
            #print(f"length of vid_link: {len(vid_link)}")
            resources[i]["link-tier2"] = vid_link
            print()
        else:
            resources[i]["link-tier2"] = "unknown"
    save_json(resources, json_filepath)
    print(f"time consumed: {time()-t0} seconds")
    '''
    time consumed: 43.725194692611694 seconds
    '''
# =============================================================================
# 3. 載入所有資源(含暫存的外部連結)，
#    另存為 csv 檔案。
# =============================================================================
def save_as_csv(dict_):
    df = pd.DataFrame(dict_)
    df.to_csv(get_csv_filepath(2), index=False, encoding="utf-8-sig")
    
def exec_load_video_res():
    t0 = time()
    yt_course_playlist = {"編號": list(),\
                          "影音資源": list(),\
                          "影音連結": list()}
    print("execute: `exec_load_video_resources`")
    resources = load_json(get_json_filepath_tier_i(2))
    keyword = "影音連結"
    counter = 1
    for i, res_info in resources.items(): 
        if res_info["flag"] and keyword in res_info["title"]:
            vid_title = res_info["title"]
            #print(f'影音資源: {vid_title}')
            vid_link = res_info["link-tier2"]
            #print(f'影音連結: \n{vid_link}')
            yt_course_playlist["編號"].append(counter)
            yt_course_playlist["影音資源"].append(vid_title)
            yt_course_playlist["影音連結"].append(vid_link)
            counter += 1
    save_as_csv(yt_course_playlist)
    print(f"yt_course_playlist: {yt_course_playlist}")
    print(f"time consumed: {time()-t0} seconds")
    '''
    time consumed: 0.028620004653930664 seconds
    '''

if __name__ == "__main__":
    #exec_get_res_and_save_json()
    #exec_load_json_and_get_vid_links()
    exec_load_video_res()