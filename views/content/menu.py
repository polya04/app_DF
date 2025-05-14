# from PyQt5.QtCore import Qt  # Імпорт перерахування Qt для налаштування вирівнювання та інших властивостей
from functools import partial  # Імпорт partial для передачі додаткових аргументів у функцію при з'єднанні сигналів
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout  # Імпорт необхідних віджетів із PyQt5

from views.content.centerPages.common import updateStyle  # Імпорт функції для оновлення стилю кнопок

# Клас меню верхньої навігації
class Menu(QWidget):
    def __init__(self, parent):  # Конструктор класу, приймає батьківський елемент
        super().__init__()  # Виклик конструктора базового класу
        self.parent = parent  # Збереження посилання на батьківський об’єкт
        self.setLayout(self.createWidget())  # Встановлення головного макета, створеного у createWidget
        self.setObjectName("menuLayout")  # Присвоєння імені об’єкту для стилізації через CSS

    # Метод для створення віджетів меню
    def createWidget(self):
        layout = QHBoxLayout()  # Основний горизонтальний макет
        layout.setContentsMargins(30, 20, 30, 0)  # Встановлення внутрішніх відступів
        layout.addStretch(1)  # Додавання гнучкого простору зліва

        menu_widget = QWidget(self)  # Віджет для розміщення кнопок меню
        menu_widget.setObjectName("menuLayout")  # Присвоєння імені для стилізації
        center_layout = QHBoxLayout()  # Горизонтальний макет для кнопок
        center_layout.setContentsMargins(0, 0, 0, 0)  # Встановлення нульових відступів

        # Список кнопок меню
        self.tabs = [QPushButton("Теоретичний матеріал"), QPushButton("Тестування"),
                     QPushButton("Мій прогрес"), QPushButton("Налаштування") ]

        # Додавання кожної кнопки до макета та встановлення стилю і обробника натискання
        for i, tab in enumerate(self.tabs):
            center_layout.addWidget(tab)  # Додавання кнопки до макета
            tab.setProperty("class", "menuBtn")  # Встановлення CSS-класу для стилізації
            tab.clicked.connect(partial(self.handleMenuBtn, i))  # Прив'язка обробника з номером кнопки

        self.tabs[0].setProperty("class", "menuBtn selectedBtn")  # Встановлення стилю для активної кнопки (перша за замовчуванням)
        menu_widget.setLayout(center_layout)  # Застосування макета до контейнера кнопок
        layout.addWidget(menu_widget)  # Додавання контейнера кнопок до головного макета

        layout.addStretch(1)  # Додавання гнучкого простору справа
        self.logout_button = QPushButton("Вихід")  # Кнопка виходу з системи
        self.logout_button.clicked.connect(self.logout)  # Прив’язка методу виходу до кнопки
        layout.addWidget(self.logout_button)  # Додавання кнопки виходу до макета

        mainWiget = QWidget(self)  # Головний контейнер меню
        mainWiget.setLayout(layout)  # Встановлення головного макета
        mainWiget.setObjectName("menuLayout")  # Ім'я для CSS-оформлення

        mLay = QVBoxLayout()  # Вертикальний макет як обгортка для всього меню
        mLay.setContentsMargins(0, 0, 0, 0)  # Встановлення нульових відступів
        mLay.addWidget(mainWiget)  # Додавання головного контейнера до вертикального макета
        return mLay  # Повернення готового макета

    # Метод для обробки натискання на кнопки меню
    def handleMenuBtn(self, number):
        for i, tab in enumerate(self.tabs):  # Перебір усіх кнопок
            if i == number:  # Якщо це обрана кнопка
                tab.setProperty("class", "menuBtn selectedBtn")  # Встановити її як активну
            else:
                tab.setProperty("class", "menuBtn")  # Інші — як неактивні
            updateStyle(tab)  # Оновити стиль кожної кнопки
        self.parent.setPage(number)  # Встановити відповідну сторінку

    # Метод для виходу з акаунта
    def logout(self):
        self.parent.logout()  # Виклик методу logout з батьківського об’єкта
