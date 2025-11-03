from base.base_test import BaseTest
from pages.collections_page import CollectionsPage
import allure

@allure.title("Verify user can open Collection page after skipping login via cookies")
class TestCollection(BaseTest):
    def test_collection_page(self):
        collection = CollectionsPage(self.driver)
        collection.navigate_to_categories_page()
        assert "collection" in self.driver.current_url.lower()
        print("✅ Mở Collection Page thành công qua menu")

