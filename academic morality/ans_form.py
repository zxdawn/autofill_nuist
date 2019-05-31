import os
import getpass
import selenium
import numpy as np
import pandas as pd
import pytesseract
from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import compress

# read data
df = pd.read_csv('data.csv', delimiter = ',', dtype = {"A" : "str"})

# read paras
driver = webdriver.Chrome()
driver.get('http://ystu.nuist.edu.cn/login.aspx')
username = input("Input your ID: ")
password = getpass.getpass("Input your password: ")
vcode = input("Input the vcode on the screen: ")

# Send username
id_box = driver.find_element_by_name('userbh').send_keys(username)
# Send password
pass_box = driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
# Send vcode
pass_box = driver.find_element_by_name('vcode').send_keys(vcode)
# Click login button
login_button = driver.find_element_by_name('save2').click()
# load form
driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr/td[2]/table[2]/tbody/tr/td/div/span[1]/a[9]').click()
driver.find_element_by_xpath('//*[@id="my_menu"]/div/a').click()
# in case you have completed the form once
alert = driver.switch_to.alert
alert.accept()

# switch to frame
driver.switch_to.frame('r_3_3')
# pass to beautifulsoup
html = driver.page_source
soup = BeautifulSoup(html, features='lxml')

# A -> 0, B -> 1, C -> 2, D -> 3
order = {'A':0,'B':1,'C':2,'D':3}
for q_index in np.arange(0,50,1):
    id = 'Mydatalist__ctl0_Mydatalist1__ctl{}_tm'.format(q_index)
    q = soup.find("span", id = lambda s: s and s == id).get_text().strip(' ')
    n = order[df[df.Q == q].drop_duplicates(subset='A', keep='first')['A'].to_string(index = False).strip(' ')]
    id_click = "Mydatalist__ctl0_Mydatalist1__ctl{}_xz_{}".format(q_index, n)
    driver.find_element_by_id(id_click).click()
# submit
submit_button = driver.find_element_by_name('tjck').click()

################################################
# This part is written for getting vcode automatically,
# but it doesn't work well.

# set the size of window
# driver.set_window_size(1200, 800)

# # screenshot
# screenshot_path = 'screenshot.png'
# if os.path.exists(screenshot_path):
#     os.remove(screenshot_path)
# driver.save_screenshot(screenshot_path)

# # find element of captcha and get location
# element = driver.find_element_by_id('Image2')
# left = int(element.location['x'])
# top = int(element.location['y'])
# right = int(element.location['x'] + element.size['width'])
# bottom = int(element.location['y'] + element.size['height'])
# # crop captcha
# captcha_path = 'captcha.png'
# if os.path.exists(captcha_path):
#     os.remove(captcha_path)
# img = Image.open(screenshot_path)
# img = img.crop((left, top, right, bottom))
# img.save(captcha_path)

# # distinguish captcha
# image = Image.open(captcha_path)
# vcode = pytesseract.image_to_string(image)

# print (vcode)
################################################