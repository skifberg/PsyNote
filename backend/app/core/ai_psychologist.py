from typing import Dict
from api_client import yandex_gpt_client

class AIPsychologist:
    """AI-психолог для анализа результатов и рекомендаций"""
    
    async def analyze_test_results(self, test_data: Dict) -> str:
        """Анализ результатов психологического теста"""
        prompt = f"""
Проанализируй результаты теста {test_data['name']}:
- Полученные баллы: {test_data['score']} из {test_data['max_score']}
- Интерпретация: {test_data['interpretation']}

Предоставь:
1. Глубокий психологический анализ
2. Конкретные рекомендации для работы с состоянием
3. 3 вопроса для саморефлексии
4. Профессиональные советы
"""
        return await yandex_gpt_client.send_message(
            prompt,
            "Ты — опытный клинический психолог с 20-летним стажем. Анализируй результаты тестов и давай персонализированные рекомендации."
        )
    
    async def suggest_methods(self, user_problem: str) -> str:
        """Подбор методик based на проблеме пользователя"""
        prompt = f"""
Пользователь описывает проблему: "{user_problem}"

Подбери подходящие психологические методики и тесты:
1. 2-3 диагностических теста
2. 3-5 практических techniques
3. Рекомендации по последовательности работы
"""
        return await yandex_gpt_client.send_message(
            prompt,
            "Ты — эксперт по психологическим методикам. Подбирай инструменты based на конкретных проблемах пользователей."
        )
    
    async def daily_reflection(self, user_entry: str) -> str:
        """Анализ дневниковой записи"""
        return await yandex_gpt_client.send_message(
            f"Проанализируй дневниковую запись: {user_entry}",
            "Ты — внимательный и эмпатичный психолог. Анализируй дневниковые записи, задавай глубокие вопросы для рефлексии."
        )

ai_psychologist = AIPsychologist()