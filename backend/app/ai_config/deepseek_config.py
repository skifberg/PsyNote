import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv('/Users/oleg/PsyNote/.env')

class DeepSeekConfig:
    """Конфигурация для DeepSeek API"""
    
    API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = "deepseek-chat"

    def get_auth_headers(self) -> dict:
        """Получаем заголовки для аутентификации"""
        if not self.api_key:
            raise Exception("DeepSeek API key not configured")
            
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def is_configured(self) -> bool:
        """Проверяем настроен ли API"""
        return bool(self.api_key and self.api_key.startswith("sk-"))

# Создаем экземпляр конфигурации
deepseek_config = DeepSeekConfig()