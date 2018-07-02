# -*- coding: utf-8 -*-
import unittest
import re
import logging
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
from bs4 import BeautifulSoup

class MakeList(unittest.TestCase):

    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=13'
    dialog_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/dialog/syz?pref='
    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川'}
    pref_json = 'pref.json'

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        # self.driver = webdriver.Chrome('./chromedriver-Windows')
        self.logging = logging.getLogger('LoggingTest')
        self.logging.setLevel(10)
        fh = logging.FileHandler(self.pref_json, delay=True, encoding='utf-8')
#        formatter = logging.Formatter('%(asctime)s - '
#                              '%(levelname)s - '
#                              '%(filename)s:%(lineno)d - '
#                              '%(funcName)s - '
#                              '%(message)s')
#        fh.setFormatter(formatter)
        self.logging.addHandler(fh)

    def test_make_list(self):
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
#                self.logging.info(i.find('label').string)
#                self.logging.info(json.dumps(city))
#            self.logging.info(json.dumps(city)) 
#            pref_json[][id] = pref
#            pref_json[][name] = self.pref_list[pref]
#            pref_json[][city] = city
            pref_list_json.append(pref_json)
        self.logging.info(json.dumps(pref_list_json))

    def my_log(data):
        self.logging.info(data)

    def tearDown(self):
        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
