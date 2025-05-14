# Клас для роботи з прогресом користувача в базі даних
from models.database import get_db_connection

class ProgressModel:
    
    # Метод для створення або оновлення запису прогресу користувача в категорії
    @staticmethod
    def create_progress(user_id, category_id, true_answers, false_answers):
        """
        Створює нову запис прогресу для користувача в категорії.
        Якщо вже існує — оновлює дані.
        """
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор для виконання SQL запитів

        # Перевірка, чи існує вже запис прогресу для цього користувача і категорії
        cursor.execute("""
            SELECT id FROM progress WHERE user_id = ? AND category_id = ?
        """, (user_id, category_id))
        row = cursor.fetchone()  # Отримуємо перший знайдений запис

        if row:
            # Якщо запис існує, оновлюємо його
            cursor.execute("""
                UPDATE progress
                SET correct_count = ?, incorrect_count = ?
                WHERE user_id = ? AND category_id = ?
            """, (true_answers, false_answers, user_id, category_id))
        else:
            # Якщо запис не існує, створюємо новий
            cursor.execute("""
                INSERT INTO progress (user_id, category_id, correct_count, incorrect_count)
                VALUES (?, ?, ?, ?)
            """, (user_id, category_id, true_answers, false_answers))

        conn.commit()  # Зберігаємо зміни в БД
        conn.close()  # Закриваємо підключення

    # Метод для отримання прогресу користувача по всіх категоріях
    @staticmethod
    def get_user_progress(user_id):
        """
        Повертає прогрес користувача по всіх категоріях.
        :return: list[dict]
        """
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        cursor.execute("""
            SELECT category_id, correct_count, incorrect_count
            FROM progress
            WHERE user_id = ?
        """, (user_id,))  # Виконуємо запит для отримання прогресу користувача по всіх категоріях

        rows = cursor.fetchall()  # Отримуємо всі записи
        conn.close()  # Закриваємо підключення

        # Повертаємо результат у вигляді списку словників
        return [
            {
                'category_id': row[0],  # ID категорії
                'correct_count': row[1],  # Кількість правильних відповідей
                'incorrect_count': row[2]  # Кількість неправильних відповідей
            }
            for row in rows
        ]

    # Метод для отримання прогресу по конкретній категорії для користувача
    @staticmethod
    def get_progress_by_user_and_category(user_id, category_id):
        """
        Отримує прогрес по конкретній категорії.
        """
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        cursor.execute("""
            SELECT correct_count, incorrect_count
            FROM progress
            WHERE user_id = ? AND category_id = ?
        """, (user_id, category_id))  # Виконуємо запит для отримання прогресу по категорії

        row = cursor.fetchone()  # Отримуємо один запис
        conn.close()  # Закриваємо підключення

        if row:
            # Якщо запис знайдений, повертаємо дані
            return {
                'correct_count': row[0],  # Кількість правильних відповідей
                'incorrect_count': row[1]  # Кількість неправильних відповідей
            }
        return None  # Якщо запис не знайдений, повертаємо None
