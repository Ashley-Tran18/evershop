# base_test.py
from selenium import webdriver
from utils.config_reader import ConfigReader
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest
import allure
import os


class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self,request):
        
        options = Options()
        options.add_argument("--start-maximized")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        options.add_argument("--incognito")
        prefs = {
            "credentials_enable_service": False,         # Tắt dịch vụ lưu mật khẩu
            "profile.password_manager_enabled": False    # Tắt gợi ý lưu mật khẩu
        }
        options.add_experimental_option("prefs", prefs)
        
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        base_url = ConfigReader.get_base_url()
        self.driver.get(base_url)
        # self.driver.maximize_window()

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


