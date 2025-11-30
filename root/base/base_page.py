# base/base_page.py
import os
import allure
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from utils.config_reader import ConfigReader
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
from datetime import datetime



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
        return self.wait_for_visible(locator, timeout)
        # """Return visible element."""
        # try:
        #     return self.wait_for_visible(locator, timeout)
        # except TimeoutException as e:
        #     self._screenshot(f"find_fail_{locator}")
        #     raise TimeoutException(f"Element not visible: {locator}") from e     
       
        
    @allure.step("Find all element {locator}")
    def find_elements(self, locator, timeout: int = None):
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_all_elements_located(locator)
            )
        return self.driver.find_elements(*locator)
        # """Return list of present elements (may be empty)."""
        # try:
        #     WebDriverWait(self.driver, timeout or self.timeout).until(
        #         EC.presence_of_all_elements_located(locator)
        #     )
        #     return self.driver.find_elements(*locator)
        # except TimeoutException:
        #     return []
    @allure.step("Find first row containing text: {text}")
    def find_row_contains(self, rows, text: str):
        text = text.lower().strip()
        # Sử dụng logic tối ưu hóa (list comprehension)
        selected_row = next((
            row for row in rows
            if text in row.get_attribute("innerText").lower().strip()
        ), None)
        return selected_row


    # ------------------------------------------------------------------ #
    # INTERACTIONS
    # ------------------------------------------------------------------ #
    @allure.step("Click {locator}")
    def click(self, locator, timeout: int = None):
            element = WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        # try:
        #     element = WebDriverWait(self.driver, timeout or self.timeout).until(
        #         EC.element_to_be_clickable(locator)
        #     )
        #     element.click()
        #     self._screenshot(f"clicked_{locator}")
        # except TimeoutException:
        #     self._screenshot(f"click_fail_{locator}")
        #     raise

    @allure.step("Type '{text}' into {locator}")
    def send_keys(self, locator, text:str):
        el = self.wait_for_visible(locator)
        el.clear()
        el.send_keys(text)

    @staticmethod
    def remove_non_bmp(text: str) -> str:
        """
        Loại bỏ ký tự có codepoint > 0xFFFF (những ký tự ngoài BMP như nhiều emoji).
        Cách an toàn: giữ các ký tự có ord <= 0xFFFF.
        """
        if text is None:
            return text
        return ''.join(c for c in text if ord(c) <= 0xFFFF)
    
    def send_keys_remove_non_bmp(self, locator, text, clear_first=True):
        """
        Gồm bước: lọc ký tự ngoài BMP -> clear input -> send_keys
        """
        safe_text = self.remove_non_bmp(text)
        elem = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))
        if clear_first:
            elem.clear()
        elem.send_keys(safe_text)


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

    # @allure.step("take screenshot")
    def _screenshot(self, name="screenshot"):
        """
        Tên file screenshot sẽ được sanitize để tránh lỗi WinError 123.
        """
        # Loại ký tự không hợp lệ: <>:"/\|?* , ' ( )
        safe_name = re.sub(r'[<>:"/\\|?*\',() ]+', "_", name)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        file_name = f"{safe_name}_{timestamp}.png"
        path = os.path.join("screenshots", file_name)
        # Chụp ảnh
        self.driver.save_screenshot(path)
        # Attach vào allure
        allure.attach.file(
            path,
            name=f"{safe_name}",
            attachment_type=allure.attachment_type.PNG,
        )
    
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



    # ------------------------------------------------------------------ #
    # Hàm verify chung cho mọi table (product, collection, v.v.)
    # ------------------------------------------------------------------ # 
    def verify_record_added(self, expected_name, table_locator):
        """
        Verify that a record (product, collection, etc.) with given name
        exists in the displayed table.
        """
        elements = self.find_elements(table_locator)
        record_names = [el.text.strip() for el in elements if el.text.strip()]

        for name in record_names:
            if name.lower() == expected_name.lower():
                print(f"✅ Found new record '{expected_name}' in table!")
                return True

        raise AssertionError(
            f"❌ Record '{expected_name}' not found in table. Got: {record_names}"
        )
    

    def wait_for_page_loaded(self, timeout=None):
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )


    # ======================================
    # 1. Wait for Toast (locator passed from Page)
    # ======================================
    def wait_for_toast(self, toast_locator: tuple, expected_text: str, timeout=10):
        WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(toast_locator, expected_text)
            )
        return True
        # try:
        #     WebDriverWait(self.driver, timeout).until(
        #         EC.text_to_be_present_in_element(toast_locator, expected_text)
        #     )
        #     return True
        # except Exception:
        #     self.attach_screenshot("toast_not_found")
        #     raise AssertionError(
        #         f"❌ Toast message not found: '{expected_text}'"
        #     )

    # ======================================
    # 2. Check toast success (locator passed from Page)
    # ======================================
    def is_success_displayed(self, toast_locator: tuple, expected_text: str) -> bool:
        try:
            el = self.driver.find_element(*toast_locator)
            return expected_text.lower() in el.text.lower()
        except Exception:
            return False

    # ======================================
    # 3. Wait for page ready (toast + URL)
    # ======================================
    # --- 3.1. Toast success message ---
    def wait_for_toast_message(
        self,
        toast_locator: tuple,
        toast_text: str,
        timeout=None
    ):
        timeout = timeout or self.timeout
        try:
            if toast_locator:
                toast_el = self.find_element(toast_locator)
                if toast_text:
                    WebDriverWait(self.driver, self.timeout).until(
                        lambda d: toast_text in toast_el.text
                    )
                return True
        except Exception as e:
            print(f"Page not ready: {e}")
            return False

       # --- 3.2. URL change --- 
    def wait_for_redirect_edit_page(
        self,
        expected_url_part: str,
        timeout=None
    ):
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(expected_url_part)
            )
            return True
        except Exception:
            
            self.attach_screenshot("url_not_changed")
            raise AssertionError(
                f"❌ URL did not change to include: {expected_url_part}\n"
                f"Current: {self.driver.current_url}"
            )


    # ======================================
    # 4. Screenshot (Allure attach)
    # ======================================
    def get_screenshot_as_png(self):
        """
        Chụp màn hình hiện tại của browser và trả về dạng binary PNG.
        Dùng cho Allure.attach(..., attachment_type=PNG)
        """
        return self.driver.get_screenshot_as_png()
    
    def attach_screenshot(self, name="screenshot"):
        try:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass

    # ======================================
    # 4. Upload image
    # ======================================

    def wait_for_upload_complete(self, locator_done, timeout=None): 
        timeout = timeout or self.timeout 
        try: 
            WebDriverWait(self.driver, timeout).until( 
                EC.visibility_of_element_located(locator_done) 
                ) 
            print("✅ Upload complete")
        except TimeoutException: print("⚠️ Upload may not have completed in time")