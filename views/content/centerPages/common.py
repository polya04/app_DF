from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton,
                             QScrollArea, QScroller, QAbstractItemView, QGridLayout)
from PyQt5.QtGui import QPixmap, QIcon
from config import imgPaht
import pyttsx3
import os
import tempfile
from playsound import playsound

# Ініціалізація об'єкта для синтезу мови
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Функція для озвучення тексту
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)  # Озвучення тексту
        engine.runAndWait()  # Очікуємо завершення озвучення
        engine.stop()  # Завершуємо синтезатор
    except Exception as e:
        print(f"Помилка синтезу мови: {e}")

# Функція для відтворення звуку або озвучення слова
def play_or_speak(word, audio_bytes):
    if audio_bytes:
        try:
            # Створення тимчасового файлу для збереження звуку
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name
            playsound(temp_audio_path)  # Відтворення звуку
            os.remove(temp_audio_path)  # Видалення тимчасового файлу після відтворення
        except Exception as e:
            print(f"⚠️ Помилка при відтворенні звуку: {e}")
            speak(word)  # Якщо не вдалося відтворити звук, озвучуємо слово
    else:
        speak(word)  # Якщо немає аудіо, озвучуємо слово

# Функція для створення області прокрутки для контенту
def createScrol(content_widget):
    scroll_area = QScrollArea()  # Створюємо область прокрутки
    scroll_area.setWidgetResizable(True)  # Встановлюємо можливість зміни розміру віджета
    scroll_area.setWidget(content_widget)  # Встановлюємо контент для прокрутки

    # Вимикаємо горизонтальну прокрутку
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # Включаємо вертикальну прокрутку тільки при необхідності
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)  # Додаємо жест прокрутки

    # Гарантуємо, що текст в QLabel буде переноситись
    for label in content_widget.findChildren(QLabel):
        label.setWordWrap(True)  # Включаємо перенос слів

    # Створюємо головний віджет та додаємо область прокрутки
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.addWidget(scroll_area)

    return main_widget

# Функція для налаштування таблиці
def createTable(table, sz, nc=True):
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Відключаємо редагування
    table.setSelectionMode(QAbstractItemView.NoSelection)  # Відключаємо вибір рядків
    table.setFocusPolicy(Qt.NoFocus)  # Відключаємо фокус на таблиці
    table.setShowGrid(True)  # Включаємо показ сітки
    table.setAlternatingRowColors(True)  # Включаємо зміну кольору рядків
    table.horizontalHeader().setStretchLastSection(True)  # Розтягуємо останню секцію
    table.horizontalHeader().setSectionResizeMode(0, table.horizontalHeader().Stretch)  # Розтягуємо першу колонку
    table.horizontalHeader().setSectionResizeMode(1, table.horizontalHeader().Stretch)  # Розтягуємо другу колонку
    if nc:
        table.horizontalHeader().setSectionResizeMode(2, table.horizontalHeader().Stretch)  # Розтягуємо третю колонку, якщо потрібно
    table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Вимикаємо вертикальну прокрутку
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Вимикаємо горизонтальну прокрутку
    if sz == 0:
        table.setFixedHeight(0)  # Якщо розмір 0, приховуємо таблицю
    else:
        table.setFixedHeight(table.horizontalHeader().height() + table.rowHeight(0) * sz)  # Встановлюємо висоту таблиці
    return table

