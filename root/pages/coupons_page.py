from selenium.webdriver.common.by import By
from base.base_page import BasePage
from base.base_locator import BaseLocator
from utils.config_reader import ConfigReader
from pages.login_page import LoginPage
from selenium.webdriver import ActionChains
from time import sleep


class CouponsPage(BasePage, BaseLocator):
    def __init__(self, driver):
        super().__init__(driver)
        BaseLocator.__init__(self, driver)

    def get_cookie(self):
        login_page = LoginPage(self.driver) 
        login_page.login(*ConfigReader.get_email_password()) 

    def navigate_to_coupons_page(self):
        self.wait_and_click(self.coupons_menu)

    def create_multi_coupon(self, coupon_data):
        # Get coupon data
        coupon_code = coupon_data['coupon_code']
        coupon_des = coupon_data['coupon_description']
        coupon_amount = coupon_data['coupon_amount']
        coupon_discount_type = coupon_data['coupon_discount_type']

        # Click on New Coupon
        self.click(self.new_coupon_btn)

        # Fill the form
        self.send_keys(self.coupon_code_input, coupon_code)
        self.send_keys(self.coupon_des_input, coupon_des)
        self.send_keys(self.coupon_amount_input, coupon_amount)

        # Map discount type string → locator
        discount_map = {
        "fixed_discount_to_entire_order": self.fixed_discount_to_entire_order,
        "percentage_discount_to_entire_order": self.percentage_discount_to_entire_order,
        "fixed_discount_to_specific_products": self.fixed_discount_to_specific_products,
        "percentage_discount_to_specific_products": self.percentage_discount_to_specific_products,
        "buy_x_get_y": self.buy_x_get_y,
        }

        # Click the correct discount type radio
        locator = discount_map.get(coupon_discount_type)
        if locator:
            self.wait_and_click(locator)
        else:
            print(f"⚠️ Unknown discount type '{coupon_discount_type}', using default (fixed_discount_to_entire_order)")
            self.wait_and_click(self.fixed_discount_to_entire_order)

        # # Select discount type
        # self.wait_and_click(self.fixed_discount_to_entire_order)

        # Submit form
        self.wait_and_click(self.save_btn)

        # Verify toast msg & edit URL
        self.wait_for_page_ready_after_submit(
            toast_text="Coupon created successfully",
            expected_url_part="coupon/edits"
        )

        # Back to Coupons page
        self.wait_and_click(self.edit_back_btn)


        