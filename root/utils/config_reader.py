import json
import os
from typing import Any

class ConfigReader:
    _config = None

    @staticmethod
    def load_config():
        if ConfigReader._config is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'testsetting.json')
            # Load config.json
            with open(config_path, 'r') as config_file:
                ConfigReader._config = json.load(config_file)
        return ConfigReader._config

    @staticmethod
    def get_base_url():
        return ConfigReader.load_config()['base_url']
    
    @staticmethod
    def get_dashboard_url():
        return ConfigReader.load_config()["dashboard_url"]
    
    @staticmethod
    def get_timeout() -> int:
        return int(ConfigReader.load_config()['timeout'])

    @staticmethod
    def get_email_password():
        config = ConfigReader.load_config()
        return config['email'], config['password']

    @staticmethod
    def get_credentials(key):
        """
        Get email/password following key in test_data
        key example: "invalid_user", "invalid_password", "invalid_email_format", "blank"
        """
        config = ConfigReader.load_config()
        data = config.get(key, {})
        email = data.get("email", "")
        password = data.get("password", "")
        return email, password
    
    @staticmethod
    def get_error_message(key: str):
        config = ConfigReader.load_config()
        return config["error_messages"][key]

    @staticmethod
    def get_collection_data():
        return ConfigReader.load_config()['collection_data']
    
    @staticmethod
    def get_product_data():
        return ConfigReader.load_config()['product_data']
    
   
    # @staticmethod
    # def get_product_name(scenario: str = "normal") -> str:
    #     config = ConfigReader.load_config()
    #     try:
    #         return config["product_data"]["product_name"][scenario]
    #     except KeyError as e:
    #         raise KeyError(f"Không tìm thấy product_name cho scenario '{scenario}'. "
    #                     f"Các scenario có sẵn: {list(config['product_data']['product_name'].keys())}") from e
    
    @staticmethod
    def get_product_name(scenario: str = "normal") -> str:
        config = ConfigReader.load_config()
        return config["product_data"]["product_name"][scenario]
        

    @staticmethod
    def get_category_data():
        return ConfigReader.load_config()['category_data']
    
    @staticmethod
    def get_attribute_data():
        return ConfigReader.load_config()['attribute_data']

    @staticmethod
    def get_coupon_data():
        return ConfigReader.load_config()['coupon_data']
        
        


