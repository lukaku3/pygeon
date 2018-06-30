# -*- coding: utf-8 -*-
import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool

class PygeonSearch(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Remote(
        #     command_executor='http://selenium-hub:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME)
        self.driver = webdriver.Chrome()
        self.logging = logging.getLogger('LoggingTest')
        self.logging.setLevel(10)
        fh = logging.FileHandler('test.log', delay=True)
        # formatter = logging.Formatter('%(asctime)s - '
        #                       '%(levelname)s - '
        #                       '%(filename)s:%(lineno)d - '
        #                       '%(funcName)s - '
        #                       '%(message)s')
        fh.setFormatter(formatter)
        self.logging.addHandler(fh)

    def test_pygeon_search(self):
        self.logging.warning('warning')
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        #        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
