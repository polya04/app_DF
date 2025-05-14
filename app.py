import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.fonts=false"

import sys
from PyQt5.QtWidgets import QApplication
from models.database import create_tables
from views.MainWindow import MainApp

from assets.style import getStyle
from config import lightTheme


# ымпорти для завантаження бд
from models.updateTables.updateTests import updateTests
from models.updateTables.UbdateLetters import loadLeters
from models.updateTables.UpdateLeksika import insert_words_from_excel_data, read_excel_all_sheets
from config import updateData



def loadBd():
    loadLeters(f"{updateData}\\alphabet.json")
    excel_data = read_excel_all_sheets(f"{updateData}\\leksika.xlsx")
    insert_words_from_excel_data(excel_data)
    updateTests(updateData)
# точка входу до програми
if __name__ == "__main__":
    # створюємо таблиці
    create_tables()
    # завантаження бд (розкоментувати коли бд порожня)
    # loadBd()  
    # users = get_all_users_controller()

    # Створюємо екземпляр застосунку
    app = QApplication(sys.argv)
    # Встановлюємо стиль оформлення інтерфейсу (світла тема)
    app.setStyleSheet(getStyle(lightTheme))
    # Створюємо та показуємо головне вікно застосунку
    window = MainApp(app)
    window.show()
    # Запускаємо цикл подій застосунку
    sys.exit(app.exec_())
