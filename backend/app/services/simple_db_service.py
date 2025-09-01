import json
import aiofiles
from models.database_simple import simple_db

class SimpleDBService:
    @staticmethod
    async def initialize():
        """Простая инициализация"""
        return await simple_db.connect() and await simple_db.create_tables()

    @staticmethod
    async def import_questions():
        """Импорт вопросов в SQLite"""
        try:
            async with aiofiles.open('data/ipip_100_items.json', 'r') as f:
                data = await f.read()
                questions = json.loads(data)
            
            cursor = simple_db.conn.cursor()
            for q in questions:
                cursor.execute('''
                    INSERT OR IGNORE INTO items (item_id, text, domain, keyed_direction)
                    VALUES (?, ?, ?, ?)
                ''', (q['item_id'], q['text'], q['domain'], q['keyed']))
            
            simple_db.conn.commit()
            print(f"✅ Импортировано {len(questions)} вопросов")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка импорта: {e}")
            return False