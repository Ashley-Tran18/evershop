from base.base_test import BaseTest
from pages.collections_page import CollectionsPage
from utils.config_reader import ConfigReader
import allure
from time import sleep

@allure.story("Verify user can open Collection page after skipping login via cookies")
class TestCollection(BaseTest):
    def test_collection_page(self):
        
        "Step 1: Login to the website"
        collection = CollectionsPage(self.driver)
        collection.get_cookie()

        "Step 2: Navigate to Collections page"
        collection.navigate_to_collections_page()
        assert "collection" in self.driver.current_url.lower()
        self.driver.save_screenshot("navigate_to_collections_page_success.png")
        print("✅ Navigate to Collection Page successfully through menu")

        "Step 3: Create a new Collection"
        collection.create_new_collection()
        collection.add_collection_data_and_submit(ConfigReader.get_collection_data)

        """Verify the collection created successfully"""
        """Show toast message"""
        collection.verify_collection_created_successfully()
        
        """Or redirect to edit page"""
        collection.verify_redirect_to_collection_edit_page()
        
        # "Step 4: Back to the Collection listing page"
        collection.back_to_collection_page()

        """Verify the newly collection added"""
        collection.verify_new_collection_added(ConfigReader.get_collection_data)
        self.driver.save_screenshot("new_collections_display.png")

        """Delete collection"""
        collection.del_collection()
        self.driver.save_screenshot("deleted.png")
        
        
        
        
        

