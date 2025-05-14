# Клас для роботи з спеціальними тестами (spectests)
from models.database import get_db_connection

class SpecTestModel:
    
    # Метод для створення нового спеціального тесту
    @staticmethod
    def create_test(question_text, audio_data, correct_answer, test_type, category_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        # Перевірка, чи такий тест вже існує в БД
        cursor.execute("""
            SELECT id FROM spectests
            WHERE question_text = ? AND audio_data = ?
        """, (question_text, audio_data))
        exists = cursor.fetchone()  # Якщо тест існує, отримуємо його ID

        if exists:
            print("Такий тест вже існує і не буде додано повторно.")  # Виводимо повідомлення про наявність тесту
        else:
            # Якщо тесту немає, створюємо новий запис
            cursor.execute("""
                INSERT INTO spectests (question_text, audio_data, correct_answer, type, category_id)
                VALUES (?, ?, ?, ?, ?)
            """, (question_text, audio_data, correct_answer, int(test_type), category_id))  # Вставляємо новий тест
            conn.commit()  # Зберігаємо зміни
        conn.close()  # Закриваємо підключення

    # Метод для отримання всіх тестів по ID категорії
    @staticmethod
    def get_tests_by_category(category_id):
        """
        Отримує всі тести по ID категорії.
        :param category_id: int
        :return: list of dict
        """
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        # Виконуємо запит для отримання тестів по категорії
        cursor.execute("""
            SELECT id, question_text, audio_data, correct_answer, type
            FROM spectests WHERE category_id = ?
        """, (category_id,))
        rows = cursor.fetchall()  # Отримуємо всі записи
        conn.close()  # Закриваємо підключення

        tests = []  # Список для збереження тестів
        for row in rows:
            # Додаємо тести в список у вигляді словників
            tests.append({
                'id': row[0],  # ID тесту
                'question': row[1],  # Текст питання
                'audio_data': row[2],  # Аудіо дані
                'correct_answer': bool(row[3]),  # Правильна відповідь (перетворюємо на bool)
                'type': 3  # Тип тесту (жорстко встановлено як 3)
            })

        return tests  # Повертаємо список тестів

    # Метод для отримання одного тесту по ID
    @staticmethod
    def get_test_by_id(test_id):
        """
        Отримує один тест по ID.
        :param test_id: int
        :return: dict або None
        """
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор

        # Виконуємо запит для отримання тесту по ID
        cursor.execute("""
            SELECT question_text, audio_data, correct_answer, category_id
            FROM spectests WHERE id = ?
        """, (test_id,))
        row = cursor.fetchone()  # Отримуємо один запис
        conn.close()  # Закриваємо підключення

        if row:
            # Якщо запис знайдений, повертаємо його у вигляді словника
            return {
                'question_text': row[0],  # Текст питання
                'audio_data': row[1],  # Аудіо дані
                'correct_answer': bool(row[2]),  # Правильна відповідь (перетворюємо на bool)
                'category_id': row[3]  # ID категорії
            }
        return None  # Якщо запис не знайдений, повертаємо None
