from unittest import TestCase
from selenium import webdriver
from selenium_test.pages.search_page import SearchPage


class SearchTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")

    def tearDown(self):
        self.driver.quit()

    def test_search_product(self):
        search_test = SearchPage(self.driver)
        assert search_test.search_product('ЧУЖАК')
        assert search_test.is_title_matches()
