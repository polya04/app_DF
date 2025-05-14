from functools import partial  # Імпортуємо partial з бібліотеки functools для створення часткових функцій
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QHBoxLayout , QStackedWidget)  # Імпортуємо необхідні віджети для роботи з PyQt5
from controllers.category_controller import get_category_by_page  # Імпортуємо функцію для отримання категорій
from controllers.spectest_controller import get_spec_tests_by_category  # Імпортуємо функцію для отримання специфічних тестів за категорією
from controllers.tests_controller import get_tests_by_category  # Імпортуємо функцію для отримання тестів за категорією
from views.content.centerPages.TestsMaterial.parentTest import parentTest  # Імпортуємо базовий клас для тестів
from views.content.centerPages.common import updateStyle  # Імпортуємо функцію для оновлення стилю

class PhoneticTests(parentTest):  # Клас для фонетичних тестів, наслідується від класу parentTest
    def __init__(self, parent):
        super().__init__(parent)  # Викликаємо конструктор батьківського класу
        self.setLayout(self.createWidget())  # Встановлюємо макет для віджету

    def createWidget(self):  # Функція для створення основного віджету
        layout = QHBoxLayout()  # Створюємо горизонтальний макет
        asside_widget = self.createAsside()  # Створюємо бічну панель
        layout.addWidget(asside_widget, stretch=2)  # Додаємо бічну панель до макету з коефіцієнтом розтягування 2
        self.content_widget = QStackedWidget()  # Створюємо віджет для перемикання між різними сторінками
        self.content_widget.addWidget(self.createContent())  # Додаємо основний контент
        # self.content_widget.setObjectName("cr")  # Можливе задання імені для стилізації (закоментовано)
        layout.addWidget(self.content_widget, stretch=8)  # Додаємо віджет контенту з коефіцієнтом розтягування 8
        return layout  # Повертаємо макет

    def createAsside(self):  # Функція для створення бічної панелі з меню
        MenuWiget = QWidget()  # Створюємо віджет для бічної панелі
        layout = QVBoxLayout()  # Створюємо вертикальний макет для віджету

        categories = get_category_by_page(1)[2:]  # Отримуємо категорії для меню (ігноруємо перші 2)
        TopLayout = QVBoxLayout()  # Створюємо вертикальний макет для кнопок
        self.tabs = []  # Ініціалізуємо список для кнопок
        for idx, c in enumerate(categories):  # Проходимо по всіх категоріях
            tab = QPushButton(c['name'])  # Створюємо кнопку для кожної категорії
            TopLayout.addWidget(tab)  # Додаємо кнопку до макету
            tab.clicked.connect(partial(self.getTestByCategory, idx, c['id'], c['name']))  # Прив'язуємо подію натискання кнопки
            self.tabs.append(tab)  # Додаємо кнопку до списку вкладок
        layout.addLayout(TopLayout, 3)  # Додаємо макет кнопок до основного макету з коефіцієнтом розтягування 3
        layout.addStretch(2)  # Додаємо відступ для вирівнювання елементів

        self.btnBack = QPushButton("Назад")  # Створюємо кнопку "Назад"
        self.btnBack.clicked.connect(self.backBtnHandle)  # Прив'язуємо подію натискання кнопки "Назад"
        
        layout.addWidget(self.btnBack, 1)  # Додаємо кнопку "Назад" до макету з коефіцієнтом розтягування 1
        MenuWiget.setLayout(layout)  # Встановлюємо макет до віджету
        return MenuWiget  # Повертаємо віджет бічної панелі
    
    def getTestByCategory(self, number, categNum, cutName):  # Функція для отримання тестів за категорією
        for i, b in enumerate(self.tabs):  # Проходимо по вкладках
            b.setObjectName("selected" if i == number else "")  # Встановлюємо стиль для вибраної вкладки
            updateStyle(b)  # Оновлюємо стиль вкладки
        data = get_tests_by_category(categNum)  # Отримуємо тести для цієї категорії
        if categNum == 14:  # Якщо категорія має номер 14, отримуємо специфічні тести
            data = get_spec_tests_by_category(categNum)  # Отримуємо специфічні тести для категорії
        self.category_id = categNum  # Зберігаємо ID категорії
        self.updateTests(data)  # Оновлюємо список тестів
        # self.parent.parent.parent.setTheme()  # Можливе оновлення теми (закоментовано)
        self.title.setText(cutName)  # Встановлюємо назву категорії на титульний текст
