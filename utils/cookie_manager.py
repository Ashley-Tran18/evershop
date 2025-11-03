import json
import os

class CookieManager:
    COOKIE_PATH = os.path.join("utils", "cookies.json")

    @staticmethod
    def save_cookies(driver):
        """Lưu cookies hiện tại của trình duyệt sau khi login thành công"""
        cookies = driver.get_cookies()
        with open(CookieManager.COOKIE_PATH, "w") as f:
            json.dump(cookies, f)
        print("💾 Cookies saved to cookies.json")

    @staticmethod
    def load_cookies(driver, base_url):
        """Load cookies từ file để bỏ qua login"""
        if not os.path.exists(CookieManager.COOKIE_PATH):
            print("⚠️ cookies.json not found")
            return False

        with open(CookieManager.COOKIE_PATH, "r") as f:
            cookies = json.load(f)

        driver.get(base_url)
        for cookie in cookies:
            # Selenium không chấp nhận sameSite
            cookie.pop("sameSite", None)
            driver.add_cookie(cookie)

        print("✅ Cookies loaded into browser")
        return True

