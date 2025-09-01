import sqlite3
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

class Database:
    def __init__(self):
        self.db_path = os.getenv('DB_PATH', 'data/psynote.db')
        self.conn = None

    async def connect(self):
        """Подключаемся к SQLite базе данных"""
        try:
            # Создаем папку data если не существует
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
            logger.info(f"✅ Подключение к SQLite установлено: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к SQLite: {e}")
            return False

    async def create_tables(self):
        """Создаем все необходимые таблицы в SQLite"""
        if not self.conn:
            await self.connect()
        
        try:
            cursor = self.conn.cursor()

            # Таблица вопросов Big Five
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    item_id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    facet TEXT NOT NULL,
                    keyed_direction TEXT NOT NULL CHECK (keyed_direction IN ('plus', 'minus')),
                    param_a REAL DEFAULT NULL,
                    param_b REAL DEFAULT NULL,
                    param_c REAL DEFAULT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Таблица ответов пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_responses (
                    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
                    item_id TEXT REFERENCES items(item_id) ON DELETE CASCADE,
                    score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
                    response_time INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, item_id)
                )
            ''')

            # Таблица результатов тестов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
                    test_type TEXT NOT NULL DEFAULT 'big5',
                    extraversion REAL,
                    agreeableness REAL,
                    conscientiousness REAL,
                    neuroticism REAL,
                    openness REAL,
                    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Создаем индексы для оптимизации
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_domain ON items(domain)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_responses_user_id ON user_responses(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_responses_item_id ON user_responses(item_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_results_user_id ON test_results(user_id)')

            self.conn.commit()
            logger.info("✅ Все таблицы SQLite созданы/проверены")
            return True

        except Exception as e:
            logger.error(f"❌ Ошибка при создании таблиц SQLite: {e}")
            return False

    async def execute(self, query, params=None):
        """Выполнить SQL запрос"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения запроса: {e}")
            return None

    async def fetchall(self, query, params=None):
        """Получить все строки"""
        cursor = await self.execute(query, params)
        return cursor.fetchall() if cursor else []

    async def fetchone(self, query, params=None):
        """Получить одну строку"""
        cursor = await self.execute(query, params)
        return cursor.fetchone() if cursor else None

    async def close(self):
        """Закрыть соединение"""
        if self.conn:
            self.conn.close()
            logger.info("🔌 Соединение с SQLite закрыто")

# Глобальный экземпляр БД
db = Database()