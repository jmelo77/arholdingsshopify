import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:

    @staticmethod
    def get_shop_config() -> dict:
        return {
            "shop_acces_token": os.getenv("SHOP_ACCESS_TOKEN"),
            "shop_url": os.getenv("SHOP_URL"),
        }
    
    @staticmethod
    def get_ngrok_config() -> dict:
        return {
            "ngrok_url": os.getenv("NGROK_URL"),
        }
