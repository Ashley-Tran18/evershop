import json
import os

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
    def get_timeout():
        return int(ConfigReader.load_config()['timeout'])

    # @staticmethod
    # def get_email_password():
    #     config = ConfigReader.load_config()
    #     return config['email'], config['password']

    @staticmethod
    def get_credentials():
        return ConfigReader.load_config()['credentials']

    @staticmethod
    def get_login_attempts():
        """
        Trả về danh sách các attempt (invalid + valid login)
        lấy từ credentials trong file config.
        """
        creds = ConfigReader.get_credentials()

        attempts = [
            {
                "email": creds["invalid_email"],
                "password": creds["invalid_password"],
            },
            {
                "email": creds["email"],
                "password": creds["password"],
            }
        ]
        return attempts

    @staticmethod
    def get_user_information():
        return ConfigReader.load_config()['pages_url']
    

    

        
        



