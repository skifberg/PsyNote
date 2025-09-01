from models.database import db
from models.entities import Item, UserResponse, TestResult
import json
import aiofiles
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    @staticmethod
    async def initialize_database():
        """Инициализация SQLite базы данных"""
        success = await db.connect()
        if success:
            return await db.create_tables()
        return False

    @staticmethod
    async def import_ipip_items(json_file_path: str = "data/ipip_100_items.json"):
        """Импорт вопросов из JSON файла в SQLite"""
        try:
            async with aiofiles.open(json_file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                items = json.loads(content)
            
            imported_count = 0
            for item_data in items:
                # Проверяем, существует ли уже вопрос
                existing = await db.fetchone(
                    "SELECT item_id FROM items WHERE item_id = ?", 
                    (item_data['item_id'],)
                )
                
                if not existing:
                    await db.execute('''
                        INSERT INTO items (item_id, text, domain, facet, keyed_direction)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        item_data['item_id'], 
                        item_data['text'], 
                        item_data['domain'], 
                        item_data['facet'], 
                        item_data['keyed']
                    ))
                    imported_count += 1
            
            logger.info(f"✅ Импортировано {imported_count} вопросов в SQLite")
            return True
                
        except Exception as e:
            logger.error(f"❌ Ошибка импорта вопросов: {e}")
            return False

    @staticmethod
    async def save_user_response(response: UserResponse):
        """Сохранение ответа пользователя в SQLite"""
        try:
            await db.execute('''
                INSERT OR REPLACE INTO user_responses 
                (user_id, item_id, score, response_time)
                VALUES (?, ?, ?, ?)
            ''', (response.user_id, response.item_id, response.score, response.response_time))
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения ответа: {e}")
            return False

    @staticmethod
    async def get_next_question(user_id: int):
        """Получить следующий вопрос для пользователя"""
        try:
            question = await db.fetchone('''
                SELECT * FROM items 
                WHERE item_id NOT IN (
                    SELECT item_id FROM user_responses WHERE user_id = ?
                )
                ORDER BY RANDOM() 
                LIMIT 1
            ''', (user_id,))
            
            return question
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения вопроса: {e}")
            return None

    @staticmethod
    async def get_user_results(user_id: int):
        """Получить результаты теста для пользователя"""
        try:
            results = await db.fetchall('''
                SELECT 
                    domain,
                    AVG(CASE WHEN keyed_direction = 'plus' THEN score ELSE 6 - score END) as score
                FROM user_responses ur
                JOIN items i ON ur.item_id = i.item_id
                WHERE ur.user_id = ?
                GROUP BY domain
            ''', (user_id,))
            
            return {result["domain"]: result["score"] for result in results}
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения результатов: {e}")
            return {}