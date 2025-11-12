from base.base_test import BaseTest
from pages.categories_page import CategoriesPage
from utils.config_reader import ConfigReader
import allure
from time import sleep

@allure.story("Verify user can open Collection page after skipping login via cookies")
class TestCategories(BaseTest):
    def test_categories_page(self):
        
        "Step 1: Login to the website"
        category = CategoriesPage(self.driver)
        category.get_cookie()

        "Step 2: Navigate to Collections page"
        category.navigate_to_categories_page()
        assert "categories" in self.driver.current_url.lower()
        print("✅ Navigate to Collection Page successfully through menu")

        "Step 3: Create a new Collection"
        category.create_new_category()
        category.add_category_data_and_submit(ConfigReader.get_category_data)

        """ Verify the category created successfully"""
        category.verify_category_created_successfully()

        """ Verify the newly category added"""
        category.verify_new_category_added(ConfigReader.get_category_data)
        self.driver.save_screenshot("new category added.png")
       
