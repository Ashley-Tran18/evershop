from selenium.webdriver.common.by import By
from base.base_page import BasePage  

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        # Locators
        self.email_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-email']")
        self.password_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-password']")
        self.login_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button")
    
    def login(self, email, password):
        self.send_keys(self.email_input, email)
        self.send_keys(self.password_input, password)
        self.click(self.login_btn)