import sqlite3
import os

def check_database():
    db_path = "data/psynote.db"
    
    if not os.path.exists(db_path):
        print("❌ База данных не найдена!")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Проверяем таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("📊 Таблицы в базе:")
    for table in tables:
        print(f"  - {table['name']}")
    
    # Проверяем вопросы
    cursor.execute("SELECT COUNT(*) as count FROM items")
    items_count = cursor.fetchone()['count']
    print(f"📝 Количество вопросов: {items_count}")
    
    # Покажем несколько вопросов
    if items_count > 0:
        cursor.execute("SELECT * FROM items LIMIT 3")
        questions = cursor.fetchall()
        print("\n🔍 Примеры вопросов:")
        for q in questions:
            print(f"  - {q['item_id']}: {q['text']}")
    
    conn.close()

if __name__ == "__main__":
    check_database()