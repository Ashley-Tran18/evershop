from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver    
        self.timeout = ConfigReader.get_timeout()
     
    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_element(*locator)
        )

    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    def send_keys(self, locator, text):
        self.wait_for_element_visible(locator).clear()
        self.wait_for_element_visible(locator).send_keys(text)
    
    def get_text(self, locator):
        return self.wait_for_element_visible(locator).text
    
    def wait_for_element_visible(self, locator, timeout=None):
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_and_click(self, locator, timeout = None):
        timeout = timeout or self.timeout
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.click()

    def wait_and_find_element(self, locator):
        # chờ element hiển thị rồi trả về element
        return self.wait_for_element_visible(locator)
    
    def verify_text(self, locator, expected_text):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        actual_text = element.text.strip()
        assert actual_text == expected_text, f"Expected '{expected_text}' but got '{actual_text}'"

    def get_error_message(self, locator):
        # wait for error message to be visible and return its text
        try:
            error_element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return error_element.text
        except TimeoutException:
            return False
