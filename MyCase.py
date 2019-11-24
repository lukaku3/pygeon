import unittest, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from sub import subClass

class MyTestCase(unittest.TestCase):

    def setUp(self):
        # ----- launch visible
        #        self.driver = webdriver.Remote(
        #           command_executor= self.selenium_server,
        #            desired_capabilities=DesiredCapabilities.CHROME)
        # ----- launch background start
        opts = Options()
        # opts.binary_location = self.browser_path
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=opts)
        # self.driver = webdriver.Chrome(executable_path="/c/Users/kazuh/bin/chromedriver", chrome_options=opts)

    def test_something(self):
        subClass.display(self, self.driver)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
