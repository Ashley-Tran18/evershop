# conftest.py
import pytest
import allure

# Hook để lưu kết quả từng giai đoạn test (setup/call/teardown)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print("Hook file loaded")
   
    outcome = yield
    rep = outcome.get_result()
    print(f"Test  {item.name} - {rep.when} - {rep.outcome}")
    setattr(item, f"rep_{rep.when}", rep)
    #setattr(item, "rep_call", rep)

def pytest_exception_interact(node, call, report):
    driver = getattr(node.instance, "driver", None)
    if driver:
        try:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"failure_{node.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"[!] Cannot capture screenshot: {e}")

