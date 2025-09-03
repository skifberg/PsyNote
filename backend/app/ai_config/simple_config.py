import os

class YandexGPTConfig:
    """Упрощенная конфигурация для Yandex GPT API"""
    
    API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    def __init__(self):
        # Читаем переменные напрямую из env
        self.api_key = os.environ.get("YANDEX_GPT_API_KEY")
        self.folder_id = os.environ.get("YANDEX_GPT_FOLDER_ID")
        self.model = "yandexgpt-lite"

    def get_auth_headers(self) -> dict:
        if not self.api_key:
            raise Exception("Yandex GPT API key not configured")
            
        return {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }

    def get_model_uri(self) -> str:
        if not self.folder_id:
            raise Exception("Yandex GPT folder_id not configured")
        return f"gpt://{self.folder_id}/{self.model}"

    def is_configured(self) -> bool:
        return bool(self.api_key and self.folder_id)

yandex_gpt_config = YandexGPTConfig()
