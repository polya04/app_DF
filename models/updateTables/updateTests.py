import json  # Імпортуємо бібліотеку для роботи з JSON файлами
import os  # Імпортуємо бібліотеку для роботи з операційною системою

from models.category_model import CategoryModel  # Імпортуємо модель категорій
from models.tests_model import TestModel  # Імпортуємо модель тестів
from models.spectest_model import SpecTestModel  # Імпортуємо модель спеціальних тестів


def loadAudio(audioPath):  # Функція для завантаження аудіофайлу за вказаним шляхом
    try:
        with open(audioPath, 'rb') as f:  # Спроба відкрити аудіофайл у двійковому режимі
            return f.read()  # Повертаємо вміст файлу
    except Exception as e:  # Якщо виникла помилка при відкритті файлу
        dir_path, file_name = os.path.split(audioPath)  # Отримуємо директорію та ім'я файлу
        cleaned_path = os.path.join(dir_path, file_name)  # Формуємо шлях до файлу
        try:
            with open(cleaned_path, 'rb') as f:  # Спроба відкрити файл з очищеною назвою
                return f.read()  # Повертаємо вміст файлу
        except Exception as e2:  # Якщо виникла помилка при повторній спробі
            print(f"аудио:— {e2}")  # Виводимо повідомлення про помилку
            return None  # Повертаємо None, якщо файл не вдалося завантажити

def updateTests(folder_path):  # Функція для оновлення тестів із заданої папки
    test_json = os.path.join(folder_path, 'tests.json')  # Формуємо шлях до файлу tests.json
    spectest_json = os.path.join(folder_path, 'spectest.json')  # Формуємо шлях до файлу spectest.json
    spectestfolder = os.path.join(folder_path, 'tests')  # Формуємо шлях до папки tests
    if not os.path.exists(test_json):  # Перевіряємо, чи існує файл tests.json
        print(f"Файл не знайдено: {test_json}")  # Якщо файл не знайдено, виводимо повідомлення
        return  # Виходимо з функції
    with open(test_json, 'r', encoding='utf-8') as f:  # Відкриваємо файл tests.json для читання
        data = json.load(f)  # Завантажуємо дані з файлу у змінну data
    if not os.path.exists(spectest_json):  # Перевіряємо, чи існує файл spectest.json
        print(f"Файл не знайдено: {spectest_json}")  # Якщо файл не знайдено, виводимо повідомлення
        return  # Виходимо з функції
    with open(spectest_json, 'r', encoding='utf-8') as f:  # Відкриваємо файл spectest.json для читання
        specdata = json.load(f)  # Завантажуємо дані з файлу у змінну specdata

    all_categories = [cat['name'] for cat in CategoryModel.get_all_categories()]  # Отримуємо всі категорії з бази даних
    for theme in data['categories']:  # Перебираємо всі категорії з файлу tests.json
        if theme['name'] not in all_categories:  # Якщо категорія ще не існує в базі даних
            CategoryModel.create_category(theme['name'], theme['page'])  # Створюємо нову категорію в базі даних
    
    for block in data['body']:  # Перебираємо всі блоки тестів у файлі tests.json
        categoryid = CategoryModel.get_category_by_name(block['theme'])  # Отримуємо категорію по назві
        for t in block['tests']:  # Перебираємо всі тести в поточному блоці
            TestModel.create_test(t['question'], t['answers'], t['correct'], t['type'], categoryid['id'])  # Додаємо тест в базу даних
    
    categoryid  = CategoryModel.get_category_by_name(specdata['theme'])  # Отримуємо категорію для спеціальних тестів
    for t in specdata['tests']:  # Перебираємо всі спеціальні тести
        audio_data = loadAudio(os.path.join(spectestfolder, t['audio_data']))  # Завантажуємо аудіофайл для тесту
        SpecTestModel.create_test(t['question'], audio_data, t['correct_answer'], t['type'], categoryid['id'])  # Додаємо спеціальний тест в базу даних
