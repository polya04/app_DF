from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QHBoxLayout , QStackedWidget,QFrame,
                             QTableWidget, QTableWidgetItem, QLabel)
from views.content.centerPages.common import createScrol, createTable, updateStyle
from staticData.gramaticTexts import page1, page2, page3, page4, page5

class GramaticPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setLayout(self.createWidget())  # Встановлення основного макету для сторінки

    def createWidget(self):
        layout = QHBoxLayout()  # Створення горизонтального макету
        asside_widget = self.createAsside()  # Створення бічного меню
        layout.addWidget(asside_widget, stretch=2)  # Додавання бічного меню до макету з розтягуванням
        self.content_widget = QStackedWidget()  # Створення віджету для багатосторінкових вкладок
        self.content_widget.addWidget(self.page1())  # Додавання першої сторінки
        self.content_widget.addWidget(self.page2())  # Додавання другої сторінки
        self.content_widget.addWidget(self.page3())  # Додавання третьої сторінки
        self.content_widget.addWidget(self.page4())  # Додавання четвертої сторінки
        self.content_widget.addWidget(self.page5())  # Додавання п’ятої сторінки
        layout.addWidget(self.content_widget, stretch=8)  # Додавання вмісту сторінки до макету

        return layout

    def createAsside(self):
        MenuWiget = QWidget()  # Створення віджету для бічного меню
        layout = QVBoxLayout()  # Створення вертикального макету

        self.tabs = [QPushButton("Артиклі der, die, das"), QPushButton("Множина іменників "),
                     QPushButton("Артиклі ein / eine "), QPushButton('Займенники er / sie / es'), 
                     QPushButton("Відмінювання дієслів")]  # Кнопки для кожної теми
        TopLayout = QVBoxLayout()  # Макет для розміщення кнопок
        for i, tab in enumerate(self.tabs):  # Перебір всіх кнопок
            tab.setProperty("class", "asideBtn")  # Додавання класу CSS для кнопки
            TopLayout.addWidget(tab)  # Додавання кнопки до макету
            tab.clicked.connect(partial(self.setWigetInStack, i))  # Підключення функції до натискання кнопки
        self.tabs[0].setObjectName("selected")  # Вибір першої кнопки як активної
        layout.addLayout(TopLayout, 2)  # Додавання макету кнопок до головного макету
        layout.addStretch(3)  # Додавання простору після кнопок

        self.btnBack = QPushButton("Назад")  # Кнопка "Назад"
        self.btnBack.clicked.connect(self.backBtnHandle)  # Підключення функції для кнопки "Назад"
        
        layout.addWidget(self.btnBack, 1)  # Додавання кнопки "Назад" до макету
        MenuWiget.setLayout(layout)  # Встановлення макету для бічного меню
        return MenuWiget  # Повернення готового бічного меню

    def backBtnHandle(self):
        self.parent.setWigetInStack(0)  # Перехід до першої сторінки при натисканні "Назад"

    def setWigetInStack(self, number):
        for i, b in enumerate(self.tabs):  # Перебір кнопок
            b.setObjectName("selected" if i == number else "")  # Вибір активної кнопки
            updateStyle(b)  # Оновлення стилю кнопки
        self.content_widget.setCurrentIndex(number)  # Зміна поточної сторінки

    def InfoBlock (self, obj):
        widget = QFrame()  # Створення віджету для інформаційного блоку
        widget.setObjectName("Infoblock")  # Встановлення CSS класу
        widget.setFrameShape(QFrame.StyledPanel)  # Встановлення форми для віджету
        layout = QVBoxLayout(widget)  # Вертикальний макет для віджету
        titleLabel = QLabel(f"<b>{obj['title']}</b>")  # Заголовок блоку
        titleLabel.setObjectName("InfoLabel")  # Встановлення класу для заголовка
        layout.addWidget(titleLabel)  # Додавання заголовка до макету
        for line in obj['example']:  # Перебір прикладів
            lbl = QLabel(line)  # Створення етикетки для кожного прикладу
            lbl.setWordWrap(True)  # Увімкнення переносу тексту
            lbl.setObjectName("InfoLabel")  # Встановлення класу для етикетки
            layout.addWidget(lbl)  # Додавання етикетки до макету

        return widget  # Повернення готового блоку

    def createToGramaticPage(self, text, btn, p):
        widget = QWidget()  # Створення віджету для переходу на іншу сторінку
        layout = QVBoxLayout(widget)  # Створення вертикального макету для цього віджету
        row = QHBoxLayout()  # Горизонтальний макет для розміщення тексту та кнопки
        row.setAlignment(Qt.AlignLeft)  # Встановлення вирівнювання по лівому краю
        label = QLabel(text)  # Створення етикетки з текстом
        button = QPushButton(btn)  # Створення кнопки
        button.clicked.connect(lambda: self.setWigetInStack(p))  # Підключення функції для натискання кнопки
        row.addWidget(label)  # Додавання етикетки до макету
        row.addWidget(button)  # Додавання кнопки до макету
        row.addStretch()  # Додавання простору після етикетки і кнопки
        layout.addLayout(row)  # Додавання горизонтального макету до вертикального
        return widget  # Повернення готового віджету

    def page1(self):
        Wiget = QWidget()  # Створення віджету для сторінки
        layout = QVBoxLayout(Wiget)  # Створення вертикального макету для сторінки

        self.title = QLabel(page1['section'])  # Заголовок сторінки
        self.title.setObjectName("title")  # Встановлення класу для заголовка
        self.title.setAlignment(Qt.AlignCenter)  # Вирівнювання заголовка по центру
        layout.addWidget(self.title)  # Додавання заголовка до макету

        # Розділ вступу
        introBlock = QWidget()  # Створення віджету для вступу
        introLayout = QVBoxLayout(introBlock)  # Вертикальний макет для вступу
        for paragraph in page1['intro']:  # Перебір абзаців вступу
            label = QLabel(paragraph)  # Створення етикетки для кожного абзацу
            label.setWordWrap(True)  # Увімкнення переносу тексту
            introLayout.addWidget(label)  # Додавання абзацу до макету
        layout.addWidget(introBlock)  # Додавання вступу до макету

        # Розділ артиклів
        for article in page1['articles']:  # Перебір артиклів
            articleBlock = QWidget()  # Створення віджету для артиклів
            articleLayout = QVBoxLayout(articleBlock)  # Вертикальний макет для артиклів

            title = QLabel(f"{article['article']} — {article['description']}")  # Заголовок для артикля
            title.setObjectName('subtitle')  # Встановлення класу для заголовка
            articleLayout.addWidget(title)  # Додавання заголовка до макету

            for example in article['examples']:  # Перебір прикладів
                ex = QLabel(f'● {example}')  # Створення етикетки для кожного прикладу
                ex.setWordWrap(True)  # Увімкнення переносу тексту
                articleLayout.addWidget(ex)  # Додавання прикладу до макету

            layout.addWidget(articleBlock)  # Додавання артикля до макету


        layout.addWidget(self.InfoBlock(page1["gender_mismatch"]))  # Додавання інформаційного блоку
        layout.addWidget(self.InfoBlock(page1["plural"]))  # Додавання інформаційного блоку
        layout.addWidget(self.createToGramaticPage('Про множину іменників можна більше дізнатись в окремому розділі', 'Множина', 1))  # Кнопка для переходу
        layout.addWidget(self.InfoBlock({'title':"Складні слова", 'example':page1["compound_words"]}))  # Інформаційний блок для складних слів

        layout.addStretch()  # Додавання простору після контенту
        return createScrol(Wiget)  # Створення прокручуваного віджету

    def page2(self):
        Wiget = QWidget()  # Створення віджету для сторінки
        layout = QVBoxLayout(Wiget)  # Створення вертикального макету для сторінки

        # Заголовок сторінки
        self.title = QLabel(page2['title'])  # Заголовок сторінки
        self.title.setObjectName("title")  # Встановлення класу для заголовка
        self.title.setAlignment(Qt.AlignCenter)  # Вирівнювання заголовка по центру
        layout.addWidget(self.title)  # Додавання заголовка до макету

        desc = QLabel(page2["description"])  # Опис для сторінки
        desc.setWordWrap(True)  # Увімкнення переносу тексту
        layout.addWidget(desc)  # Додавання опису до макету

        for article in page2['blocks']:  # Перебір блоків сторінки
            articleBlock = QWidget()  # Створення віджету для блоку
            articleLayout = QVBoxLayout(articleBlock)  # Вертикальний макет для блоку
            title = QLabel(f"{article['title']}")  # Заголовок для блоку
            title.setObjectName('subtitle')  # Встановлення класу для заголовка
            articleLayout.addWidget(title)  # Додавання заголовка до макету
            for example in article['items']:  # Перебір елементів блоку
                ex = QLabel(f'● {example}')  # Створення етикетки для кожного елементу
                ex.setWordWrap(True)  # Увімкнення переносу тексту
                articleLayout.addWidget(ex)  # Додавання елементу до макету
            layout.addWidget(articleBlock)  # Додавання блоку до макету

        layout.addStretch()  # Додавання простору після контенту
        return createScrol(Wiget)  # Створення прокручуваного віджету

    def page3(self):
        Wiget = QWidget()  # Створюємо віджет для сторінки
        layout = QVBoxLayout(Wiget)  # Створюємо вертикальний лейаут для сторінки

        # Заголовок сторінки
        self.title = QLabel(page3['title'])  # Створюємо елемент QLabel для заголовка
        self.title.setObjectName("title")  # Встановлюємо ім'я об'єкта для стилізації
        self.title.setAlignment(Qt.AlignCenter)  # Встановлюємо вирівнювання заголовка по центру
        layout.addWidget(self.title)  # Додаємо заголовок до лейаута

        # Опис сторінки
        description_layout = QVBoxLayout()  # Створюємо вертикальний лейаут для опису
        for text in page3['description']:  # Проходимо по кожному тексту в описі
            description_label = QLabel(text)  # Створюємо елемент QLabel для тексту
            description_label.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання тексту по лівому краю
            description_layout.addWidget(description_label)  # Додаємо текст до лейаута опису
        layout.addLayout(description_layout)  # Додаємо лейаут з описом до основного лейаута

        # Створюємо кнопку для переходу на сторінку граматики
        layout.addWidget(self.createToGramaticPage('Означені артиклі ми детально розглянули у розділі', 'Іменники та означені артиклі (Der, Die, Das)',0))

        # Створюємо таблицю
        table = QTableWidget()  # Створюємо віджет таблиці
        table.setRowCount(len(page3['table']['rows']))  # Встановлюємо кількість рядків таблиці
        table.setColumnCount(3)  # Встановлюємо кількість стовпців таблиці
        table.setHorizontalHeaderLabels(page3['table']['headers'])  # Встановлюємо заголовки стовпців
        for i, word in enumerate(page3['table']['rows']):  # Проходимо по рядках таблиці
            table.setItem(i, 0, QTableWidgetItem(word[0]))  # Додаємо елементи до першого стовпця
            table.setItem(i, 1, QTableWidgetItem(word[1]))  # Додаємо елементи до другого стовпця
            table.setItem(i, 2, QTableWidgetItem(word[2]))  # Додаємо елементи до третього стовпця
        layout.addWidget(createTable(table, len(page3['table']['rows'])))  # Додаємо таблицю до лейаута

        # Створюємо блоки з прикладами
        for block in page3['blocks']:  # Проходимо по кожному блоку
            block_layout = QVBoxLayout()  # Створюємо вертикальний лейаут для блоку
            for item in block['list']:  # Проходимо по кожному елементу списку в блоці
                block_label = QLabel(item)  # Створюємо елемент QLabel для кожного елемента списку
                block_layout.addWidget(block_label)  # Додаємо елемент списку до лейаута блоку

            block_example = QLabel(block['example'])  # Створюємо елемент QLabel для прикладу
            block_example.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання прикладу по лівому краю
            block_layout.addWidget(block_example)  # Додаємо приклад до блоку

            layout.addLayout(block_layout)  # Додаємо блок до основного лейаута

        layout.addStretch()  # Додаємо відступ внизу
        return createScrol(Wiget)  # Повертаємо віджет зі скролом

    def page4(self):
        Wiget = QWidget()  # Створюємо віджет для сторінки
        layout = QVBoxLayout(Wiget)  # Створюємо вертикальний лейаут для сторінки
        
        # Заголовок сторінки
        self.title = QLabel(page4['title'])  # Створюємо елемент QLabel для заголовка
        self.title.setObjectName("title")  # Встановлюємо ім'я об'єкта для стилізації
        self.title.setAlignment(Qt.AlignCenter)  # Встановлюємо вирівнювання заголовка по центру
        layout.addWidget(self.title)  # Додаємо заголовок до лейаута

        # Опис сторінки
        self.description = QLabel(page4['description'])  # Створюємо елемент QLabel для опису
        self.description.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання тексту по лівому краю
        layout.addWidget(self.description)  # Додаємо опис до лейаута

        # Проходимо по списках та додаємо їх
        for list_data in page4['lists']:  # Проходимо по кожному списку
            list_title = QLabel(list_data['title'])  # Створюємо елемент QLabel для заголовка списку
            list_title.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання заголовка списку по лівому краю
            list_title.setObjectName('subtitle')  # Встановлюємо ім'я об'єкта для стилізації
            layout.addWidget(list_title)  # Додаємо заголовок списку до лейаута

            # Створюємо список з пунктами
            for item in list_data['items']:  # Проходимо по кожному елементу списку
                list_item = QLabel(f'● {item}')  # Створюємо елемент QLabel для пункту списку
                list_item.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання пункту списку по лівому краю
                layout.addWidget(list_item)  # Додаємо пункт списку до лейаута

        layout.addStretch()  # Додаємо відступ внизу
        return createScrol(Wiget)  # Повертаємо віджет зі скролом

    def page5(self):
        Wiget = QWidget()  # Створюємо віджет для сторінки
        layout = QVBoxLayout(Wiget)  # Створюємо вертикальний лейаут для сторінки

        # Заголовок сторінки
        self.title = QLabel(page5['title'])  # Створюємо елемент QLabel для заголовка
        self.title.setObjectName("title")  # Встановлюємо ім'я об'єкта для стилізації
        self.title.setAlignment(Qt.AlignCenter)  # Встановлюємо вирівнювання заголовка по центру
        layout.addWidget(self.title)  # Додаємо заголовок до лейаута

        # Опис сторінки
        self.description = QLabel(page5['description'])  # Створюємо елемент QLabel для опису
        self.description.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання тексту по лівому краю
        layout.addWidget(self.description)  # Додаємо опис до лейаута

        # Створюємо таблицю
        table = QTableWidget()  # Створюємо віджет таблиці
        table.setRowCount(len(page5['table']['rows']))  # Встановлюємо кількість рядків таблиці
        table.setColumnCount(3)  # Встановлюємо кількість стовпців таблиці
        table.setHorizontalHeaderLabels(page5['table']['headers'])  # Встановлюємо заголовки стовпців
        for i, word in enumerate(page5['table']['rows']):  # Проходимо по рядках таблиці
            table.setItem(i, 0, QTableWidgetItem(word[0]))  # Додаємо елементи до першого стовпця
            table.setItem(i, 1, QTableWidgetItem(word[1]))  # Додаємо елементи до другого стовпця
            table.setItem(i, 2, QTableWidgetItem(word[2]))  # Додаємо елементи до третього стовпця
        layout.addWidget(createTable(table, len(page5['table']['rows'])))  # Додаємо таблицю до лейаута

        # Створюємо список
        list_title = QLabel(page5['list']['title'])  # Створюємо елемент QLabel для заголовка списку
        list_title.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання заголовка списку по лівому краю
        list_title.setObjectName('subtitle')  # Встановлюємо ім'я об'єкта для стилізації
        layout.addWidget(list_title)  # Додаємо заголовок списку до лейаута
        for item in page5['list']['items']:  # Проходимо по кожному елементу списку
            list_item = QLabel(f'● {item}')  # Створюємо елемент QLabel для пункту списку
            list_item.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання пункту списку по лівому краю
            layout.addWidget(list_item)  # Додаємо пункт списку до лейаута

        layout.addStretch()  # Додаємо відступ внизу
        return createScrol(Wiget)  # Повертаємо віджет зі скролом
