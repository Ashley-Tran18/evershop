# base/base_page.py
import os
import time
import allure
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """
    Core page-object foundation.
    All page classes inherit from this.
    """
    # ------------------------------------------------------------------ #
    # INITIALISATION
    # ------------------------------------------------------------------ #
    def __init__(self, driver):
        self.driver = driver    
        self.timeout = ConfigReader.get_timeout()
        self.wait = WebDriverWait(driver, self.timeout)
        self.actions = ActionChains(driver)
       
    # ------------------------------------------------------------------ #
    # NAVIGATION
    # ------------------------------------------------------------------ #
    @allure.step("Navigate to {url}")
    def navigate_to(self, url:str = None):
        """Open URL. If None → use base_url from config."""
        url =  ConfigReader.get_base_url()
        self.driver.get(url)

    @allure.step("Refresh current page")   
    def refresh(self):
        self.driver.refresh()

    # ------------------------------------------------------------------ #
    # WAITS & ELEMENT FINDERS
    # ------------------------------------------------------------------ #
    @allure.step("Wait for visibility of {locator}")
    def wait_for_visible(self, locator, timeout: int = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Wait for clickable of {locator}")
    def wait_for_clickable(self, locator, timeout: int = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @allure.step("Wait for presence of {locator}")
    def wait_for_presence(self, locator, timeout: int = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )
    

    @allure.step("Find element {locator}")
    def find_element(self, locator, timeout: int = None):
        """Return visible element."""
        try:
            return self.wait_for_visible(locator, timeout)
        except TimeoutException as e:
            self._screenshot(f"find_fail_{locator}")
            raise TimeoutException(f"Element not visible: {locator}") from e
        
    @allure.step("Find all element {locator}")
    def find_elements(self, locator, timeout: int = None):
        """Return list of present elements (may be empty)."""
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    # ------------------------------------------------------------------ #
    # INTERACTIONS
    # ------------------------------------------------------------------ #
    @allure.step("Click {locator}")
    def click(self, locator, timeout: int = None):
        try:
            element = WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self._screenshot(f"clicked_{locator}")
        except TimeoutException:
            self._screenshot(f"click_fail_{locator}")
            raise

    @allure.step("Type '{text}' into {locator}")
    def send_keys(self, locator, text:str):
        el = self.wait_for_visible(locator)
        el.clear()
        el.send_keys(text)
    
    @allure.step("Get text of {locator}")
    def get_text(self, locator):
        return self.wait_for_visible(locator).text.strip()
    
    def assert_text_contains(self, locator, expected_text):
        assert expected_text in self.get_text(locator), \
            f"❌ Expected '{expected_text}' in '{self.get_text(locator)}'"

    
    @allure.step("Get attribute '{attr}' of {locator}")
    def get_attribute(self, locator, attr:str):
        return self.wait_for_visible(locator).get_attribute(attr)
    
    @allure.step("Is {locator} visible?")
    def is_visible(self, locator, timeout:int = 3) -> bool:
        try:
            return self.wait_for_visible(locator, timeout).is_displayed()
        except TimeoutException:
            return False
        
    @allure.step("Is {locator} enabled?")
    def is_enabled(self, locator) -> bool:
        return self.wait_for_visible(locator).is_enabled()
    
    @allure.step("Is {locator} displayed?")
    def is_displayed(self, locator):
        return self.find_element(locator).is_displayed()
    
    @allure.step("Wait for {locator} url")
    # def wait_for_url_contains(self, text, timeout=None):
    #     try:
    #         WebDriverWait(self.driver, timeout or self.timeout).until(
    #             EC.url_contains(text)
    #         )
    #     except:
    #         raise AssertionError(f"URL does not contain: {text}")
    def wait_for_url_contains(self, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def focus_login_button_with_tab(self, tab_count=3):
        actions = ActionChains(self.driver)
        for _ in range(tab_count):
            actions.send_keys(Keys.TAB)
        actions.perform()

    @allure.step("take screenshot")
    def _screenshot(self, name):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(path)
        allure.attach.file(path, name=f"screenshot_{name}", attachment_type=allure.attachment_type.PNG)
    
    # ------------------------------------------------------------------ #
    # DROPDOWN (Select)
    # ------------------------------------------------------------------ #
    @allure.step("Select '{option}' by visible text in dropdown {locator}")
    def select_by_visible_text(self, locator, option: str):
        Select(self.wait_for_visible(locator)).select_by_visible_text(option)

    @allure.step("Select value='{value}' in dropdown {locator}")
    def select_by_value(self, locator, value:str):
        Select(self.wait_for_visible(locator)).select_by_value(value)

    @allure.step("Select index={index} in dropdown {locator}")
    def select_by_index(self, locator, index:int):
        Select(self.wait_for_visible(locator)).select_by_index(index)