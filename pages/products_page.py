from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
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

        self.product_color_list = (By.XPATH, "//tr//select[@id = 'field-attributes.1.value']")
        self.product_color_option = (By.XPATH, "//tr//select[@id = 'field-attributes.1.value']//option[text() = 'White']")
    
        self.inline_error_msg = (By.XPATH, "//p[@class = 'field-error']")


    @allure.title("Login Successfully with Valid Credentials")
    def login(self):
        login_page = LoginPage(self.driver)
        login_page.login(*ConfigReader.get_email_password()) 

    @allure.title("Click product menu")
    def click_product_menu(self):
        self.click(self.products_menu)

    @allure.step("Search product by name: {keyword}")
    def search_product(self, keyword):
        self.send_keys(self.search_input, keyword + Keys.ENTER)
        self.wait_for_page_loaded()

    @allure.step("Get product table name column")
    def get_product_name_column(self):
        return self.find_elements((self.product_name_column))
    
    @allure.step("Get product table rows")
    def get_table_rows(self):
        return self.find_elements((self.table_rows)) # Wait for table rows to be visible

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
   
    @allure.step("Fill Product form")
    def fill_product_form(self, product_data):
        product_data = ConfigReader.get_product_data()
        product_name = product_data['product_name']
        product_sku = product_data['product_sku']
        # product_sku = f"TEST_{int(time.time())}"
        product_price = product_data['product_price']
        product_weight = product_data['product_weight']
        product_quantity = product_data['product_quantity']
        product_url_key = product_data['product_url_key']
        # product_url_key =  f"{product_name.replace(' ', '-').lower()}-{int(time.time())}"
        product_meta_title = product_data['product_meta_title']
     
        # fill general form
        self.send_keys(self.product_name_input, product_name)
        self.send_keys(self.product_sku_input, product_sku)
        self.send_keys(self.product_price_input, product_price)
        self.send_keys(self.product_weight_input, product_weight)

        # fill quantity and search engine optimize
        self.send_keys(self.product_quantity_input, product_quantity)
        self.send_keys(self.product_url_key_input, product_url_key)
        self.send_keys(self.product_meta_title_input, product_meta_title)
        
        # select attribute
        self.click(self.product_color_list)
        self.click(self.product_color_option)

    @allure.step("Save product")
    def click_save_btn(self):
        self.click(self.save_btn)

    @allure.step("Check success message visible")
    def is_success_displayed(self):
        return self.is_displayed(self.toast_msg)
    
    @allure.step("Check success message visible")
    def is_inline_error_message_displayed(self):
        return self.is_displayed(self.inline_error_msg)

    @allure.step("Verify product created successfully")
    def verify_toast_message(self):
        return self.wait_for_toast_message(
            toast_locator=self.toast_msg,
            toast_text="Product created successfully"
        )
    
    @allure.step("Verify redirect to edit page after submit")
    def redirect_to_edit_page(self):
        return self.wait_for_redirect_edit_page(
            expected_url_part="/products/edit")

    @allure.step("Verify SKU Uniqueness Validation")
    def verify_sku_uniqueness(self):
        return self.wait_for_toast_message(
            toast_locator=self.toast_msg,
            toast_text='Exception in middleware createProduct: duplicate key value violates unique constraint "PRODUCT_SKU_UNIQUE"'
            # expected_url_part="/products/edits"
        )



    # def add_product_data_and_submit(self, product_data):
    #     product_data = ConfigReader.get_product_data()
    #     product_name = product_data['product_name']
    #     product_sku = product_data['product_sku']
    #     product_price = product_data['product_price']
    #     product_weight = product_data['product_weight']
    #     product_quantity = product_data['product_quantity']
    #     product_url_key = product_data['product_url_key']
    #     product_meta_title = product_data['product_meta_title']
    #     product_meta_des = product_data['product_meta_description']
    #     product_des = product_data['product_description']
    #     product_image = product_data['product_image']

    #     # fill general form
    #     self.send_keys(self.product_name_input, product_name)
    #     self.send_keys(self.product_sku_input, product_sku)
    #     self.send_keys(self.product_price_input, product_price)
    #     self.send_keys(self.product_weight_input, product_weight)

    #     # select category
    #     self.click(self.select_product_category)
    #     self.wait_and_click(self.product_men_category)

    #     # select and fill quotes description
    #     self.wait_and_click(self.product_des_type)
    #     self.hover_to_element(self.product_available_block_1)
    #     self.wait_and_click(self.product_des_type_plus_1)    
    #     self.wait_and_click(self.product_des_quote_select)     
    #     self.send_keys(self.product_quote_input, product_des)
    #     self.send_keys(self.product_quote_caption_input, product_des)
    
    #     # select and fill raw HTML description
    #     self.wait_and_click(self.product_available_block_2)
    #     self.wait_and_click(self.product_des_type_plus_2)
    #     self.wait_and_click(self.product_des_rawhtml_select)
    #     self.send_keys(self.product_rawhtml_input, product_des)

    #     # upload image
    #     base = os.path.abspath("images")
    #     images = os.path.join(base, product_image)
    #     file_input = self.presence_of_element(self.product_upload_image)
    #     file_input.send_keys(images)
    #     self.wait_for_upload_complete(self.product_uploaded_image)
        
    #     # fill quantity and search engine optimize
    #     self.send_keys(self.product_quantity_input, product_quantity)
    #     self.send_keys(self.product_url_key_input, product_url_key)
    #     self.send_keys(self.product_meta_title_input, product_meta_title)
    #     self.send_keys(self.product_meta_des_input, product_meta_des)
        
    #     # select attribute
    #     self.wait_and_click(self.product_color_list)
    #     self.wait_and_click(self.product_color_option)


        

    # def back_to_product_page(self):
    #     "Back to the product listing page"
    #     self.wait_and_click(self.edit_product_back_btn)
       
        
    # def verify_new_product_added(self, expected_name):
    #     """ Verify the newly product added"""
    #     expected_name = ConfigReader.get_product_data()['product_name']
    #     print(f"🔍 Verifying new product: {expected_name}")
    #     return self.verify_record_added(expected_name, self.product_table)