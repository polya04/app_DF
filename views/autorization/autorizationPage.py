from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget  # Імпортуємо необхідні класи віджетів з PyQt5

from views.autorization.login import LoginPage  # Імпортуємо сторінку входу
from views.autorization.redistration import RegisterPage  # Імпортуємо сторінку реєстрації

class autorizationPage(QWidget):  # Клас сторінки авторизації, наслідується від QWidget
    def __init__(self, parent):  # Конструктор, приймає головне вікно як батьківський елемент
        super().__init__()  # Викликаємо конструктор базового класу
        self.parent = parent  # Зберігаємо посилання на батьківський об'єкт
        self.stacked_widget = QVBoxLayout()  # Створюємо вертикальний макет
        self.inner_stack = QStackedWidget()  # Створюємо стек сторінок (вхід / реєстрація)
        self.inner_stack.addWidget(LoginPage(self))  # Додаємо сторінку входу
        self.inner_stack.addWidget(RegisterPage(self))  # Додаємо сторінку реєстрації
        self.stacked_widget.addWidget(self.inner_stack)  # Додаємо стек у вертикальний макет
        self.parent.setTitleAndSize('Вхід', (300, 450))  # Встановлюємо початковий заголовок і розмір вікна
        self.setLayout(self.stacked_widget)  # Встановлюємо основний макет для цього віджету
        self.inner_stack.currentChanged.connect(self.update_window_size)  # Змінюємо розмір вікна при зміні сторінки

    def update_window_size(self, index):  # Функція для зміни розміру вікна відповідно до поточної сторінки
        """Змінює розмір вікна залежно від поточної сторінки"""
        if index == 0:  # Якщо активна сторінка входу
            self.setTitleAndSize("Вхід", (300, 450))  # Встановлюємо заголовок і розмір для сторінки входу
        elif index == 1:  # Якщо активна сторінка реєстрації
            self.setTitleAndSize("Реєстрація", (300, 450))  # Встановлюємо заголовок і розмір для сторінки реєстрації

    def set_page_parent(self, numOfPage):  # Змінює сторінку на рівні батьківського компонента
        self.parent.setPage(numOfPage)  # Викликає метод встановлення сторінки у батька

    def set_page(self, numOfPage):  # Змінює поточну сторінку в середині стеку
        self.inner_stack.setCurrentIndex(numOfPage)  # Встановлює індекс активної сторінки

    def get_stacked_widget(self):  # Повертає стек віджетів
        return self.stacked_widget  # Повертає вертикальний макет

    def setTitleAndSize(self, title, size):  # Встановлює заголовок і розмір вікна через батьківський елемент
        self.parent.setTitleAndSize(title, size)  # Викликає відповідний метод батька