# Функція для створення картки зі словом
def createWordCard(word, translation, transcription, image_data, audio_bytes):
    card = QWidget()
    card.setFixedSize(370, 120)  # Встановлюємо фіксований розмір картки
    card.setObjectName("wordCard")

    mainLayout = QHBoxLayout(card)  # Створюємо горизонтальний лейаут для картки
    mainLayout.setContentsMargins(0, 0, 0, 0)  # Відключаємо відступи
    mainLayout.setSpacing(0)  # Відключаємо відстань між елементами

    # 🖼️ Ліва частина — картинка
    imgLabel = QLabel()  # Створюємо віджет для зображення
    pixmap = QPixmap()  # Створюємо об'єкт для роботи з зображеннями
    pixmap.loadFromData(image_data)  # Завантажуємо зображення з даних
    imgLabel.setPixmap(pixmap.scaled(120, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))  # Встановлюємо зображення з масштабуванням
    imgLabel.setFixedSize(120, 120)  # Встановлюємо фіксований розмір зображення
    imgLabel.setObjectName("wordImage")  # Встановлюємо ім'я об'єкта для стилізації
    mainLayout.addWidget(imgLabel)  # Додаємо зображення в лейаут

    # 📦 Правая частина — слово + звук
    rightContainer = QWidget()  # Створюємо контейнер для правої частини
    rightLayout = QVBoxLayout(rightContainer)  # Створюємо вертикальний лейаут
    rightLayout.setContentsMargins(10, 5, 5, 5)  # Встановлюємо відступи
    rightLayout.setSpacing(5)  # Встановлюємо відстань між елементами

    # 🔊 Кнопка озвучки в правому верхньому куті
    soundBtnLayout = QHBoxLayout()  # Створюємо горизонтальний лейаут для кнопки
    soundBtnLayout.addStretch()  # Додаємо розтягнення

    soundBtn = QPushButton()  # Створюємо кнопку
    soundBtn.setIcon(QIcon(os.path.join(imgPaht, 'speaker.png')))  # Встановлюємо іконку для кнопки
    soundBtn.setIconSize(QSize(20, 20))  # Встановлюємо розмір іконки
    soundBtn.clicked.connect(lambda: play_or_speak(word, audio_bytes))  # При натисканні відтворюємо звук або озвучуємо слово
    soundBtn.setFixedSize(26, 26)  # Встановлюємо фіксований розмір кнопки
    soundBtn.setObjectName("soundButton")  # Встановлюємо ім'я об'єкта для стилізації
    soundBtnLayout.addWidget(soundBtn)  # Додаємо кнопку до лейауту
    rightLayout.addLayout(soundBtnLayout)  # Додаємо лейаут кнопки в правий лейаут

    # 🧠 Слово
    wordLabel = QLabel(word)  # Створюємо віджет для слова
    wordLabel.setObjectName("wordText")  # Встановлюємо ім'я об'єкта
    wordLabel.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання по лівому краю
    rightLayout.addWidget(wordLabel)  # Додаємо слово в лейаут

    # 🔡 Транскрипція
    transcrLabel = QLabel(f"{transcription}")  # Створюємо віджет для транскрипції
    transcrLabel.setObjectName("transcriptionText")  # Встановлюємо ім'я об'єкта
    transcrLabel.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання по лівому краю
    rightLayout.addWidget(transcrLabel)  # Додаємо транскрипцію в лейаут

    # 🌍 Переклад
    translationLabel = QLabel(translation)  # Створюємо віджет для перекладу
    translationLabel.setObjectName("translationText")  # Встановлюємо ім'я об'єкта
    translationLabel.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання по лівому краю
    rightLayout.addWidget(translationLabel)  # Додаємо переклад в лейаут

    rightLayout.addStretch()  # Додаємо розтягнення для заповнення простору
    mainLayout.addWidget(rightContainer)  # Додаємо праву частину в основний лейаут

    return card

# Функція для створення сітки карток зі словами
def createWordGrid(words, img_path, items_per_row=3):
    container = QWidget()  # Створюємо контейнер для сітки
    layout = QGridLayout()  # Створюємо сітковий лейаут
    layout.setSpacing(20)  # Встановлюємо відстань між картками
    layout.setContentsMargins(0, 0, 0, 0)  # Відключаємо відступи
    layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Встановлюємо вирівнювання

    row = 0
    col = 0
    for idx, word in enumerate(words):  # Проходимо по списку слів
        card = createWordCard(
            word['word'],
            word['translation'],
            word['transcription'],
            f'{img_path}\\nf.png'
        )
        layout.addWidget(card, row, col, alignment=Qt.AlignCenter)  # Додаємо картку до сітки
        col += 1
        if col >= items_per_row:  # Якщо кількість елементів в рядку досягла максимума
            col = 0
            row += 1

    container.setLayout(layout)  # Встановлюємо лейаут в контейнер
    return container

# Функція для оновлення стилю віджету
def updateStyle(wiget):
    wiget.style().unpolish(wiget)  # Очищаємо стиль
    wiget.style().polish(wiget)  # Оновлюємо стиль
    wiget.update()  # Оновлюємо віджет
