# import pickle
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager


# def save_cookies_to_file(
#     login_url="https://e2e.evershop.app/admin/login",
#     output_path="cookies.pkl",
#     wait_time=25
# ):
#     """
#     Mở trình duyệt → chờ người dùng đăng nhập thủ công → lưu cookies vào file pickle.

#     Args:
#         login_url (str): URL trang login.
#         output_path (str): Nơi lưu file cookie, mặc định 'cookies.pkl'.
#         wait_time (int): Thời gian chờ (giây) để người dùng hoàn tất login.
#     """

#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#     try:
#         # 1️⃣ Mở trang login
#         driver.get(login_url)
#         print(f"🔹 Trình duyệt đã mở tại: {login_url}")
#         print(f"⏳ Vui lòng đăng nhập thủ công trong {wait_time} giây...")

#         # 2️⃣ Chờ user login
#         time.sleep(wait_time)

#         # 3️⃣ Lấy cookies sau khi login
#         cookies = driver.get_cookies()
#         print(f"✅ Đã lấy {len(cookies)} cookie(s). Lưu vào file...")

#         # 4️⃣ Ghi cookies ra file pickle
#         with open(output_path, "wb") as f:
#             pickle.dump(cookies, f)

#         print(f"💾 Cookies đã được lưu tại: {output_path}")

#     finally:
#         driver.quit()
#         print("🚪 Đã đóng trình duyệt.")

#     # ở cuối file save_cookies_to_file.py
# def test_save_cookie():
#     save_cookies_to_file(output_path= r"C:\Users\ThaoTran\Downloads\Automation file\e2e\load_cookies\cookies.pkl", wait_time=30)


# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager


# def save_cookies_to_file(
#     login_url="https://e2e.evershop.app/admin/login",
#     output_path="cookies.json",
#     wait_time=25
# ):
#     """
#     Mở trình duyệt → chờ người dùng đăng nhập thủ công → lưu cookies vào file JSON.

#     Args:
#         login_url (str): URL trang login.
#         output_path (str): Nơi lưu file cookie, mặc định 'cookies.json'.
#         wait_time (int): Thời gian chờ (giây) để người dùng hoàn tất login.
#     """

#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#     try:
#         # 1️⃣ Mở trang login
#         driver.get(login_url)
#         print(f"🔹 Trình duyệt đã mở tại: {login_url}")
#         print(f"⏳ Vui lòng đăng nhập thủ công trong {wait_time} giây...")

#         # 2️⃣ Chờ user login
#         time.sleep(wait_time)

#         # 3️⃣ Lấy cookies sau khi login
#         cookies = driver.get_cookies()
#         print(f"✅ Đã lấy {len(cookies)} cookie(s). Lưu vào file...")

#         # 4️⃣ Ghi cookies ra file JSON
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(cookies, f, indent=4, ensure_ascii=False)

#         print(f"💾 Cookies đã được lưu tại: {output_path}")

#     finally:
#         driver.quit()
#         print("🚪 Đã đóng trình duyệt.")


# # ở cuối file save_cookies_to_file.py
# def test_save_cookie():
#     save_cookies_to_file(
#         output_path=r"C:\Users\ThaoTran\Downloads\Automation file\e2e\load_cookies\cookies.json",
#         wait_time=30
#     )

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def save_cookies_to_file(
    login_url="https://e2e.evershop.app/admin/login",
    output_path="cookie_value.json",
    wait_time=25
):
    """
    Mở trình duyệt → chờ người dùng đăng nhập thủ công → lưu cookie sid + asid vào file JSON.
    """

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 1️⃣ Mở trang login
        driver.get(login_url)
        print(f"🔹 Trình duyệt đã mở tại: {login_url}")
        print(f"⏳ Vui lòng đăng nhập thủ công trong {wait_time} giây...")

        # 2️⃣ Chờ user login
        time.sleep(wait_time)

        # 3️⃣ Đợi cho tới khi vào trang /admin
        if "/admin" not in driver.current_url:
            print("⚠️ Có vẻ bạn chưa login xong. Đang chờ thêm 10s...")
            time.sleep(10)

        # 4️⃣ Lấy toàn bộ cookie
        cookies = driver.get_cookies()
        print(f"✅ Đã lấy {len(cookies)} cookie(s).")

        # 5️⃣ Lọc 2 cookie quan trọng
        sid_cookie = next((c for c in cookies if c["name"] == "sid"), None)
        asid_cookie = next((c for c in cookies if c["name"] == "asid"), None)

        if sid_cookie or asid_cookie:
            # Ghép chúng lại dạng header string
            cookie_parts = []
            if sid_cookie:
                cookie_parts.append(f"{sid_cookie['name']}={sid_cookie['value']}")
            if asid_cookie:
                cookie_parts.append(f"{asid_cookie['name']}={asid_cookie['value']}")

            header_cookie_string = "; ".join(cookie_parts)
            header_cookie = {"header_cookie": header_cookie_string}

            # 6️⃣ Lưu cookie vào file JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(header_cookie, f, indent=4, ensure_ascii=False)

            print(f"💾 Đã lưu cookie hợp lệ: {header_cookie_string}")
            print(f"📁 File lưu tại: {output_path}")
        else:
            print("⚠️ Không tìm thấy cookie 'sid' hoặc 'asid' — hãy đảm bảo đã login vào trang admin thành công.")

    finally:
        driver.quit()
        print("🚪 Đã đóng trình duyệt.")


# Ở cuối file
def test_save_cookie():
    save_cookies_to_file(
        output_path=r"C:\Users\ThaoTran\Downloads\Automation file\e2e\load_cookies\cookie_value.json",
        wait_time=30
    )
