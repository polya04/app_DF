# Клас для роботи з базою даних, створенням таблиць та підключенням до БД
import sqlite3
from config import DB_NAME

# Отримання підключення до бази даних
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)  # Підключення до бази даних
    conn.row_factory = sqlite3.Row  # Встановлення фабрики рядків для отримання результату у вигляді словників
    return conn  # Повертаємо підключення

# Створення таблиць у базі даних
def create_tables():
    conn = get_db_connection()  # Отримуємо підключення до БД
    cursor = conn.cursor()  # Створюємо курсор для виконання SQL запитів

    # Створення таблиці користувачів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE NOT NULL,        
        password TEXT NOT NULL,              
        theme INTEGER                          
    )
    """)

    # Створення таблиці категорій
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        name TEXT NOT NULL,                    
        page INTEGER                           
    )
    """)

    # Створення таблиці слів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,       
        word TEXT NOT NULL,                         
        transcription TEXT,                        
        translation TEXT,                           
        image BLOB,                                 
        audio BLOB,                                 
        category_id INTEGER,                       
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE  
    )
    """)

    # Створення таблиці тестів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,       
        question TEXT UNIQUE NOT NULL,              
        options TEXT NOT NULL,                      
        correct_answer INTEGER NOT NULL,            
        type INTEGER NOT NULL,                     
        category_id INTEGER NOT NULL,               
        FOREIGN KEY (category_id) REFERENCES categories(id)  
    )
    """)

    # Створення таблиці спеціалізованих тестів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spectests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,       
        question_text TEXT,                         
        audio_data BLOB,                            
        correct_answer BOOLEAN NOT NULL,            
        type INTEGER NOT NULL,                      
        category_id INTEGER NOT NULL,               
        FOREIGN KEY (category_id) REFERENCES categories(id) 
    )
    """)

    # Створення таблиці прогресу користувачів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,       
        user_id INTEGER NOT NULL,                   
        category_id INTEGER NOT NULL,               
        correct_count INTEGER DEFAULT 0,            
        incorrect_count INTEGER DEFAULT 0,          
        FOREIGN KEY (user_id) REFERENCES users(id), 
        FOREIGN KEY (category_id) REFERENCES categories(id)  
    )
    """)

    conn.commit()  # Зберігаємо зміни в базі даних
    conn.close()   # Закриваємо підключення до бази даних
