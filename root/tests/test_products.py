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
    def setup(self, request):
        """Fixture to login and navigate to Create Product page before each test."""
        login = ProductsPage(self.driver)
        login.login()
        self.product_page = ProductsPage(self.driver)
        self.product_page.click_product_menu()

        # KHỞI TẠO DỮ LIỆU và lưu vào self.  
        # Get scenario from marker or use default
        self.scenario = getattr(request, "param", {}).get("scenario", "normal")
        
        # Create product data as scenario
        product_data = ProductFactory.create_product(scenario=self.scenario)

        # Store all required attributes in self.
        self.name = product_data['name']
        self.sku = product_data['sku']
        self.price = product_data['price']
        self.weight = product_data['weight']
        self.quantity = product_data['quantity']
        self.url_key = product_data['url_key']


    @allure.title("TC004 - View Products List")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_product_list(self):
        rows = self.product_page.get_table_rows()
        assert len(rows) > 0, "No products found in the list"


    @allure.title("TC012 - Search product") 
    @pytest.mark.parametrize("setup", [
        pytest.param({"scenario": "normal"},        marks=pytest.mark.normal),
        pytest.param({"scenario": "max_length"},    marks=pytest.mark.max_length),
        pytest.param({"scenario": "special_chars"}, marks=pytest.mark.special_chars),
        pytest.param({"scenario": "with_emoji"},    marks=pytest.mark.emoji),
], indirect=True)
    def test_search_product(self):
        self.product_page.wait_for_page_loaded()
        self.keyword = self.name
        self.product_page.search_product(self.keyword)
        row = self.product_page.find_product_row_by_name(self.keyword)
        assert self.keyword.lower().strip() in row.text.lower().strip()
        self.product_page.select_product(row)
