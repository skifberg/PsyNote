#!/usr/bin/env python3
import sys
import os
sys.path.append('/Users/oleg/PsyNote/backend/app')

from api_client import yandex_gpt_client

def test_integration():
    print("🧪 Тестируем интеграцию с Yandex GPT...")
    
    if not yandex_gpt_client.is_configured():
        print("❌ Yandex GPT не настроен")
        return False
    
    print("✅ API настроен")
    
    try:
        response = yandex_gpt_client.send_message(
            "Привет! Это тест интеграции PsyNote с Yandex GPT.",
            "Ты — профессиональный психолог-консультант."
        )
        
        print("✅ Yandex GPT успешно отвечает!")
        print(f"💬 Ответ: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_integration()
    if success:
        print("\n🎉 Интеграция успешна!")
    else:
        print("\n🔧 Требуется настройка")