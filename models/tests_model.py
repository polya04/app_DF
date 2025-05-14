# Клас для роботи з тестами
from models.database import get_db_connection
# import json

class TestModel:
    
    # Метод для створення нового тесту
    @staticmethod
    def create_test(question, answers, true_answer, test_type, category_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        # Перевірка, чи тест з таким питанням вже існує
        cursor.execute("SELECT id FROM tests WHERE question = ?", (question,))
        exists = cursor.fetchone()  # Якщо тест існує, отримуємо його ID
        if exists:
            # print(f"Тест з питанням вже існує: {question}")  # Можна розкоментувати для відладки
            pass  # Якщо тест вже існує, нічого не робимо
        else:
            # Перетворюємо список відповідей в рядок, розділений комами
            answers_str = ', '.join(answers)

            # Вставляємо новий тест у таблицю
            cursor.execute("""
                INSERT INTO tests (question, options, correct_answer, type, category_id)
                VALUES (?, ?, ?, ?, ?)
            """, (question, answers_str, true_answer, test_type, category_id))  # Виконуємо запит
            conn.commit()  # Зберігаємо зміни
        conn.close()  # Закриваємо підключення

    # Метод для отримання всіх тестів за категорією
    @staticmethod
    def get_tests_by_category(category_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        # Виконуємо запит для отримання всіх тестів по категорії
        cursor.execute("""
            SELECT id, question, options, correct_answer, type FROM tests
            WHERE category_id = ?
        """, (category_id,))
        rows = cursor.fetchall()  # Отримуємо всі записи
        conn.close()  # Закриваємо підключення

        tests = []  # Список для збереження тестів
        for row in rows:
            # Додаємо тест у список у вигляді словника
            tests.append({
                'id': row[0],  # ID тесту
                'question': row[1],  # Питання
                'answers': row[2].split(', '),  # Відповіді (розбиваємо рядок на список)
                'correct_answer': row[3],  # Правильна відповідь
                'type': row[4]  # Тип тесту
            })

        return tests  # Повертаємо список тестів

    # Метод для отримання одного тесту за ID
    @staticmethod
    def get_test_by_id(test_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        # Виконуємо запит для отримання тесту по ID
        cursor.execute("""
            SELECT question, options, correct_answer, type, category_id
            FROM tests WHERE id = ?
        """, (test_id,))
        row = cursor.fetchone()  # Отримуємо один запис
        conn.close()  # Закриваємо підключення

        if row:
            # Якщо тест знайдений, повертаємо його у вигляді словника
            return {
                'question': row[0],  # Питання
                'answers': row[1].split(', '),  # Відповіді (розбиваємо рядок на список)
                'correct_answer': row[2],  # Правильна відповідь
                'type': row[3],  # Тип тесту
                'category_id': row[4]  # ID категорії
            }
        return None  # Якщо тест не знайдений, повертаємо None
