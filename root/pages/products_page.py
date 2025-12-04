# pages.products_page.py
from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
from utils.helper import HelperConfig
from pages.login_page import LoginPage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import allure
import os
import time


class ProductsPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        BaseLocator.__init__(self, driver)

        # Menu & button
        self.products_menu = (By.XPATH, "//li[@class='root-nav-item nav-item']//a[@href='https://e2e.evershop.app/admin/products']")
        self.new_product_btn = (By.XPATH, "//div[@class = 'flex justify-end space-x-2 items-center']//span[text() = 'New Product']")
        self.create_product_header = (By.XPATH, "//h1[@class = 'page-heading-title']")
        self.search_input = (By.XPATH, "//input[@id = 'field-keyword']")
        self.filter_status = (By.XPATH, "//div[@class = 'filter-container']//span[text() = 'Status']")
        self.enabled_status = (By.XPATH, "//ul//li//a[text() = 'Enabled']")
        self.disabled_status = (By.XPATH, "//ul//li//a[text() = 'Disabled']")
        self.table_rows = (By.XPATH, "//table//tbody/tr")
        self.table = (By.XPATH, "//table/tbody")
        self.product_name_column = (By.XPATH, "//tbody/tr/td[3]//a")
        self.table_column_header = (By.XPATH, "//table/thead/tr/th")
        self.check_box = (By.XPATH, "//input[@type='checkbox']")
        self.inline_error_msg = (By.XPATH, "//p[@class = 'field-error']")


        self.enabled_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'Enabled']")
        self.disabled_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'Disabled']")
        self.not_visible_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'Not visible individually']")
        self.catalog_search_visible_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'Not visible individually']")
        self.manage_stock_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'Yes']")
        self.no_manage_stock_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'No']")
        self.in_stock_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'In Stock']")
        self.out_of_stock_toggle = (By.XPATH, "//div[@class = 'radio-item']//label[text() = 'Out of Stock']")

        self.product_attributes_section = (By.XPATH, "//div[@class = 'card-section border-b box-border']//h3[text() = 'Attributes']")
        self.product_size_list = (By.XPATH, "//tr//select[@id = 'field-attributes.0.value']")
        self.product_color_list = (By.XPATH, "//tr//select[@id = 'field-attributes.1.value']")
        self.product_color_option = (By.XPATH, "//tr//select[@id = 'field-attributes.1.value']//option[text() = 'White']")
        

    @allure.title("Login Successfully with Valid Credentials")
    def login(self):
        login_page = LoginPage(self.driver)
        login_page.login(*ConfigReader.get_email_password()) 

    # ======================================
    # 1. Products Page
    # ======================================

    @allure.title("Click product menu")
    def click_product_menu(self):
        self.click(self.products_menu)

    @allure.step("Search product by name: {keyword}")
    def search_product(self, keyword):
        self.send_keys(self.search_input, keyword + Keys.ENTER)
        self.wait_for_page_loaded()

    @allure.step("Get product table name column")
    def get_product_name_column(self):
        print(f"DEBUG: Gọi find_elements với locator: {self.product_name_column}")
        return self.find_elements((self.product_name_column))
    
    @allure.step("Get product table rows")
    def get_table_rows(self):
        return self.find_elements((self.table_rows)) # Wait for table rows to be visible
    
    @allure.step("Find row that contains product name: {expected_name}")
    def find_product_row_by_name(self, expected_name: str):
        rows = self.get_product_name_column()
        return self.find_row_contains(rows, expected_name)

    @allure.step("Select a product to edit")
    def select_product(self, row):
        return self.click(row)
        
      
        

    # ======================================
    # 2. Create Products Page
    # ======================================

    @allure.step("Click create new product")
    def click_new_product(self):
        self.click(self.new_product_btn)
        self.wait_for_page_loaded()

    @allure.step("Wait for new product form")
    def wait_for_new_product_form(self):
        self.wait_for_visible(self.create_product_header)

    @allure.step("Get title")
    def get_create_product_title_text(self):
        return self.find_element(self.create_product_header).text
    
    @allure.step("Check if General Information Fields display - UI Elements ")
    def is_product_name_displayed(self):
        return self.is_displayed(self.product_name_input)
    def is_sku_displayed(self):
        return self.is_displayed(self.product_sku_input)
    def is_price_displayed(self):
        return self.is_displayed(self.product_price_input)
    def is_weight_displayed(self):
        return self.is_displayed(self.product_weight_input)
    def is_select_category_displayed(self):
        return self.is_displayed(self.select_product_category)
    def is_description_displayed(self):
        return self.is_displayed(self.product_description)
    def is_media_displayed(self):
        return self.is_displayed(self.product_upload_image)

    @allure.step("# Check if Search engine optimize display - UI Elements")
    def is_url_key_displayed(self):
        return self.is_displayed(self.product_url_key_input)
    def is_meta_title_displayed(self):
        return self.is_displayed(self.product_meta_title_input)
    def is_meta_description_displayed(self):
        return self.is_displayed(self.product_meta_des_input)
    
    @allure.step("# Check if product status & visibility display - UI Elements")
    def is_status_enabled_selected(self):
        return self.is_displayed(self.enabled_toggle)
    def is_visibility_catalog_search_selected(self):
        return self.is_displayed(self.catalog_search_visible_toggle)
    
    @allure.step("# Check if inventory management display - UI Elements")
    def is_manage_stock_yes_selected(self):
        return self.is_displayed(self.manage_stock_toggle)
    def is_in_stock_availability_selected(self):
        return self.is_displayed(self.in_stock_toggle)
    def is_quantity_displayed(self):
        return self.is_displayed(self.product_quantity_input)

    
    @allure.step("# Check if attribute section display - UI Elements")
    def is_attributes_section_displayed(self):
        return self.is_displayed(self.product_attributes_section)
    def is_size_dropdown_displayed(self):
        return self.is_displayed(self.product_size_list)
    def is_color_dropdown_displayed(self):
        return self.is_displayed(self.product_color_list)


    @allure.step("Upload image") 
    def upload_image(self, image): 
        image_path = HelperConfig.get_absolute_image_path(image)
        file_input = self.wait_for_presence(self.product_upload_image)
        file_input.send_keys(image_path)
        self.wait_for_upload_complete(self.product_uploaded_image)
        self._screenshot(f"clicked_{12}")

    @allure.step("Check if image is uploaded")
    def is_image_uploaded(self):
        return self.is_displayed(self.product_uploaded_image)

    @allure.step("Remove image")
    def remove_image(self):
        return self.click(self.remove_image_btn)

    @allure.step("Enter Product Name")
    def enter_product_name(self, name):
        self.send_keys(self.product_name_input, name)

    def get_product_name_value(self):
        return self.find_element(self.product_name_input).get_attribute("value")

    @allure.step("Enter SKU")
    def enter_product_sku(self, sku):
        self.send_keys(self.product_sku_input, sku)

    @allure.step("Enter Price")
    def enter_product_price(self, price):
        self.send_keys(self.product_price_input, price)

    @allure.step("Enter weight")
    def enter_product_weight(self, weight):
        self.send_keys(self.product_weight_input, weight)

    @allure.step("Enter quantity")
    def enter_product_quantity(self, quantity):
        self.send_keys(self.product_quantity_input, quantity)

    @allure.step("Enter URL Key")
    def enter_product_url_key(self, url_key):
        self.send_keys(self.product_url_key_input, url_key)

    @allure.step("Enter meta title")
    def enter_product_meta_title(self, meta_title):
        self.send_keys(self.product_meta_title_input, meta_title)

    @allure.step("Enter meta description")
    def enter_product_meta_description(self, meta_description):
        self.send_keys(self.product_meta_des_input, meta_description)

    @allure.step("Save product")
    def click_save_btn(self):
        self.click(self.save_btn)

    @allure.step("Cancel create product")
    def click_cancel_btn(self):
        self.click(self.cancel_btn)

    @allure.step("Check success message visible")
    def is_success_displayed(self):
        return self.is_displayed(self.toast_msg)
    
    @allure.step("Check success message visible")
    def is_inline_error_message_displayed(self):
        return self.is_displayed(self.inline_error_msg)

    @allure.step("Verify product created successfully")
    def verify_toast_success_message(self, expected_text):
        return self.wait_for_toast_message(
            toast_locator = self.toast_msg,
            toast_text = expected_text
        )
    
    @allure.step("Verify redirect to edit page after submit")
    def redirect_to_edit_page(self):
        return self.wait_for_redirect_edit_page(
            expected_url_part="/products/edit")
    
    
    @allure.step("Verify redirect to edit page after submit")
    def create_product_with_required_fields(self, name, sku, price, weight, quantity, url_key, meta_title):
        self.enter_product_name(name)
        self.enter_product_sku(sku)
        self.enter_product_price(price)
        self.enter_product_weight(weight)
        self.enter_product_quantity(quantity)
        self.enter_product_url_key(url_key)
        self.enter_product_meta_title(meta_title)

    @allure.step("Verify redirect to edit page after submit")
    def edit_product_with_required_fields(self, name, sku, price, weight, quantity, url_key, meta_title):
        self.enter_product_name(name)
        self.enter_product_sku(sku)
        self.enter_product_price(price)
        self.enter_product_weight(weight)
        self.enter_product_quantity(quantity)
        self.enter_product_url_key(url_key)
        self.enter_product_meta_title(meta_title)
        
    @allure.step("Select color attribute") 
    def select_color(self, color):   
        self.select_by_visible_text(self.product_color_list, color)
        
    @allure.step("Select category") 
    def select_category(self): 
        self.click(self.select_product_category)
        self.click(self.product_men_category)
        # self._screenshot(f"clicked_{1}")
      
    @allure.step("Add description") 
    def add_description(self, product_description): 
        self.click(self.product_des_type)
        # self._screenshot(f"clicked_{2}")
        self.click(self.product_available_block_1)
        # self._screenshot(f"clicked_{3}")
        self.click(self.product_des_type_plus_1)  
        # self._screenshot(f"clicked_{4}")  
        self.click(self.product_des_quote_select) 
        # self._screenshot(f"clicked_{5}")    
        self.send_keys(self.product_quote_input, product_description)
        # self._screenshot(f"clicked_{6}")
        self.send_keys(self.product_quote_caption_input, product_description)
        # self._screenshot(f"clicked_{7}")

        # select and fill raw HTML description
        self.click(self.product_available_block_2)
        # self._screenshot(f"clicked_{8}")
        self.click(self.product_des_type_plus_2)
        # self._screenshot(f"clicked_{9}")
        self.click(self.product_des_rawhtml_select)
        # self._screenshot(f"clicked_{10}")
        self.send_keys(self.product_rawhtml_input, product_description)
        # self._screenshot(f"clicked_{11}")
    
    @allure.step("Back to product listing page") 
    def back_to_product_page(self):
        self.click(self.edit_back_btn)
  


    
       
        
    # def verify_new_product_added(self, expected_name):
    #     """ Verify the newly product added"""
    #     expected_name = ConfigReader.get_product_data()['product_name']
    #     print(f"🔍 Verifying new product: {expected_name}")
    #     return self.verify_record_added(expected_name, self.product_table)

    # @allure.step("Verify SKU Uniqueness Validation")
    # def verify_sku_uniqueness(self):
    #     return self.wait_for_toast_message(
    #         toast_locator=self.toast_msg,
    #         toast_text='Exception in middleware createProduct: duplicate key value violates unique constraint "PRODUCT_SKU_UNIQUE"'
    #     )

    # @allure.step("Fill sku_uniqueness in Product form")
    # def fill_sku_uniqueness_in_product_form(self, product_data):
    #     product_data = ConfigReader.get_product_data()
    #     product_name = product_data['product_name']
    #     product_sku = product_data['product_sku']
    #     product_price = product_data['product_price']
    #     product_weight = product_data['product_weight']
    #     product_quantity = product_data['product_quantity']
    #     product_url_key = product_data['product_url_key']
    #     product_meta_title = product_data['product_meta_title']
     
    #     # fill general form
    #     self.send_keys(self.product_name_input, product_name)
    #     self.send_keys(self.product_sku_input, product_sku)
    #     self.send_keys(self.product_price_input, product_price)
    #     self.send_keys(self.product_weight_input, product_weight)

    #     # fill quantity and search engine optimize
    #     self.send_keys(self.product_quantity_input, product_quantity)
    #     self.send_keys(self.product_url_key_input, product_url_key)
    #     self.send_keys(self.product_meta_title_input, product_meta_title)