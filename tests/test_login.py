
from base.base_test import BaseTest
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
import time
import allure
import pytest
from time import sleep


@allure.epic("Evershop Admin")
@allure.feature("Admin Login")
class TestLogin(BaseTest):
   
    # @allure.title("TC001 - Verify Login Page UI Elements")
    # def test_verify_login_ui_elements(self):
    #     login_page = LoginPage(self.driver) 
    #     assert login_page.is_email_displayed()
    #     assert login_page.is_password_displayed()
    #     assert login_page.is_sign_in_button_displayed()

    #     # with allure.step("Assert Email field is displayed"):
    #     #     assert login_page.is_email_displayed(), "Email field not visible"
    #     # with allure.step("Assert Password field is displayed"):
    #     #     assert login_page.is_password_displayed(), "Password field not visible"
    #     # with allure.step("Assert Sign In button is displayed"):
    #     #     assert login_page.is_sign_in_button_displayed(), "Sign In button not visible"
    
    # @allure.title("TC002 - Verify Placeholder Texts")
    # def test_placeholders(self):
    #     login_page = LoginPage(self.driver)
    #     assert "Email" in login_page.get_email_placeholder()
    #     assert "Password" in login_page.get_password_placeholder()


    @allure.title("TC003 - Verify Login Successfully with Valid Credentials")
    def test_login_valid_credentials(self):
        login_page = LoginPage(self.driver)
        login_page.login(*ConfigReader.get_email_password()) 
        login_page.wait_for_dashboard()
        assert "Dashboard" in login_page.dashboard_title()

    # @allure.title("TC004 - Verify Login Unsuccessfully with Invalid Credentials")
    # def test_login_invalid_credentials(self):
    #     login_page = LoginPage(self.driver)
    #     login_page.login(*ConfigReader.get_credentials("invalid_user"))
    #     assert login_page.is_error_message_displayed()

    # @allure.title("TC005 - Verify login with valid email - invalid password")
    # def test_login_valid_email_invalid_password(self):
    #     login_page = LoginPage(self.driver)
    #     email, password = ConfigReader.get_credentials("invalid_password")
    #     login_page.login(email, password)
    #     assert login_page.is_error_message_displayed()

    # @allure.title("TC006 - Verify login with invalid email format valid password") 
    # def test_invalid_email_format(self):
    #     login_page = LoginPage(self.driver)
    #     login_page.login(*ConfigReader.get_credentials("invalid_email_format"))  # ---> login with test data
    #     assert login_page.is_email_error_visible() # ---> verify error visible
    #     assert ConfigReader.get_error_message("email_format_error") in login_page.get_email_error_text() # ---> verify error text match json
        
        
    # @allure.title("TC007 - Verify login with blank fields")
    # def test_blank_fields(self):
    #     login_page = LoginPage(self.driver)
    #     login_page.login(*ConfigReader.get_credentials("blank"))
    #     assert login_page.is_email_error_visible()
    #     assert ConfigReader.get_error_message("email_required") in login_page.get_email_error_text()
    #     assert login_page.is_password_error_visible()
    #     assert ConfigReader.get_error_message("password_required") in login_page.get_password_error_text()

    # @allure.title("TC008 - Verify Email Only Filled → Login Should Fail")
    # def test_email_only(self):
    #     login_page = LoginPage(self.driver)
    #     login_page.enter_email(ConfigReader.get_credentials("invalid_password"))
    #     login_page.click_sign_in()
    #     assert login_page.is_password_displayed()
    #     assert ConfigReader.get_error_message("password_required") in login_page.get_password_error_text()

    # @allure.title("TC009 - Password Only Filled → Login Should Fail")
    # def test_password_only(self):
    #   login_page = LoginPage(self.driver)
    #   login_page.enter_password(ConfigReader.get_credentials("invalid_email_format"))
    #   login_page.click_sign_in()
    #   assert login_page.is_email_displayed()
    #   assert ConfigReader.get_error_message("email_required") in login_page.get_email_error_text()

    # @allure.title("TC010 - Verify Show/Hide password works correctly")    
    # def test_show_hide_password(self):
    #     login_page = LoginPage(self.driver)
    #     login_page.enter_password(ConfigReader.get_credentials("invalid_email_format"))
    #     assert login_page.is_password_masked() # ---> initially password should be masked

    #     login_page.show_hide_password_icon() # ---> click show icon → should unmask
    #     assert login_page.is_password_unmasked()

    #     login_page.show_hide_password_icon() # --->  click again → should mask again
    #     assert login_page.is_password_masked()

    # @allure.title("TC011 - Login Using ENTER Key") # ==> Failed
    # def test_enter_key_login(self):
    #     login_page = LoginPage(self.driver)
    #     email, password = ConfigReader.get_email_password()
    #     login_page.login(email, password, use_enter=True)
    #     login_page.wait_for_dashboard()
    #     sleep(1)
    #     assert "Dashboard" in login_page.dashboard_title()

    # @allure.title("TC012 - Verify Logout Functionality")
    # def test_logout_flow(self):
    #     login_page = LoginPage(self.driver)
    #     login_page.login(*ConfigReader.get_email_password())
    #     login_page.wait_for_dashboard()
    #     login_page.logout()
    #     sleep(1)
    #     assert "login" in login_page.get_current_url()
    #     self.driver.save_screenshot("login_page.png")
       

    # @allure.title("TC013 - Login Performance Should Be < 5 Seconds")
    # def test_login_performance(self):
    #     login_page = LoginPage(self.driver)
    #     start_time = time.time()
    #     login_page.login(*ConfigReader.get_email_password())     
    #     duration = time.time() - start_time
    #     assert duration < 2, f"Login too slow: {duration:.1f}s"
        