import asyncio
import sys
sys.path.append('/Users/oleg/PsyNote/backend/app')

from core.ai_psychologist import ai_psychologist

async def test_ai_psychologist():
    print("🧠 Тестируем AI-психолога...")
    
    # Тест анализа результатов
    test_data = {
        "name": "Тест на тревожность (BAI)",
        "score": 25,
        "max_score": 63,
        "interpretation": "Умеренный уровень тревожности"
    }
    
    try:
        analysis = await ai_psychologist.analyze_test_results(test_data)
        print("✅ AI-анализ результатов:")
        print(analysis)
        print("\n" + "="*50 + "\n")
        
        # Тест подбора методик
        methods = await ai_psychologist.suggest_methods("Постоянная тревога и беспокойство")
        print("✅ AI-подбор методик:")
        print(methods)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ai_psychologist())
    if success:
        print("\n🎉 AI-психолог работает отлично!")
    else:
        print("\n🔧 Нужна дополнительная настройка")