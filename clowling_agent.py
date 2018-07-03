# -*- coding: utf-8 -*-
import unittest
import re
import logging
import requests
import json
import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
from bs4 import BeautifulSoup

class MakeList(unittest.TestCase):

    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=%s'
    dialog_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/dialog/syz?pref=%s'
    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川'}
    # url_json = 'url.json'
    url_json = 'sample.json'
    agent_csv = 'agent.csv'
    city_cnt_limit = 5
    iframe_id = 'fancybox-frame'

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        # self.driver.implicitly_wait(5)
        # self.driver = webdriver.Chrome('./chromedriver-Windows')
        self.logging = logging.getLogger('LoggingTest')
        self.logging.setLevel(10)
        fh = logging.FileHandler(self.agent_csv, delay=True, encoding='utf-8')
#        formatter = logging.Formatter('%(asctime)s - '
#                              '%(levelname)s - '
#                              '%(filename)s:%(lineno)d - '
#                              '%(funcName)s - '
#                              '%(message)s')
#        fh.setFormatter(formatter)
        self.logging.addHandler(fh)

    def test_make_list(self):
        driver = self.driver
        with open(self.url_json, "r") as f:
            url_json = json.load(f)
            for url in url_json:
                # dialog_elem = driver.get( self.base_url % url['id'] )
                time.sleep(3)
                city_cnt = 0 # 最大５つまでチェック（市区町村）
                for city in url['city']:
                    dialog_elem = driver.get( self.base_url % url['id'] )
                    city_cnt += 1
                    iframe = driver.find_element_by_id('fancybox-frame')
                    driver.switch_to_frame(iframe)
                    print(city["id"])
                    driver.find_element_by_id(city['id']).click() # 市区町村をclick
                    next_page = 1
                    if ( city_cnt % self.city_cnt_limit != 0 ):
                        continue
                    else:
                        driver.find_element_by_css_selector('body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE').click() # 検索btnをクリック
                        # driver.switch_to.default_content()
                        elem = driver.get(driver.current_url) # 区の表者一覧ページを取得
                        time.sleep(5)
                        driver.find_element_by_id('all_check').click()
                        driver.save_screenshot('./aaa.png')

                        # elem = driver.find_element_by_id('listArea')
                        # self.logging.info()
                        # req = requests.get(driver.current_url) # 業者一覧
                        soup = BeautifulSoup(driver.page_source, "lxml")
                        listArea = soup.select('#listArea')
                        # div > a.button.button-rounded.PIE:nth-child(1) # linkBtn
                        # print(soup.find('span'))
                        # for i in soup.find_all("table"): # 全inputをリストへ格納


                        break
                    time.sleep(3)

    def tearDown(self):
#        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
