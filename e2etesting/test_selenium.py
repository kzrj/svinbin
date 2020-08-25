import time
import unittest
from selenium import webdriver

# driver = webdriver.Chrome(executable_path='C:\projects\SmileMan\bin\BIN_WEB_ROOT\e2etesting\chromedriver.exe')
# driver = webdriver.Chrome()
# driver.get('http://46.229.212.205/')

# driver.find_element_by_xpath('//input[@name="username"]').send_keys("test_admin1")
# driver.find_element_by_xpath('//input[@name="password"]').send_keys("svinbin123")
# driver.find_element_by_xpath('//div[@class="input-group"]/button').click()

# time.sleep(1)
# print('1')

# driver.find_element_by_xpath('//a[@href="/workshop1/"]').click()
# print('2')


class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        self.client = webdriver.Chrome()

    def test_login_page(self):
        self.client.get('http://46.229.212.205/')
        driver.find_element_by_xpath('//input[@name="username"]').send_keys("test_admin1")
        driver.find_element_by_xpath('//input[@name="password"]').send_keys("svinbin123")
        driver.find_element_by_xpath('//div[@class="input-group"]/button').click()
        print('Test text')