# This script will answer the academic morality questionnaire automatically.
# 1. Please check all packages installed.
# 2. Drivers can be downloaded from Third Party Drivers, Bindings, and Plugins
#    of https://www.seleniumhq.org/download/
#    This script uses Google Chrome Driver

import os, time
import getpass
import selenium
import numpy as np
import pandas as pd
# import pytesseract
from bs4 import BeautifulSoup
from selenium import webdriver

file = 'data.csv'
web = 'http://ystu.nuist.edu.cn/login.aspx'
driver_path = '/usr/bin/chromedriver'

class FORM(object):
    def __init__(self, web, file):
        self.web = web
        self.file = file

    def read(self):
        # read data
        df = pd.read_csv(self.file, delimiter = ',', dtype = {"A" : "str"})        

        # read paras
        driver = webdriver.Chrome(driver_path)
        driver.get(self.web)
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
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass

        self.driver = driver
        self.data = df

    def ans(self):
        # switch to frame
        self.driver.switch_to.frame('r_3_3')
        # pass to beautifulsoup
        html = self.driver.page_source
        soup = BeautifulSoup(html, features='lxml')

        # A -> 0, B -> 1, C -> 2, D -> 3
        order = {'A':0,'B':1,'C':2,'D':3}
        for q_index in np.arange(0,50,1):
            id = 'Mydatalist__ctl0_Mydatalist1__ctl{}_tm'.format(q_index)
            q = soup.find("span", id = lambda s: s and s == id).get_text().strip(' ')
            n = order[self.data[self.data.Q == q].drop_duplicates(subset='A', keep='first')['A'].to_string(index = False).strip(' ')]
            id_click = "Mydatalist__ctl0_Mydatalist1__ctl{}_xz_{}".format(q_index, n)
            self.driver.find_element_by_id(id_click).click()

        # submit
        submit_button = self.driver.find_element_by_name('tjck').click()

    def close(self):
        state = input("Do you get 100? (y/n) ")
        if state.lower() == 'y':
            self.driver.quit()
        else:
            print ('Answer the rest questions by your own :)')
            time.sleep(1e3)

def main():
    form = FORM(web, file)
    form.read()
    form.ans()
    form.close()

if __name__ == '__main__':
    main()

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