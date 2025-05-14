from functools import partial  # Імпортуємо partial для часткового застосування функцій (передача аргументів)
from PyQt5.QtCore import Qt  # Імпортуємо Qt для вирівнювання та інших параметрів
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QHBoxLayout, QStackedWidget, QSizePolicy)  # Імпортуємо елементи GUI з PyQt5

from controllers.category_controller import get_category_by_page  # Функція для отримання категорій з контролера
from controllers.word_controller import get_words_by_category  # Функція для отримання слів за категорією
from views.content.centerPages.common import createScrol, QGridLayout, createWordCard, updateStyle  # Імпорт спільних компонентів
from config import imgPaht  # Імпорт шляху до зображень
from staticData.lexis import lexis, lexisToNumber  # Статичні словники з лексикою
from PyQt5.QtWidgets import QWIDGETSIZE_MAX  # Константа для встановлення максимального розміру віджету

# Функція для завантаження зображення як байтів
def load_image_as_bytes(path):
    try:
        with open(path, 'rb') as f:  # Відкриваємо файл у бінарному режимі
            return f.read()  # Повертаємо байти зображення
    except FileNotFoundError:  # Якщо файл не знайдено
        print(f"Файл не найден: {path}")  # Виводимо повідомлення про помилку
        return None  # Повертаємо None як індикатор помилки

