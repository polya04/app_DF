# Клас для роботи з користувачами
from models.database import get_db_connection

class UserModel:
    
    # Метод для створення нового користувача
    @staticmethod
    def create_user(username, password):
        """Створює нового користувача в БД і повертає його"""
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        try:
            # Виконуємо запит для вставки нового користувача
            cursor.execute(
                "INSERT INTO users (username, password, theme) VALUES (?, ?, ?)",
                (username, password, 0)  # За замовчуванням тема = 0
            )
            conn.commit()  # Зберігаємо зміни
            user_id = cursor.lastrowid  # Отримуємо ID останнього вставленого користувача

            # Отримуємо інформацію про створеного користувача
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()  # Отримуємо дані користувача
            return user  # Повертаємо дані користувача
        except Exception as e:
            print("Помилка при реєстрації:", e)  # Логування помилки
            return None  # Повертаємо None у разі помилки
        finally:
            conn.close()  # Закриваємо підключення до БД

    # Метод для отримання користувача за логіном і паролем
    @staticmethod
    def get_user(username, password):
        """Отримує користувача з БД за логіном і паролем"""
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()  # Отримуємо дані користувача
        conn.close()  # Закриваємо підключення
        return user  # Повертаємо дані користувача

    # Метод для отримання всіх користувачів (для адмінки)
    @staticmethod
    def get_all_users():
        """Отримує список всіх користувачів (для адмінки)"""
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("SELECT id, username FROM users")  # Отримуємо список користувачів
        users = cursor.fetchall()  # Отримуємо всі записи
        conn.close()  # Закриваємо підключення
        return users  # Повертаємо список користувачів

    # Метод для оновлення теми користувача
    @staticmethod
    def update_user_theme(user_id, new_theme):
        """Оновлює тему користувача за його ID"""
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        try:
            cursor.execute("UPDATE users SET theme = ? WHERE id = ?", (new_theme, user_id))  # Оновлюємо тему
            conn.commit()  # Зберігаємо зміни
        except Exception as e:
            print(f"Помилка при оновленні теми: {e}")  # Логування помилки
        finally:
            conn.close()  # Закриваємо підключення

    # Метод для видалення користувача за ID
    @staticmethod
    def delete_user(user_id):
        """Видаляє користувача за ID"""
        conn = get_db_connection()  # Отримуємо підключення до БД
        cursor = conn.cursor()  # Створюємо курсор
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))  # Видаляємо користувача
        conn.commit()  # Зберігаємо зміни
        conn.close()  # Закриваємо підключення
