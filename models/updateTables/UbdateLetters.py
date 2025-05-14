import json  # Імпортуємо бібліотеку для роботи з JSON файлами
import os  # Імпортуємо бібліотеку для роботи з операційною системою (перевірка існування файлів тощо)

from models.category_model import CategoryModel  # Імпортуємо модель категорії з бази даних
from models.word_model import WordModel  # Імпортуємо модель слів з бази даних

def insert_default_alphabet_from_json(json_path):  # Функція для вставки алфавіту за допомогою даних з JSON файлу
    if not os.path.exists(json_path):  # Якщо файл не існує за вказаним шляхом
        print(f"Файл не знайдено: {json_path}")  # Виводимо повідомлення про відсутність файлу
        return  # Виходимо з функції, не виконуючи подальших дій
    with open(json_path, 'r', encoding='utf-8') as f:  # Відкриваємо файл у режимі читання
        data = json.load(f)  # Завантажуємо вміст файлу в форматі JSON

    all_categories = [cat['name'] for cat in CategoryModel.get_all_categories()]  # Отримуємо всі категорії з бази даних
    for category in data.get('categories', []):  # Перебираємо всі категорії з JSON файлу
        if category['name'] not in all_categories:  # Якщо категорія з файлу ще не існує в базі
            CategoryModel.create_category(category['name'], category['numberOfPage'])  # Створюємо нову категорію в базі
    categories = CategoryModel.get_all_categories()  # Отримуємо оновлений список категорій з бази
    cat_name_to_id = {c['name']: c['id'] for c in categories}  # Створюємо словник, де ключ — назва категорії, а значення — її ID
    existing_words = [w['word'] for w in WordModel.get_all_words()]  # Отримуємо всі слова з бази даних
    for entry in data.get("normal_letters", []):  # Перебираємо всі нормальні літери з JSON файлу
        word = entry['word']  # Беремо слово з поточного запису
        if word not in existing_words:  # Якщо таке слово ще не існує в базі
            WordModel.create_word(  # Створюємо нове слово в базі
                word,
                entry['transcription'],
                entry['translation'],
                None, None,  # Параметри для зображення та аудіо не вказано
                cat_name_to_id.get("Звичайні букви")  # Встановлюємо категорію "Звичайні букви"
            )
    for entry in data.get("special_letters", []):  # Перебираємо всі спеціальні літери з JSON файлу
        word = entry['word']  # Беремо слово з поточного запису
        if word not in existing_words:  # Якщо таке слово ще не існує в базі
            WordModel.create_word(  # Створюємо нове слово в базі
                word,
                entry['transcription'],
                entry['translation'],
                None, None,  # Параметри для зображення та аудіо не вказано
                cat_name_to_id.get("Особливі букви")  # Встановлюємо категорію "Особливі букви"
            )


def loadLeters(updateData):  # Функція для завантаження літер
    insert_default_alphabet_from_json(f'{updateData}')  # Викликаємо функцію для вставки алфавіту з JSON файлу за вказаним шляхом
    # print("\nЗагруженные буквы:")
    # all_words = WordModel.get_all_words()  # Виводимо всі слова з бази даних
    # for word in all_words:  # Для кожного слова в базі
    #     print(f"{word['word']} — {word['transcription']} — {word['translation']} (категория ID: {word['category_id']})")

def printAll():  # Функція для виведення всіх слів
    all_words = WordModel.get_all_words()  # Отримуємо всі слова з бази
    for word in all_words:  # Перебираємо всі слова
        print(f"{word['word']} — {word['transcription']} — {word['translation']} (категория ID: {word['category_id']})")  # Виводимо кожне слово, його транскрипцію, переклад та ID категорії
