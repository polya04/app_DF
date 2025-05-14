from PyQt5.QtCore import Qt  # Імпортуємо модуль для вирівнювання та інших атрибутів
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QHBoxLayout
from controllers.auth_controller import register_user_controller  # Імпортуємо функцію реєстрації

class RegisterPage(QWidget):  # Клас сторінки реєстрації
    def __init__(self, parent):
        super().__init__()  # Ініціалізуємо батьківський клас QWidget
        self.parent = parent  # Зберігаємо посилання на батьківський елемент
        self.setLayout(self.createForm())  # Встановлюємо головний макет

    def createForm(self):  # Метод створення форми реєстрації
        layout = QVBoxLayout()  # Вертикальний макет

        self.title  =  QLabel("Реєстрація", self)  # Заголовок
        self.title.setObjectName("title")  # Ім’я об’єкта для стилізації
        self.title.setAlignment(Qt.AlignCenter)  # Центрування заголовка
        layout.addWidget(self.title)  # Додаємо до макету

        self.username_input = QLineEdit(self)  # Поле введення логіна
        self.username_input.setPlaceholderText("Логін")  # Підказка
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)  # Поле введення пароля
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)  # Приховування символів
        layout.addWidget(self.password_input)

        self.repeat_password_input = QLineEdit(self)  # Поле повторного введення пароля
        self.repeat_password_input.setPlaceholderText("Повторіть пароль")
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.repeat_password_input)

        self.login_btn = QPushButton("Реєстрація", self)  # Кнопка для підтвердження реєстрації
        self.login_btn.clicked.connect(self.try_register)  # Обробник натискання
        layout.addWidget(self.login_btn)

        horizontal_layout = QHBoxLayout()  # Горизонтальний макет для навігації
        horizontal_layout.setAlignment(Qt.AlignCenter)

        self.label1 = QLabel("Є акаунт? ", self)  # Текст перед посиланням
        self.register_link = QPushButton('Увійдіть', self)  # Кнопка переходу на сторінку входу
        self.register_link.setObjectName("registerLink")  # Ім’я об’єкта для стилів
        self.register_link.clicked.connect(self.go_to_login)  # Перехід до сторінки входу

        self.label2 = QLabel("!", self)  # Декоративний елемент

        # Додаємо елементи до горизонтального макету
        horizontal_layout.addWidget(self.label1)
        horizontal_layout.addWidget(self.register_link)
        horizontal_layout.addWidget(self.label2)

        layout.addLayout(horizontal_layout)  # Додаємо горизонтальний макет до головного

        return layout  # Повертаємо макет

    def try_register(self):  # Метод спроби реєстрації
        username = self.username_input.text().strip()  # Отримуємо логін і обрізаємо пробіли
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()

        # Перевірка на порожні поля
        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Логін та пароль не повинні бути порожніми")
            return

        # Перевірка збігу паролів
        if password != repeat_password:
            QMessageBox.warning(self, "Помилка", "Паролі не збігаються")
            return

        user = register_user_controller(username, password)  # Виклик функції реєстрації

        if user:  # Якщо реєстрація успішна
            QMessageBox.information(self, "Успішно", "Реєстрація пройшла успішно")
            self.parent.parent.setUser(user['id'], user['theme'])  # Зберігаємо ID і тему
            self.parent.set_page_parent(1)  # Переходимо на головну сторінку
        else:  # Якщо логін уже існує
            QMessageBox.warning(self, "Помилка", "Користувач із таким ім'ям вже існує")

    def go_to_login(self):  # Перехід на сторінку входу
        self.parent.set_page(0)
