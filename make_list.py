# -*- coding: utf-8 -*-
import unittest
import os
import csv
import re
import sys
import logging
import requests
import pprint
import json
import time
import nose.tools as nose
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

class MakeList(unittest.TestCase):

    selenium_server = 'http://localhost:4444/wd/hub'
    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=%s'
    detail_url = 'http://www.hatomarksite.com%s'
    dialog_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/dialog/syz?pref='
#    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川','27':'大阪'}
    pref_list = {'11':'埼玉','12':'千葉','14':'神奈川','27':'大阪','13':'東京'}
    default_log = 'test.log'
    pref_json = 'pref%s.json'
    tmp_pref_csv = 'tmp%s.csv'
    agent_csv    = 'agents%s.csv'
    city_max  = 5
    css_search_btn = 'body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE'
    css_next_link = 'div.pagination.align-center > ol > li.next > a'
#    next_a1 = '#container > div.main.right > div:nth-child(2) > div:nth-child(2) > div > ol > li.next > a'
#    css_next_link = '#container > div.main.right > div:nth-child(7) > div:nth-child(1) > div > ol > li.next > a'
    x = 1024
    y = 768
    browser_path = '/usr/bin/google-chrome'

    def setUp(self):
        self.pref_list = self.get_pref_list()
#        self.driver = webdriver.Remote(
#           command_executor= self.selenium_server,
#            desired_capabilities=DesiredCapabilities.CHROME)
        opts = Options()
        opts.binary_location = self.browser_path
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=opts)
#        user_agent = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'
#        pjs_path = 'node_modules/phantomjs/bin/phantomjs'
#        dcap = {
#                    "phantomjs.page.settings.userAgent" : user_agent,
#                        'marionette' : True
#                        }
#        self.driver = webdriver.PhantomJS(executable_path=pjs_path, desired_capabilities=dcap)
        self.driver.set_window_size(self.x, self.y)
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

    def get_pref_list(self):
        args = sys.argv[2:]
        new_list = {}
        if len(args):
            for arg in args:
                if arg in self.pref_list.keys():
                    new_list[arg] = arg
        return new_list

    def test_make_list(self):
        print('start make pref.json')
        driver = self.driver
        pref_list_json = []
        self.setup_logger(self.pref_json)
        for pref in self.pref_list.keys():
            f = open(self.pref_json % pref,'a')
            driver.get(self.base_url % pref ) # 最初、のページを開く
            pref_json = {}
            pref_json['id'] = pref
            pref_json['name'] = self.pref_list[pref]
            pref_json['city'] = []
            req = requests.get(self.dialog_url + pref) # 各dialogのページを開く
            soup = BeautifulSoup(req.text, "lxml")
            for i in soup.find_all("dt"): # 全inputをリストへ格納
                if ( pref == "14" and re.match(r'(横浜|川崎)', i.find('label').string)) is None: # 神奈川は川崎と横浜
                    continue
                # jsonデータ準備
                city = {}
                city['id'] = i.find("input").get('id')
#                city['value'] = i.find("input").get('value')
#                city['name']  = re.sub( r'\(|\)|[0-9]+','', i.find('label').string)
#                city['count']  = re.sub(r'\D', '', i.find('label').string)
                pref_json['city'].append(city)

            time.sleep(1)
            json.dump(pref_json, f)
            f.close()

    def test_scrape_detail_link(self):
        driver = self.driver
        # self.setup_logger(None)
        for pref in self.pref_list.keys():
            fpath = self.pref_json % pref
            if os.path.exists(fpath): #　県別 市区町村を開く
                tmp_f = open(self.tmp_pref_csv % pref,'a')
                self.tmp_f = None
                self.tmp_f = writer = csv.writer(tmp_f)
                with open(fpath, "r") as f:
                    pref = json.load(f)
#                    for url in pref_json:
#                    driver.get( self.base_url % pref['id'] )
                    time.sleep(2)
                    city_cnt = 0 # 最大５つまでチェック（市区町村）
                    city_list = []
                    for city in pref['city']:
                        driver.get( self.base_url % pref['id'] )
                        city_list.append(city['id'])
                        if len(city_list) == self.city_max:
                            print(city_list)
                            time.sleep(1)
                            self.click_city(city_list)
                            self.collect_link()
                            print('init city_list')
                            city_list = []
                        else:
                            pass
                    if len(city_list) > 0:
                            self.click_city(city_list)
                            self.collect_link()
                            city_list = []

                tmp_f.close()
            else:
                print('%s is not exists.' % fpath)
