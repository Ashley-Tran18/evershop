# tests.test_create_products.py
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
class TestCreateProducts(BaseTest):
    
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, request):
        """Fixture to login and navigate to Create Product page before each test."""
        login = ProductsPage(self.driver)
        login.login()
        self.create_product_page = ProductsPage(self.driver)
        self.create_product_page.click_product_menu()
        self.create_product_page.click_new_product()
        self.create_product_page.wait_for_new_product_form()

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
        self.meta_title = product_data['meta_title']

        # Fields that are optional → use product_data.get('field', default)
        self.meta_description = product_data.get('meta_description', '')
        self.description = product_data.get('description', '')
        self.image = product_data.get('image', '')

    @allure.title("TC001 - Open New Product Form")
    def test_open_create_product_form(self):
        assert "Create a new product" in self.create_product_page.get_create_product_title_text()

    # ======================================
    # Verify General Information Fields UI Elements
    # ======================================
    @allure.title("TC002 -Verify General Information Fields")
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
    @allure.title("TC003 - Verify Search engine optimize")
    def test_search_engine_optimize_fields(self):
        assert self.create_product_page.is_url_key_displayed()
        assert self.create_product_page.is_meta_title_displayed()
        assert self.create_product_page.is_meta_description_displayed()

    # ======================================
    # Verify Product status UI Elements
    # ======================================
    @allure.title("TC004 - Verify Product Status and Visibility")
    def test_product_status_visibility(self):
        assert self.create_product_page.is_status_enabled_selected()
        assert self.create_product_page.is_visibility_catalog_search_selected()
        allure.attach(self.driver.get_screenshot_as_png(), name="inventory", attachment_type=allure.attachment_type.PNG)
    
    # ======================================
    # Verify Inventory UI Elements
    # ======================================
    @allure.title("VTC005 - Verify Inventory Management Fields")
    def test_inventory_management(self):
        assert self.create_product_page.is_manage_stock_yes_selected()
        assert self.create_product_page.is_in_stock_availability_selected()
        assert self.create_product_page.is_quantity_displayed()

    # ======================================
    # Verify Attributes UI Elements
    # ======================================
    @allure.title("TC006 - Verify Attributes section")
    def test_attributes_section(self):
        assert self.create_product_page.is_attributes_section_displayed()
        assert self.create_product_page.is_size_dropdown_displayed()
        assert self.create_product_page.is_color_dropdown_displayed()

    # ======================================
    # Verify Media upload function
    # ======================================
    @allure.title("TC007 - Verify Media upload function")
    def test_media_upload(self):
        self.create_product_page.upload_image(self.image)
        assert self.create_product_page.is_image_uploaded()
        self.create_product_page.remove_image()


    @allure.title("TC008 - Create Product with required Fields - {scenario}")
    @allure.title("Create Product - {marker}")
    @pytest.mark.parametrize("setup", [
    pytest.param({"scenario": "normal"},        marks=pytest.mark.normal),
    pytest.param({"scenario": "max_length"},    marks=pytest.mark.max_length),
    pytest.param({"scenario": "special_chars"}, marks=pytest.mark.special_chars),
    pytest.param({"scenario": "with_emoji"},    marks=pytest.mark.emoji),
], indirect=True)
    def test_create_product_with_required_fields(self):
        # Form validation
        self.create_product_page.click_save_btn()
        assert self.create_product_page.is_inline_error_message_displayed() # Show empty required fields
        
        # Fill in product data (auto-generate unique values + match the selected scenario).
        self.create_product_page.create_product_with_required_fields(self.name,
            self.sku, self.price, self.weight, self.quantity, self.url_key, self.meta_title)
        
        self.create_product_page.select_color("Black")
        self.create_product_page.click_save_btn()
        assert self.create_product_page.verify_toast_success_message(expected_text="Product created successfully")
        assert self.create_product_page.redirect_to_edit_page()
        # Bonus: Log product to debug easily
        allure.attach(f"Created product: {self.name}\nSKU: {self.sku}", name="Product Info", attachment_type=allure.attachment_type.TEXT)


    @allure.title("TC009 - Verify Cancel button works")
    def test_cancel_button(self):
        self.create_product_page.create_product_with_required_fields(self.name,
            self.sku, self.price, self.weight, self.quantity, self.url_key, self.meta_title)
        self.create_product_page.select_color("Black")
        self.create_product_page.click_cancel_btn()
        assert self.create_product_page.get_create_product_title_text()

    
    @allure.title("TC010 - Create a product filling all available fields (General, Media, Search Engine Optimize, Inventory, Attributes)") 
    @pytest.mark.parametrize("setup", [
    pytest.param({"scenario": "normal"},        marks=pytest.mark.normal),
    # pytest.param({"scenario": "max_length"},    marks=pytest.mark.max_length),
    # pytest.param({"scenario": "special_chars"}, marks=pytest.mark.special_chars),
    # pytest.param({"scenario": "with_emoji"},    marks=pytest.mark.emoji),
], indirect=True)
    def test_create_product(self):
        self.create_product_page.wait_for_new_product_form()
        self.create_product_page.create_product_with_required_fields(self.name,
            self.sku, self.price, self.weight, self.quantity, self.url_key, self.meta_title)
        self.create_product_page.select_category()
        self.create_product_page.add_description(self.description)
        self.create_product_page.select_color("Black")
        self.create_product_page.upload_image(self.image)
        self.create_product_page.enter_product_meta_description(self.meta_description)
        self.create_product_page.click_save_btn()
        assert self.create_product_page.verify_toast_success_message(expected_text="Product created successfully")
        assert self.create_product_page.redirect_to_edit_page()
        # Bonus: Log product to debug easily
        allure.attach(f"Created product: {self.name}\nSKU: {self.sku}", name="Product Info", attachment_type=allure.attachment_type.TEXT)


    @allure.title("TC011 - Add more info after summitted product form") 
    @pytest.mark.parametrize("setup", [
    pytest.param({"scenario": "normal"},        marks=pytest.mark.normal),
    pytest.param({"scenario": "max_length"},    marks=pytest.mark.max_length),
    pytest.param({"scenario": "special_chars"}, marks=pytest.mark.special_chars),
    pytest.param({"scenario": "with_emoji"},    marks=pytest.mark.emoji),
], indirect=True)
    def test_create_product_with_more_info(self):
        self.create_product_page.create_product_with_required_fields(self.name, 
            self.sku, self.price, self.weight, self.quantity, self.url_key, self.meta_title)
        self.create_product_page.select_color("White")
        self.create_product_page.click_save_btn()
        assert self.create_product_page.verify_toast_success_message(expected_text="Product created successfully")
        assert self.create_product_page.redirect_to_edit_page()
        self.create_product_page.wait_for_page_loaded()
        self.create_product_page.select_category()
        self.create_product_page.add_description(self.description)
        self.create_product_page.upload_image(self.image)
        self.create_product_page.enter_product_meta_description(self.meta_description)
        self.create_product_page.click_save_btn()
        assert self.create_product_page.verify_toast_success_message(expected_text="Product updated successfully")
        
         # Bonus: Log product to debug easily
        allure.attach(f"Created product: {self.name}\nSKU: {self.sku}", name="Product Info", attachment_type=allure.attachment_type.TEXT)


    @allure.title("TC012 - Edit product") 
    @pytest.mark.parametrize("setup, product_data", [
    pytest.param(
        {"scenario": "normal"},
        {"name": "Test Product Normal ", "suffix": "UPDATED",
        "sku": f"TEST_SKU_UPDATED-{int(time.time())}"},
        marks=pytest.mark.normal,
        id="normal"
    ),
], indirect=["setup"])
    def test_find_product_to_edit(self, product_data):
        # Step 1: Go back to product list
        self.create_product_page.back_to_product_page()

        # Original name was saved during creation in fixture (self.name)
        self.original_name = self.name  # This is the name used when the product was created
        self.new_name = product_data["name"] + product_data["suffix"]
        self.new_sku = product_data["sku"] 
        self.new_price = "999"
        self.new_weight = "5.9"
        self.new_quantity = "1000"

       # Step 2: Find the product by original name
        self.product_page = ProductsPage(self.driver)
        self.product_page.wait_for_page_loaded()
        self.selected_row = self.product_page.find_product_row_by_name(self.original_name)
        assert self.selected_row is not None, f"No product found: {self.original_name}"
        self.product_page.select_product(self.selected_row)

       # Step 3: Edit the product with updated data
        self.create_product_page.edit_product_with_required_fields(
            name = self.new_name, 
            sku = self.new_sku, 
            price = self.new_price,
            weight = self.new_weight, 
            quantity = self.new_quantity, 
            url_key = self.url_key, 
            meta_title = self.meta_title)
        self.create_product_page.select_color("White")
        self.create_product_page.click_save_btn()
        assert self.create_product_page.verify_toast_success_message(expected_text="Product updated successfully")

        # Step 4: Go back and verify the edited product appears with new name
        self.create_product_page.back_to_product_page()

        # Search by full edited name or part of it
        edited_row = self.product_page.find_product_row_by_name(self.new_name)
        assert edited_row is not None, f"No product found: {self.new_name}"


   
    # @allure.title("TC013 - SKU Uniqueness Validation")
    # def test_sku_uniqueness(self):
    #     self.product_page.click_new_product()
    #     self.product_page.wait_for_new_product_form()
    #     self.product_page.fill_sku_uniqueness_in_product_form(ConfigReader.get_product_data)
    #     self.product_page.select_color()
    #     self.product_page.click_save_btn()
    #     assert self.product_page.verify_sku_uniqueness()
    #     # self.driver.save_screenshot("sku_uniqueness.png")


    # # @allure.title("TC014 - Add Product Description")
    # # def test_add_product_description(self):

       