# Клас для відображення сторінки з лексикою
class LexisPageFlex(QWidget):
    def __init__(self, parent):
        super().__init__()  # Викликаємо конструктор базового класу QWidget
        self.parent = parent  # Зберігаємо батьківський елемент
        self.setLayout(self.createWidget())  # Встановлюємо головний layout
    # Створюємо головний layout сторінки
    def createWidget(self):
        layout = QHBoxLayout()  # Горизонтальний layout для розміщення меню та контенту
        asside_widget = self.createAsside()  # Створюємо меню (бокова панель)
        layout.addWidget(asside_widget, stretch=2)  # Додаємо меню з коефіцієнтом розтягування 2

        self.content_widget = QStackedWidget()  # Стек віджетів для відображення контенту
        self.content_widget.addWidget(self.createWordsPart())  # Додаємо перший віджет зі словами
        self.content_widget.setObjectName("cr")  # Задаємо ім’я об’єкта для стилізації
        layout.addWidget(self.content_widget, stretch=8)  # Додаємо до layout з більшою шириною

        return layout  # Повертаємо готовий layout
    # Створюємо бокове меню з категоріями
    def createAsside(self):
        MenuWiget = QWidget()  # Створюємо новий віджет для меню
        layout = QVBoxLayout()  # Вертикальний layout для меню

        categories = get_category_by_page(2)  # Отримуємо список категорій з бази
        TopLayout = QVBoxLayout()  # Layout для кнопок категорій
        self.tabs = []  # Список для збереження вкладок (кнопок)

        for idx, c in enumerate(categories):  # Проходимо по кожній категорії
            tab = QPushButton(c['name'])  # Створюємо кнопку з назвою категорії
            TopLayout.addWidget(tab)  # Додаємо кнопку до layout
            tab.clicked.connect(partial(self.setWigetInStack, idx, c['id'], c['name']))  # Прив’язуємо функцію перемикання
            self.tabs.append(tab)  # Додаємо кнопку до списку вкладок

        layout.addLayout(TopLayout, 3)  # Додаємо кнопки в основний layout меню
        layout.addStretch(2)  # Додаємо розтяг знизу

        self.btnBack = QPushButton("Назад")  # Кнопка повернення назад
        self.btnBack.clicked.connect(self.backBtnHandle)  # Прив’язуємо дію для повернення

        layout.addWidget(self.btnBack, 1)  # Додаємо кнопку "Назад" до меню
        MenuWiget.setLayout(layout)  # Встановлюємо layout для віджета меню
        return MenuWiget  # Повертаємо готовий віджет меню
    # Обробник кнопки "Назад" — повертає на попередню сторінку
    def backBtnHandle(self):
        self.parent.setWigetInStack(0)  # Повертаємось до першого екрана (індекс 0)

    def createGrid(self, words):
        while self.wordGridLayout.count():  # Поки є елементи в grid-розмітці
            item = self.wordGridLayout.takeAt(0)  # Видаляємо елемент
            if item.widget():  # Якщо це віджет
                item.widget().deleteLater()  # Видаляємо віджет

        row = 0  # Початковий рядок
        col = 0  # Початковий стовпець
        items_per_row = 3  # Кількість карток у рядку

        for idx, word in enumerate(words):  # Проходимо по списку слів
            wordCard = createWordCard(  # Створюємо картку слова
                word['word'],  # Слово
                word['translation'],  # Переклад
                word['transcription'],  # Транскрипція
                word['image'] if (word['image'] != None) else load_image_as_bytes(f'{imgPaht}\\nf.png'),  # Зображення або заміна
                word['audio']  # Аудіо
            )

            # Вирівнювання карток залежно від позиції
            if idx == 0:
                self.wordGridLayout.addWidget(wordCard, row, col, alignment=Qt.AlignLeft)
            elif idx == 1:
                self.wordGridLayout.addWidget(wordCard, row, col, alignment=Qt.AlignCenter)
            else:
                self.wordGridLayout.addWidget(wordCard, row, col, alignment=Qt.AlignRight)

            col += 1  # Переходимо до наступного стовпця
            if col >= items_per_row:  # Якщо досягнуто максимум — новий рядок
                col = 0
                row += 1
    def createToGramaticPage(self):
        widget = QWidget()  # Створюємо новий віджет
        layout = QVBoxLayout(widget)  # Вертикальний layout
        row = QHBoxLayout()  # Горизонтальний рядок
        row.setAlignment(Qt.AlignLeft)  # Вирівнювання зліва

        label = QLabel("Детальніше про рід кожного артикля можна дізнатись у розділі")  # Текст-підказка
        button = QPushButton("Граматика")  # Кнопка для переходу
        button.clicked.connect(lambda: self.parent.setWigetInStack(3))  # Обробник кліку — перехід до сторінки 3

        row.addWidget(label)  # Додаємо текст
        row.addWidget(button)  # Додаємо кнопку
        row.addStretch()  # Додаємо розтяг з правого боку

        layout.addLayout(row)  # Додаємо рядок у layout
        return widget  # Повертаємо створений віджет
    def clearLayoutFromWidget(self, widget):
        layout = widget.layout()  # Отримуємо layout з віджета
        if layout is not None:
            # Видаляємо всі елементи з layout
            while layout.count():
                item = layout.takeAt(0)
                child_widget = item.widget()  # Якщо елемент — віджет
                if child_widget is not None:
                    child_widget.setParent(None)  # Від'єднуємо його
                elif item.layout():
                    self.clearLayoutFromWidget(item.layout())  # Рекурсивно чистимо вкладені layout'и

            # Від'єднуємо сам layout від віджета
            QWidget().setLayout(layout)
    def createTips(self, tips):
        layout = QVBoxLayout()  # Створюємо вертикальний layout
        self.tips_label = QLabel(tips)  # Створюємо мітку з порадами
        self.tips_label.setObjectName("tips")  # Ім’я для стилізації
        self.tips_label.setAlignment(Qt.AlignLeft)  # Вирівнювання зліва
        layout.addWidget(self.tips_label)  # Додаємо мітку до layout
        return layout  # Повертаємо готовий layout
    def createExample(self, examples):
        layout = QVBoxLayout()  # Створюємо вертикальний layout
        self.examples_title = QLabel('Приклади:')  # Заголовок блоку прикладів
        self.examples_title.setObjectName("examples_title")
        self.examples_title.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.examples_title)  # Додаємо заголовок

        for example in examples:  # Додаємо кожен приклад у layout
            example_item = QLabel(f"• {example}")  # Один приклад з маркером
            example_item.setObjectName("example_item")
            example_item.setAlignment(Qt.AlignLeft)
            layout.addWidget(example_item)  # Додаємо до layout

        return layout  # Повертаємо зібраний блок з прикладами

    def createGridNumber(self, data):  # Функція для створення сітки з числовими даними
        wordGridLayout = QGridLayout()  # Створюємо макет сітки
        wordGridLayout.setSpacing(20)  # Встановлюємо відстань між елементами сітки
        wordGridLayout.setContentsMargins(0, 20, 0, 20)  # Встановлюємо поля макету
        wordGridLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Встановлюємо вирівнювання елементів по верху та по горизонталі
        gridContainer = QWidget()  # Створюємо контейнер для сітки
        gridContainer.setLayout(wordGridLayout)  # Встановлюємо макет сітки до контейнера
        gridContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Встановлюємо політику розміру контейнера
        scrollable = createScrol(gridContainer)  # Створюємо скролюючий віджет для контейнера
        fixedContainer = QWidget()  # Створюємо фіксований контейнер
        fixedLayout = QVBoxLayout(fixedContainer)  # Створюємо вертикальний макет для фіксованого контейнера
        fixedLayout.setContentsMargins(0, 0, 0, 0)  # Встановлюємо поля для вертикального макету
        fixedLayout.addWidget(scrollable)  # Додаємо скролюючий віджет до макету
        fixedContainer.setMinimumHeight(500)  # Встановлюємо мінімальну висоту контейнера
        row = 0  # Ініціалізуємо змінну для рядка
        col = 0  # Ініціалізуємо змінну для стовпця
        items_per_row = 3  # Кількість елементів в рядку
        for idx, word in enumerate(data):  # Перебираємо всі слова в даних
            wordCard = createWordCard(  # Створюємо картку для кожного слова
                word['word'],  # Слово
                word['translation'],  # Переклад
                word['transcription'],  # Транскрипція
                word['image'] if (word['image']!=None) else load_image_as_bytes(f'{imgPaht}\\nf.png'),  # Зображення або стандартне
                word['audio']  # Аудіо
            )
            if idx == 0:  # Якщо індекс 0
                wordGridLayout.addWidget(wordCard, row, col, alignment=Qt.AlignLeft)  # Додаємо картку в сітку з вирівнюванням по лівому краю
            elif idx == 1:  # Якщо індекс 1
                wordGridLayout.addWidget(wordCard, row, col, alignment=Qt.AlignCenter)  # Додаємо картку в сітку з вирівнюванням по центру
            else:  # Якщо індекс більший за 1
                wordGridLayout.addWidget(wordCard, row, col, alignment=Qt.AlignRight)  # Додаємо картку в сітку з вирівнюванням по правому краю
            col += 1  # Збільшуємо стовпець на 1
            if col >= items_per_row:  # Якщо кількість елементів в рядку більше або дорівнює кількості елементів в рядку
                col = 0  # Скидаємо стовпець до 0
                row += 1  # Збільшуємо рядок на 1

        return fixedContainer  # Повертаємо контейнер з сіткою
    def createList(self, layout, list):  # Функція для створення списку з елементів
        for item in list:  # Перебираємо всі елементи в списку
            list_item = QLabel(f'● {item}')  # Створюємо мітку для кожного елемента
            list_item.setAlignment(Qt.AlignLeft)  # Встановлюємо вирівнювання по лівому краю
            layout.addWidget(list_item)  # Додаємо мітку до макету
    def createSpecialToNumber(self):  # Функція для створення спеціальних даних до числа
        words = get_words_by_category(4)  # Отримуємо слова з категорії 4
        w1 = words[12:19]  # Вибираємо слова з індексами від 12 до 19
        w2 = words[19:len(words)-4]  # Вибираємо слова з індексами від 19 до кінця (мінус 4)
        widget = QWidget()  # Створюємо віджет
        layout = QVBoxLayout(widget)  # Створюємо вертикальний макет для віджету
        layout.addWidget(QLabel(lexisToNumber['1']))  # Додаємо мітку з першою частиною лексики
        self.createList(layout, lexisToNumber['l1'])  # Створюємо список для першої групи лексики
        layout.addWidget(QLabel(lexisToNumber['2']))  # Додаємо мітку з другою частиною лексики
        layout.addWidget(self.createGridNumber(w1))  # Додаємо сітку з першими словами
        layout.addWidget(QLabel(lexisToNumber['3']))  # Додаємо мітку з третьою частиною лексики
        self.createList(layout, lexisToNumber['l2'])  # Створюємо список для другої групи лексики
        layout.addWidget(QLabel(lexisToNumber['4']))  # Додаємо мітку з четвертою частиною лексики
        layout.addWidget(QLabel(lexisToNumber['5']))  # Додаємо мітку з п’ятою частиною лексики
        layout.addWidget(QLabel(lexisToNumber['t11']))  # Додаємо тестову мітку
        layout.addWidget(QLabel(lexisToNumber['t12']))  # Додаємо тестову мітку
        layout.addWidget(QLabel(lexisToNumber['t13']))  # Додаємо тестову мітку
        layout.addWidget(QLabel(lexisToNumber['6']))  # Додаємо мітку з шостою частиною лексики
        layout.addWidget(QLabel(lexisToNumber['7']))  # Додаємо мітку з сьомою частиною лексики
        self.createList(layout, lexisToNumber['l3'])  # Створюємо список для третьої групи лексики
        layout.addWidget(QLabel(lexisToNumber['8']))  # Додаємо мітку з восьмою частиною лексики
        self.createList(layout, lexisToNumber['l4'])  # Створюємо список для четвертої групи лексики

        layout.addWidget(QLabel(lexisToNumber['9']))  # Додаємо мітку з дев’ятою частиною лексики
        layout.addWidget(QLabel(lexisToNumber['t21']))  # Додаємо тестову мітку
        layout.addWidget(QLabel(lexisToNumber['t22']))  # Додаємо тестову мітку
        layout.addWidget(QLabel(lexisToNumber['t23']))  # Додаємо тестову мітку
        layout.addWidget(QLabel(lexisToNumber['10']))  # Додаємо мітку з десятою частиною лексики
        layout.addWidget(QLabel(lexisToNumber['t31']))  # Додаємо тестову мітку
        layout.addWidget(QLabel(lexisToNumber['t32']))  # Додаємо тестову мітку
        layout.addWidget(self.createGridNumber(w2))  # Додаємо сітку з іншими словами
        return widget  # Повертаємо віджет зі всіма елементами

    def setWigetInStack(self, number, categNum, cutName):
        # Цикл для обробки всіх вкладок
        for i, b in enumerate(self.tabs):
            # Встановлення стилю для вибраної вкладки
            b.setObjectName("selected" if i == number else "")
            updateStyle(b)
        
        # Встановлення заголовку
        self.title.setText(cutName)
        # Встановлення опису з лексикону
        self.desc.setText(lexis[number]['description'])

        # Отримання порад для лексеми
        tips = lexis[number]['tips'] 
        # Очищаємо старі поради
        self.clearLayoutFromWidget(self.widgetTrips)
        if (tips!=''):
            # Якщо є поради, встановлюємо їх
            self.widgetTrips.setLayout(self.createTips(tips))
            self.widgetTrips.setVisible(True)
        else:
            # Якщо порад немає, просто робимо їх видимими
            self.widgetTrips.setVisible(True)

        # Отримання прикладів для лексеми
        examples = lexis[number]['examples']
        # Очищаємо старі приклади
        self.clearLayoutFromWidget(self.widgetexamples)
        if (examples!=[]):
            # Якщо є приклади, встановлюємо їх
            self.widgetexamples.setLayout(self.createExample(examples))
            self.widgetexamples.setVisible(True)
        else:
            # Якщо прикладів немає, просто робимо їх видимими
            self.widgetexamples.setVisible(True)
        
        # Встановлюємо видимість кнопки для граматики
        self.toGramatic.setVisible((number==4))

        # Отримуємо слова для категорії
        words = get_words_by_category(categNum)
        if number == 1:
            # Якщо номер 1, робимо контейнер більшим
            self.stn.setVisible(True)
            self.fixedContainer.setMinimumHeight(600 if (number==1) else QWIDGETSIZE_MAX)
            words = words[:12]
        else:
            # Якщо не номер 1, приховуємо стн і збільшуємо висоту контейнера
            self.stn.setVisible(False)
            self.fixedContainer.setMinimumHeight(QWIDGETSIZE_MAX)
        
        # Створюємо сітку для слів
        self.createGrid(words)  
    def createWordsPart(self):
        # Створюємо віджет
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Створюємо заголовок
        self.title = QLabel('')
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Створюємо опис
        self.desc = QLabel('')
        self.desc.setObjectName("")
        layout.addWidget(self.desc)
        
        # Створюємо віджет для порад
        self.widgetTrips = QWidget()
        self.widgetTrips.setVisible(False)
        layout.addWidget(self.widgetTrips)
        
        # Створюємо кнопку для переходу до граматики
        self.toGramatic = self.createToGramaticPage()
        self.toGramatic.setVisible(False)
        layout.addWidget(self.toGramatic)

        # Створюємо віджет для прикладів
        self.widgetexamples = QWidget()
        self.widgetexamples.setVisible(False)
        layout.addWidget(self.widgetexamples)

        # Створюємо сітку для карток слів
        self.wordGridLayout = QGridLayout()
        self.wordGridLayout.setSpacing(20)
        self.wordGridLayout.setContentsMargins(0, 20, 0, 20)
        self.wordGridLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Створюємо контейнер для сітки
        gridContainer = QWidget()
        gridContainer.setLayout(self.wordGridLayout)
        gridContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Обгортаємо контейнер у скрол
        scrollable = createScrol(gridContainer)

        # Створюємо зовнішній контейнер з фіксованою висотою
        self.fixedContainer = QWidget()
        fixedLayout = QVBoxLayout(self.fixedContainer)
        fixedLayout.setContentsMargins(0, 0, 0, 0)
        fixedLayout.addWidget(scrollable)

        # Фіксуємо висоту зовнішнього контейнера
        self.fixedContainer.setMinimumHeight(QWIDGETSIZE_MAX)

        # Додаємо на основну розкладку
        layout.addWidget(self.fixedContainer)

        # Створюємо спеціальну частину для цифр
        self.stn = self.createSpecialToNumber()
        self.stn.setVisible(False)
        layout.addWidget(self.stn)

        # Повертаємо прокручуваний віджет
        return createScrol(widget)
