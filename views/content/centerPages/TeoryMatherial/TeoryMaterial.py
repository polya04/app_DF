# Імпортуємо необхідні модулі з PyQt5
from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget

# Імпортуємо сторінки з теоретичними матеріалами
from views.content.centerPages.TeoryMatherial.GramaticPage import GramaticPage
from views.content.centerPages.TeoryMatherial.LexisPageFlex import LexisPageFlex
# з коментарем видалено іншу версію сторінки
# from views.content.centerPages.TeoryMatherial.LexisPage import LexisPage
from views.content.centerPages.TeoryMatherial.PhoneticsPage import PhoneticsPage

# Основна сторінка теоретичних матеріалів
class TeoryPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Зберігаємо батьківський віджет
        self.setLayout(self.createWidget())  # Встановлюємо макет віджету

    # Створюємо віджет, що містить основні компоненти
    def createWidget(self):
        layout = QVBoxLayout()  # Вертикальний лейаут для основного вікна
        self.inner_stack = QStackedWidget()  # Стек для різних сторінок
        # Додаємо сторінки до стека
        self.inner_stack.addWidget(self.createMenuWidget())
        self.inner_stack.addWidget(PhoneticsPage(self))  # Додаємо сторінку з фонетикою
        self.inner_stack.addWidget(LexisPageFlex(self))  # Додаємо сторінку з лексикою
        self.inner_stack.addWidget(GramaticPage(self))  # Додаємо сторінку з граматикою

        layout.addWidget(self.inner_stack)  # Додаємо стек до основного макету
        return layout

    # Створюємо меню для навігації між сторінками
    def createMenuWidget(self):
        MenuWiget = QWidget()  # Створюємо віджет для меню
        layout = QVBoxLayout()  # Вертикальний лейаут для меню
        layout.addStretch(1)  # Додаємо відступ зверху

        # Створюємо кнопки для кожної теми
        self.tabs = [QPushButton("Фонетика"), QPushButton("Лексика"),
                     QPushButton("Граматика")]
        for i, tab in enumerate(self.tabs):
            tab.setFixedWidth(int(self.width() * 0.6))  # Встановлюємо фіксовану ширину кнопок
            tab.setProperty("class", "teotyBtn")  # Додаємо CSS клас для стилізації
            h_layout = QHBoxLayout()  # Горизонтальний лейаут для кнопок
            h_layout.addStretch(3)  # Додаємо відступи для центрування кнопки
            h_layout.addWidget(tab, 4)  # Додаємо кнопку до лейаута
            h_layout.addStretch(3)  # Додаємо відступ з іншого боку
            layout.addLayout(h_layout)  # Додаємо горизонтальний лейаут до вертикального
            tab.clicked.connect(partial(self.setWigetInStack, i+1))  # Прив'язуємо подію до кнопки
        layout.addStretch(1)  # Додаємо відступ знизу
        MenuWiget.setLayout(layout)  # Встановлюємо лейаут для меню
        return MenuWiget

    # Функція для перемикання між сторінками
    def setWigetInStack(self, number):
        self.inner_stack.setCurrentIndex(number)  # Встановлюємо поточну сторінку в стеку
