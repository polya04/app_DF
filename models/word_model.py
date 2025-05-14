# Клас для роботи зі словами
from models.database import get_db_connection

class WordModel:
    
    # Метод для створення нового слова в базі даних
    @staticmethod
    def create_word(word, transcription, translation, image, audio, category_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("""
            INSERT INTO words (word, transcription, translation, image, audio, category_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (word, transcription, translation, image, audio, category_id))  # Виконуємо запит на вставку
        conn.commit()  # Зберігаємо зміни
        conn.close()  # Закриваємо підключення

    # Метод для отримання всіх слів з БД
    @staticmethod
    def get_all_words():
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT * FROM words")  # Отримуємо всі слова
        words = cursor.fetchall()  # Отримуємо всі записи
        conn.close()  # Закриваємо підключення
        return words  # Повертаємо список слів

    # Метод для отримання слів по категорії
    @staticmethod
    def get_words_by_category(category_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT * FROM words WHERE category_id = ?", (category_id,))  # Отримуємо слова за категорією
        words = cursor.fetchall()  # Отримуємо всі записи
        conn.close()  # Закриваємо підключення
        return words  # Повертаємо список слів

    # Метод для видалення слова за ID
    @staticmethod
    def delete_word(word_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))  # Видаляємо слово
        conn.commit()  # Зберігаємо зміни
        conn.close()  # Закриваємо підключення
