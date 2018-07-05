
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

    url = 'http://www.hatomarksite.com'
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
        with open(self.url_json, "r") as f:
            url_json = json.load(f)
            for url in url_json:
                # dialog_elem = driver.get( self.base_url % url['id'] )
                time.sleep(3)
                city_cnt = 0 # 最大５つまでチェック（市区町村）
                city_max = len(url['city'])
                for city in url['city']:
                    dialog_elem = driver.get( self.base_url % url['id'] )
                    city_cnt += 1
                    iframe = driver.find_element_by_id('fancybox-frame')
                    driver.switch_to_frame(iframe)
                    driver.find_element_by_id(city['id']).click() # 市区町村をclick
                    next_page = 1
                    # print("%s:%s:%s" % (city_cnt,city_max,city["id"]) )
                    # print("%s:%s" % (type(city_cnt),type(city_max)) )

                    print("%s:%s:%s:%s" % (city_cnt,city_max,city["id"],"city_cnt == city_max") )
                    # driver.save_screenshot('./screenshots/aaa_.png')
                    # print("%s:%s:%s" % (city_cnt,city_max,city["id"]) )
                    driver.find_element_by_css_selector('body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE').click() # 検索btnをクリック
                    time.sleep(2)
                    self.parseAgentPage()

                    # if (city_cnt == city_max): # 残りの端数の時
                    #     print("%s:%s:%s:%s" % (city_cnt,city_max,city["id"],"city_cnt == city_max") )
                    #     driver.save_screenshot('./screenshots/aaa_.png')
                    #     # print("%s:%s:%s" % (city_cnt,city_max,city["id"]) )
                    #     driver.find_element_by_css_selector('body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE').click() # 検索btnをクリック
                    #     time.sleep(2)
                    #     self.parseAgentPage()
                    # elif city_cnt != city_max:
                    #     print("%s:%s:%s:%s" % (city_cnt,city_max,city["id"],"city_cnt != city_max:") )
                    #     driver.find_element_by_css_selector('body > div.dialogBody > div.box.align-center.clearfix.PIE > button.button.button-bordered.button-royal.PIE').click() # 検索btnをクリック
                    #     wc = 0
                    #     li_next_flg = False
                    #     while li_next_flg == False:
                    #         json_dta = {}
                    #         # driver.switch_to.default_content()
                    #         driver.get(driver.current_url) # 区の表者一覧ページを取得
                    #         print(driver.current_url)
                    #         time.sleep(2)
                    #         Select(driver.find_element_by_css_selector('select.displayCount')).select_by_value('50')
                    #         time.sleep(3)
                    #
                    #         driver.find_element_by_id('all_check').click()
                    #         driver.save_screenshot('./screenshots/aaa%s.png' % wc)
                    #         soup = BeautifulSoup(driver.page_source, "lxml")
                    #         area = soup.find('span').string
                    #
                    #         # for t in soup.select('table'):
                    #         #     json_dta['area'] = area
                    #         #     tenant = t.find('h3')
                    #         #     if( tenant.find('a') ):
                    #         #         json_dta['tenant'] = tenant.find('a').string
                    #         #         json_dta['href'] = tenant.find('a').get('href')
                    #         #     else:
                    #         #         json_dta['tenane'] = tenant.string
                    #         #         json_dta['href'] = ''
                    #         #     json_dta['attr'] = t.find_all('td')[3].get_text(' ', strip=True)
                    #         #     self.logging.info(', '.join(json_dta.values()))
                    #
                    #         li_next = soup.select("li.next > a")
                    #         if(li_next is None):
                    #             li_next_flg = True # 次ページ無ければ終了
                    #             # break
                    #         elif(li_next_flg is not True):
                    #             wc += 1
                    #             driver.find_element_by_css_selector('li.next > a').click()
                    #
                    #         li_next_flg = True # 次ページ無ければ終了
                    #     else:
                    #         pass
                    #
                    # elif ( city_cnt % self.city_cnt_limit != 0 ):
                    #     print("%s:%s:%s" % (city_cnt,city_max,city["id"]) )
                    #
                    #     continue
                    #
                    # else:
                    #     pass
                    #     #     break
                    #     # break
                    time.sleep(1)

    def parseAgentPage(self):
        driver = self.driver

        wc = 0
        li_next_flg = False
        while li_next_flg == False:
            json_dta = {}
            # driver.switch_to.default_content()
            driver.get(driver.current_url) # 区の表者一覧ページを取得
            print(driver.current_url)
            time.sleep(2)
            Select(driver.find_element_by_css_selector('select.displayCount')).select_by_value('50')
            time.sleep(3)

            driver.find_element_by_id('all_check').click()
            driver.save_screenshot('./screenshots/aaa%s.png' % wc)
            soup = BeautifulSoup(driver.page_source, "lxml")
            area = soup.find('span').string

            for t in soup.select('table'):
                json_dta['area'] = area
                tenant = t.find('h3')
                if( tenant.find('a') ):
                    json_dta['tenant'] = tenant.find('a').string
                    json_dta['href'] = tenant.find('a').get('href')
                else:
                    json_dta['tenane'] = tenant.string
                    json_dta['href'] = ''
                json_dta['attr'] = t.find_all('td')[3].get_text(' ', strip=True)
                detail_link = t.find('a', class_='button button-rounded PIE').get('href') # 詳細リンク遷移
                if detail_link:
                    print(detail_link)
                    driver.get(self.url + detail_link)
                    time.sleep(1)
                    detail_src = BeautifulSoup(driver.page_source, "lxml")
                    json_dta['tel_fax'] = ','.join(driver.find_element_by_css_selector('p.tel').text.split('／'))
                    driver.back()
                else:
                    json_dta['tel_fax'] = ''
                self.logging.info(', '.join(json_dta.values()))

            li_next = soup.select("li.next > a")
            if(li_next is None):
                li_next_flg = True # 次ページ無ければ終了
                break
                # break
            elif(li_next_flg is not True):
                wc += 1
                driver.find_element_by_css_selector('li.next > a').click()

            # li_next_flg = True # 次ページ無ければ終了

        else:
            pass



    def tearDown(self):
#        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
