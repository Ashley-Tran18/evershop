from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader

class BaseLocator:
    def __init__(self, driver):
        self.driver = driver    
        self.timeout = ConfigReader.get_timeout()


        # General Locators
        # self.toast_msg = (By.XPATH, "//div[contains(@class, 'Toastify__toast-container')]")
        self.toast_msg = (By.XPATH, "//div[contains(@class, 'Toastify__toast-body')]")
        self.save_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button[@class = 'button primary']")
        self.edit_back_btn = (By.XPATH, "//div[contains(@class, 'flex justify-start')]//span[@class = 'flex items-center justify-center']")
        self.del_btn = (By.XPATH, "//div[contains(@class, 'border border-divider')]//span[text()= 'Delete']")
        self.remove_image_btn = (By.XPATH, "//span[@class = 'remove cursor-pointer text-critical fill-current ']")
        
        # Login Page Locators
        
        self.dashboard_header = (By.XPATH, "//h1[@class = 'page-heading-title']")
        self.login_error_message = (By.XPATH, "//div[@class = 'Toastify']//div[@class = 'Toastify__toast-body']")

        # Collections Page Locators
        self.admin_nav = (By.XPATH, "//div[@class = 'admin-navigation']")
        self.collections_menu = (By.XPATH, "//li[@class='root-nav-item nav-item']//a[@href='https://e2e.evershop.app/admin/collections']")
        self.new_collections_btn = (By.XPATH, "//div[@class = 'flex justify-end space-x-2 items-center']//span[text() = 'New Collection']")
        self.collection_name_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-name']")
        self.collection_code_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-code']")
        self.collection_des_type = (By.XPATH, "//div[contains(@class , 'row-templates')]//a[1]")
        self.collection_des_input = (By.XPATH, "//div[contains(@class, 'row grid')]//div[@class = 'ce-paragraph cdx-block']")
        self.cancel_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button[@class = 'button danger outline']")
        self.add_collection_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button[@class = 'button primary']")
        self.collection_created_msg = (By.XPATH, "//div[contains(@class, 'Toastify__toast-container')]//div[text()= 'Collection created successfully!']")
        self.collection_edit_header = (By.XPATH, "//h1[@class = 'page-heading-title']")
        self.edit_collection_back_btn = (By.XPATH, "//div[contains(@class, 'flex justify-start')]//span[@class = 'flex items-center justify-center']")
        self.collection_table = (By.XPATH, "//tbody/tr/td[3]//a")
        self.collection_rows = (By.XPATH, "//tbody/tr")
        self.collection_cell = (By.XPATH, "//./td[3]")
        self.collection_checkbox = (By.XPATH, "//./td[1]//input[@type='checkbox']")
        self.collection_del_btn = (By.XPATH, "//div[contains(@class, 'border border-divider')]//span[text()= 'Delete']")
        self.collection_confirm_del_btn = (By.XPATH, "//div[contains(@class, 'flex justify-end space-x-2')]//button[@class = 'button critical']//span[text() = 'Delete']")

        
        # Categories Page Locators
        self.categories_menu = (By.XPATH, "//li[@class='root-nav-item nav-item']//a[@href='https://e2e.evershop.app/admin/categories']")
        self.new_category_btn = (By.XPATH, "//div[@class = 'flex justify-end space-x-2 items-center']//span[text() = 'New Category']")
        self.category_name_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-name']")
        self.category_des_type = (By.XPATH, "//div[contains(@class , 'row-templates')]//a[2]")
        self.category_available_block_1 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][1]")
        self.category_des_type_plus_1 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][1]//div[@class = 'ce-toolbar__plus']")
        self.category_des_heading_select = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][1]//div[text() = 'Heading']")
        self.category_heading_input = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][1]//h2[@class = 'ce-header']")
        self.category_available_block_2 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][2]//div[@class = 'ce-paragraph cdx-block']")
        self.category_des_type_plus_2 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][2]//div[@class = 'ce-toolbar__plus']")
        self.category_des_list_select = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][2]//div[text() = 'List']")
        self.category_list_input = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1'][2]//li[@class = 'cdx-list__item']")
        self.category_url_key_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-url_key']")
        self.category_meta_title_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-meta_title']")
        self.category_meta_des_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//div[@class = 'form-field undefined']//textarea")
        self.category_upload_image = (By.XPATH, "//div[contains(@class,'uploader')]//input[@type='file']")
        self.category_uploaded_image = (By.XPATH, "//div[@class = 'uploader grid-item']")
        self.add_categry_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button[@class = 'button primary']")
        self.edit_category_back_btn = (By.XPATH, "//div[contains(@class, 'flex justify-start')]//span[@class = 'flex items-center justify-center']")
        self.category_table = (By.XPATH, "//table//tr//td[2]//a")


        # Products Page Locators
        
        self.product_name_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-name']")
        self.product_sku_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-sku']")
        self.product_price_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id='field-price']")
        self.product_weight_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id='field-weight']")
        self.select_product_category = (By.XPATH, "//div[@class = 'mt-4 relative']//a[@class = 'text-interactive']")
        self.product_men_category = (By.XPATH, "//span[text() = 'Men']/ancestor::div[contains(@class, 'grid grid-cols-8')]/descendant::button")
        self.product_description = (By.XPATH, "//div[@class = 'editor form-field-container']")
        self.product_des_type = (By.XPATH, "//div[contains(@class , 'row-templates')]//a[3]")
        self.product_available_block_1 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1']")
        self.product_des_type_plus_1 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-1']//div[@class = 'ce-toolbar__plus']")
        self.product_des_quote_select = (By.XPATH, "//div[@class='column p-3 md:col-span-1']//div[text() = 'Quote']")
        self.product_quote_input = (By.XPATH, "//div[@class =  'column p-3 md:col-span-1']//div[@class = 'cdx-input cdx-quote__text']")
        self.product_quote_caption_input = (By.XPATH, "//div[@class =  'column p-3 md:col-span-1']//div[@class = 'cdx-input cdx-quote__caption']")
        self.product_available_block_2 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-2']//div[@class = 'ce-paragraph cdx-block']")
        self.product_des_type_plus_2 = (By.XPATH, "//div[@class = 'column p-3 md:col-span-2']//div[@class = 'ce-toolbar__plus']")
        self.product_des_rawhtml_select = (By.XPATH, "//div[@class='column p-3 md:col-span-2']//div[text() = 'Raw HTML']")
        self.product_rawhtml_input = (By.XPATH, "//div[@class='column p-3 md:col-span-2']//div[@class = 'cdx-block ce-rawtool']//textarea")
        self.product_upload_image = (By.XPATH, "//div[contains(@class,'uploader')]//input[@type='file']")
        self.product_uploaded_image = (By.XPATH, "//div[@class = 'image grid-item first-item']")
        self.product_url_key_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-url_key']")
        self.product_meta_title_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-meta_title']")
        self.product_meta_des_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//div[@class = 'form-field undefined']//textarea")
        self.product_quantity_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-qty']")
        self.product_des_input = (By.XPATH, "//div[contains(@class, 'row grid')]//div[@class = 'ce-paragraph cdx-block']")
        
        self.add_product_btn = (By.XPATH, "//div[@class = 'form-submit-button flex border-t border-divider mt-4 pt-4 justify-between']//button[@class = 'button primary']")
        self.edit_product_back_btn = (By.XPATH, "//div[contains(@class, 'flex justify-start')]//span[@class = 'flex items-center justify-center']")
        

       


        # Attributes Page Locators
        self.attributes_menu = (By.XPATH, "//li[@class='root-nav-item nav-item']//a[@href='https://e2e.evershop.app/admin/attributes']")
        self.new_attribute_btn = (By.XPATH, "//div[@class = 'flex justify-end space-x-2 items-center']//span[text() = 'New Attribute']")
        self.attribute_name_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-attribute_name']")
        self.attribute_code_input = (By.XPATH, "//div[@class = 'card-session-content pt-lg']//input[@id = 'field-attribute_code']")
        self.attribute_text_type = (By.XPATH, "//div[@class = 'radio-group']//input[@id = 'field-type-text']")
        self.attribute_select_type = (By.XPATH, "//div[@class = 'radio-group']//input[@id = 'field-type-select']")
        self.attribute_multiselect_type = (By.XPATH, "//div[@class = 'radio-group']//input[@id = 'field-type-multiselect']")
        self.attribute_textarea_type = (By.XPATH, "//div[@class = 'radio-group']//input[@id = 'field-type-textarea']")
        self.attribute_group_select = (By.XPATH, "//div[@class = 'css-b62m3t-container']")
        self.attribute_default_group = (By.XPATH, "//div[@class = 'css-1nmdiq5-menu']//div[@class = 'css-d7l1ni-option']")
        self.attribute_group_input = (By.XPATH, "//div[@class = 'grid gap-5 grid-cols-1']")
        self.attribute_sort_order_input = (By.XPATH, "//div[@class= 'form-field']//input[@id = 'field-sort_order']")
        self.attribute_table = (By.XPATH, "//table//tr/td[2]//a")


        # Coupons Page Locators
        self.coupons_menu = (By.XPATH, "//li[@class='root-nav-item nav-item']//a[@href='https://e2e.evershop.app/admin/coupons']")
        self.new_coupon_btn = (By.XPATH, "//div[@class = 'flex justify-end space-x-2 items-center']//span[text() = 'New Coupon']")
        self.coupon_code_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-coupon']")
        self.coupon_des_input = (By.XPATH, "//div[@class = 'form-field undefined']//textarea[@id = 'field-description']")
        self.coupon_amount_input = (By.XPATH, "//div[@class = 'form-field']//input[@id = 'field-discount_amount']")
        self.coupon_start_date_input = (By.XPATH, "//div[@class = 'form-field undefined']//input[@id = 'field-start_date']")
        self.coupon_end_date_input = (By.XPATH, "//div[@class = 'form-field undefined']//input[@id = 'field-end_date']")
        self.coupon_free_ship_checkbox = (By.XPATH, "//div[@class = 'checkbox-item']//input[@id = 'field-free_shipping']")
        self.fixed_discount_to_entire_order = (By.XPATH, "//div[@class = 'radio-item']//input[@id = 'field-discount_type-fixed_discount_to_entire_order']")
        self.percentage_discount_to_entire_order = (By.XPATH, "//div[@class = 'radio-item']//input[@id = 'field-discount_type-percentage_discount_to_entire_order']")
        self.fixed_discount_to_specific_products = (By.XPATH, "//div[@class = 'radio-item']/input[@id='field-discount_type-fixed_discount_to_specific_products']")                                    
        self.percentage_discount_to_specific_products = (By.XPATH, "//div[@class = 'radio-item']//input[@id = 'field-discount_type-percentage_discount_to_specific_products']")
        self.buy_x_get_y = (By.XPATH, "//div[@class = 'radio-item']//input[@id = 'field-discount_type-buy_x_get_y']")
        self.max_target_product_input = (By.XPATH, "//div[@class = 'form-field form-field mb-0']//input[@id = 'field-target_products.maxQty']")
        self.add_target_product_btn = (By.XPATH, "//h3[text() = 'Target products']/following-sibling::div//div[@class = 'pl-2']")









