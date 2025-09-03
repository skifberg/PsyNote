import json
from typing import Dict, List
from datetime import datetime
from core.ai_psychologist import ai_psychologist

class AIService:
    """Сервис для работы с AI-функционалом и базой данных"""
    
    async def save_ai_analysis(self, user_id: int, test_id: int, analysis_data: Dict):
        """Сохраняет AI-анализ в базу данных"""
        # Здесь будет логика сохранения в вашу БД
        analysis_record = {
            "user_id": user_id,
            "test_id": test_id,
            "analysis": analysis_data,
            "created_at": datetime.now().isoformat(),
            "ai_model": "yandex-gpt"
        }
        
        # TODO: Реализовать сохранение в вашу БД
        print(f"💾 Saving AI analysis for user {user_id}, test {test_id}")
        return analysis_record
    
    async def get_user_ai_history(self, user_id: int) -> List[Dict]:
        """Получает историю AI-анализов пользователя"""
        # TODO: Реализовать получение из вашей БД
        return []
    
    async def analyze_and_save_test(self, user_id: int, test_data: Dict) -> Dict:
        """Полный цикл: анализ + сохранение"""
        try:
            # AI-анализ
            analysis = await ai_psychologist.analyze_test_results(test_data)
            
            # Сохранение в БД
            saved_analysis = await self.save_ai_analysis(
                user_id=user_id,
                test_id=test_data.get("id"),
                analysis_data={
                    "text": analysis,
                    "test_data": test_data
                }
            )
            
            return {
                "success": True,
                "analysis": analysis,
                "saved_record": saved_analysis
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Создаем экземпляр сервиса
ai_service = AIService()