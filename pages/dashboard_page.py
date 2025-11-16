import pytest
import time
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("login_page")
class TestLogin:

    def test_verify_login_ui_elements(self, login_page):
        assert login_page.is_email_displayed()
        assert login_page.is_password_displayed()
        assert login_page.is_sign_in_button_displayed()

    def test_verify_placeholder_texts(self, login_page):
        assert login_page.get_email_placeholder() == login_page.test_data["placeholders"]["email"]
        assert login_page.get_password_placeholder() == login_page.test_data["placeholders"]["password"]

    def test_login_valid_credentials(self, login_page):
        data = login_page.test_data["valid_user"]
        login_page.login(data["email"], data["password"])
        login_page.wait_for_dashboard()
        assert "/dashboard" in login_page.get_current_url()

    def test_login_invalid_credentials(self, login_page):
        data = login_page.test_data["invalid_user"]
        login_page.login(data["email"], data["password"])
        assert login_page.is_error_message_displayed()
        assert login_page.test_data["error_messages"]["invalid_credentials"] in login_page.get_error_message()

    def test_login_valid_email_invalid_password(self, login_page):
        data = login_page.test_data["invalid_password"]
        login_page.login(data["email"], data["password"])
        assert login_page.is_error_message_displayed()

    def test_invalid_email_format(self, login_page):
        data = login_page.test_data["invalid_email_format"]
        login_page.enter_email(data["email"])
        login_page.enter_password(data["password"])
        assert not login_page.is_sign_in_button_enabled() or login_page.is_email_error_visible()

    def test_blank_fields(self, login_page):
        login_page.click_sign_in()
        assert login_page.is_email_error_visible()
        assert login_page.is_password_error_visible()

    def test_email_only(self, login_page):
        login_page.enter_email(login_page.test_data["valid_user"]["email"])
        login_page.click_sign_in()
        assert login_page.test_data["error_messages"]["password_required"] in login_page.get_error_message()

    def test_password_only(self, login_page):
        login_page.enter_password(login_page.test_data["valid_user"]["password"])
        login_page.click_sign_in()
        assert login_page.test_data["error_messages"]["email_required"] in login_page.get_error_message()

    def test_password_masking(self, login_page):
        login_page.enter_password("secret")
        assert login_page.is_password_masked()

    def test_enter_key_submits(self, login_page):
        data = login_page.test_data["valid_user"]
        login_page.login(data["email"], data["password"], use_enter=True)
        login_page.wait_for_dashboard()
        assert "/dashboard" in login_page.get_current_url()

    @pytest.mark.skip("Session persistence requires cookie handling across sessions")
    def test_session_persistence(self, login_page, driver_init):
        # Implementation requires saving/loading cookies
        pass

    def test_logout_flow(self, login_page, driver_init):
        # Login first
        data = login_page.test_data["valid_user"]
        login_page.login(data["email"], data["password"])
        login_page.wait_for_dashboard()

        # Find and click logout (adjust selector as needed)
        logout_btn = (By.XPATH, "//a[contains(text(), 'Logout')]")
        login_page.click(logout_btn)
        login_page.wait.until(EC.url_contains("/admin"))
        assert "login" in login_page.get_current_url() or "admin" in login_page.get_current_url()

    def test_unauthorized_access(self, login_page, driver_init):
        from utilities.config_reader import ConfigReader
        base = ConfigReader.get("base_url").rstrip("/")
        dashboard = ConfigReader.get("dashboard_url").lstrip("/")
        driver_init.get(f"{base}/{dashboard}")
        assert "login" in login_page.get_current_url() or "admin" in login_page.get_current_url()

    def test_login_performance(self, login_page):
        data = login_page.test_data["valid_user"]
        start = time.time()
        login_page.login(data["email"], data["password"])
        login_page.wait_for_dashboard()
        duration = time.time() - start
        assert duration < 5, f"Login took {duration:.2f}s, expected < 5s"