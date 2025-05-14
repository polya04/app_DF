import pandas as pd  # Імпортуємо бібліотеку для роботи з Excel файлами та даними в таблицях
import re  # Імпортуємо бібліотеку для роботи з регулярними виразами
import os  # Імпортуємо бібліотеку для роботи з операційною системою (файли, шляхи тощо)
from models.category_model import CategoryModel  # Імпортуємо модель категорій з бази даних
from models.word_model import WordModel  # Імпортуємо модель слів з бази даних
import unicodedata  # Імпортуємо бібліотеку для роботи з Unicode

def clean_filename(name):  # Функція для очищення та нормалізації імені файлу
    name = unicodedata.normalize('NFC', name)  # Нормалізуємо Unicode в формат NFC
    name = re.sub(r'[<>:"/\\|?*]', '', name)  # Видаляємо заборонені символи з імені
    name = name.replace('\xa0', '').replace(' ', '')  # Видаляємо пробіли та зайві символи
    name = name.replace(' ', '').lower()  # Видаляємо пробіли і приводимо до нижнього регістру
    base, ext = os.path.splitext(name)  # Розділяємо ім'я файлу та розширення
    base = re.sub(r'\.+', '.', base).strip('.')  # Видаляємо зайві крапки в імені файлу
    return f"{base}{ext}"  # Повертаємо очищене ім'я файлу з розширенням

def loadImg(imgPath):  # Функція для завантаження зображень з файлу
    try:
        with open(imgPath, 'rb') as f:  # Спробуємо відкрити зображення
            return f.read()  # Повертаємо вміст зображення
    except Exception as e:  # Якщо виникла помилка
        # print(f"❗ Не удалось открыть изображение: {imgPath} — {e}")
        dir_path, file_name = os.path.split(imgPath)  # Отримуємо шлях до каталогу та ім'я файлу
        cleaned_name = clean_filename(file_name)  # Очищаємо ім'я файлу
        cleaned_path = os.path.join(dir_path, cleaned_name)  # Формуємо новий шлях до файлу

        try:
            with open(cleaned_path, 'rb') as f:  # Спробуємо знову відкрити зображення за новим шляхом
                return f.read()  # Повертаємо вміст зображення
        except Exception as e2:  # Якщо знову виникла помилка
            print(f":{e2}")
            return None  # Повертаємо None, якщо не вдалося відкрити зображення

def loadAudio(audioPath):  # Функція для завантаження аудіо файлів
    try:
        with open(audioPath, 'rb') as f:  # Спробуємо відкрити аудіо файл
            return f.read()  # Повертаємо вміст аудіо файлу
    except Exception as e:  # Якщо виникла помилка
        dir_path, file_name = os.path.split(audioPath)  # Отримуємо шлях до каталогу та ім'я файлу
        cleaned_path = os.path.join(dir_path, file_name)  # Формуємо новий шлях до файлу

        try:
            with open(cleaned_path, 'rb') as f:  # Спробуємо знову відкрити аудіо файл за новим шляхом
                return f.read()  # Повертаємо вміст аудіо файлу
        except Exception as e2:  # Якщо знову виникла помилка
            print(f"аудио:— {e2}")
            return None  # Повертаємо None, якщо не вдалося відкрити аудіо файл

def read_excel_all_sheets(file_path):  # Функція для зчитування всіх листів з Excel файлу
    excel_data = pd.read_excel(file_path, sheet_name=None)  # Завантажуємо всі листи з Excel
    result = []  # Список для зберігання результатів
    for sheet_name, df in excel_data.items():  # Перебираємо кожен лист в Excel
        df = df.dropna()  # Видаляємо порожні рядки
        df.columns = [col.lower() for col in df.columns]  # Перетворюємо імена колонок на нижній регістр
        if not {"німецька фраза", "українська транскрипція", "український переклад"}.issubset(df.columns):  # Перевіряємо чи є необхідні колонки
            print(f"Пропущен лист {sheet_name} — неверные колонки.")  # Якщо колонки не знайдені, виводимо повідомлення
            continue  # Пропускаємо цей лист
        data = [  # Формуємо список даних для кожного рядка листа
            {
                "word": row["німецька фраза"],
                "transcription": row["українська транскрипція"],
                "translate": row["український переклад"],
                "image": loadImg(os.path.join(os.path.dirname(file_path), 'img', sheet_name, f'{row["український переклад"]}.png')),  # Завантажуємо зображення
                "audio": loadAudio(os.path.join(os.path.dirname(file_path), 'audio', clean_filename(sheet_name), clean_filename(f'{row["німецька фраза"]}.mp3')))  # Завантажуємо аудіо
            }
            for _, row in df.iterrows()  # Для кожного рядка в таблиці
        ]
        result.append({"name": sheet_name, "data": data})  # Додаємо результат для кожного листа
    return result  # Повертаємо список результатів

def insert_words_from_excel_data(data):  # Функція для вставки слів з даних з Excel
    all_categories = [cat['name'] for cat in CategoryModel.get_all_categories()]  # Отримуємо всі категорії з бази даних
    existing_words = [w['word'] for w in WordModel.get_all_words()]  # Отримуємо всі слова з бази даних

    for entry in data:  # Перебираємо кожен запис у даних
        if entry['name'] not in all_categories:  # Якщо категорія не існує в базі
            CategoryModel.create_category(entry['name'], 2)  # Створюємо нову категорію (номер сторінки можна змінити)

    categories = CategoryModel.get_all_categories()  # Оновлюємо список категорій
    cat_name_to_id = {c['name']: c['id'] for c in categories}  # Створюємо словник з назви категорії на її ID

    for entry in data:  # Перебираємо кожен запис у даних
        cat_id = cat_name_to_id.get(entry['name'])  # Отримуємо ID категорії
        if not cat_id:  # Якщо категорія не знайдена, пропускаємо
            continue

        for item in entry['data']:  # Перебираємо кожен елемент у даних категорії
            word = item['word']  # Отримуємо слово
            transcription = item['transcription']  # Отримуємо транскрипцію
            translation = item['translate']  # Отримуємо переклад
            image = item['image']  # Отримуємо зображення
            audio = item['audio']  # Отримуємо аудіо

            if word not in existing_words:  # Якщо слово ще не існує в базі
                WordModel.create_word(word, transcription, translation, image, audio, cat_id)  # Створюємо нове слово в базі

def printData(updateData):  # Функція для виведення даних з Excel файлу
    file_path = f"{updateData}\\leksika.xlsx"  # Шлях до Excel файлу
    sheets_data = read_excel_all_sheets(file_path)  # Читаємо всі листи з файлу

    for sheet in sheets_data:  # Перебираємо кожен лист
        print(f"\nЛист: {sheet['name']}")  # Виводимо ім'я листа
        for entry in sheet["data"]:  # Перебираємо кожен запис в листі
            print(f"{entry['word']} — {entry['transcription']} — {entry['translate']}")  # Виводимо слово, транскрипцію та переклад
