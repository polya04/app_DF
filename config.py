# файл в якому зберігаются загальні налаштування проекту
import os

# Отримуємо шлях до батьківської директорії (де знаходиться цей файл)
parent_dir = os.path.dirname(os.path.abspath(__file__))
# Формуємо шлях до папки з даними
updateData = os.path.join(parent_dir, 'data', "")
# Формуємо шлях до папки з зображеннями
imgPaht = os.path.join(parent_dir, 'assets', "img")
# Назва бази даних
DB_NAME = "app.db"


# Світла тема оформлення інтерфейсу
lightTheme = {
    'mainBg': '#FCFCFC',             # Основний фон
    'headerColor': '#F0F0F0',        # Колір заголовків
    'colorFont': '#2C3E50',          # Основний колір тексту
    'colorFont2': '#666',            # Додатковий колір тексту
    'colorFont3': '#333',            # Третій варіант кольору тексту
    'colorBtn': '#5A9B76',           # Колір кнопок
    'colorBtnHover': ' #1F644C',       # Колір кнопок при наведенні
}
# Темна тема оформлення інтерфейсу
darkTheme = {
    'mainBg': '#2C3E50',             # Основний фон
    'headerColor': '#34495E',        # Колір заголовків
    'colorFont': '#ECF0F1',          # Основний колір тексту
    'colorFont2': '#D0D6D8',         # Додатковий колір тексту
    'colorFont3': '#fff',            # Третій варіант кольору тексту
    'colorBtn': '#E74C3C',           # Колір кнопок
    'colorBtnHover': '#C0392B',       # Колір кнопок при наведенні
}
