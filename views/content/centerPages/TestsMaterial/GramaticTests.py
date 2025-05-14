from functools import partial  # Імпортуємо partial з functools для створення часткових функцій
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QHBoxLayout , QStackedWidget)  # Імпортуємо необхідні віджети для побудови інтерфейсу
from controllers.category_controller import get_category_by_page  # Імпортуємо функцію для отримання категорій
from controllers.tests_controller import get_tests_by_category  # Імпортуємо функцію для отримання тестів за категорією
from views.content.centerPages.TestsMaterial.parentTest import parentTest  # Імпортуємо базовий клас для тестів
from views.content.centerPages.common import updateStyle  # Імпортуємо функцію для оновлення стилю кнопок


class GramaticTests(parentTest):  # Клас для тестів з граматики, який наслідується від parentTest
    def __init__(self, parent):
        super().__init__(parent)  # Викликаємо конструктор батьківського класу
        self.setLayout(self.createWidget())  # Встановлюємо віджет для інтерфейсу
    
    def createWidget(self):  # Створюємо головний віджет для макету
        layout = QHBoxLayout()  # Використовуємо горизонтальний макет для розташування елементів
        asside_widget = self.createAsside()  # Створюємо бічну панель
        layout.addWidget(asside_widget, stretch=2)  # Додаємо бічну панель до макету з коефіцієнтом розтягування 2
        self.content_widget = QStackedWidget()  # Створюємо віджет для переключення між сторінками
        self.content_widget.addWidget(self.createContent())  # Додаємо основний контент до віджета
        # self.content_widget.setObjectName("cr")  # Можливе задання імені для стилізації (закоментовано)
        layout.addWidget(self.content_widget, stretch=8)  # Додаємо віджет контенту до макету з коефіцієнтом розтягування 8
        return layout  # Повертаємо макет

    def createAsside(self):  # Створюємо бічну панель з меню
        MenuWiget = QWidget()  # Створюємо віджет для бічної панелі
        layout = QVBoxLayout()  # Використовуємо вертикальний макет для розташування елементів

        categories = get_category_by_page(3)  # Отримуємо категорії для меню
        TopLayout = QVBoxLayout()  # Створюємо вертикальний макет для розміщення кнопок
        self.tabs = []  # Ініціалізуємо список для кнопок
        for idx, c in enumerate(categories):  # Проходимо по кожній категорії
            tab = QPushButton(c['name'])  # Створюємо кнопку для кожної категорії
            TopLayout.addWidget(tab)  # Додаємо кнопку до макету
            tab.clicked.connect(partial(self.getTestByCategory, idx, c['id'], c['name']))  # Прив'язуємо подію натискання кнопки
            self.tabs.append(tab)  # Додаємо кнопку до списку вкладок
        layout.addLayout(TopLayout, 3)  # Додаємо макет з кнопками до основного макету з коефіцієнтом розтягування 3
        layout.addStretch(2)  # Додаємо відступи для вирівнювання елементів

        self.btnBack = QPushButton("Назад")  # Створюємо кнопку "Назад"
        self.btnBack.clicked.connect(self.backBtnHandle)  # Прив'язуємо подію натискання кнопки "Назад"
        
        layout.addWidget(self.btnBack, 1)  # Додаємо кнопку "Назад" до макету з коефіцієнтом розтягування 1
        MenuWiget.setLayout(layout)  # Встановлюємо макет до віджету
        return MenuWiget  # Повертаємо віджет бічної панелі

    def getTestByCategory(self, number, categNum, cutName):  # Функція для отримання тестів за категорією
        for i, b in enumerate(self.tabs):  # Проходимо по вкладках
            b.setObjectName("selected" if i == number else "")  # Встановлюємо стиль для вибраної вкладки
            updateStyle(b)  # Оновлюємо стиль вкладки
        data = get_tests_by_category(categNum)  # Отримуємо тести для даної категорії
        self.updateTests(data)  # Оновлюємо список тестів
        self.category_id = categNum  # Зберігаємо ID категорії
        # self.parent.parent.parent.setTheme()  # Можливе оновлення теми (закоментовано)
        self.title.setText(cutName)  # Встановлюємо назву категорії на титульний текст
