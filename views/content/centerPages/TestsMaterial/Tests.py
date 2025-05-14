# Імпортуємо необхідні модулі
from functools import partial  # для частичного виконання функції
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QHBoxLayout  # імпортуємо віджети для побудови інтерфейсу

# Імпортуємо тести з різних розділів
from views.content.centerPages.TestsMaterial.GramaticTests import GramaticTests  # тести з граматики
from views.content.centerPages.TestsMaterial.LexisTests import LexisTests  # тести з лексики
from views.content.centerPages.TestsMaterial.PhoneticTests import PhoneticTests  # тести з фонетики

# Клас для створення сторінки з тестами
class TestsPage(QWidget):
    def __init__(self, parent):
        super().__init__()  # викликаємо конструктор батьківського класу
        self.parent = parent  # зберігаємо батьківський елемент
        self.setLayout(self.createWidget())  # встановлюємо макет сторінки

    # Метод для створення макету сторінки
    def createWidget(self):
        layout = QVBoxLayout()  # створюємо вертикальний макет
        self.inner_stack = QStackedWidget()  # створюємо віджет для стекових сторінок
        self.inner_stack.addWidget(self.createMenuWidget())  # додаємо меню до стека
        self.inner_stack.addWidget(PhoneticTests(self))  # додаємо сторінку з тестами з фонетики
        self.inner_stack.addWidget(LexisTests(self))  # додаємо сторінку з тестами з лексики
        self.inner_stack.addWidget(GramaticTests(self))  # додаємо сторінку з тестами з граматики
        layout.addWidget(self.inner_stack)  # додаємо стек до макету
        return layout  # повертаємо макет

    # Метод для створення меню
    def createMenuWidget(self):
        MenuWiget = QWidget()  # створюємо віджет для меню
        layout = QVBoxLayout()  # створюємо вертикальний макет для меню
        layout.addStretch(1)  # додаємо порожній простір зверху
        self.tabs = [QPushButton("Тести Фонетика"), QPushButton("Тести Лексика"), QPushButton("Тести Граматика")]  # кнопки для кожного розділу
        for i, tab in enumerate(self.tabs):  # проходимо по кожній кнопці
            tab.setFixedWidth(int(self.width() * 0.6))  # встановлюємо фіксовану ширину кнопки
            tab.setProperty("class", "teotyBtn")  # додаємо CSS клас для кнопки
            h_layout = QHBoxLayout()  # створюємо горизонтальний макет
            h_layout.addStretch(3)  # додаємо порожній простір зліва
            h_layout.addWidget(tab, 4)  # додаємо кнопку до макету
            h_layout.addStretch(3)  # додаємо порожній простір справа
            layout.addLayout(h_layout)  # додаємо горизонтальний макет до вертикального
            tab.clicked.connect(partial(self.setWigetInStack, i+1))  # підключаємо подію для кожної кнопки
        layout.addStretch(1)  # додаємо порожній простір знизу
        MenuWiget.setLayout(layout)  # встановлюємо макет для меню
        return MenuWiget  # повертаємо меню

    # Метод для зміни відображення сторінок в стеку
    def setWigetInStack(self, number):
        self.inner_stack.setCurrentIndex(number)  # встановлюємо поточну сторінку за індексом

    # Закоментовані методи для тестів, які не використовуються
    # def PhoneticsPageTests(self):
    #     pass

    # def LexisPageTests(self):
    #     pass
