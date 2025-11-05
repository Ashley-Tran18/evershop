# import pytest
# import time
# import urllib.parse
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager


# BASE_URL = "https://e2e.evershop.app"
# ADMIN_URL = f"{BASE_URL}/admin"

# # 👉 cookie bạn có (thay ở đây cho đúng)
# COOKIE_STRING = "asid=s%3AarCFlsQEBU_SwySH_zCVknnKZbPwyRFP.jGDro2Ra8WchAvynSHQb53PFEp9YEIdL%2Fy8V%2BwxaUBU"


# def parse_cookie_string(cookie_str):
#     """Parse cookie string dạng name=value"""
#     if "=" not in cookie_str:
#         pytest.skip("Cookie string invalid")

#     name, val = cookie_str.split("=", 1)
#     return {
#         "name": name.strip(),
#         "value": urllib.parse.unquote(val.strip()),
#         "path": "/",
#         "secure": True,
#         "httpOnly": True,
#     }


# @pytest.fixture(scope="session")
# def driver():
#     """Tạo WebDriver (Chrome) cho toàn bộ session"""
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless=new")  # bỏ dòng này nếu muốn thấy browser
#     options.add_argument("--window-size=1920,1080")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     yield driver
#     driver.quit()


# def test_login_with_cookie(driver):
#     """Test: Dùng cookie thủ công để vào trang admin"""

#     driver.get(BASE_URL)
#     time.sleep(1)

#     cookie = parse_cookie_string(COOKIE_STRING)

#     # Thử add cookie (có thể fail nếu domain khác, nên bắt lỗi thử lại)
#     try:
#         driver.add_cookie(cookie)
#     except Exception:
#         # thử lại mà không set domain
#         cookie.pop("domain", None)
#         driver.add_cookie(cookie)

#     driver.get(ADMIN_URL)
#     time.sleep(3)

#     current = driver.current_url
#     title = driver.title

#     print(f"➡️ URL hiện tại: {current}")
#     print(f"➡️ Title: {title}")
#     driver.save_screenshot("login_cookie_result.png")

#     # ✅ Kiểm tra điều kiện login thành công (ví dụ: không bị redirect về /login)
#     assert "login" not in current.lower(), "Cookie không hợp lệ — vẫn bị redirect về trang login"
#     assert "Dashboard" in title, "Không vào được dashboard admin"


import pytest
import time
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://e2e.evershop.app"
ADMIN_URL = f"{BASE_URL}/admin"
COOKIE_FILE = "cookie_value.json"  # file JSON vừa được tạo


import json
import pytest
import os

BASE_DIR = os.path.dirname(__file__)
COOKIE_FILE = os.path.join(BASE_DIR, "cookie_value.json")

def load_cookie_from_json(file_path=COOKIE_FILE):
    """Đọc cookie string từ file JSON"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"DEBUG JSON DATA: {data}")  # giúp kiểm tra thực tế file

        cookie_str = data.get("header_cookie")
        if not cookie_str:
            raise ValueError(f"⚠️ Không tìm thấy key 'header_cookie' trong {file_path}. Data: {data}")

        return cookie_str.strip()

    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ Không tìm thấy file {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"⚠️ File {file_path} không phải JSON hợp lệ")


def parse_cookie_string(cookie_str):
    """Parse cookie string dạng name=value"""
    if "=" not in cookie_str:
        pytest.skip("⚠️ Cookie string invalid (không có '=')")

    name, val = cookie_str.split("=", 1)
    return {
        "name": name.strip(),
        "value": urllib.parse.unquote(val.strip()),
        "path": "/",
        "secure": True,
        "httpOnly": True,
    }


@pytest.fixture(scope="session")
def driver():
    """Tạo WebDriver (Chrome) cho toàn bộ session"""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # bỏ dòng này nếu muốn thấy browser
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


def test_login_with_cookie(driver):
    """Test: Dùng cookie trong file JSON để vào trang admin"""

    cookie_str = load_cookie_from_json(COOKIE_FILE)
    cookie = parse_cookie_string(cookie_str)

    driver.get(BASE_URL)
    time.sleep(1)

    driver.delete_all_cookies()  # Xóa toàn bộ cookies của trình duyệt
    driver.execute_script("window.localStorage.clear();")  # Xóa localStorage
    driver.execute_script("window.sessionStorage.clear();")  # Xóa sessionStorage
    time.sleep(1)

    # Thử add cookie (bắt lỗi domain)
    try:
        driver.add_cookie(cookie)
    except Exception:
        cookie.pop("domain", None)
        driver.add_cookie(cookie)

    driver.get(ADMIN_URL)
    time.sleep(3)

    current = driver.current_url
    title = driver.title

    print(f"➡️ URL hiện tại: {current}")
    print(f"➡️ Title: {title}")
    driver.save_screenshot("login_cookie_result.png")

    # ✅ Kiểm tra login thành công
    assert "login" not in current.lower(), "❌ Cookie không hợp lệ — bị redirect về /login"
    assert "Dashboard" in title, "❌ Không vào được dashboard admin"
