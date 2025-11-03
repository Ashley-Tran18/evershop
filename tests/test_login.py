
from base.base_test import BaseTest
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from utils.cookie_manager import CookieManager
import allure

class TestLogin(BaseTest):
    @allure.story("Test Login")
    @allure.severity(allure.severity_level.CRITICAL)
    
    def test_login(self):
        login_page = LoginPage(self.driver) 
        login_page.login(*ConfigReader.get_email_password()) 
        
        assert "admin" in self.driver.current_url.lower()
        print("✅ Login thành công!")

        # Lưu cookies
        CookieManager.save_cookies(self.driver)
