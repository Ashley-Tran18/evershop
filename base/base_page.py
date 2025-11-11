from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    def __init__(self, driver):
        self.driver = driver    
        self.timeout = ConfigReader.get_timeout()
        self.actions = ActionChains(driver)
     
    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_element(locator)
        )
    
    def find_elements(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*locator)
        )

    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    def send_keys(self, locator, text):
        # self.wait_for_element_visible(locator).clear()
        self.wait_for_element_visible(locator).send_keys(text)
    
    def get_text(self, locator):
        return self.presence_of_element(locator).text
    
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

    def wait_and_find_elements(self, locator, timeout=None):
        timeout = timeout or self.timeout
        # chờ element hiển thị rồi trả về element
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
    
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
    
    def presence_of_element(self, locator, timeout=None):
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
   
    def wait_for_page_loaded(self, timeout=None):
        timeout = timeout or self.timeout
        """
        Chờ trang load hoàn toàn (document.readyState = 'complete')
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print("⚠️ Warning: Page did not finish loading within timeout")



    def hover_to_element(self, locator):
        """Hover đến element bằng locator"""
        element = self.wait_for_element_visible(locator)
        self.actions.move_to_element(element).perform()
        return element  # Trả về element để dùng tiếp nếu cần

    def click_with_hover(self, hover_locator, click_locator):
        """Hover đến phần tử cha, rồi click phần tử con"""
        self.hover_to_element(hover_locator)
        element_to_click = self.wait_for_element_visible(click_locator)
        self.actions.move_to_element(element_to_click).click().perform()

    def reset_actions(self):
        """Reset chuỗi hành động (nếu cần dùng lại sạch)"""
        self.actions = ActionChains(self.driver)