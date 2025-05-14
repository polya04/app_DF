from PyQt5.QtCore import Qt  # Імпортуємо Qt для вирівнювання та інших флагів
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QHBoxLayout  # Імпортуємо необхідні віджети
from controllers.auth_controller import login_user_controller  # Імпортуємо контролер для входу користувача

class LoginPage(QWidget):  # Клас сторінки входу, наслідується від QWidget
    def __init__(self, parent):  # Конструктор класу, приймає батьківський віджет
        super().__init__()  # Викликаємо конструктор базового класу
        self.parent = parent  # Зберігаємо батьківський елемент
        self.setLayout(self.createForm())  # Встановлюємо головний макет форми

    def createForm(self):  # Метод створення форми входу
        layout = QVBoxLayout()  # Створюємо вертикальний макет

        self.title  =  QLabel("Вхід", self)  # Створюємо заголовок "Вхід"
        self.title.setObjectName("title")  # Встановлюємо об'єктне ім'я для стилізації
        self.title.setAlignment(Qt.AlignCenter)  # Вирівнюємо по центру
        layout.addWidget(self.title)  # Додаємо заголовок до макету

        self.username_input = QLineEdit(self)  # Поле введення логіна
        self.username_input.setPlaceholderText("Логін")  # Підказка всередині поля
        layout.addWidget(self.username_input)  # Додаємо до макету

        self.password_input = QLineEdit(self)  # Поле введення паролю
        self.password_input.setPlaceholderText("Пароль")  # Підказка
        self.password_input.setEchoMode(QLineEdit.Password)  # Сховати символи при введенні
        layout.addWidget(self.password_input)  # Додаємо до макету

        self.login_btn = QPushButton("Увійти", self)  # Кнопка входу
        self.login_btn.clicked.connect(self.try_login)  # Підключаємо метод входу до події натискання
        layout.addWidget(self.login_btn)  # Додаємо до макету

        horizontal_layout = QHBoxLayout()  # Горизонтальний макет для посилання на реєстрацію
        horizontal_layout.setAlignment(Qt.AlignCenter)  # Вирівнюємо по центру

        self.label1 = QLabel("Немає акаунту? ", self)  # Текст перед кнопкою реєстрації
        self.register_link = QPushButton('Зареєструйтесь', self)  # Кнопка переходу до реєстрації
        self.register_link.setObjectName("registerLink")  # Встановлюємо об'єктне ім’я
        self.register_link.clicked.connect(self.go_to_register)  # Переходимо до сторінки реєстрації при натисканні

        self.label2 = QLabel("!", self)  # Декоративний елемент після кнопки

        horizontal_layout.addWidget(self.label1)  # Додаємо елементи до горизонтального макету
        horizontal_layout.addWidget(self.register_link)
        horizontal_layout.addWidget(self.label2)
        layout.addLayout(horizontal_layout)  # Додаємо горизонтальний макет до основного

        return layout  # Повертаємо зібраний макет

    def try_login(self):  # Метод для спроби входу
        username = self.username_input.text()  # Отримуємо логін
        password = self.password_input.text()  # Отримуємо пароль
        user = login_user_controller(username, password)  # Перевіряємо логін/пароль через контролер
        if user:  # Якщо користувача знайдено
            self.parent.parent.setUser(user['id'], user['theme'])  # Зберігаємо ID та тему користувача у головному вікні
            self.parent.set_page_parent(1)  # Переходимо до головної сторінки додатку
        else:  # Якщо логін або пароль неправильні
            QMessageBox.warning(self, "Помилка", "Неправильні дані")  # Показуємо повідомлення про помилку

    def go_to_register(self):  # Метод переходу до сторінки реєстрації
        self.parent.set_page(1)  # Встановлюємо індекс сторінки реєстрації у внутрішньому стеку
