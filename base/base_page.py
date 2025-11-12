from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from base.base_locator import BaseLocator
from selenium.webdriver.common.by import By
import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver    
        self.timeout = ConfigReader.get_timeout()
        self.actions = ActionChains(driver)
        BaseLocator.__init__(self, driver)

     
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
        self.wait_for_element_visible(locator).clear()
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

    
    def wait_for_upload_complete(self, locator_done, timeout=None):
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator_done)
            )
            print("✅ Upload complete")
        except TimeoutException:
            print("⚠️ Upload may not have completed in time")

    def upload_image(self, upload_input_locator, uploaded_image_locator, image_name):
        """
        Upload 1 ảnh và chờ upload hoàn tất.
        - upload_input_locator: locator của thẻ <input type='file'>
        - uploaded_image_locator: locator của thumbnail / preview sau khi upload
        - image_name: tên file ảnh (VD: "sofa.png") nằm trong thư mục /images
        """

        try:
            base = os.path.abspath("images")
            full_path = os.path.join(base, image_name)

            # Tìm input upload và gửi đường dẫn file
            upload_input = self.presence_of_element(upload_input_locator)
            upload_input.send_keys(full_path)
            print(f"📤 Uploading image: {image_name}")

            # Chờ ảnh upload hoàn tất (thumbnail hiển thị)
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(uploaded_image_locator)
            )
            print("✅ Upload completed successfully!")
            

        except TimeoutException:
            print("⚠️ Upload may not have completed in time.")
        except Exception as e:
            print(f"❌ Upload failed: {str(e)}")




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


    # --- Hàm chờ trang load cơ bản ---
    def wait_for_page_loaded(self, timeout=None):
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print("⚠️ Warning: Page did not finish loading within timeout")

    # --- Hàm chờ sau khi Submit ---
    def wait_for_page_ready_after_submit(self, expected_url_part=None, toast_text=None, timeout=None):
        """
        Chờ redirect + verify toast message sau khi click Submit
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)

        try:
            # 1️⃣ Chờ toast message xuất hiện
            # ✅ dùng self.toast_msg (được định nghĩa ở page con)
            # toast_locator = getattr(self, "toast_msg", None)
            toast_locator = (By.XPATH, "//div[contains(@class, 'Toastify__toast-container')]")
            if toast_text and toast_locator:
                wait.until(EC.visibility_of_element_located(toast_locator))
                toast_el = self.presence_of_element(toast_locator)
                if toast_text.lower() in toast_el.text.lower():
                    print(f"✅ Toast appeared: '{toast_el.text}'")
                    self.driver.save_screenshot("toast msg.png")
        
                else:
                    print(f"⚠️ Toast text didn't match: '{toast_el.text}'")
            
            # 2️⃣ Chờ URL thay đổi (redirect)
            if expected_url_part:
                wait.until(EC.url_contains(expected_url_part))
                print(f"✅ Redirected to URL containing: {expected_url_part}")
                self.driver.save_screenshot("edit page.png")

            # 3️⃣ Đảm bảo DOM đã hoàn tất
            self.wait_for_page_loaded(timeout)

            print("🎯 Page is fully ready after submit")

        except TimeoutException:
            print("⚠️ Timeout: Page did not finish loading or toast not found")



    # ✅ Hàm verify chung cho mọi table (product, collection, v.v.)
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