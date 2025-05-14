from PyQt5.QtCore import Qt  # Імпорт Qt констант (наприклад, вирівнювання)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout  # Імпорт віджетів з PyQt5
from QSwitchControl import SwitchControl  # Імпорт кастомного перемикача (світла/темна тема)

# Клас сторінки налаштувань
class SettingsPage(QWidget):
    def __init__(self, parent):
        super().__init__()  # Ініціалізація батьківського класу QWidget
        self.parent = parent  # Збереження посилання на батьківський елемент
        self.setLayout(self.createWidget())  # Встановлення головного макета

    # Метод створення інтерфейсу сторінки
    def createWidget(self):
        layout = QVBoxLayout()  # Головний вертикальний макет

        content_container = QWidget()  # Контейнер для контенту сторінки
        content_container.setObjectName('content')  # Ім’я для стилізації (через CSS/Qt Styles)
        content_layout = QVBoxLayout(content_container)  # Макет для контейнера
        content_layout.setAlignment(Qt.AlignTop)  # Вирівнювання по верхньому краю

        settings_box = QGroupBox("Тема")  # Групбокс із заголовком "Тема"
        settings_layout = QVBoxLayout()  # Внутрішній макет для групбоксу
        settings_layout.setContentsMargins(10, 30, 10, 10)  # Внутрішні відступи

        option1_layout = QHBoxLayout()  # Горизонтальний макет для перемикача теми
        option1_layout.setAlignment(Qt.AlignLeft)  # Вирівнювання вліво

        self.option1 = SwitchControl(self)  # Створення перемикача теми (кастомний клас)
        self.option1.setText("Світла тема")  # Початковий текст (можливо, не видно — залежить від реалізації)
        self.option1.stateChanged.connect(self.onOptionChanged)  # Зв’язування зміни стану з функцією
        option1_layout.addWidget(self.option1)  # Додавання перемикача

        self.labelTeme = QLabel("Світла тема", self)  # Підпис до перемикача
        option1_layout.addWidget(self.labelTeme)  # Додавання підпису до макета

        settings_layout.addLayout(option1_layout)  # Додавання макета з перемикачем до групбоксу
        settings_box.setLayout(settings_layout)  # Встановлення макета для групбоксу

        content_layout.addWidget(settings_box)  # Додавання групбоксу до контенту
        content_container.setLayout(content_layout)  # Встановлення макета для контейнера

        layout.addWidget(content_container)  # Додавання контейнера до головного макета
        return layout  # Повернення готового макета

    # Метод, що викликається при зміні стану перемикача
    def onOptionChanged(self, state):
        if state:  # Якщо перемикач увімкнений — темна тема
            self.labelTeme.setText('Темна тема')  # Оновлюємо текст
            self.parent.parent.setColorTheme(1)  # Викликаємо метод для зміни теми на темну
        else:  # Інакше — світла тема
            self.labelTeme.setText('Світла тема')
            self.parent.parent.setColorTheme(0)  # Викликаємо метод для зміни теми на світлу
