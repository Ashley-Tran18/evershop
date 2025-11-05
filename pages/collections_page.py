from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator

class CollectionsPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_categories_page(self):
        self.wait_and_click(self.collections_menu)


