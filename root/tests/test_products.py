# test_products.py
from base.base_test import BaseTest
from pages.products_page import ProductsPage
from factories.product_factory import ProductFactory
from utils.config_reader import ConfigReader

import allure
import pytest
from time import sleep
import time

@allure.epic("E-commerce Admin")
@allure.feature("Product Module")
class TestProducts(BaseTest):
    
    @pytest.fixture(scope="function", autouse=True)
    def login_and_navigate_to_product_page(self):
        """Fixture to login and navigate to Create Product page before each test."""
        login = ProductsPage(self.driver)
        login.login()
        self.product_page = ProductsPage(self.driver)
        self.product_page.click_product_menu()


    @allure.title("TC004 - View Products List")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_product_list(self):
        rows = self.product_page.get_table_rows()
        assert len(rows) > 0, "No products found in the list"

    @allure.title("TC005 - Search Product by Name")
    def test_search_product(self):
        keyword = ConfigReader.get_product_name("normal")
        self.product_page.search_product(keyword)
        rows = self.product_page.get_product_name_column()
        for row in rows:
            assert keyword.lower() in row.text.lower()
    #         # self.driver.save_screenshot("search_product.png")

   
       
    