from PyQt5.QtCore import Qt  # Імпортуємо константи Qt (наприклад, для вирівнювання)
# from functools import partial  # (Не використовується — закоментовано)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel  # Імпортуємо необхідні віджети з PyQt5

from controllers.category_controller import get_categoryId  # Імпортуємо функцію для отримання назви категорії за її ID
from controllers.progress_controller import get_user_progress_controller
from views.content.centerPages.common import createScrol  # Імпортуємо функцію для отримання прогресу користувача

class ProgresPage(QWidget):  # Клас для створення сторінки з прогресом користувача
    def __init__(self, parent):  # Конструктор класу
        super().__init__()  # Викликаємо конструктор батьківського класу
        self.createProgresData()  # Ініціалізуємо словник для зберігання прогресу
        self.parent = parent  # Зберігаємо посилання на батьківський об’єкт
        self.setLayout(self.createWidget())  # Встановлюємо макет головного вікна

    def createProgresData(self):  # Метод для створення порожньої структури даних прогресу
        self.progress_data = {"Фонетика": [], "Лексика": [], "Граматика": []}  # Ініціалізація словника з трьома категоріями

    def getProgress(self):  # Метод для отримання та обробки даних прогресу
        self.createProgresData()  # Очищаємо попередні дані
        uId = self.parent.parent.userId  # Отримуємо ID користувача з головного вікна
        data = get_user_progress_controller(uId)  # Отримуємо список результатів користувача
        for p in data:  # Перебираємо кожен запис
            category = get_categoryId(p['category_id'])  # Отримуємо деталі категорії за ID
            if category:  # Перевіряємо, чи знайдена категорія
                proc = (int((p['correct_count'] / p['incorrect_count']) * 100) if p['incorrect_count'] > 0 else 0)  # Розраховуємо відсоток правильних відповідей
                obj = {"theme_name": category['name'], "percentage": proc }  # Створюємо об’єкт для збереження
                if category['page'] == 1:  # Якщо категорія на сторінці "Фонетика"
                    self.progress_data['Фонетика'].append(obj)  # Додаємо до відповідного розділу
                elif category['page'] == 2:  # Якщо категорія на сторінці "Лексика"
                    self.progress_data['Лексика'].append(obj)  # Додаємо до розділу "Лексика"
                else:  # Інакше – вважаємо, що це "Граматика"
                    self.progress_data['Граматика'].append(obj)  # Додаємо до розділу "Граматика"

    def clear_widget(self, widget):  # Метод для повного очищення віджета
        """ Повністю очищає QWidget: видаляє layout і всі дочірні віджети. """
        if widget.layout() is not None:  # Якщо в віджета є layout
            while widget.layout().count():  # Поки в layout є елементи
                item = widget.layout().takeAt(0)  # Видаляємо перший елемент
                child_widget = item.widget()  # Отримуємо віджет
                if child_widget is not None:  # Якщо це віджет
                    child_widget.setParent(None)  # Від'єднуємо його
                else:
                    child_layout = item.layout()  # Інакше перевіряємо чи є layout всередині
                    if child_layout is not None:
                        self.clear_layout(child_layout)  # Рекурсивно очищаємо вкладений layout
            QWidget().setLayout(widget.layout())  # Скидаємо старий layout

    def clear_layout(self, layout):  # Метод для рекурсивного очищення layout
        """ Рекурсивне очищення layout. """
        while layout.count():  # Поки layout містить елементи
            item = layout.takeAt(0)  # Забираємо елемент
            child_widget = item.widget()  # Перевіряємо, чи це віджет
            if child_widget is not None:
                child_widget.setParent(None)  # Видаляємо з layout
            else:
                child_layout = item.layout()  # Якщо це вкладений layout
                if child_layout is not None:
                    self.clear_layout(child_layout)  # Рекурсивно очищаємо

    def updateProgres(self):  # Метод для оновлення відображення прогресу
        self.getProgress()  # Отримуємо нові дані
        self.clear_widget(self.content_container)  # Очищаємо контейнер
        content_layout = QVBoxLayout(self.content_container)  # Створюємо новий вертикальний макет
        content_layout.setAlignment(Qt.AlignTop)  # Вирівнюємо по верхньому краю
        for category in self.progress_data.keys():  # Проходимося по кожній категорії
            group_box = QGroupBox(category)  # Створюємо групу для категорії
            group_layout = QVBoxLayout()  # Макет для групи
            group_layout.setContentsMargins(10, 30, 10, 10)  # Задаємо відступи
            themes = self.progress_data.get(category, [])  # Отримуємо теми з даної категорії
            for theme in themes:  # Проходимося по кожній темі
                label = QLabel(f"{theme['theme_name']}: {theme['percentage']}%")  # Створюємо мітку з назвою теми і відсотком
                label.setObjectName('gbLabel')  # Встановлюємо ім’я об’єкта для стилізації
                group_layout.addWidget(label)  # Додаємо мітку до макета групи
            group_box.setLayout(group_layout)  # Встановлюємо layout для групи
            content_layout.addWidget(group_box)  # Додаємо групу до головного контейнера

    def createWidget(self):  # Метод для створення головного layout сторінки
        Wiget = QWidget() 
        layout = QVBoxLayout(Wiget)  # Створюємо вертикальний layout
        layout.setAlignment(Qt.AlignTop)  # Вирівнюємо по верху
        self.content_container = QWidget()  # Створюємо контейнер для контенту
        self.content_container.setObjectName('content')  # Встановлюємо ім’я об’єкта для стилізації
        self.updateProgres()  # Оновлюємо вміст контейнера
        layout.addWidget(self.content_container)  # Додаємо контейнер до головного макета
        mlayout = QVBoxLayout()
        mlayout.addWidget(createScrol(Wiget))
        return  mlayout  # Повертаємо готовий layout
