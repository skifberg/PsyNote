import requests
from typing import Optional
from .yandex_gpt_config import yandex_gpt_config
from .fallback_ai import fallback_ai

class YandexGPTClient:
    """Клиент для работы с Yandex GPT API"""
    
    def __init__(self):
        self.config = yandex_gpt_config

    def send_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        if not self.config.is_configured():
            raise Exception("Yandex GPT не настроен")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "text": system_prompt})
        messages.append({"role": "user", "text": message})
        
        payload = {
            "modelUri": self.config.get_model_uri(),
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 2000
            },
            "messages": messages
        }
        
        try:
            response = requests.post(
                self.config.API_URL,
                headers=self.config.get_auth_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["result"]["alternatives"][0]["message"]["text"]
            
        except Exception as e:
            print(f"Yandex GPT ошибка: {e}")
            raise

    def analyze_test_results(self, test_name: str, score: int, max_score: int, interpretation: dict) -> str:
        system_prompt = "Ты опытный психолог-консультант. Анализируй результаты психологических тестов и давай персонализированные рекомендации."
        
        message = f"""
Проанализируй результаты теста {test_name}:
- Полученные баллы: {score} из {max_score}
- Интерпретация: {interpretation['result']}  
- Описание: {interpretation['description']}

Предоставь:
1. Глубокий анализ результатов
2. Конкретные рекомендации
3. Вопросы для саморефлексии
4. Профессиональные советы
"""
        try:
            return self.send_message(message, system_prompt)
        except Exception as e:
            print(f"⚠️  Yandex GPT недоступен: {e}")
            return fallback_ai.analyze_test_results(test_name, score, max_score, interpretation)

yandex_gpt_client = YandexGPTClient()