# Контролер для роботи з таблицею спеціалізованих тестів (SpecTestModel)
from models.spectest_model import SpecTestModel

# Контролер для створення нового спеціалізованого тесту (текстового або з аудіо)
def create_spec_test_controller(question_text, audio_data, correct_answer, category_id):
    """
    Контролер для створення нового спеціалізованого тесту (з текстом або аудіо).
    Лише один з параметрів question_text або audio_data має бути заповненим.
    """
    try:
        # Викликаємо метод моделі для створення тесту
        SpecTestModel.create_test(question_text, audio_data, correct_answer, category_id)
        return True  # Успішне створення тесту
    except Exception as e:
        # Виводимо повідомлення про помилку, якщо створення не вдалося
        print(f"Помилка при створенні спеціалізованого тесту: {e}")
        return False  # Повертаємо False у разі помилки

# Контролер для отримання тестів за категорією
def get_spec_tests_by_category(category_id):
    """
    Отримує список спеціалізованих тестів за категорією.
    """
    try:
        # Повертаємо список тестів із вказаною категорією
        return SpecTestModel.get_tests_by_category(category_id)
    except Exception as e:
        # Виводимо повідомлення про помилку при отриманні тестів
        print(f"Помилка при отриманні тестів за категорією: {e}")
        return []  # Повертаємо порожній список у разі помилки

# Контролер для отримання одного тесту за його ID
def get_spec_test_by_id(test_id):
    """
    Отримує один спеціалізований тест за його ID.
    """
    try:
        # Повертаємо тест з вказаним ID
        return SpecTestModel.get_test_by_id(test_id)
    except Exception as e:
        # Виводимо повідомлення про помилку при отриманні тесту
        print(f"Помилка при отриманні тесту за ID: {e}")
        return None  # Повертаємо None у разі помилки
