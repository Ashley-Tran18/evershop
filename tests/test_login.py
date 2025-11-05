
# from base.base_test import BaseTest
# from pages.login_page import LoginPage
# from utils.config_reader import ConfigReader
# from utils.cookie_manager import CookieManager
# import allure

# class TestLogin(BaseTest):
#     @allure.story("Successful login with valid admin credentials")
#     @allure.severity(allure.severity_level.CRITICAL)
    
#     def test_login(self):
#         login_page = LoginPage(self.driver) 
#         login_page.login(*ConfigReader.get_email_password()) 
        
#         login_page.verify_login_successful()
#         login_page.get_invalid_login_error_message()
#         print("✅ Login thành công!")
#         self.driver.save_screenshot("login_success.png")

        

#         # # # Lưu cookies
#         # CookieManager.save_cookies(self.driver)



from base.base_test import BaseTest
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
import allure
from time import sleep

class TestLogin(BaseTest):
    @allure.story("Successful login with valid admin credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    
    def test_login(self):
        login_page = LoginPage(self.driver) 
        attempts = ConfigReader.get_login_attempts()

        logged_in = False
        for index, attempt in enumerate(attempts, 1):
            print(f"\n🔄 Attempt {index}")
            login_page.login(attempt["email"], attempt["password"])

            if login_page.is_logged_in():
                print(f"✅ Login successful on attempt {index}")
                logged_in = True
                break
            else:
                error_text = login_page.get_invalid_login_error_message() 
                print(f"❌ Error message (attempt {index}): {error_text}")
                self.driver.refresh()
        assert logged_in, "❌ Login failed after all attempts"