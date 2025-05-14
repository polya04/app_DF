from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget  # Імпорт базових віджетів для побудови інтерфейсу
from views.content.menu import Menu  # Імпорт віджету меню
from views.content.centerPages.TeoryMatherial.TeoryMaterial import TeoryPage  # Імпорт сторінки з теоретичними матеріалами
from views.content.centerPages.TestsMaterial.Tests import TestsPage  # Імпорт сторінки тестування
from views.content.centerPages.ProgresPage import ProgresPage  # Імпорт сторінки прогресу
from views.content.centerPages.SettingsPage import SettingsPage  # Імпорт сторінки налаштувань

# Основний клас вмісту, який включає меню та сторінки
class contentMain(QWidget):
    def __init__(self, parent):  # Конструктор класу, приймає батьківський елемент
        super().__init__()  # Виклик конструктора базового класу
        self.parent = parent  # Збереження посилання на батьківський об’єкт
        
        self.setLayout(self.createWindow())  # Встановлення головного макета, створеного у createWindow

    # Метод створення інтерфейсу (вікна)
    def createWindow(self):
        layout = QVBoxLayout()  # Створення вертикального макета
        layout.setContentsMargins(0, 0, 0, 0)  # Встановлення нульових відступів

        self.menu = Menu(self)  # Створення меню, передача поточного віджету як батьківського
        self.menu.setFixedHeight(int(self.height() * 0.2))  # Встановлення фіксованої висоти меню (20% висоти)
        layout.addWidget(self.menu)  # Додавання меню до макета

        self.inner_stack = QStackedWidget()  # Створення стекового віджету для перемикання сторінок
        # self.inner_stack.setObjectName("cr")  # Коментар: можливо, планувалось використати для стилізації

        self.inner_stack.addWidget(TeoryPage(self))  # Додавання сторінки з теорією
        self.inner_stack.addWidget(TestsPage(self))  # Додавання сторінки з тестами

        self.progrPage = ProgresPage(self)  # Ініціалізація сторінки прогресу як окремого атрибуту
        self.inner_stack.addWidget(self.progrPage)  # Додавання сторінки прогресу до стеку

        self.inner_stack.addWidget(SettingsPage(self))  # Додавання сторінки налаштувань
        layout.addWidget(self.inner_stack)  # Додавання стеку сторінок до основного макета

        return layout  # Повернення готового макета

    # Метод для оновлення розміру вікна в залежності від поточної сторінки (поки не реалізований)
    def update_window_size(self, index):
        """Змінює розмір вікна в залежності від поточної сторінки"""
        if index == 0:
            pass  # Тут можна буде налаштувати поведінку для першої сторінки
        elif index == 1: 
            pass  # І для другої

    # Метод для оновлення інформації про прогрес
    def updateProgress(self):
        # print('update')  # Коментарований рядок для відлагодження
        self.progrPage.updateProgres()  # Виклик методу оновлення прогресу на відповідній сторінці

    # Метод для перемикання сторінки за індексом
    def setPage(self, numOfPage):
        self.inner_stack.setCurrentIndex(numOfPage)  # Встановлення активної сторінки за номером

    # Метод для виходу з акаунта
    def logout(self):
        self.parent.logout()  # Виклик методу виходу з батьківського елементу
