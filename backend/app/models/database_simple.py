import sqlite3
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleDatabase:
    def __init__(self):
        self.db_path = "data/psynote.db"
        self.conn = None
        
    async def connect(self):
        """Подключаемся к SQLite"""
        try:
            # Создаем папку data если нет
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            logger.info("✅ SQLite подключен")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка SQLite: {e}")
            return False

    async def create_tables(self):
        """Создаем простые таблицы"""
        try:
            cursor = self.conn.cursor()
            
            # Простая таблица вопросов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    item_id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    keyed_direction TEXT NOT NULL
                )
            ''')
            
            # Простая таблица ответов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    item_id TEXT,
                    score INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            logger.info("✅ Таблицы созданы")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания таблиц: {e}")
            return False

# Глобальный экземпляр
simple_db = SimpleDatabase()