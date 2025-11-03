from selenium.webdriver.common.by import By
from base.base_page import BasePage

class CollectionsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.categories_menu = (By.XPATH, "//ul[@class='item-group']//a[@href='https://e2e.evershop.app/admin/collections']")


    def navigate_to_categories_page(self):
        self.click(self.categories_menu)

