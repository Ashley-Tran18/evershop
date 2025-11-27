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

    # ======================================
    # Verify General Information Fields UI Elements
    # ======================================
    @allure.title("Verify General Information Fields")
    def test_general_info_fields(self):
        assert self.create_product_page.is_product_name_displayed()
        assert self.create_product_page.is_sku_displayed()
        assert self.create_product_page.is_price_displayed()
        assert self.create_product_page.is_weight_displayed()
        assert self.create_product_page.is_select_category_displayed()
        assert self.create_product_page.is_description_displayed()

    # ======================================
    # Verify Search engine optimize UI Elements
    # ======================================
    @allure.title("Verify Search engine optimize")
    def test_search_engine_optimize_fields(self):
        assert self.create_product_page.is_url_key_displayed()
        assert self.create_product_page.is_meta_title_displayed()
        assert self.create_product_page.is_meta_description_displayed()

    # ======================================
    # Verify Product status UI Elements
    # ======================================
    @allure.title("Verify Product Status and Visibility")
    def test_product_status_visibility(self):
        assert self.create_product_page.is_status_enabled_selected()
        assert self.create_product_page.is_visibility_catalog_search_selected()
        allure.attach(self.driver.get_screenshot_as_png(), name="inventory", attachment_type=allure.attachment_type.PNG)
    
    # ======================================
    # Verify Inventory UI Elements
    # ======================================
    @allure.title("Verify Inventory Management Fields")
    def test_inventory_management(self):
        assert self.create_product_page.is_manage_stock_yes_selected()
        assert self.create_product_page.is_in_stock_availability_selected()
        assert self.create_product_page.is_quantity_displayed()

    # ======================================
    # Verify Attributes UI Elements
    # ======================================
    @allure.title("Verify Attributes section")
    def test_attributes_section(self):
        assert self.create_product_page.is_attributes_section_displayed()
        assert self.create_product_page.is_size_dropdown_displayed()
        assert self.create_product_page.is_color_dropdown_displayed()


    # ======================================
    # Verify Media upload function
    # ======================================
    @allure.title("Verify Media upload function")
    def test_media_upload(self):
        image = ConfigReader.get_product_image()
        self.create_product_page.upload_image(image)
        assert self.create_product_page.is_image_uploaded()
        self.create_product_page.remove_image()



    @allure.title("TC010 - Product Name Accepts Valid Characters & Max Length")
    def test_product_name_validations(self):
        name = ConfigReader.get_product_name("normal")
        self.create_product_page.enter_product_name(name)
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

       
    