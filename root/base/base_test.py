# base_test.py
from selenium import webdriver
from utils.config_reader import ConfigReader
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest
import allure
import os


class BaseTest:
    @pytest.fixture(autouse=True)
    def driver(self,request):
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        prefs = {
            "credentials_enable_service": False,         # Tắt dịch vụ lưu mật khẩu
            "profile.password_manager_enabled": False    # Tắt gợi ý lưu mật khẩu
        }
        options.add_experimental_option("prefs", prefs)
        
        # Các args cho Linux/headless
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')  # Thêm để ổn định headless
        options.add_argument('--disable-features=VizDisplayCompositor')  # Fix lỗi render
        
        self.driver = webdriver.Chrome(service=Service(), options=options)
        
        base_url = ConfigReader.get_base_url()
        self.driver.get(base_url)

        # Cho phép các class test kế thừa sử dụng driver
        request.cls.driver = self.driver
        yield
        self.driver.quit()


#     # @pytest.fixture(autouse=True)
#     def login_with_cookies(self, driver):
#         # Load cookies cho mọi test
#         self.load_cookies(driver, "https://e2e.evershop.app/")
#         # Đảm bảo đã vào trang cần test
#         driver.get("https://e2e.evershop.app/admin")


