from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
prefs = {
    "credentials_enable_service": False,         # Tắt dịch vụ lưu mật khẩu
    "profile.password_manager_enabled": False    # Tắt gợi ý lưu mật khẩu
}
options.add_experimental_option("prefs", prefs)

# Các args cho Linux/headless
options.add_argument('--headless-new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')  # Thêm để ổn định headless
options.add_argument('--disable-features=VizDisplayCompositor')  # Fix lỗi render
# options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
driver.get("https://google.com")
print("Current window size →", driver.get_window_size()["width"], "×", driver.get_window_size()["height"])
# Example output: Current window size → 1920 × 1080