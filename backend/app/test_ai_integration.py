import asyncio
import sys
sys.path.append('/Users/oleg/PsyNote/backend/app')

from core.ai_psychologist import ai_psychologist

async def test_ai_functionality():
    print("🧠 Тестируем базовый функционал AI...")
    
    # Тест анализа результатов
    test_data = {
        "name": "Тест на тревожность (BAI)",
        "score": 25,
        "max_score": 63,
        "interpretation": "Умеренный уровень тревожности"
    }
    
    try:
        analysis = await ai_psychologist.analyze_test_results(test_data)
        print("✅ AI-анализ результатов работает!")
        print(f"📝 Результат: {analysis[:200]}...")
        
        # Тест подбора методик
        methods = await ai_psychologist.suggest_methods("потеря интереса к жизни")
        print("✅ AI-подбор методик работает!")
        print(f"📋 Методики: {methods[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Запуск теста AI функционала...")
    success = asyncio.run(test_ai_functionality())
    
    if success:
        print("\n🎉 AI функционал работает отлично!")
    else:
        print("\n⚠️  Требуется настройка")