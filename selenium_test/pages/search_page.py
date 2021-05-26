from selenium.webdriver.common.keys import Keys

from .base import BasePage
from selenium.webdriver.common.by import By


class SearchPage(BasePage):

    def search_product(self, text):
        self.driver.find_element_by_id('search').send_keys(text + Keys.ENTER)
        # text2 = self.driver.find_element(By.CSS_SELECTOR, "span").text
        return text in self.driver.page_source


    def is_title_matches(self):
        return "Home page" in self.driver.title

