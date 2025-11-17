from base.base_test import BaseTest
from pages.products_page import ProductsPage
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from base.base_locator import BaseLocator
import allure
import pytest
from time import sleep
import time

@allure.epic("E-commerce Admin")
@allure.feature("Product Module")
@pytest.mark.usefixtures("setup")
class TestProducts(BaseTest):
    
    # @allure.title("TC004 - View Products List")
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test_view_product_list(self):
    #     product = ProductsPage(self.driver)
    #     product.login()
    #     product.click_product_menu()
    #     rows = product.get_table_rows()
    #     assert len(rows) > 0, "No products found in the list"


    # @allure.title("TC005 - Search Product by Name")
    # def test_search_product(self):
    #     product = ProductsPage(self.driver)
    #     product.login()
    #     product.click_product_menu()
    #     keyword = ConfigReader.get_product_data()["product_name"]
    #     product.search_product(keyword)
    #     rows = product.get_product_name_column()
    #     for row in rows:
    #         assert keyword.lower() in row.text.lower()
    #         self.driver.save_screenshot("search_product.png")


    # @allure.title("TC010 - Open New Product Form")
    # def test_open_create_product_form(self):
    #     product = ProductsPage(self.driver)
    #     product.login()
    #     product.click_product_menu()
    #     product.click_new_product()
    #     assert "Create a new product" in product.get_create_product_title_text()


    @allure.title("TC011 - Create Product with Minimal Fields") 
    def test_create_product_minimal(self):
        product = ProductsPage(self.driver)
        product.login()
        product.click_product_menu()
        product.click_new_product()
        sleep(2)
        # sku = f"TEST_{int(time.time())}"
        product.fill_product_form(ConfigReader.get_product_data)
        sleep(3)
        product.save_btn()
        # assert product.is_success_displayed()


       

   
        

