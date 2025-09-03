import asyncio
import sys
sys.path.append('/Users/oleg/PsyNote/backend/app')

from core.ai_psychologist import ai_psychologist
from services.ai_service import ai_service

async def test_full_integration():
    print("🔗 Тестируем полную интеграцию AI...")
    
    # Тестовые данные
    test_data = {
        "id": 1,
        "name": "Тест на тревожность (BAI)",
        "score": 25,
        "max_score": 63,
        "interpretation": "Умеренный уровень тревожности"
    }
    
    user_id = 123  # Тестовый пользователь
    
    try:
        # Полный цикл: анализ + сохранение
        result = await ai_service.analyze_and_save_test(user_id, test_data)
        
        if result["success"]:
            print("✅ Полная интеграция успешна!")
            print(f"📊 Анализ: {result['analysis'][:200]}...")
            print("💾 Данные сохранены в БД")
        else:
            print(f"❌ Ошибка: {result['error']}")
            
        return result["success"]
        
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

async def test_api_endpoints():
    """Тестируем API эндпоинты"""
    print("\n🌐 Тестируем API эндпоинты...")
    
    # Тест анализа теста
    test_data = {
        "name": "Тест депрессии Бека",
        "score": 18,
        "max_score": 63,
        "interpretation": "Легкая депрессия"
    }
    
    try:
        analysis = await ai_psychologist.analyze_test_results(test_data)
        print("✅ API анализ теста работает")
        
        methods = await ai_psychologist.suggest_methods("потеря интереса к жизни")
        print("✅ API подбор методик работает")
        
        return True
        
    except Exception as e:
        print(f"❌ API ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Запуск тестов интеграции AI...")
    
    # Запускаем все тесты
    results = asyncio.run(asyncio.gather(
        test_full_integration(),
        test_api_endpoints()
    ))
    
    if all(results):
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! AI интегрирован успешно!")
    else:
        print("\n⚠️  Некоторые тесты не прошли")