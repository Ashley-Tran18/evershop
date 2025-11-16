
from base.base_page import BasePage  
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import allure
from time import sleep

class LoginPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        # BasePage.__init__(self, driver)
        BaseLocator.__init__(self, driver)

        # Locator
        self.email_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-email']")
        self.password_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-password']")
        self.login_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button")
        self.error_toast = (By.XPATH, "//div[@class = 'Toastify']//div[@class = 'Toastify__toast-body']")
        self.email_error = (By.XPATH, "//p[@id = 'field-email-error']")
        self.password_error = (By.XPATH, "//p[@id = 'field-password-error']")
        self.eye_password_icon = (By.XPATH, "//button[@class = 'text-gray-400 hover:text-gray-600 transition-colors']")
        self.dashboard_title = (By.XPATH, "//h1[@class = 'page-heading-title']")
        self.avatar_icon = (By.XPATH, "//div[@class = 'flex justify-items-start gap-2 justify-center']")
        self.logout_btn = (By.XPATH, "//div[@class = 'mt-2']//a[text() = 'Logout']")
        self.admin_dropdown = (By.XPATH, "//div[@class = 'logout bg-background shadow p-5']")

    def is_email_displayed(self):
        return self.is_displayed(self.email_input)

    def is_password_displayed(self):
        return self.is_displayed(self.password_input)

    def is_sign_in_button_displayed(self):
        return self.is_displayed(self.login_btn)
    
    def get_email_placeholder(self):
        return self.get_attribute(self.email_input, "placeholder")

    def get_password_placeholder(self):
        return self.get_attribute(self.password_input, "placeholder")

    def enter_email(self, email):
        self.send_keys(self.email_input, email)

    def enter_password(self, password):
        self.send_keys(self.password_input, password)

    def click_sign_in(self):
        self.click(self.login_btn)

    def press_enter_on_password(self):
        self.find_element(self.password_input).send_keys(Keys.ENTER)

    def login(self, email, password, use_enter=False):
        self.enter_email(email)
        self.enter_password(password)
        if use_enter:
            login_button = self.wait_for_presence(self.login_btn)
            login_button.send_keys(Keys.ENTER)
            # self.press_enter_on_password()
        else:
            self.click_sign_in()

    def logout(self):
        avatar_icon = self.wait_for_visible(self.avatar_icon)
        avatar_icon.click()
        self.wait_for_presence(self.admin_dropdown)
        logout_btn = self.wait_for_visible(self.logout_btn)
        logout_btn.click()

    
    def is_error_message_displayed(self):
        try:
            return self.is_displayed(self.error_toast)
        except:
            return False

    def get_error_message(self):
        try:
            return self.get_text(self.error_toast)
        except:
            return ""

    def is_email_error_visible(self):
        try:
            return self.is_displayed(self.email_error)
        except:
            return False
    
    def get_email_error_text(self):
        return self.get_text(self.email_error)

    def is_password_error_visible(self):
        try:
            return self.is_displayed(self.password_error)
        except:
            return False
        
    def get_password_error_text(self):
        return self.get_text(self.password_error)

    def is_password_masked(self):
        return self.get_attribute(self.password_input, "type") == "password" # ---> Return True if password is hidden (type='password')
    
    def is_password_unmasked(self):
        return self.get_attribute(self.password_input, "type") == "text" # ---> Return True if password is visible (type='text')
    
    def show_hide_password_icon(self):
        return self.click(self.eye_password_icon) # ---> Click the eye icon to show/hide password

    def is_sign_in_button_enabled(self):
        return self.is_enabled(self.login_btn)

    def wait_for_dashboard(self):
        # dashboard_url = ConfigReader.get_base_url().rstrip("/") + ConfigReader.get_base_url()
        # self.wait_for_url_contains(dashboard_url)
        self.assert_text_contains(self.dashboard_title, "Dashboard")

    def get_current_url(self):
        return self.driver.current_url
    

