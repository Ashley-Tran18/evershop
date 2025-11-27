# factories/product_factory.py
import time
from utils.config_reader import ConfigReader

class ProductFactory:
    @staticmethod
    def create_simple_product():
        product_data = ConfigReader.get_product_data()
        timestamp = int(time.time())
        valid_product_name = product_data['product_name']['normal']
        
        
        return {
            # 'name': product_data['product_name'],
            'name': f"{valid_product_name}_{timestamp}",
            'sku': f"TEST_{timestamp}",
            'price': product_data['product_price'],
            'weight': product_data['product_weight'],
            'image': product_data['product_image'],
            'quantity': product_data['product_quantity'],
            # 'url_key': f"{product_data['product_name'].replace(' ', '-').lower()}-{timestamp}",
            'url_key': f"{valid_product_name.replace(' ', '-').lower()}-{timestamp}",
            # 'meta_title': product_data['product_meta_title']
            'meta_title': valid_product_name
        }

        # product_sku = f"TEST_{int(time.time())}"
        # product_url_key =  f"{product_name.replace(' ', '-').lower()}-{int(time.time())}"

