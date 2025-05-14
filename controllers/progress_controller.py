# Контролер для роботи з таблицею прогресу
from models.progress_model import ProgressModel

# Контролер для збереження або оновлення прогресу користувача
def save_progress_controller(user_id, category_id, correct, incorrect):
    """ Контролер для збереження або оновлення прогресу """
    if user_id == -1:
        return False  # Якщо ID користувача некоректний, повертаємо False
    try:
        # Викликаємо метод моделі для створення або оновлення прогресу
        ProgressModel.create_progress(user_id, category_id, correct, incorrect)
        return True  # Повертаємо True у випадку успішного збереження
    except Exception as e:
        # Виводимо повідомлення про помилку, якщо щось пішло не так
        print(f"Помилка під час збереження прогресу: {e}")
        return False  # Повертаємо False у випадку помилки

# Контролер для отримання загального прогресу користувача
def get_user_progress_controller(user_id):
    """
    Отримує прогрес користувача по всіх категоріях
    """
    return ProgressModel.get_user_progress(user_id)  # Повертаємо дані прогресу користувача

# Контролер для отримання прогресу користувача по конкретній категорії
def get_progress_for_category_controller(user_id, category_id):
    """
    Отримує прогрес користувача по конкретній категорії
    """
    return ProgressModel.get_progress_by_user_and_category(user_id, category_id)  # Повертаємо прогрес по категорії
