# This script will crawl the academic morality questionnaire automatically.
# 1. Please check all packages installed.
# 2. Drivers can be downloaded from Third Party Drivers, Bindings, and Plugins
#    of https://www.seleniumhq.org/download/
#    This script uses Google Chrome Driver

import os, re
import selenium
import getpass
import numpy as np
import pandas as pd
# import pytesseract
from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import compress

web = 'http://ystu.nuist.edu.cn/login.aspx'
driver_path = '/usr/bin/chromedriver'

class FORM(object):
    def __init__(self, web):
        self.web = web

    def login(self):
        # login and read form
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
        alert = driver.switch_to.alert
        alert.accept()
        # switch to frame
        driver.switch_to.frame('r_3_3')

        self.driver = driver

    def iterate(self):
        # iterate A, B, C and D as default option
        n_indexs = np.arange(0,4,1)
        n_times = np.arange(0,11,1)

        for n_index in n_indexs:
            # 0: A; 1: B; 2: C; 3: D
            # 10 times for each option
            for n_time in n_times:
                for q_index in np.arange(0,50,1):
                    id = 'Mydatalist__ctl0_Mydatalist1__ctl{}_xz_{}'.format(q_index, n_index)
                    self.driver.find_element_by_id(id).click()
                # submit
                submit_button = self.driver.find_element_by_name('tjck').click()

                # check answers and filter
                alert = self.driver.switch_to.alert
                alert.accept()

                # pass to beautifulsoup
                html = self.driver.page_source
                soup = BeautifulSoup(html, features='lxml')

                # get questions
                pattern = re.compile('Mydatalist__ctl0_Mydatalist1__ctl*')
                questions = soup.find_all("span", id = lambda s: s and s.startswith('Mydatalist__ctl0_Mydatalist1__ctl') and s.endswith('_tm'))

                # check whether the default answer of question is false
                valid_list = []
                for q in questions:
                    tmp = []
                    # iterate A, B, C and D to check if it's false
                    for c_index in np.arange(0,4,1):
                        choice = q.attrs['id'].replace('tm','xz_' + str(c_index))
                        tmp.append(soup.find("label", {'for': choice}).span)
                    valid_list.append(any(tmp))
                
                # drop spaces
                questions = [q.get_text().strip(' ') for q in questions]
                # only store red questions and answers
                questions = list(compress(questions, valid_list))

                # find red texts which are correct answer
                spans = soup.find_all("span", {'style':'background-color:red;color:white'})
                ans = [span.get_text()[0] for span in spans]

                # save them to pandas and run again
                if n_index == 0 and n_time == 0:
                    data = pd.DataFrame(np.column_stack([questions, ans]), 
                                           columns=['Q', 'A'])
                else:
                    tmp_frame = pd.DataFrame(np.column_stack([questions, ans]), 
                                           columns=['Q', 'A'])
                    data = pd.concat([data, tmp_frame])
                    # Don't know why drop_duplicates doesn't work???????
                    data.drop_duplicates(subset='Q', keep='first')

                print ('The shape of data: ', data.shape)

                # try again
                submit_button = self.driver.find_element_by_name('tjck').click()

        self.data = data

    def save(self):
        data.to_csv('data.csv', sep=',', encoding='utf-8')

def main():
    form = FORM(web)
    form.login()
    form.iterate()
    form.save()

if __name__ == '__main__':
    main()

################################################
# This part is written for getting vcode automatically,
# but it doesn't work well.

# set the size of window
# driver.set_window_size(1200, 800)

# # screenshot
# screenshot_path = '/home/xin/Desktop/screenshot.png'
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
# captcha_path = '/home/xin/Desktop/captcha.png'
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


