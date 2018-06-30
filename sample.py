import sys
import re
import pprint
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

base_url = "http://www.hatomarksite.com/search/zentaku/agent/area/#!"
pref_list = [{13: 'tokyo'},{14: 'kanagawa'},{12: 'chiba'},{11: 'saitama'}]
driver = webdriver.Chrome()
driver.get(base_url)

#f = urllib.request.urlopen(base_url)
#print(f.read())
for pref in pref_list.keys():
    print(pref)
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
driver.close()

