from unittest import TestCase
from selenium import webdriver
from selenium_test.pages import search_page


class SearchTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")

    # def tearDown(self):
    #     self.driver.quit()

    def test_search_product(self):
        search_test = search_page.SearchPage(self.driver)

        print('h')
