from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
drive=webdriver.Chrome(executable_path='chromedriver')
drive.maximize_window()
drive.get('http://192.168.11.81:8080/woniusales/')
time.sleep(3)
acc1=drive.find_element_by_id('username')
passwd1=drive.find_element(By.ID,'password')
verifycode1=drive.find_element_by_id("verifycode")
login1=drive.find_elements(By.CLASS_NAME,'btn-primary')
acc1.clear()
acc1.send_keys('admin')
passwd1.send_keys('123456')
verifycode1.send_keys('0000')
drive.find_elements(By.CLASS_NAME,'btn-primary')[1].click()
time.sleep(3)
drive.find_element_by_link_text('批次管理').click()
drive.get_screenshot_as_file('C:\\Users\树先生\Desktop\python\dada.png')
time.sleep(2)
a=drive.find_element_by_id('batchfile')
a.send_keys('D:\python test\\agdad\hjhj.png')
drive.find_element_by_xpath('/html/body/div[4]/div[1]/form[2]/div/input[1]').click()
time.sleep(2)
drive.find_element_by_xpath('/html/body/div[7]/div/div/div[3]/button').click()
drive.quit()





