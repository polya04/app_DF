# Клас для роботи з категоріями у базі даних
from models.database import get_db_connection

class CategoryModel:
    
    # Метод для створення нової категорії
    @staticmethod
    def create_category(name, page_number):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор для виконання SQL запитів
        cursor.execute("INSERT INTO categories (name, page) VALUES (?, ?)", (name, page_number))  # Виконуємо SQL запит на вставку нової категорії
        conn.commit()  # Зберігаємо зміни в БД
        conn.close()  # Закриваємо підключення

    # Метод для отримання всіх категорій
    @staticmethod
    def get_all_categories():
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT * FROM categories")  # Виконуємо SQL запит для отримання всіх категорій
        categories = cursor.fetchall()  # Отримуємо всі результати запиту
        conn.close()  # Закриваємо підключення
        return categories  # Повертаємо всі категорії

    # Метод для отримання категорій за номером сторінки
    @staticmethod
    def get_categories_by_page(page):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT * FROM categories WHERE page = ?", (page,))  # Виконуємо запит на отримання категорій за номером сторінки
        categories = cursor.fetchall()  # Отримуємо всі категорії для вказаної сторінки
        conn.close()  # Закриваємо підключення
        return categories  # Повертаємо категорії

    # Метод для отримання категорії за її назвою
    @staticmethod
    def get_category_by_name(name):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT id, name FROM categories WHERE name = ?", (name,))  # Виконуємо запит для отримання категорії за назвою
        row = cursor.fetchone()  # Отримуємо одну категорію
        conn.close()  # Закриваємо підключення
        if row:  # Якщо категорія знайдена
            return { 'id': row[0], 'name': row[1]}  # Повертаємо id та name категорії
        return None  # Якщо категорія не знайдена, повертаємо None

    # Метод для отримання категорії за її ID
    @staticmethod
    def get_category_by_id(category_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))  # Виконуємо запит для отримання категорії за її ID
        result = cursor.fetchone()  # Отримуємо одну категорію
        conn.close()  # Закриваємо підключення
        return result  # Повертаємо результат (якщо категорія знайдена)

    # Метод для видалення категорії за її ID
    @staticmethod
    def delete_category(category_id):
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))  # Виконуємо запит на видалення категорії за ID
        conn.commit()  # Зберігаємо зміни в БД
        conn.close()  # Закриваємо підключення
