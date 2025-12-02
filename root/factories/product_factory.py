# factories/product_factory.py
import time
from utils.config_reader import ConfigReader
from typing import Dict, List

class ProductFactory:
    # @staticmethod
    # def create_simple_product():
    #     product_data = ConfigReader.get_product_data()
    #     timestamp = int(time.time())
    #     valid_product_name = product_data['product_name']['normal']
        
        
    #     return {
    #         # 'name': product_data['product_name'],
    #         'name': valid_product_name,
    #         # 'name': f"{valid_product_name}_{timestamp}",
    #         'sku': f"TEST_{timestamp}",
    #         'price': product_data['product_price'],
    #         'weight': product_data['product_weight'],
    #         'image': product_data['product_image'],
    #         'quantity': product_data['product_quantity'],
    #         # 'url_key': f"{product_data['product_name'].replace(' ', '-').lower()}-{timestamp}",
    #         'url_key': f"{valid_product_name.replace(' ', '-').lower()}-{timestamp}",
    #         # 'meta_title': product_data['product_meta_title']
    #         'meta_title': valid_product_name
    #     }

    #     # product_sku = f"TEST_{int(time.time())}"
    #     # product_url_key =  f"{product_name.replace(' ', '-').lower()}-{int(time.time())}"

    @staticmethod
    def create_product(scenario:str = "normal", suffix: str = None) -> Dict:

        # if __name__ == "__main__":
        #     for scenario in ["normal", "max_length", "special_chars", "with_emoji"]:
        #         try:
        #             p = ProductFactory.create_product(scenario)
        #             print(f"{scenario.upper():12} → {p['name'][:60]}... SKU: {p['sku']}")
        #         except Exception as e:
        #             print(f"{scenario.upper():12} → ERROR: {e}")

        template = ConfigReader.get_product_template(scenario)
        if not template:
            raise ValueError(f"Scenario '{scenario}' not found")
        timestamp = str(int(time.time())) if suffix is None else suffix
        product_name = template['product_name']

        return {
            'name': f"{product_name}" if not suffix else f"{product_name} [{timestamp}]",
            'sku': f"{template['sku_base']}-{timestamp}",
            'price': template['price'],
            'weight': template['weight'],
            'description': template['description'],
            'image': template['image'],
            'quantity': template['quantity'],
            'url_key': f"{template['url_key']}-{timestamp}",
            'meta_title': template['meta_title'],
            'meta_description': template['meta_description'],
            'scenario': scenario  # để debug dễ hơn
        }
    
    @staticmethod
    def create_multiple_products(scenarios: List[str] = None, count_per_scenario: int = 1):
        if scenarios is None:
            scenarios = ["normal", "max_lenght", "special_chars", "with_emoji"]
        
        products = []
        for scenario in scenarios:
            for i in range(count_per_scenario):
                suffix = f"auto{i+1}" if count_per_scenario > 1 else None
                products.append(ProductFactory.create_product(scenario, suffix))
        
        return products
    















#     // "product_data":
# //     {
# //       "product_name": {
# //         "max_length": "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above a",
# //         "special_chars": "Men's Jacket & Special 'Chars' 2025! \"<>{}[];:/",
# //         "with_emoji": "Winter Jacket 2025 ₊✩‧₊˚౨ৎ˚₊✩‧₊ 😁",
# //         "normal": "Blue Jacket Premium"
# //       }
# //       ,
# //         "product_sku": "SKU0001",
# //         "product_price": "3999",
# //         "product_weight": "1",
# //         "product_description": "ShirtAdidas Premium Essentials Padded Jacket BlueIY2283 is a fashionable and functional product from Adidas",
# //         "product_image":"Premium-Jacket-Blue.png",
# //         "product_quantity": "100",
# //         "product_url_key": "sofa-luxury-set-0001",
# //         "product_meta_title": "Sofa Luxury Set",
# //         "product_meta_description": "Product information adidas Premium Essentials Padded Jacket – Blue"
# //     }