# //     {
# //         "product_name": "Modern Dining Table",
# //         "product_sku": "SKU0002",
# //         "product_price": "349.50",
# //         "product_weight": "8",
# //         "product_description": "Wooden dining table for 6 people.",
# //         "product_quantity": "15",
# //         "product_url_key": "modern_dining_table",
# //         "product_meta_title": "Modern Dining Table",
# //         "product_meta_description": "product meta description Modern Dining Table"
# //     },
# //     {
# //         "product_name": "Office Ergonomic Chair",
# //         "product_sku": "SKU0003",
# //         "product_price": "129.00",
# //         "product_weight": "3",
# //         "product_description": "Comfortable ergonomic office chair.",
# //         "product_quantity": "20",
# //         "product_url_key": "office_ergonomic_chair",
# //         "product_meta_title": "Office Ergonomic Chair",
# //         "product_meta_description": "product meta description Office Ergonomic Chair"
# //     },
# //     {
# //         "product_name": "LED Desk Lamp",
# //         "product_sku": "SKU0004",
# //         "product_price": "39.90",
# //         "product_weight": "0.5",
# //         "product_description": "Adjustable LED light with touch control.",
# //         "product_quantity": "50",
# //         "product_url_key": "led_desk_lamp",
# //         "product_meta_title": "LED Desk Lamp",
# //         "product_meta_description": "product meta description LED Desk Lamp"
# //     },
# //     {
# //         "product_name": "Minimalist Bookshelf",
# //         "product_sku": "SKU0005",
# //         "product_price": "89.99",
# //         "product_weight": "4",
# //         "product_description": "Minimalist design bookshelf with 5 layers.",
# //         "product_quantity": "12",
# //         "product_url_key": "minimalist_bookshelf",
# //         "product_meta_title": "Minimalist Bookshelf",
# //         "product_meta_description": "product meta description Minimalist Bookshelf"
# //     }
# // ]