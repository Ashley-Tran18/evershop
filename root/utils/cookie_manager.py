# import pickle
# import os

# class CookieManager:
#     COOKIE_PATH = os.path.join(os.path.dirname(__file__), "..", "cookies", "login_cookies.pkl")

#     @staticmethod
#     def save_cookies(driver):
#         os.makedirs(os.path.dirname(CookieManager.COOKIE_PATH), exist_ok=True)
#         pickle.dump(driver.get_cookies(), open(CookieManager.COOKIE_PATH, "wb"))
#         print(f" Cookies đã lưu: {CookieManager.COOKIE_PATH}")

#     @staticmethod
#     def load_cookies(driver, domain_url):
#         driver.get(domain_url)
#         if not os.path.exists(CookieManager.COOKIE_PATH):
#             raise FileNotFoundError("Chưa có file cookies! Chạy test login trước.")
        
#         cookies = pickle.load(open(CookieManager.COOKIE_PATH, "rb"))
#         for cookie in cookies:
#             if 'expiry' in cookie:
#                 del cookie['expiry']
#             driver.add_cookie(cookie)
#         driver.refresh()
#         print(" Load cookies thành công!")


# utils/cookie_manager.py
import pickle
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CookieManager:
    COOKIE_PATH =  os.path.join(os.path.dirname(__file__), "..", "cookies", "login_cookies.pkl")

    @staticmethod
    def save_cookies(driver):
        os.makedirs(os.path.dirname(CookieManager.COOKIE_PATH), exist_ok=True)
        pickle.dump(driver.get_cookies(), open(CookieManager.COOKIE_PATH, "wb"))
        print(" Cookies đã lưu!")

    @staticmethod
    def load_cookies(driver, domain_url):
        driver.get(domain_url)
        if not os.path.exists("cookies/login_cookies.pkl"):
            raise FileNotFoundError("Chạy: pytest .\tests\test_login.py  ")

        cookies = pickle.load(open("cookies/login_cookies.pkl", "rb"))
        for c in cookies:
            cookie = {
                "name": c["name"],
                "value": c["value"],
                "path": c.get("path", "/"),
                "secure": c.get("secure", True),
                "httpOnly": c.get("httpOnly", True),
                "sameSite": c.get("sameSite", "Lax")
            }
            # BỎ HẲN DOMAIN & EXPIRY → Chrome tự điền đúng domain hiện tại
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print("Skip cookie lỗi:", e)

        driver.refresh()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'Welcome back')]"))
        )
        print("ĐÃ VÀO DASHBOARD – COOKIE HOẠT ĐỘNG 100%!")