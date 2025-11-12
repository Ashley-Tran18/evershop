from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
from pages.login_page import LoginPage
from time import sleep


class CategoriesPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        BaseLocator.__init__(self, driver)

    def get_cookie(self):
        "Step 1: Login to the website"
        login_page = LoginPage(self.driver) 
        login_page.login(*ConfigReader.get_email_password()) 

    def navigate_to_categories_page(self):
        "Step 2: Navigate to Collections page"
        self.wait_and_click(self.categories_menu)
        self.driver.save_screenshot("navigate_to_category_page_success.png")

    def create_new_category(self):
        "Step 3: Create a new Category"
        self.wait_and_click(self.new_category_btn)    

    def add_category_data_and_submit(self, category_data):
        "Step 4: Add collection data & submit"
        category_data = ConfigReader.get_category_data()
        category_name = category_data['category_name']
        category_des = category_data['category_description']
        category_image = category_data['category_image']
        category_url_key = category_data['category_url_key']
        category_meta_title = category_data['category_meta_title']
        category_meta_des = category_data['category_meta_description']
        

        # fill form
        self.send_keys(self.category_name_input, category_name)
        
        # select & fill heading description
        self.wait_and_click(self.category_des_type)
        self.wait_and_click(self.category_available_block_1)
        self.wait_and_click(self.category_des_type_plus_1)
        self.wait_and_click(self.category_des_heading_select)
        self.send_keys(self.category_heading_input, category_des)
        
        # select & fill list description
        self.wait_and_click(self.category_available_block_2)
        self.wait_and_click(self.category_des_type_plus_2)
        self.wait_and_click(self.category_des_list_select)
        self.send_keys(self.category_list_input, category_des)
        
        # upload image
        self.upload_image(
            self.category_upload_image,
            self.category_uploaded_image,
            category_image
        )

        # fill search engine optimize
        self.send_keys(self.category_url_key_input, category_url_key)
        self.send_keys(self.category_meta_title_input, category_meta_title)
        self.send_keys(self.category_meta_des_input, category_meta_des)
        
        # submit
        self.wait_and_click(self.add_categry_btn)
        
    def verify_category_created_successfully(self):
        """ Verify the category created successfully"""
        self.wait_for_page_ready_after_submit(
            toast_text="Category created successfully",
            expected_url_part="/categories/edits"
        )

    def verify_new_category_added(self, expected_name):
        "Back to the category listing page"
        self.wait_and_click(self.edit_category_back_btn)

        """ Verify the newly category added"""
        expected_name = ConfigReader.get_category_data()['category_name']
        print(f"🔍 Verifying new category: {expected_name}")
        return self.verify_record_added(expected_name, self.category_table)

       

   
