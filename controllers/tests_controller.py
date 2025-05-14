# Контролер для роботи з таблицею звичайних тестів (TestModel)
from models.tests_model import TestModel

# Контролер для створення нового тесту
def create_test_controller(question, answers, true_answer, category_id):
    """
    Контролер для створення нового тесту
    """
    try:
        # Викликаємо метод моделі для створення тесту з переданими параметрами
        TestModel.create_test(question, answers, true_answer, category_id)
        return True  # Повертаємо True, якщо створення пройшло успішно
    except Exception as e:
        # Виводимо повідомлення про помилку у випадку неуспішного створення
        print(f"Помилка при створенні тесту: {e}")
        return False  # Повертаємо False у разі помилки

# Контролер для отримання списку тестів за категорією
def get_tests_by_category(category_id):
    """
    Отримує список тестів за категорією
    """
    # Викликаємо метод моделі для отримання тестів певної категорії
    return TestModel.get_tests_by_category(category_id)

# Контролер для отримання всіх тестів
def get_all_tests():
    """
    Повертає всі тестові завдання
    """
    # Викликаємо метод моделі для отримання повного списку тестів
    return TestModel.get_all_tests()
