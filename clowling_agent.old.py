
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
from selenium.webdriver.support.ui import Select

class MakeList(unittest.TestCase):

    base_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/#!pref=%s'
    dialog_url = 'http://www.hatomarksite.com/search/zentaku/agent/area/dialog/syz?pref=%s'
    pref_list = {'13':'東京','12':'千葉','11':'埼玉','14':'神奈川'}
    # pref_json = 'pref.json'
    pref_json = 'sample.json'
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
        with open(self.pref_json, "r") as f:
            pref_json = json.load(f)
            for url in pref_json:
                # dialog_elem = driver.get( self.base_url % url['id'] )
                time.sleep(3)
                city_cnt = 0 # 最大５つまでチェック（市区町村）
                print( "pref:%s, city length:%s" % (url['id'] , len(url['city'])))
                for city in url['city']:
                    print()
                    dialog_elem = driver.get( self.base_url % url['id'] )
                    # time.sleep(1)
                    city_cnt += 1
                    iframe = driver.find_element_by_id('fancybox-frame')
                    driver.switch_to_frame(iframe)
                    driver.find_element_by_id(city['id']).click() # 市区町村をclick
                    next_page = 1
                    if ( city_cnt % self.city_cnt_limit != 0 ):
                        continue
                    elif( city_cnt == len(url['city'])):
                        pass
                    else:
                        driver.find_element_by_css_selector('body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE').click() # 検索btnをクリック
                        wc = 0
                        li_next_flg = False
                        while li_next_flg == False:
                            json_dta = {}
                            # driver.switch_to.default_content()
                            driver.get(driver.current_url) # 区の表者一覧ページを取得
                            time.sleep(2)
                            Select(driver.find_element_by_css_selector('select.displayCount')).select_by_value('50')
                            time.sleep(3)

                            driver.find_element_by_id('all_check').click()
                            driver.save_screenshot('./aaa%s.png' % wc)
                            soup = BeautifulSoup(driver.page_source, "lxml")
                            area = soup.find('span').string

                            # for a in soup.select('h3 > a'):
                            #     json_dta['area'] = area
                            #     json_dta['href'] = a.get('href')
                            for t in soup.select('table'):
                                json_dta['area'] = area
                                tenant = t.find('h3')
                                if( tenant.find('a') ):
                                    json_dta['tenant'] = tenant.find('a').string
                                    json_dta['href'] = tenant.find('a').get('href')
                                else:
                                    json_dta['tenane'] = tenant.string
                                    json_dta['href'] = None
                                json_dta['href'] = a.get('href')
                                attr_cnt = 1
                                for i in t.select('.mr-03'):
                                    json_dta['attr%s' % attr_cnt] = i.string
                                self.logging.info(json.dumps(json_dta))

                            li_next = soup.select("li.next")
                            if(li_next is None):
                                print("no next")
                                li_next_flg = True # 次ページ無ければ終了
                            else:
                                print("go next")
                                wc += 1
                                driver.find_element_by_css_selector('li.next > a').click()

                        else:

                            break
                        break
                    time.sleep(3


    # def myLog(self):
    #     print(self.driver.current_url)
    #     #------------------------------------------
    #     # url回収
    #     #------------------------------------------
    #     driver = self.driver
    #     while li_next_flg == False:
    #         json_dta = {}
    #         driver.get(driver.current_url) # 区の表者一覧ページを取得
    #         time.sleep(2)
    #         Select(driver.find_element_by_css_selector('select.displayCount')).select_by_value('50')
    #         time.sleep(3)
    #
    #         driver.find_element_by_id('all_check').click()
    #         driver.save_screenshot('./screenshots/aaa%s.png' % wc)
    #         soup = BeautifulSoup(driver.page_source, "lxml")
    #         area = soup.find('span').string
    #
    #         for t in soup.select('table'):
    #             json_dta['area'] = area
    #             tenant = t.find('h3')
    #             if( tenant.find('a') ):
    #                 json_dta['tenant'] = tenant.find('a').string
    #                 json_dta['href'] = tenant.find('a').get('href')
    #             else:
    #                 json_dta['tenane'] = tenant.string
    #                 json_dta['href'] = None
    #             json_dta['href'] = a.get('href')
    #             attr_cnt = 1
    #             for i in t.select('.mr-03'):
    #                 json_dta['attr%s' % attr_cnt] = i.string
    #             self.logging.info(json.dumps(json_dta))
    #
    #         li_next = soup.select("li.next")
    #         if(li_next is None):
    #             li_next_flg = True # 次ページ無ければ終了
    #         else:
    #             wc += 1
    #             driver.find_element_by_css_selector('li.next > a').click()
    #     else:
    #         # break
    #         pass

    def tearDown(self):
#        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
