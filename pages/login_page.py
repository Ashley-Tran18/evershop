# from base.base_page import BasePage  
# from base.base_locator import BaseLocator

# class LoginPage(BasePage, BaseLocator):
#     def __init__(self, driver):
#         super().__init__(driver)
#         # BasePage.__init__(self, driver)
#         BaseLocator.__init__(self, driver)
    

#     def login(self, email, password):
#         "TC1: Enter valid email and password, then click Login button"
#         self.send_keys(self.email_input, email)
#         self.send_keys(self.password_input, password)
#         self.click(self.login_btn)
        
#     def verify_login_successful(self):
#         self.wait_for_element_visible(self.dashboard_header)
#         self.verify_text(self.dashboard_header, "Dashboard")
        
#     def get_invalid_login_error_message(self):
#         self.get_error_message(self.invalid_login_error)

from base.base_page import BasePage  
from base.base_locator import BaseLocator

class LoginPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        # BasePage.__init__(self, driver)
        BaseLocator.__init__(self, driver)
    

    def login(self, email, password):
        "Step 1: Enter valid email and password, then click Login button"
        self.send_keys(self.email_input, email)
        self.send_keys(self.password_input, password)
        self.click(self.login_btn)
        
    
    def is_logged_in(self):
        "Verify login successfully"
        try:
            self.wait_for_element_visible(self.dashboard_header)
            return True
        except:
            return False
        
        
    def get_invalid_login_error_message(self):
         "Verify error message appears when entering invalid password"
         self.get_error_message(self.invalid_login_error)