#                tmp_f.close()
        else:
            pass # for  pref in self.pref_list.keys()
        print('end loop')

#        fpath = self.pref_json #　県別 市区町村を読む
#        if os.path.exists(fpath):
#            with open(fpath, "r") as f:
#                pref_json = json.load(f)
#                for url in pref_json:
#                    # self.setup_logger(self.tmp_pref_csv % url['id'])
#                    f = open(self.tmp_pref_csv % pref,'a')
#                    driver.get( self.base_url % url['id'] )
#                    time.sleep(2)
#                    city_cnt = 0 # 最大５つまでチェック（市区町村）
#                    city_list = []
#                    city_idx = 0
#                    for city in url['city']:
#                        driver.get( self.base_url % url['id'] )
#                        print("append:" + city['id'])
#                        city_list.append(city['id'])
#                        if len(city_list) == self.city_max:
#                            self.click_city(city_list)
#                            time.sleep(1)
#                            print('init city_list')
#                            self.collect_link(f)
#                            city_list = []
#                        city_idx += 1
#                    if len(city_list) > 0:
#                            self.click_city(city_list)
#                            self.collect_link(f)
#                            city_list = []
#                    f.close()
#        else:
#            print('%s is not exists.' % fpath)
#            pass

    def test_scrape_agent(self):
        print('start scrape fax')
        driver = self.driver
        # self.setup_logger(None)
        for pref in self.pref_list:
            driver.get( self.base_url % pref )
            self.setup_logger(self.agent_csv % pref)
            csv_path = self.tmp_pref_csv % pref
            if os.path.exists(csv_path):
                with open(csv_path,  newline='') as f:
                    dataReader = csv.reader(f)
                    for row in dataReader:
                        print(row[0])
                        driver.get( self.detail_url % row[0] )
                        time.sleep(1)
                        soup = BeautifulSoup(driver.page_source, "lxml")
                        tbl = soup.find('table').find_all('td')
                        detail = []
                        detail.append(tbl[0])
                        detail.append(tbl[1])
                        detail.append(tbl[2])
                        detail.append(tbl[7])
                        detail.append(tbl[8])
                        detail_str = ",".join(map(str,detail))
                        self.logging.info( re.sub( r'<((/|)td|td\scolspan="[0-9]")>', '', detail_str) )
                    else:
                        f.close()
            else:
                print('%s is not exists.' % csv_path)
                pass


    def click_city(self, city_list):
        driver = self.driver
        iframe = driver.find_element_by_css_selector('#fancybox-frame')
        driver.switch_to.frame(iframe)
        for c in city_list:
            driver.find_element_by_id(c).click() # 市区町村をclick

#        driver.save_screenshot('screenshots/1.png')
        driver.find_element_by_css_selector(self.css_search_btn).click() # 検索btnをクリック
        time.sleep(1)
        Select(driver.find_element_by_css_selector('select.displayCount')).select_by_value('50')
        driver.switch_to.default_content()


    def collect_link(self):
        driver = self.driver
#        logging = self.logging
#        driver.switch_to_default_content()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        tbl = soup.find_all('table')
        for t in tbl:
            url = []
            if t.find('a').string is not None:
                url.append(t.find('a').get('href'))
                url.append(t.find('a').string)
#                print(','.join(url))
#                f.writerows( url )
                self.tmp_f.writerow( url )
#                self.logging.info( ','.join(url) )
#            url.append(t.find('a').get('href'))
#            if t.find('a').string:
#                url.append(t.find('a').string)
#                self.logging.info( ','.join(url) )

        else:
            paginate = soup.select(self.css_next_link)
            if len(paginate) > 0:
                time.sleep(1)
#                element.click()
#                driver.find_element_by_css_selector(self.css_next_link).click()
                try:
                    #driver.find_element_by_css_selector(self.css_next_link)
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.css_next_link)))
                    element.click()
                except OSError as err:
                    driver.save_screenshot('screenshots/paginate_err.png')
                    print("OS error: {0}".format(err))
                self.collect_link()
            else:
                print('next-link is not exists.')
            pass

    def tearDown(self):
        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
