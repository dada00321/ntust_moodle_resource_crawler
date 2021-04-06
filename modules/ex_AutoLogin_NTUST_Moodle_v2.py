"""
自動登入台科Moodle網頁
"""
from selenium import webdriver as wd
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def auto_login_moodle():
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	wd_path = r"D:\geckodriver\chromedriver.exe"
    
	driver = wd.Chrome(wd_path, options=chrome_options)
	#driver = wd.Chrome(wd_path)
	driver.implicitly_wait(10)
	url = "https://moodle.ntust.edu.tw/"
	driver.get(url)

	txtbox_User = driver.find_element_by_name("username")
	txtbox_User.send_keys("account/student-ID")
	time.sleep(0.2)

	txtbox_Pass = driver.find_element_by_name("password")
	txtbox_Pass.send_keys("password")
	time.sleep(0.2)

	#btnLogin = driver.find_element_by_xpath("//*[@id=\"login\"]/div[4]/input")
	btnLogin = driver.find_element_by_xpath(r"//div[@class='c1 btn']/input")
	time.sleep(1)
	btnLogin.click()
	return driver

'''
def get_new_driver():
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	wd_path = r"D:\geckodriver\chromedriver.exe"
	driver = wd.Chrome(wd_path, options=chrome_options)
	return driver
'''