from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QLabel,QHBoxLayout , QStackedWidget,
                             QTableWidget, QTableWidgetItem)

from controllers.category_controller import  get_category_by_page
from controllers.word_controller import get_words_by_category
from views.content.centerPages.common import createTable, createScrol

class LexisPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setLayout(self.createWidget())

    def createWidget(self):
        layout = QHBoxLayout()
        asside_widget = self.createAsside()
        layout.addWidget(asside_widget, stretch=2) 

        self.content_widget = QStackedWidget()
        self.content_widget.addWidget(self.createWordsPart())
        self.content_widget.setObjectName("cr")
        layout.addWidget(self.content_widget, stretch=8) 

        return layout
    
    def createAsside(self):
        MenuWiget = QWidget()
        layout = QVBoxLayout()

        categories = get_category_by_page(2)
        TopLayout = QVBoxLayout()
        self.tabs = []
        for idx, c in enumerate(categories):
            tab = QPushButton(c['name'])   
            TopLayout.addWidget(tab)
            tab.clicked.connect(partial(self.setWigetInStack, idx, c['id'], c['name']))
            self.tabs.append(tab)
        layout.addLayout(TopLayout, 3)
        layout.addStretch(2) 

        self.btnBack = QPushButton("Назад")
        self.btnBack.clicked.connect(self.backBtnHandle)
        
        layout.addWidget(self.btnBack, 1)
        MenuWiget.setLayout(layout)
        return MenuWiget  
    def backBtnHandle(self):
        self.parent.setWigetInStack(0)
    def setWigetInStack(self, number, categNum, cutName):
        for i, b in enumerate(self.tabs):
            b.setObjectName("selected" if i == number else "")
        self.parent.parent.parent.setTheme()

        words = get_words_by_category(categNum)
        self.title.setText(cutName)
        self.table.setRowCount(len(words))
        for i, word in enumerate(words):
            self.table.setItem(i, 0, QTableWidgetItem(word['word']))
            self.table.setItem(i, 1, QTableWidgetItem(word['transcription']))
            self.table.setItem(i, 2, QTableWidgetItem(word['translation']))
        # self.table.scrollToTop()
        self.table=createTable(self.table, len(words))

    def createWordsPart(self):
        Wiget = QWidget()
        layout = QVBoxLayout(Wiget)
        layout.setContentsMargins(20,20,20,20)
        self.title = QLabel('')
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Слово", "Транскрипція", "Переклад"])
        self.table = createTable(table, 0)
        layout.addWidget(self.table)
        layout.addStretch()

        return createScrol(Wiget)
 