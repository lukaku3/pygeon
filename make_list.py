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

class MakeList(unittest.TestCase):

#    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=13'
    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=%s'
    dialog_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/dialog/syz?pref='
    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川'}
    pref_json = 'pref.json'
    default_log = 'test.log'
    city_max  = 5

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
#                print(url['id'])
                time.sleep(2)
                city_cnt = 0 # 最大５つまでチェック（市区町村）
#                print( "pref:%s, city length:%s" % (url['id'] , len(url['city'])))
                city_list = []
                for city in url['city']:
#                    if len(city_list) == self.city_max:
#                        self.click_city(city_list)
#                        city_list = []
#                    else:
#                        city_list.append(city['id'])

                    dialog_elem = driver.get( self.base_url % url['id'] )
                    time.sleep(1)
                    city_cnt += 1
                    driver.save_screenshot('./aaa.png')
                    iframe = driver.find_element_by_id('fancybox-frame')
                    driver.switch_to.frame(iframe)
                    driver.find_element_by_id(city['id']).click() # 市区町村をclick
                    next_page = 1
                    if ( city_cnt % self.city_cnt_limit != 0 ):
                        continue
                    elif( city_cnt == len(url['city'])):
                        pass
                    else:
                        driver.find_element_by_css_selector('body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE').click() # 検索btnをクリック
                        wc = 0
        pass

    def click_city(self, city_list):
        print(city_list)
        driver = self.driver
        driver.save_screenshot('./screenshots/aaa_.png')
        iframe = ''
        try:
            #iframe = driver.find_element_by_id('#fancybox-frame')
            #driver.switch_to.frame(iframe)
            #driver.switch_to.frame(1)
            iframe = driver.find_element_by_css_selector('#fancybox-frame')
            driver.switch_to_frame(iframe)
            driver.find_element_by_css_selector('#SYZ_13102').click()
        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        for c in city_list:

            driver.find_element_by_id(c).click() # 市区町村をclick

        driver.switch_to_default_content()



    def tearDown(self):
#        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
