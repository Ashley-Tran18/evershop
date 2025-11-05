from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader

class BaseLocator:
    def __init__(self, driver):
        self.driver = driver    
        self.timeout = ConfigReader.get_timeout()
        
        # Login Page Locators
        self.email_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-email']")
        self.password_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-password']")
        self.login_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button")
        self.dashboard_header = (By.XPATH, "//h1[@class = 'page-heading-title']")
        self.invalid_login_error = (By.XPATH, "//div[@class = 'Toastify']//div[@class = 'Toastify__toast-body']")



        # Collections Page Locators
        self.collections_menu = (By.XPATH, "//ul[@class='item-group']//a[@href='https://e2e.evershop.app/admin/collections']")