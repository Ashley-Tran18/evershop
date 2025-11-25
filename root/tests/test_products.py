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
    
    @allure.title("TC004 - View Products List")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_product_list(self):
        product = ProductsPage(self.driver)
        product.login()
        product.click_product_menu()
        rows = product.get_table_rows()
        assert len(rows) > 0, "No products found in the list"


    @allure.title("TC005 - Search Product by Name")
    def test_search_product(self):
        product = ProductsPage(self.driver)
        product.login()
        product.click_product_menu()
        keyword = ConfigReader.get_product_data()["product_name"]
        product.search_product(keyword)
        rows = product.get_product_name_column()
        for row in rows:
            assert keyword.lower() in row.text.lower()
            # self.driver.save_screenshot("search_product.png")


    @allure.title("TC010 - Open New Product Form")
    def test_open_create_product_form(self):
        product = ProductsPage(self.driver)
        product.login()
        product.click_product_menu()
        product.click_new_product()
        assert "Create a new product" in product.get_create_product_title_text()


    @allure.title("TC011 - Create Product with required Fields") 
    def test_create_product_with_required_fields(self):
        product = ProductsPage(self.driver)
        product.login()
        product.click_product_menu()
        product.click_new_product()
        product.wait_for_new_product_form()
        product.fill_product_form(ConfigReader.get_product_data)
        product.click_save_btn()
        assert product.verify_toast_message()
        # self.driver.save_screenshot("toast.png")
        assert product.redirect_to_edit_page()
        # self.driver.save_screenshot("edit.png")


    @allure.title("TC012 - Validation for Required Fields")
    def test_required_fields_validation(self):
        product = ProductsPage(self.driver)
        product.login()
        product.click_product_menu()
        product.click_new_product()
        product.wait_for_new_product_form()
        product.click_save_btn()
        assert product.is_inline_error_message_displayed()
        # self.driver.save_screenshot("inline_error_msg.png")


    @allure.title("TC013 - SKU Uniqueness Validation")
    def test_sku_uniqueness(self):
        product = ProductsPage(self.driver)
        product.login()
        product.click_product_menu()
        product.click_new_product()
        product.wait_for_new_product_form()
        product.fill_sku_uniqueness_in_product_form(ConfigReader.get_product_data)
        product.click_save_btn()
        assert product.verify_sku_uniqueness()
        # self.driver.save_screenshot("sku_uniqueness.png")


    # @allure.title("TC014 - Add Product Description")
    # def test_add_product_description(self):

       
    