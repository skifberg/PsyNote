import requests
import json
from typing import Optional
from .deepseek_config import deepseek_config

class DeepSeekClient:
    """Клиент для работы с DeepSeek API"""
    
    def __init__(self):
        self.config = deepseek_config
        self.model = "deepseek-chat"

    def send_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Отправляем сообщение в DeepSeek"""
        
        if not self.config.is_configured():
            raise Exception("DeepSeek API не настроен. Проверьте DEEPSEEK_API_KEY в .env файле")
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.config.API_URL,
                headers=self.config.get_auth_headers(),
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка запроса к DeepSeek: {str(e)}")
        except KeyError as e:
            raise Exception(f"Ошибка парсинга ответа DeepSeek: {str(e)}")
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {str(e)}")

    def analyze_test_results(self, test_name: str, score: int, max_score: int, interpretation: dict) -> str:
        """Анализ результатов теста с помощью AI"""
        
        system_prompt = """Ты опытный психолог-консультант. Анализируй результаты психологических тестов и давай:
1. Персонализированные инсайты на основе результатов
2. Конкретные практические рекомендации
3. Вопросы для глубокой саморефлексии  
4. Профессиональные советы по улучшению состояния

Будь empathetic, supportive и professional. Давай конкретные рекомендации, а не общие фразы."""
        
        message = f"""
Проанализируй результаты психологического теста:

Название теста: {test_name}
Полученные баллы: {score} из {max_score}
Интерпретация результата: {interpretation['result']}
Описание: {interpretation['description']}

Пожалуйста, предоставь подробный анализ включая:
1. Что означают эти результаты в контексте психического здоровья
2. Конкретные рекомендации для улучшения состояния
3. Вопросы для самоанализа и рефлексии
4. Профессиональные советы и возможные next steps

Анализ должен быть персонализированным и практичным.
"""
        
        return self.send_message(message, system_prompt)

# Создаем экземпляр клиента
deepseek_client = DeepSeekClient()