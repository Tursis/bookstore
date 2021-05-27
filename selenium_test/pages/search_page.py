from selenium.webdriver.common.keys import Keys

from .base import BasePage
from selenium.webdriver.common.by import By

from ..locators.search_locators import SearchLocators


class SearchPage(BasePage):

    def search_product(self, text):
        self.driver.find_element(*SearchLocators.search).send_keys(text + Keys.ENTER)
        return text in self.driver.page_source

    def is_title_matches(self):
        return "Home page" in self.driver.title
