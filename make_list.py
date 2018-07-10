# -*- coding: utf-8 -*-
import unittest
import re
import sys
import logging
import requests
import json
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

class MakeList(unittest.TestCase):

    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=%s'
    dialog_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/dialog/syz?pref='
    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川'}
    pref_json = 'pref.json'
    default_log = 'test.log'
    city_max  = 5
    search_btn_css = 'body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE'
    next_a = '#container > div.main.right > div:nth-child(2) > div:nth-child(2) > div > ol > li.next > a'

    def setUp(self):
        self.driver = webdriver.Remote(
           command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
#        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

    def setup_logger(self,filepath):
        if filepath is None:
            filepath = self.default_log
        self.logging = logging.getLogger('LoggingTest')
        self.logging.setLevel(10)
        fh = logging.FileHandler(filepath, delay=True, encoding='utf-8')
#        formatter = logging.Formatter('%(asctime)s - '
#                              '%(levelname)s - '
#                              '%(filename)s:%(lineno)d - '
#                              '%(funcName)s - '
#                              '%(message)s')
#        fh.setFormatter(formatter)
        self.logging.addHandler(fh)

    def test_make_list(self):
        print('start make pref.json')
        self.setup_logger(None)
        driver = self.driver
        driver.get(self.base_url) # 最初、のページを開く
        pref_list_json = []
        for pref in self.pref_list.keys():
            pref_json = {}
            pref_json['id'] = pref
            pref_json['name'] = self.pref_list[pref]
            pref_json['city'] = []
            req = requests.get(self.dialog_url + pref) # 各dialogのページを開く
            soup = BeautifulSoup(req.text, "lxml")
            for i in soup.find_all("dt"): # 全inputをリストへ格納
                # jsonデータ準備
                city = {}
                city['id'] = i.find("input").get('id')
                city['value'] = i.find("input").get('value')
                city['name']  = re.sub( r'\(|\)|[0-9]+','', i.find('label').string)
                city['count']  = re.sub(r'\D', '', i.find('label').string)
                pref_json['city'].append(city)
            pref_list_json.append(pref_json)
        self.logging.info(json.dumps(pref_list_json))

    def test_scrape_fax(self):
        print('start scrape fax')
        driver = self.driver
        self.setup_logger(None)
        driver = self.driver
        with open(self.pref_json, "r") as f:
            pref_json = json.load(f)
            for url in pref_json:
#                print( self.base_url % url['id'] )
                driver.get( self.base_url % url['id'] )
                time.sleep(2)
                city_cnt = 0 # 最大５つまでチェック（市区町村）
#                print( "pref:%s, city length:%s" % (url['id'] , len(url['city'])))
                city_list = []
                city_idx = 0
                for city in url['city']:

                    driver.get( self.base_url % url['id'] )
                    if len(city_list) == self.city_max:
                        print("click")
                        self.click_city(city_list)
#                        driver.find_element_by_css_selector(self.search_btn_css).click() # 検索btnをクリック
#                        time.sleep(2)
                        driver.save_screenshot('./screenshots/%s_%s.png' % (url['id'], city_idx) )
                        city_list = []
                    else:
                        print("append:" + city['id'])
                        city_list.append(city['id'])

                    city_idx += 1
                if len(city_list) > 0:
                        print("click")
                        self.click_city(city_list)
#                        driver.find_element_by_css_selector(self.search_btn_css).click() # 検索btnをクリック
#                        time.sleep(2)
                        driver.save_screenshot('./screenshots/%s_%s.png' % (url['id'], city_idx) )
                        city_list = []


        pass

    def click_city(self, city_list):
        print(city_list)
        driver = self.driver
        driver.save_screenshot('./screenshots/aaa_.png')
        iframe = driver.find_element_by_css_selector('#fancybox-frame')
        driver.switch_to_frame(iframe)
        for c in city_list:
            driver.find_element_by_id(c).click() # 市区町村をclick

        driver.find_element_by_css_selector(self.search_btn_css).click() # 検索btnをクリック
        time.sleep(1)
        Select(driver.find_element_by_css_selector('select.displayCount')).select_by_value('50')
        time.sleep(1)
        self.is_next_a()
        driver.switch_to_default_content()

    def is_next_a(self):
        print("check_next_a")
        driver = self.driver
        driver.switch_to_default_content()
        soup = BeautifulSoup(driver.page_source, "lxml")
        #next_tag = soup.select(self.next_a)
        next_tag = soup.select('li.next > a')
        print(next_tag)
        pass


    def tearDown(self):
#        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
