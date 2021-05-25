from .base import BasePage
from selenium.webdriver.common.by import By


class SearchPage(BasePage):

    def search_product(self, text):
        self.driver.find_element_by_id('search').send_keys(text)
        print('wtf')

    def is_title_matches(self):
        return "Python" in self.driver.title

