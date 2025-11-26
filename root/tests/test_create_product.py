# tests.test_create_products.py
from base.base_test import BaseTest
from pages.products_page import ProductsPage
from factories.product_factory import ProductFactory
from utils.config_reader import ConfigReader
import allure
import pytest
from time import sleep


@allure.epic("E-commerce Admin")
@allure.feature("Product Module")
class TestCreateProducts(BaseTest):
    
    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        """Fixture to login and navigate to Create Product page before each test."""
        login = ProductsPage(self.driver)
        login.login()
        self.create_product_page = ProductsPage(self.driver)
        self.create_product_page.click_product_menu()
        self.create_product_page.click_new_product()
        self.create_product_page.wait_for_new_product_form()


    @allure.title("TC001 - Open New Product Form")
    def test_open_create_product_form(self):
        assert "Create a new product" in self.create_product_page.get_create_product_title_text()


    @allure.title("Verify General Information Fields UI Elements")
    def test_general_info_fields(self):
        assert self.create_product_page.is_product_name_displayed()



    @allure.title("TC010 - Product Name Accepts Valid Characters & Max Length")
    def test_product_name_validations(self):
        name = ConfigReader.get_product_name("normal")
        self.create_product_page.enter_product_name(name)
        # 🔥 ASSERT value đã được fill
        filled_value = self.create_product_page.get_product_name_value()
        assert filled_value == name, f"Expected name '{name}', but got '{filled_value}'"

        
   

    # @allure.title("TC011 - Create Product with required Fields") 
    # def test_create_product_with_required_fields(self):
    #     self.product_page.click_new_product()
    #     self.product_page.wait_for_new_product_form()
    #     self.product_page.fill_product_form(ConfigReader.get_product_data)
    #     self.product_page.add_description(ConfigReader.get_product_data)
    #     self.product_page.upload_image(ConfigReader.get_product_data)
    #     self.product_page.select_color()
    #     self.product_page.click_save_btn()
    #     assert self.product_page.verify_toast_message()
    #     # self.driver.save_screenshot("toast.png")
    #     assert self.product_page.redirect_to_edit_page()
    #     # self.driver.save_screenshot("edit.png")

    # @allure.title("TC012 - Validation for Required Fields")
    # def test_required_fields_validation(self):
    #     self.product_page.click_new_product()
    #     self.product_page.wait_for_new_product_form()
    #     self.product_page.click_save_btn()
    #     assert self.product_page.is_inline_error_message_displayed()
    #     # self.driver.save_screenshot("inline_error_msg.png")

    # @allure.title("TC013 - SKU Uniqueness Validation")
    # def test_sku_uniqueness(self):
    #     self.product_page.click_new_product()
    #     self.product_page.wait_for_new_product_form()
    #     self.product_page.fill_sku_uniqueness_in_product_form(ConfigReader.get_product_data)
    #     self.product_page.select_color()
    #     self.product_page.click_save_btn()
    #     assert self.product_page.verify_sku_uniqueness()
    #     # self.driver.save_screenshot("sku_uniqueness.png")


    # @allure.title("TC014 - Add Product Description")
    # def test_add_product_description(self):

       
    