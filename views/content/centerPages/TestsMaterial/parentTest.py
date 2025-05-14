# from functools import partial  # (не використовується) — модуль для часткового застосування функцій
import os
import re  # Імпортуємо модуль для роботи з регулярними виразами

# Імпортуємо класи з PyQt5 для роботи з GUI
from PyQt5.QtCore import Qt, QSize  # Qt — для керування вирівнюванням та розмірами
from PyQt5.QtCore import Qt  # (повторний імпорт Qt, можна видалити)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QHBoxLayout ,QGroupBox, QRadioButton,
                             QLineEdit, QMessageBox, QLabel, QComboBox)  # Віджети для побудови інтерфейсу

# from controllers.category_controller import get_category_by_page  # (закоментовано) — імпорт функції отримання категорій
# from controllers.tests_controller import get_tests_by_category  # (закоментовано) — імпорт функції отримання тестів
from controllers.progress_controller import save_progress_controller  # Імпорт функції збереження прогресу
from views.content.centerPages.common import createScrol, play_or_speak  # Імпорт скролу та функції для відтворення/озвучення
from config import imgPaht  # Імпорт шляху до іконок
from PyQt5.QtGui import QIcon  # Імпорт класу для використання іконок у кнопках

# Функція очищення тексту питання від зайвих символів
def clean_question(text):
        # Видаляємо невидимі символи: em-space, soft hyphen тощо
        cleaned = text.replace('\u2003', ' ')   # Заміна широкого пробілу на звичайний
        cleaned = cleaned.replace('\xad', '')   # Видаляємо м’яке перенесення (soft hyphen)
        cleaned = cleaned.replace('\n', ' ')    # Заміна переносу рядка на пробіл
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Заміна кількох пробілів одним
        return cleaned.strip()  # Обрізаємо пробіли з початку та кінця

