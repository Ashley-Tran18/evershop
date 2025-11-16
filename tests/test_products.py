from base.base_test import BaseTest
from pages.products_page import ProductsPage
from utils.config_reader import ConfigReader
from base.base_locator import BaseLocator
import allure
from time import sleep

@allure.story("Verify user can open Collection page after skipping login via cookies")
class TestProducts(BaseTest):
    def test_categories_page(self):
        
        "Step 1: Login to the website"
        product = ProductsPage(self.driver)
        product.get_cookie()

        "Step 2: Navigate to Products page"
        product.navigate_to_products_page()
        assert "products" in self.driver.current_url.lower()
        print("✅ Navigate to Products Page successfully through menu")

        "Step 3: Create a new product"
        product.create_new_product()
        product.add_product_data_and_submit(ConfigReader.get_product_data)

        """Verify the collection created successfully"""
        product.verify_product_created_successfully()
        
        # "Step 4: Back to the Collection listing page"
        product.back_to_product_page()
        
        """Verify the newly collection added"""
        product.verify_new_product_added(ConfigReader.get_product_data)

       
        
        
        
        

