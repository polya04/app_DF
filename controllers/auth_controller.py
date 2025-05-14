# Контролер для роботи з таблицею користувачів
from models.user_model import UserModel  # Імпортуємо модель користувача

# Контролер для реєстрації нового користувача
def register_user_controller(username, password):
    """ Контролер для реєстрації нового користувача """
    try:
        # Повертаємо результат створення нового користувача
        return UserModel.create_user(username, password)
    except Exception as e:
        # Виводимо повідомлення про помилку, якщо щось пішло не так
        print(f"Помилка під час реєстрації користувача: {e}")
        return False  # Повертаємо False у випадку помилки

# Контролер для входу користувача
def login_user_controller(username, password):
    """ Контролер для входу користувача """
    try:
        # Повертаємо користувача, якщо логін і пароль правильні
        return UserModel.get_user(username, password)
    except Exception as e:
        # Виводимо повідомлення про помилку, якщо вхід не вдався
        print(f"Помилка під час входу користувача: {e}")
        return None  # Повертаємо None у випадку помилки

# Контролер для отримання списку всіх користувачів
def get_all_users_controller():
    """ Контролер для отримання списку всіх користувачів"""
    try:
        # Повертаємо список усіх користувачів
        return UserModel.get_all_users()
    except Exception as e:
        # Виводимо повідомлення про помилку при спробі отримати список
        print(f"Помилка під час отримання списку користувачів: {e}")
        return []  # Повертаємо порожній список у випадку помилки

# Контролер для оновлення теми інтерфейсу користувача
def update_user_theme_controller(user_id, theme_id):
    """ Контролер для оновлення теми інтерфейсу користувача """
    try:
        # Оновлюємо тему користувача за його ID
        UserModel.update_user_theme(user_id, theme_id)
        return True  # Повертаємо True у разі успішного оновлення
    except Exception as e:
        # Виводимо повідомлення про помилку
        print(f"Помилка під час оновлення теми користувача: {e}")
        return False  # Повертаємо False у випадку помилки

# Контролер для видалення користувача за його ID
def delete_user_controller(user_id):
    """ Контролер для видалення користувача за ID """
    try:
        # Видаляємо користувача
        UserModel.delete_user(user_id)
        return True  # Повертаємо True, якщо видалення пройшло успішно
    except Exception as e:
        # Виводимо повідомлення про помилку
        print(f"Помилка під час видалення користувача: {e}")
        return False  # Повертаємо False у випадку помилки
