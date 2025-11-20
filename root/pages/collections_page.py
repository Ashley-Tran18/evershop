from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
from pages.login_page import LoginPage
from time import sleep
from selenium.webdriver.support import expected_conditions as EC


class CollectionsPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        BaseLocator.__init__(self, driver)

    def get_cookie(self):
        "Step 1: Login to the website"
        login_page = LoginPage(self.driver) 
        login_page.login(*ConfigReader.get_email_password()) 

    def navigate_to_collections_page(self):
        "Step 2: Navigate to Collections page"
        self.wait_and_click(self.collections_menu)

    def create_new_collection(self):
        "Step 3: Create a new Collection"
        self.wait_and_click(self.new_collections_btn)    
        sleep(2)

    def add_collection_data_and_submit(self, collection_data):
        "Step 4: Add collection data & submit"
        collection_data = ConfigReader.get_collection_data()
        collection_name = collection_data['collection_name']
        collection_code = collection_data['collection_code']
        collection_des = collection_data['collection_des']
            
        # fill form
        self.send_keys(self.collection_name_input, collection_name)
        self.send_keys(self.collection_code_input, collection_code)
        self.wait_and_click(self.collection_des_type)
        self.send_keys(self.collection_des_input, collection_des)
        sleep(1)
    
        # submit
        self.wait_and_click(self.add_collection_btn)
   
    def verify_collection_created_successfully(self):
        """Verify the collection created successfully"""
        """Show toast message"""
        sleep(1)
        return self.wait_for_element_visible(self.collection_created_msg)

    """Or redirect to edit page"""
    def verify_redirect_to_collection_edit_page(self):
        sleep(2)
        assert "edit" in self.driver.current_url.lower()

    "Step 4: Back to the Collection listing page"
    def back_to_collection_page(self):
        self.wait_and_click(self.edit_collection_back_btn)

        """ Verify the newly collection added"""
    def verify_new_collection_added(self, expected_name):
        # Get collection expected_name from file data.json
        expected_name = ConfigReader.get_collection_data()['collection_name']

        # Get all collection names displays on table
        elements = self.find_elements((self.collection_table))
        collection_names = [el.text.strip() for el in elements if el.text.strip()]
        # print(f"Newly Collection added: {expected_name}" )
       
        # Compare, ignore sensitive cases(upper/lower)
        for name in collection_names:
            if name.lower() == expected_name.lower():
                print(f"✅ Found new collection '{expected_name}' in table!")
                return True
            
        raise AssertionError(f"❌ Collection '{expected_name}' not found in table. Got: {collection_names}")
        
    """Delete new collection"""
    def del_collection(self):
        expected_name = ConfigReader.get_collection_data()['collection_name']
        print(f"Expected name is {expected_name}")

        rows = self.find_elements((self.collection_rows))
        
        for row in rows: 
                # Get column 3rd of collection name
            name_cell = row.find_element(*self.collection_cell)
            name_text = name_cell.text.strip()

            if name_text == expected_name:
                print(f"🔥 Found matching collection: {name_text}")
                
                    # Get exact checkbox of current row
                check_box = row.find_element(*self.collection_checkbox)
                self.driver.execute_script("arguments[0].click();", check_box)
                print("✅ Checkbox selected for deletion")

                    # Click Delect
                self.click(self.collection_del_btn)
                print("🗑️ Clicked Delete button")
                
                    # Confirm popup Delete
                try:
                    self.click(self.collection_confirm_del_btn)
                    print("🔴 Confirmed Delete")
                    sleep(2)
                except:
                    print("⚠️ No confirmation popup found")
                return
        else:
            raise Exception(f"❌ Collection name not found: {expected_name}")
        
            

                





