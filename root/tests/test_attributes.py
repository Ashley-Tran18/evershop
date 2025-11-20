from base.base_test import BaseTest
from pages.attributes_page import AttributesPage
from utils.config_reader import ConfigReader
import allure
from time import sleep

@allure.story("Verify user can open Collection page after skipping login via cookies")
class TestAttributes(BaseTest):
    def test_attributes_page(self):
        
        "Step 1: Login to the website"
        attribute = AttributesPage(self.driver)
        attribute.get_cookie()

        "Step 2: Navigate to Attributes page"
        attribute.navigate_to_attributes_page()
        assert "attributes" in self.driver.current_url.lower()
        print("✅ Navigate to Collection Page successfully through menu")

        "Step 3: Create a new Collection"
        attribute.create_new_attribute()
        attribute.add_attribute_data_and_submit(ConfigReader.get_attribute_data)

        """ Verify the attribute created successfully"""
        attribute.verify_attribute_created_successfully()

        """ Verify the newly category added"""
        attribute.verify_new_attribute_added(ConfigReader.get_attribute_data)
        self.driver.save_screenshot("new attribute added.png")
       
