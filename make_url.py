# -*- coding: utf-8 -*-
import unittest
import re
import logging
import requests
import json
import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
from bs4 import BeautifulSoup

class MakeList(unittest.TestCase):

    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=13'
    agent_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=%s&syz=%s'
    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川'}
    pref_json = 'pref.json'
    url_json = 'url.json'
    param_max  = 5

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        # self.driver = webdriver.Chrome('./chromedriver-Windows')
        self.logging = logging.getLogger('LoggingTest')
        self.logging.setLevel(10)
        fh = logging.FileHandler(self.url_json, delay=True, encoding='utf-8')
#        formatter = logging.Formatter('%(asctime)s - '
#                              '%(levelname)s - '
#                              '%(filename)s:%(lineno)d - '
#                              '%(funcName)s - '
#                              '%(message)s'
#        )
#        fh.setFormatter(formatter)
        self.logging.addHandler(fh)

    def myLog():
        pass

    def test_make_list(self):
        pref_json = ''
        url_list  = '' # agentの市区町村別URL
        try:
            with open(self.pref_json, 'r') as f:
                pref_json = json.load(f)
                url_json = []
                for pref in pref_json: # 県
                    cnt_c = 0
                    city_list = []
                    for city in pref['city']:
                        if (city['count'] == '0'):
                            continue

                        cnt_c += 1
                        city_list.append(city['id'])
                        url = ''
                        if(cnt_c % self.param_max == 0):
                            url = self.agent_url % (pref['id'],'|'.join(city_list))
                            url_json.append(url)
                            city_list = []
                    else:
                        if ( len('|'.join(city_list)) == 0 ):
                            continue
                        url = self.agent_url % (pref['id'],'|'.join(city_list))
                        # self.logging.info(url)
                        url_json.append(url)
                self.logging.info(json.dumps(url_json))

        except json.JSONDecodeError as e:
            print('JSONDecodeError: ', e)


    def tearDown(self):
        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