# Клас, який представляє батьківський віджет для тестів
class parentTest(QWidget):
    def __init__(self, parent):  # Конструктор класу
        super().__init__()  # Викликаємо конструктор базового класу QWidget
        self.parent = parent  # Зберігаємо посилання на батьківський віджет
        self.category_id = -1  # Початкове значення категорії (-1 — не вибрана)
        self.test_groups = []  # Список для збереження груп питань
        # self.setLayout(self.createWidget())  # (закоментовано) — можливе встановлення основного layout

    # Обробник кнопки «Назад» — повертає на попередній екран
    def backBtnHandle(self):
        self.parent.setWigetInStack(0)  # Встановлює перший віджет у стеку (головний екран)

    # Метод очищення віджета: видаляє layout і всі дочірні елементи
    def clear_widget(self, widget):
        """ Повністю очищає QWidget: видаляє layout і всі дочірні віджети. """
        if widget.layout() is not None:  # Перевіряємо, чи є layout
            while widget.layout().count():  # Поки у layout є елементи
                item = widget.layout().takeAt(0)  # Виймаємо елемент
                child_widget = item.widget()  # Перевіряємо, чи це віджет
                if child_widget is not None:
                    child_widget.setParent(None)  # Від'єднуємо від батьківського
                else:
                    child_layout = item.layout()  # Якщо це вкладений layout
                    if child_layout is not None:
                        self.clear_layout(child_layout)  # Рекурсивно очищуємо вкладений layout
            QWidget().setLayout(widget.layout())  # Скидаємо старий layout

    # Метод рекурсивного очищення layout
    def clear_layout(self, layout):
        """ Рекурсивне очищення layout. """
        while layout.count():  # Поки є елементи в layout
            item = layout.takeAt(0)  # Виймаємо елемент
            child_widget = item.widget()  # Якщо елемент — віджет
            if child_widget is not None:
                child_widget.setParent(None)  # Від'єднуємо від батьківського layout
            else:
                child_layout = item.layout()  # Якщо елемент — вкладений layout
                if child_layout is not None:
                    self.clear_layout(child_layout)  # Рекурсивно очищаємо

    def create_radio_test(self, layout, test):
        text = clean_question(test['question'])  # Очищаємо текст питання від зайвих символів
        group_box = QGroupBox(text)  # Створюємо груповий блок із текстом питання як заголовком
        group_layout = QVBoxLayout(group_box)  # Встановлюємо вертикальний layout всередині групи

        answer_layout = QHBoxLayout()  # Горизонтальний layout для розміщення колонок відповідей
        first_column = QVBoxLayout()  # Перша вертикальна колонка для відповідей
        second_column = QVBoxLayout()  # Друга вертикальна колонка для відповідей

        answers = test['answers']  # Отримуємо список відповідей з тесту
        mid = len(answers) // 2 + len(answers) % 2  # Знаходимо точку розподілу відповідей на дві колонки
        radios = []  # Список для збереження створених радіокнопок

        for i in range(mid):  # Додаємо першу половину відповідей до першої колонки
            rb = QRadioButton(answers[i])  # Створюємо радіокнопку з текстом відповіді
            radios.append(rb)  # Додаємо кнопку до списку
            first_column.addWidget(rb)  # Додаємо кнопку до layout першої колонки

        for i in range(mid, len(answers)):  # Додаємо другу половину відповідей до другої колонки
            rb = QRadioButton(answers[i])
            radios.append(rb)
            second_column.addWidget(rb)

        answer_layout.addLayout(first_column)  # Додаємо першу колонку до горизонтального layout
        answer_layout.addLayout(second_column)  # Додаємо другу колонку

        group_layout.addLayout(answer_layout)  # Додаємо відповіді до основного layout групи

        self.test_groups.append({  # Зберігаємо інформацію про створений тест у список
            'type': 0,  # Тип 0 — радіокнопки
            'question': test['question'],  # Оригінальний текст питання
            'radios': radios,  # Список радіокнопок
            'correct_answer': test['correct_answer']  # Правильна відповідь
        })

        layout.addWidget(group_box)  # Додаємо групу з питанням до основного layout
    def create_input_test(self, layout, test):
        group_box = QGroupBox()  # Створюємо порожню групу для текстового поля
        group_layout = QVBoxLayout(group_box)  # Встановлюємо вертикальний layout для групи

        text_parts = test['question'].split('___')  # Ділимо питання на частини по заповнюваному полю
        row_layout = QHBoxLayout()  # Горизонтальний layout для розміщення тексту та поля вводу

        if len(text_parts) == 2:  # Якщо є дві частини тексту (до і після поля вводу)
            row_layout.addWidget(QLabel(text_parts[0]))  # Додаємо першу частину тексту
            input_field = QLineEdit()  # Створюємо поле для вводу
            input_field.setMaximumWidth(150)  # Обмежуємо ширину
            row_layout.addWidget(input_field)  # Додаємо поле вводу до layout
            row_layout.addWidget(QLabel(text_parts[1]))  # Додаємо другу частину тексту
        else:
            # Запасний варіант, якщо розділювача ___ немає
            input_field = QLineEdit()
            row_layout.addWidget(QLabel(test['question']))  # Весь текст питання
            row_layout.addWidget(input_field)

        group_layout.addLayout(row_layout)  # Додаємо рядок до групового layout

        self.test_groups.append({  # Зберігаємо інформацію про створений тест
            'type': 1,  # Тип 1 — текстове поле
            'input': input_field,  # Поле для вводу
            'correct_answer': test['answers'][test['correct_answer']].lower().strip()  # Правильна відповідь (очищена)
        })

        layout.addWidget(group_box)  # Додаємо групу до основного layout
    def create_select_test(self, layout, test):
        group_box = QGroupBox()  # Створюємо нову групу для випадаючого списку
        group_layout = QVBoxLayout(group_box)  # Вертикальний layout групи
        group_layout.setAlignment(Qt.AlignLeft)  # Вирівнюємо по лівому краю
        text_parts = test['question'].split('___')  # Ділимо текст питання на частини
        row_layout = QHBoxLayout()  # Горизонтальний layout
        row_layout.setAlignment(Qt.AlignLeft)

        combo = QComboBox()  # Створюємо випадаючий список
        combo.setObjectName("customComboBox")  # Задаємо об'єктне ім’я
        combo.setMaximumWidth(100)  # Максимальна ширина списку
        combo.setMinimumWidth(100)
        combo.addItem("")  # Додаємо порожній пункт
        combo.addItems(test['answers'])  # Додаємо варіанти відповідей

        if len(text_parts) == 2:  # Якщо є дві частини тексту
            row_layout.addWidget(QLabel(text_parts[0]))
            row_layout.addWidget(combo)
            row_layout.addWidget(QLabel(text_parts[1]))
        else:
            row_layout.addWidget(QLabel(test['question']))
            row_layout.addWidget(combo)

        group_layout.addLayout(row_layout)  # Додаємо рядок у групу
        self.test_groups.append({
            'type': 2,  # Тип 2 — випадаючий список
            'select': combo,  # Об’єкт списку
            'correct_answer': test['correct_answer']  # Індекс правильної відповіді
        })

        layout.addWidget(group_box)
    def create_audio_test(self, layout, test):
        group_box = QGroupBox()  # Створюємо груповий блок
        group_layout = QVBoxLayout(group_box)  # Вертикальний layout групи

        # Горизонтальний блок: текст питання + кнопка відтворення
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft)  # Вирівнювання по лівому краю

        # Текст питання
        question_label = QLabel(clean_question(test['question']))  # Створюємо мітку з очищеним текстом питання
        header_layout.addWidget(question_label)  # Додаємо мітку до layout

        # Кнопка прослуховування
        soundBtn = QPushButton()  # Створюємо кнопку
        soundBtn.setIcon(QIcon(os.path.join(imgPaht, 'speaker.png')))  # Встановлюємо іконку динаміка
        soundBtn.setIconSize(QSize(20, 20))  # Розмір іконки
        soundBtn.setFixedSize(26, 26)  # Фіксований розмір кнопки
        soundBtn.setObjectName("soundButton")  # Ім’я об’єкта
        soundBtn.clicked.connect(lambda: play_or_speak("audio", test['audio_data']))  # Прив’язуємо дію відтворення
        header_layout.addWidget(soundBtn)  # Додаємо кнопку до layout

        group_layout.addLayout(header_layout)  # Додаємо заголовок до основного layout групи

        # Радіокнопки: Так / Ні
        answer_layout = QHBoxLayout()  # Горизонтальний layout для кнопок
        radios = []  # Список для радіокнопок

        true_button = QRadioButton("Так")  # Кнопка "Так"
        false_button = QRadioButton("Ні")  # Кнопка "Ні"
        radios.extend([true_button, false_button])  # Додаємо кнопки до списку

        answer_layout.addWidget(true_button)
        answer_layout.addWidget(false_button)
        group_layout.addLayout(answer_layout)

        self.test_groups.append({  # Додаємо тест у список
            'type': 3,  # Тип 3 — аудіо-тест
            'question': test['question'],
            'radios': radios,
            'correct_answer': test['correct_answer']
        })

        layout.addWidget(group_box)  # Додаємо все до головного layout

    def updateTests(self, data):
        self.clear_widget(self.testwiget)  # Очищаємо віджет, щоб додати нові тести
        testLayout = QVBoxLayout(self.testwiget)  # Створюємо вертикальний layout для тестів
        self.test_groups = []  # Очищаємо список тестів
        for test in data:  # Проходимося по всіх тестах, які надійшли у вигляді списку
            test_type = test['type']  # Визначаємо тип тесту
            if test_type == 0:  # Тип 0 — тести з радіокнопками
                self.create_radio_test(testLayout, test)
            elif test_type == 1:  # Тип 1 — тести з полем для вводу
                self.create_input_test(testLayout, test)
            elif test_type == 2:  # Тип 2 — тести з випадаючим списком
                self.create_select_test(testLayout, test)
            elif test_type == 3:  # Тип 3 — аудіо-тести
                self.create_audio_test(testLayout, test)
    def createContent(self):
        Wiget = QWidget()  # Створюємо базовий віджет
        layout = QVBoxLayout(Wiget)  # Встановлюємо вертикальний layout
        layout.setContentsMargins(20, 20, 20, 20)  # Встановлюємо відступи

        self.title = QLabel('')  # Створюємо заголовок (поки порожній)
        self.title.setObjectName("title")  # Задаємо ім’я об’єкта для стилізації
        self.title.setAlignment(Qt.AlignCenter)  # Центруємо заголовок
        layout.addWidget(self.title)  # Додаємо заголовок до layout

        self.testwiget = QWidget()  # Створюємо віджет для розміщення тестів
        layout.addWidget(self.testwiget)  # Додаємо до layout

        check_button = QPushButton("Перевірити")  # Створюємо кнопку перевірки
        check_button.clicked.connect(self.check_answer)  # Прив’язуємо функцію перевірки
        check_button.setObjectName('testBtn')  # Задаємо ім’я об’єкта
        button_layout = QHBoxLayout()  # Горизонтальний layout для кнопки
        button_layout.addStretch()  # Розтяг зліва
        button_layout.addWidget(check_button)  # Додаємо кнопку
        button_layout.addStretch()  # Розтяг справа
        layout.addLayout(button_layout)  # Додаємо кнопку до головного layout

        layout.addStretch()  # Додаємо простір знизу
        return createScrol(Wiget)  # Обгортаємо все в скрол і повертаємо
    def check_answer(self):
        total = len(self.test_groups)  # Загальна кількість тестів
        correct = 0  # Лічильник правильних відповідей

        for group in self.test_groups:  # Перевіряємо кожну групу (тест)
            t = group['type']  # Отримуємо тип тесту
            if t == 0:  # Радіокнопки
                selected = None
                for i, radio in enumerate(group['radios']):
                    if radio.isChecked():  # Якщо вибрано відповідь
                        selected = i
                        break
                if selected == group['correct_answer']:  # Перевіряємо правильність
                    correct += 1
            elif t == 1:  # Текстове поле
                answer = group['input'].text().strip().lower()  # Отримуємо текст з поля
                if answer == group['correct_answer']:
                    correct += 1
            elif t == 2:  # Випадаючий список
                selected = (group['select'].currentIndex()-1)  # Індекс вибраного пункту
                if selected == group['correct_answer']:
                    correct += 1
            elif t == 3:  # Аудіо-тест
                selected = None
                for i, radio in enumerate(group['radios']):
                    if radio.isChecked():  # Якщо вибрано "Так" або "Ні"
                        selected = (i == 0)  # "Так" — це 0, "Ні" — 1
                        break
                if selected == group['correct_answer']:
                    correct += 1

        percent = int((correct / total) * 100) if total > 0 else 0  # Обчислюємо відсоток
        save_progress_controller(self.parent.parent.parent.userId, self.category_id, correct, total)  # Зберігаємо результат
        self.parent.parent.updateProgress()  # Оновлюємо прогрес користувача
        QMessageBox.information(self, "Результат", f"Ваш результат: {percent}%")  # Виводимо повідомлення з результатом
