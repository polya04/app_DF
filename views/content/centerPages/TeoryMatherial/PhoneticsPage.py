import os
from PyQt5.QtCore import Qt
from functools import partial
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QHBoxLayout , QStackedWidget,
                             QTableWidget, QTableWidgetItem, QTextEdit, QFrame)

from controllers.word_controller import get_words_by_category
from staticData.texts import info_text, reedRules2, readRules, alphabet_blocks
from views.content.centerPages.common import createTable, createScrol, updateStyle
from PyQt5.QtGui import QPixmap
from config import imgPaht


class PhoneticsPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Збереження батьківського віджету
        self.setLayout(self.createWidget())  # Встановлення основного макету

    def createWidget(self):
        layout = QHBoxLayout()  # Створення горизонтального макету
        asside_widget = self.createAsside()  # Створення бічної панелі
        layout.addWidget(asside_widget, stretch=2)  # Додавання бічної панелі в макет

        self.content_widget = QStackedWidget()  # Створення віджету для вкладок
        self.content_widget.addWidget(self.createAlphabet())  # Додавання вкладки "Алфавіт"
        self.content_widget.addWidget(self.createReadRules())  # Додавання вкладки "Загальні правила"
        self.content_widget.addWidget(self.createIntonation())  # Додавання вкладки "Інтонація"
        self.content_widget.setObjectName("cr")  # Присвоєння ідентифікатора
        layout.addWidget(self.content_widget, stretch=8)  # Додавання віджету вкладок

        return layout  # Повернення головного макету
    
    def createAsside(self):
        MenuWiget = QWidget()  # Створення віджету для бічного меню
        layout = QVBoxLayout()  # Створення вертикального макету

        # Створення кнопок для вкладок
        self.tabs = [QPushButton("Алфавіт"), QPushButton("Загальні правила наголосу"), QPushButton("Інтонація")]
        TopLayout = QVBoxLayout()  # Створення вертикального макету для кнопок вкладок
        for i, tab in enumerate(self.tabs):
            tab.setProperty("class", "asideBtn")  # Встановлення класу для кнопок
            TopLayout.addWidget(tab)  # Додавання кнопки в макет
            tab.clicked.connect(partial(self.setWigetInStack, i))  # Зв'язування кнопки з функцією зміни вкладки
        self.tabs[0].setObjectName("selected")  # Виділення першої кнопки як вибраної
        layout.addLayout(TopLayout, 2)  # Додавання макету з кнопками
        layout.addStretch(3)  # Додавання порожнього простору

        self.btnBack = QPushButton("Назад")  # Кнопка для повернення назад
        self.btnBack.clicked.connect(self.backBtnHandle)  # Зв'язування кнопки з функцією повернення назад
        layout.addWidget(self.btnBack, 1)  # Додавання кнопки в макет
        MenuWiget.setLayout(layout)  # Встановлення макету для бічного меню
        return MenuWiget  # Повернення бічного меню

    def setWigetInStack(self, number):
        for i, b in enumerate(self.tabs):
            b.setObjectName("selected" if i == number else "")  # Вибір активної вкладки
            updateStyle(b)  # Оновлення стилю вкладки
        self.content_widget.setCurrentIndex(number)  # Зміна активної вкладки
        # self.parent.parent.parent.setTheme()  # Можливе встановлення теми для батьківського вікна

    def backBtnHandle(self):
        self.parent.setWigetInStack(0)  # Перехід до першої вкладки при натисканні кнопки "Назад"
    
    def createTable(self, words):
        table = QTableWidget()  # Створення таблиці
        table.setRowCount(len(words))  # Встановлення кількості рядків
        table.setColumnCount(2)  # Встановлення кількості стовпців
        table.setHorizontalHeaderLabels(["Буква", "Назва"])  # Встановлення заголовків таблиці
        for i, word in enumerate(words):
            table.setItem(i, 0, QTableWidgetItem(word['word']))  # Додавання слова до таблиці
            table.setItem(i, 1, QTableWidgetItem(word['transcription']))  # Додавання транскрипції
        return createTable(table, len(words), False)  # Повернення таблиці

    def createAlphabet(self):
        widget = QWidget()  # Створення віджету для алфавіту
        layout = QVBoxLayout(widget)  # Створення вертикального макету
        layout.setContentsMargins(20,20,20,20)  # Встановлення відступів
        simpleWords = get_words_by_category(1)  # Отримання слів для першої категорії
        anotherWords = get_words_by_category(2)  # Отримання слів для іншої категорії

        title = QLabel('Алфавіт')  # Заголовок для алфавіту
        title.setObjectName("title")  # Встановлення ідентифікатора для заголовка
        title.setAlignment(Qt.AlignCenter)  # Встановлення вирівнювання
        layout.addWidget(title)  # Додавання заголовка до макету
        layout.addWidget(QLabel(info_text))  # Додавання інформаційного тексту
        layout.addWidget(self.createTable(simpleWords))  # Додавання таблиці з простими словами
        title = QLabel('Особливі букви')  # Заголовок для особливих букв
        title.setObjectName("subtitle")  # Встановлення ідентифікатора для заголовка
        title.setAlignment(Qt.AlignCenter)  # Встановлення вирівнювання
        layout.addWidget(title)  # Додавання заголовка до макету
        layout.addWidget(self.createTable(anotherWords))  # Додавання таблиці з іншими словами

        intro_label = QLabel('Давайте розглянемо певні особливості у вимові.')  # Опис особливостей вимови
        intro_label.setObjectName("subtitle")  # Встановлення ідентифікатора для опису
        layout.addWidget(intro_label)  # Додавання тексту до макету

        for block in alphabet_blocks:  # Проходження по блоках алфавіту
            section_frame = QFrame()  # Створення рамки для секції
            section_frame.setObjectName("sectionBlock")  # Встановлення ідентифікатора для секції
            section_layout = QVBoxLayout(section_frame)  # Створення вертикального макету для секції

            block_title = QLabel(block["title"])  # Заголовок секції
            block_title.setObjectName("sectionTitle")  # Встановлення ідентифікатора для заголовка
            section_layout.addWidget(block_title)  # Додавання заголовка до макету

            desc_label = QLabel(block["description"])  # Опис секції
            desc_label.setWordWrap(True)  # Увімкнення переносу слів
            desc_label.setObjectName("sectionDesc")  # Встановлення ідентифікатора для опису
            section_layout.addWidget(desc_label)  # Додавання опису до макету

            if block.get("examples"):  # Якщо є приклади
                for ex in block["examples"]:  # Проходження по прикладах
                    if ex["type"] == "text":
                        label = QLabel("• " + ex["content"])  # Текстовий приклад
                        label.setObjectName("exampleText")  # Встановлення ідентифікатора для прикладу
                        label.setStyleSheet("margin-left: 10px; margin-bottom: 5px;")  # Стиль для прикладу
                    elif ex["type"] == "subtitle":
                        label = QLabel(ex["content"])  # Заголовок для прикладу
                        label.setObjectName("exampleSubtitle")  # Встановлення ідентифікатора для заголовка
                        label.setStyleSheet("font-weight: bold; margin-top: 8px; margin-bottom: 4px;")  # Стиль для заголовка
                    elif ex["type"] == "spacer":
                        label = QLabel("")  # Порожній елемент для відступу
                        label.setStyleSheet("margin-bottom: 6px;")  # Стиль для відступу
                    
                    label.setWordWrap(True)  # Увімкнення переносу слів
                    section_layout.addWidget(label)  # Додавання елементу до макету

            layout.addWidget(section_frame)  # Додавання секції до макету

        return createScrol(widget)  # Повернення скролу з віджетом


    def createReadRules(self):
        widget = QWidget()  # Створення віджету для правил
        layout = QVBoxLayout()  # Створення вертикального макету

        block = reedRules2['sections'][0]  # Отримання першого блоку правил
        title = QLabel(block['title'])  # Заголовок для правил
        title.setObjectName("title")  # Встановлення ідентифікатора для заголовка
        title.setAlignment(Qt.AlignCenter)  # Встановлення вирівнювання
        layout.addWidget(title)  # Додавання заголовка до макету
        section_description = QLabel(block['description'])  # Опис правил
        section_description.setObjectName("description")  # Встановлення ідентифікатора для опису
        layout.addWidget(section_description)  # Додавання опису до макету

        for block_item in block['blocks']:  # Проходження по блоках правила
                block_layout = QHBoxLayout()  # Створення горизонтального макету для блока    
                subtitle = QLabel(block_item['subtitle'])  # Заголовок для блока
                subtitle.setObjectName("subtitle")  # Встановлення ідентифікатора для заголовка
                block_layout.addWidget(subtitle)  # Додавання заголовка до макету

                layout.addLayout(block_layout)  # Додавання горизонтального макету до вертикального

                content = QTextEdit()  # Текстове поле для контенту
                content.setReadOnly(True)  # Встановлення режиму лише для читання
                content.setPlainText("\n".join(block_item['content']))  # Встановлення тексту в поле
                layout.addWidget(content)  # Додавання текстового поля до макету
        layout.addStretch()  # Додавання порожнього простору
        widget.setLayout(layout)  # Встановлення макету для віджету
        return createScrol(widget)  # Повернення скролу з віджетом

    def createIntonation(self):
        widget = QWidget()  # Створення віджету для інтонації
        layout = QVBoxLayout()  # Створення вертикального макету

        block = reedRules2['sections'][1]  # Отримання другого блоку правил
        title = QLabel(block['title'])  # Заголовок для інтонації
        title.setObjectName("title")  # Встановлення ідентифікатора для заголовка
        title.setAlignment(Qt.AlignCenter)  # Встановлення вирівнювання
        layout.addWidget(title)  # Додавання заголовка до макету
        section_description = QLabel(block['description'])  # Опис інтонації
        section_description.setObjectName("description")  # Встановлення ідентифікатора для опису
        layout.addWidget(section_description)  # Додавання опису до макету

        for block_item in block['blocks']:  # Проходження по блоках інтонації
                block_layout = QHBoxLayout()  # Створення горизонтального макету для блока
                
                if 'image' in block_item:  # Якщо є зображення
                    image_label = QLabel()  # Створення віджету для зображення
                    image_label.setPixmap(QPixmap( os.path.join(imgPaht, block_item['image']))  # Завантаження зображення
                                          .scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Масштабування зображення
                    image_label.setFixedSize(50, 50)  # Встановлення розміру зображення
                    block_layout.addWidget(image_label)  # Додавання зображення до макету
                
                subtitle = QLabel(block_item['subtitle'])  # Заголовок для блока
                subtitle.setObjectName("subtitle")  # Встановлення ідентифікатора для заголовка
                block_layout.addWidget(subtitle)  # Додавання заголовка до макету

                layout.addLayout(block_layout)  # Додавання горизонтального макету до вертикального

                content = QTextEdit()  # Текстове поле для контенту
                content.setReadOnly(True)  # Встановлення режиму лише для читання
                content.setPlainText("\n".join(block_item['content']))  # Встановлення тексту в поле
                layout.addWidget(content)  # Додавання текстового поля до макету
        layout.addStretch()  # Додавання порожнього простору
        widget.setLayout(layout)  # Встановлення макету для віджету
        return createScrol(widget)  # Повернення скролу з віджетом
