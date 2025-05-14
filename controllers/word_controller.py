# Контролер для роботи з таблицею слів (WordModel)
from models.word_model import WordModel  # Імпортуємо модель слів

# Контролер для додавання нового слова
def add_word(word, transcription, translation, image, audio, category_id):
    # Викликаємо метод моделі для створення слова з усіма його атрибутами
    WordModel.create_word(word, transcription, translation, image, audio, category_id)

# Контролер для отримання слів за категорією
def get_words_by_category(category_id):
    # Повертаємо список слів, що належать до певної категорії
    return WordModel.get_words_by_category(category_id)

# Контролер для отримання всіх слів
def get_all_words():
    # Повертаємо повний список усіх слів з бази даних
    return WordModel.get_all_words()

# Контролер для видалення слова за його ID
def delete_word(word_id):
    # Видаляємо слово з бази даних за допомогою ID
    WordModel.delete_word(word_id)
