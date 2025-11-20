from base.base_test import BaseTest
from pages.coupons_page import CouponsPage
from utils.config_reader import ConfigReader
import allure
from time import sleep

@allure.story("Verify user can open Collection page after skipping login via cookies")
class TestCoupons(BaseTest):
    def test_coupons_page(self):
        
        "Step 1: login to the website"
        coupon = CouponsPage(self.driver)
        coupon.get_cookie()

        "Step 2: navigate to coupons page"
        coupon.navigate_to_coupons_page()

        "Step 3: click on New Coupon button & create multi coupon"
        coupons = ConfigReader.get_coupon_data()
        for data in coupons:
            coupon.create_multi_coupon(data)