# -*- coding: utf-8 -*-
import re
import sys
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

html = '<html><body><table class="datalist agentlist"><tbody><tr><td rowspan="3" class="select"><input type="checkbox" name="kai_no[]" value="00071312242"></td><td colspan="2" class="title"><h3><a href="/search/zentaku/agent/00071312242/" target="_blank">（株）オークリサーチ</a></h3><div class="row"><p></p></div></td></tr><tr><td rowspan="2" class="photo"><a href="/search/zentaku/agent/00071312242/" target="_blank"><span class="agent-list-map-resize-span"><div class="agent-list-map-container"><div class="photo_cell_mid"><div align="center"><img src="http://img3.athome.jp//image_files/index/zentaku_agent/00071312242/1.jpg?width=100&amp;height=100" class="agent-list-map-image-max-size" alt="（株）オークリサーチ"></div></div></div></span></a></td><td><strong></strong><br>                    東京都千代田区飯田橋１丁目<br><strong class="mr-03">[営業時間]</strong><strong class="ml-10 mr-03">[定休日]</strong>&nbsp;<br><strong class="mr-03">[TEL]</strong>03-5211-5988<br><strong class="mr-03">[免許番号]</strong>東京都知事免許（３）第８６１９０号                </td></tr><tr><td colspan="7" class="clearfix"><div class="right" style="padding:5px;"><a class="button button-rounded PIE" href="/search/zentaku/agent/00071312242/" target="_blank"><i class="fa fa-home"></i>詳細を見る</a><a class="button button-rounded button-action PIE ml-05 addFavorite" href="/search/zentaku/agent/00071312242/favorite/"><i class="fa fa-plus"></i>検討中リストに追加</a></div></td></tr></tbody></table><table class="datalist agentlist"><tbody><tr><td rowspan="3" class="select"><input type="checkbox" name="kai_no[]" value="00071302755"></td><td colspan="2" class="title"><h3><a href="/search/zentaku/agent/00071302755/" target="_blank">山京商事（株）</a></h3><div class="row"><p></p></div></td></tr><tr><td rowspan="2" class="photo"><a href="/search/zentaku/agent/00071302755/" target="_blank"><span class="agent-list-map-resize-span"><div class="agent-list-map-container"><div class="photo_cell_mid"><div align="center"><img src="http://img3.athome.jp//image_files/index/zentaku_agent/00071302755/1.jpg?width=100&amp;height=100" class="agent-list-map-image-max-size" alt="山京商事（株）"></div></div></div></span></a></td><td><strong></strong><br>                    東京都千代田区飯田橋１丁目<br><strong class="mr-03">[営業時間]</strong><strong class="ml-10 mr-03">[定休日]</strong>&nbsp;<br><strong class="mr-03">[TEL]</strong>03-3264-0011<br><strong class="mr-03">[免許番号]</strong>東京都知事免許（４）第７７３８８号                </td></tr><tr><td colspan="7" class="clearfix"><div class="right" style="padding:5px;"><a class="button button-rounded PIE" href="/search/zentaku/agent/00071302755/" target="_blank"><i class="fa fa-home"></i>詳細を見る</a><a class="button button-rounded button-action PIE ml-05 addFavorite" href="/search/zentaku/agent/00071302755/favorite/"><i class="fa fa-plus"></i>検討中リストに追加</a></div></td></tr></tbody></table><table class="datalist agentlist"><tbody><tr><td rowspan="3" class="select"><input type="checkbox" name="kai_no[]" value="00071205296"></td><td colspan="2" class="title"><h3>（有）アルファビジネスサービス</h3><div class="row"><p></p></div></td></tr><tr><td rowspan="2" class="photo"><span class="agent-list-map-resize-span"><div class="agent-list-map-container"><div class="photo_cell_mid"><div align="center"><img src="http://img3.athome.jp//image_files/index/zentaku_agent/00071205296/1.jpg?width=100&amp;height=100" class="agent-list-map-image-max-size" alt="（有）アルファビジネスサービス"></div></div></div></span></td><td><strong></strong><br>                    千葉県千葉市緑区土気町<br><strong class="mr-03">[営業時間]</strong><strong class="ml-10 mr-03">[定休日]</strong>&nbsp;<br><strong class="mr-03">[TEL]</strong>043-294-3161<br><strong class="mr-03">[免許番号]</strong>千葉県知事免許（３）第１５３１８号</td></tr><tr><td colspan="7" class="clearfix"><div class="right" style="padding:5px;"><a class="button button-rounded button-action PIE ml-05 addFavorite" href="/search/zentaku/agent/00071205296/favorite/"><i class="fa fa-plus"></i>検討中リストに追加</a></div></td></tr></tbody></table></body></html>'

soup = BeautifulSoup(html, "lxml")
for t in soup.select('table'):
    print("----------------------")
    # tenant = t.find('h3')
    # if( tenant.find('a') ):
    #     print(tenant.find('a').string)
    #     print(tenant.find('a').get('href'))
    # else:
    #     print(tenant.string)

    # info = t.find('tr:nth-child(2) > td:nth-child(2)')
    for td in t.find_all('td'):
        # td = td.encode('utf-8')
        # print(td)
        # print( re.sub( r'\xa0', '', td) )
    # info = t.select('tr:nth-child(1)')
    # for i in t.find_all(info):
        # str = re.sub( r'<_.>', '', i)
        # print( i )
        # print( str )
        # print(t.select('td.title > h3').strip())
    # pprint.pprint(t.select('td.title > h3 > a').get('href'))
