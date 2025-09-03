from typing import Optional
from .yandex_gpt_client import yandex_gpt_client
from .fallback_ai import fallback_ai

class AIManager:
    """Менеджер для работы с AI провайдерами"""
    
    def __init__(self):
        self.default_provider = "yandex_gpt"

    def analyze_test_results(self, test_data: dict, provider: Optional[str] = None) -> str:
        """Анализ результатов теста"""
        try:
            return yandex_gpt_client.analyze_test_results(
                test_name=test_data["name"],
                score=test_data["score"],
                max_score=test_data["max_score"],
                interpretation=test_data["interpretation"]
            )
        except Exception as e:
            print(f"❌ Yandex GPT недоступен: {e}")
            return fallback_ai.analyze_test_results(
                test_data["name"],
                test_data["score"],
                test_data["max_score"],
                test_data["interpretation"]
            )

ai_manager = AIManager()
