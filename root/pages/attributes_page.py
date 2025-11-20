from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
from pages.login_page import LoginPage
from selenium.webdriver import ActionChains
from time import sleep


class AttributesPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        BaseLocator.__init__(self, driver)

    def get_cookie(self):
        "Step 1: Login to the website"
        login_page = LoginPage(self.driver) 
        login_page.login(*ConfigReader.get_email_password()) 

    def navigate_to_attributes_page(self):
        "Step 2: Navigate to Attributes page"
        self.wait_and_click(self.attributes_menu)
        self.driver.save_screenshot("navigate_to_attributes_page_success.png")

    def create_new_attribute(self):
        "Step 3: Create a new Category"
        self.wait_and_click(self.new_attribute_btn)    

    def add_attribute_data_and_submit(self, attribute_data):
        "Step 4: Add collection data & submit"
        attribute_data = ConfigReader.get_attribute_data()
        attribute_name = attribute_data['attribute_name']
        attribute_code = attribute_data['attribute_code']
        attribute_sort_order = attribute_data['attribute_sort_order']

        # fill form
        self.send_keys(self.attribute_name_input, attribute_name)
        self.send_keys(self.attribute_code_input, attribute_code)
        
        # select type
        self.wait_and_click(self.attribute_text_type)

        # select attribute group
        action = ActionChains(self.driver)
        self.wait_and_click( self.attribute_group_select)
        option = self.presence_of_element(self.attribute_default_group)
        action.move_to_element(option).click().perform()

        # fill sort order
        self.send_keys(self.attribute_sort_order_input, attribute_sort_order)
        
        # submit
        self.wait_and_click(self.save_btn)
        
    def verify_attribute_created_successfully(self):
        """ Verify the attribute created successfully"""
        self.wait_for_page_ready_after_submit(
            toast_text="Attribute created successfully",
            expected_url_part="attributes/edits"
        )

    def verify_new_attribute_added(self, expected_name):
        # Back to the attribute listing page
        self.click(self.edit_back_btn)

        """ Verify the newly attribute added"""
        expected_name = ConfigReader.get_attribute_data()['attribute_name']
        print(f"🔍 Verifying new category: {expected_name}")
        return self.verify_record_added(expected_name, self.attribute_table)

       

   
