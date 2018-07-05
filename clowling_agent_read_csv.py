# -*- coding: utf-8 -*-
import unittest
import csv
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
from selenium.webdriver.support.ui import Select

class MakeList(unittest.TestCase):

    url = 'http://www.hatomarksite.com%s'
    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=%s'
    dialog_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/dialog/syz?pref=%s'
    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川'}
    # url_json = 'pref11.json'
    url_json = 'sample.json'
    agent_url_csv = 'agent_url.csv'
    city_cnt_limit = 5
    iframe_id = 'fancybox-frame'
    # li_next = True

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        # self.driver.implicitly_wait(5)
        # self.driver = webdriver.Chrome('./chromedriver-Windows')
        self.logging = logging.getLogger('LoggingTest')
        self.logging.setLevel(10)
        fh = logging.FileHandler(self.agent_url_csv, delay=True, encoding='utf-8')
#        formatter = logging.Formatter('%(asctime)s - '
#                              '%(levelname)s - '
#                              '%(filename)s:%(lineno)d - '
#                              '%(funcName)s - '
#                              '%(message)s')
#        fh.setFormatter(formatter)
        self.logging.addHandler(fh)

    def test_make_list(self):
        driver = self.driver
        with open('sample.csv',  newline='') as f:
            dataReader = csv.reader(f)
            for row in dataReader:
                print(row)
                driver.get(self.url % re.sub(r' ', '', row[1]))
                time.sleep(2)
                # driver.find_element_by_css_selector('table.agentData')
                # html = urllib3.urlopen(self.url % re.sub(r' ', '', row[1])
                r = requests.get(self.url % re.sub(r' ', '', row[1]))
                soup = BeautifulSoup(driver.page_source, "lxml")
                # soup = BeautifulSoup(r.text, "lxml")
                # tenant = soup.select('table.agentData > tbody > tr:nth-child(1) > td:nth-child(4)')
                tbl = soup.find('table')
                print(tbl)
                #         area = soup.find('span').string



    def tearDown(self):
#        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
