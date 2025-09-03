import aiohttp
import os
from dotenv import load_dotenv

load_dotenv('/Users/oleg/PsyNote/.env')

class YandexGPTClient:
    def __init__(self):
        self.api_key = os.getenv('YANDEX_GPT_API_KEY')
        self.folder_id = os.getenv('YANDEX_GPT_FOLDER_ID')
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    def is_configured(self):
        return bool(self.api_key and self.folder_id)
    
    async def send_message(self, message: str, system_prompt: str = None) -> str:
        if not self.is_configured():
            raise Exception("Yandex GPT не настроен")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "text": system_prompt})
        messages.append({"role": "user", "text": message})
        
        payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 2000
            },
            "messages": messages
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.url, headers=headers, json=payload, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['result']['alternatives'][0]['message']['text']
                    else:
                        error_text = await response.text()
                        raise Exception(f"Yandex GPT error: {response.status} - {error_text}")
            except Exception as e:
                print(f"❌ Yandex GPT ошибка: {e}")
                raise

yandex_gpt_client = YandexGPTClient()