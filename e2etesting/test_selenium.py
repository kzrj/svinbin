# -*- coding: utf-8 -*-
import time
import unittest
from selenium import webdriver


class SeleniumTestCase(unittest.TestCase):
    client = webdriver.Chrome(executable_path="C:/projects/SmileMan/bin/data/chromedriver.exe")

    # def setUp(self):
    #     self.client = webdriver.Chrome(executable_path="C:/projects/SmileMan/bin/data/chromedriver.exe")
        # self.client = webdriver.Chrome()

    def login(self, username, password):
        self.client.get('http://46.229.212.205/')
        self.client.find_element_by_xpath('//input[@name="username"]').send_keys(username)
        self.client.find_element_by_xpath('//input[@name="password"]').send_keys(password)
        self.client.find_element_by_xpath('//div[@class="input-group"]/button').click()

    def test_main_page_buttons_exists(self):
        self.login(username="test_admin1", password="svinbin123")
        time.sleep(2)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop1/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop2/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop3/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop4/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop5/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop6/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop7/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop8/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/workshop_boar/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//a[@href="/reports/"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//button[text() = "Выйти"]')), 1)
        time.sleep(2)

    def test_ws1_tabs_exists(self):
        self.client.get('http://46.229.212.205/')
        time.sleep(2)
        self.client.find_element_by_xpath('//a[@href="/workshop1/"]').click()
        time.sleep(2)
        self.assertEqual(
            len(self.client.find_elements_by_xpath('//button[@data-toggle = "collapse"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//div[text() = "Импорт из Фарма"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//div[text() = "УЗИ 28"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//div[text() = "УЗИ 35"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//div[text() = "Перегон"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//div[text() = "Выбытие"]')), 1)
        self.assertEqual(len(self.client.find_elements_by_xpath('//div[text() = "Поиск по всем цехам"]')), 1)
        
    def test_ws1_uzi_35_tab_choose_sow(self):
        self.client.get('http://46.229.212.205/workshop1/')
        time.sleep(1)
        self.client.find_element_by_xpath('//button[@data-toggle = "collapse"]').click()
        time.sleep(1)
        self.client.find_element_by_xpath('//div[text() = "УЗИ 35"]').click()
        time.sleep(1)

        if len(self.client.find_elements_by_xpath('//tr[@class = "sow-row"]')) > 2:
            self.client.find_element_by_xpath('//tr[@class = "sow-row"]/th[1]').click()
            selected_sow = self.client.find_element_by_xpath('//table/tbody/tr[1]')
            self.assertEqual(selected_sow.get_attribute("class"), 'sow-row-active')

            self.client.find_element_by_xpath('//tr[@class = "sow-row"]/th[1]').click()
            self.assertEqual(len(self.client.find_elements_by_xpath('//tr[@class = "sow-row-active"]')), 2)
            time.sleep(1)

            self.client.find_element_by_xpath('//tr[@class = "sow-row-active"][1]/th').click()
            self.assertEqual(len(self.client.find_elements_by_xpath('//tr[@class = "sow-row-active"]')), 1)
        # TODO: add logger write: less than 2 sows

    def test_ws1_uzi_35_tab_mark_suporos(self):
        self.client.get('http://46.229.212.205/workshop1/')
        time.sleep(1)
        self.client.find_element_by_xpath('//button[@data-toggle = "collapse"]').click()
        time.sleep(1)
        self.client.find_element_by_xpath('//div[text() = "УЗИ 35"]').click()
        time.sleep(1)

        if len(self.client.find_elements_by_xpath('//tr[@class = "sow-row"]')) > 2:
            self.client.find_element_by_xpath('//tr[@class = "sow-row"]/th[1]').click()
            selected_sow = self.client.find_element_by_xpath('//table/tbody/tr[1]')
            self.assertEqual(selected_sow.get_attribute("class"), 'sow-row-active')

            self.client.find_element_by_xpath('//tr[@class = "sow-row"]/th[1]').click()
            self.assertEqual(len(self.client.find_elements_by_xpath('//tr[@class = "sow-row-active"]')), 2)

            self.client.find_element_by_xpath('//button[text() = "Супорос"]').click()
            time.sleep(1)
            self.assertEqual(self.client.find_element_by_xpath('//p[@class = "message"]').text, 'Узи проведено.')