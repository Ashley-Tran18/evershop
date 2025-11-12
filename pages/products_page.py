from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
from pages.login_page import LoginPage
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os


class ProductsPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        BaseLocator.__init__(self, driver)

    def get_cookie(self):
        "Step 1: Login to the website"
        login_page = LoginPage(self.driver) 
        login_page.login(*ConfigReader.get_email_password()) 

    def navigate_to_products_page(self):
        "Step 2: Navigate to Collections page"
        self.wait_and_click(self.products_menu)

    def create_new_product(self):
        "Step 3: Create a new product"
        self.wait_and_click(self.new_product_btn)    

    def add_product_data_and_submit(self, product_data):
        "Step 4: Add product data & submit" 
        # product_data_list = ConfigReader.get_product_data()
        # for product_data in product_data_list:
        product_data = ConfigReader.get_product_data()
        product_name = product_data['product_name']
        product_sku = product_data['product_sku']
        product_price = product_data['product_price']
        product_weight = product_data['product_weight']
        product_quantity = product_data['product_quantity']
        product_url_key = product_data['product_url_key']
        product_meta_title = product_data['product_meta_title']
        product_meta_des = product_data['product_meta_description']
        product_des = product_data['product_description']
        product_image = product_data['product_image']

        # fill general form
        self.send_keys(self.product_name_input, product_name)
        self.send_keys(self.product_sku_input, product_sku)
        self.send_keys(self.product_price_input, product_price)
        self.send_keys(self.product_weight_input, product_weight)

        # select category
        self.click(self.select_product_category)
        self.wait_and_click(self.product_men_category)

        # select and fill quotes description
        self.wait_and_click(self.product_des_type)
        self.hover_to_element(self.product_available_block_1)
        self.wait_and_click(self.product_des_type_plus_1)    
        self.wait_and_click(self.product_des_quote_select)     
        self.send_keys(self.product_quote_input, product_des)
        self.send_keys(self.product_quote_caption_input, product_des)
    
        # select and fill raw HTML description
        self.wait_and_click(self.product_available_block_2)
        self.wait_and_click(self.product_des_type_plus_2)
        self.wait_and_click(self.product_des_rawhtml_select)
        self.send_keys(self.product_rawhtml_input, product_des)

        # upload image
        base = os.path.abspath("images")
        images = os.path.join(base, product_image)
        file_input = self.presence_of_element(self.product_upload_image)
        file_input.send_keys(images)
        self.wait_for_upload_complete(self.product_uploaded_image)
        
        # fill quantity and search engine optimize
        self.send_keys(self.product_quantity_input, product_quantity)
        self.send_keys(self.product_url_key_input, product_url_key)
        self.send_keys(self.product_meta_title_input, product_meta_title)
        self.send_keys(self.product_meta_des_input, product_meta_des)
        
        # select attribute
        self.wait_and_click(self.product_color_list)
        self.wait_and_click(self.product_color_option)

        # submit
        self.wait_and_click(self.add_collection_btn)
        print("✅ submit success")

        
    def verify_product_created_successfully(self):
       """ Verify the product created successfully"""
       self.wait_for_page_ready_after_submit(
           toast_text="Product created successfully",
           expected_url_part="/products/edits"
       )

    def back_to_product_page(self):
        "Back to the product listing page"
        self.wait_and_click(self.edit_product_back_btn)
       
        
    def verify_new_product_added(self, expected_name):
        """ Verify the newly product added"""
        expected_name = ConfigReader.get_product_data()['product_name']
        print(f"🔍 Verifying new product: {expected_name}")
        return self.verify_record_added(expected_name, self.product_table)