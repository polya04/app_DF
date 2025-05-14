# Стилі для карток слів
def wordCardStyle(theme):
    return f'''
    #examples_title{{
        font-size: 16px;
        font-weight: bold;
        color: {theme['colorFont2']};
        margin-top: 10px;
    }}
    #wordCard {{
        background-color: #ffffff;
        border: 1px solid #000;
        border-radius: 8px;
    }}

    #wordImage {{
    }}

    #wordText {{
        font-weight: bold;
        font-size: 14px;
    }}

    #transcriptionText {{
        color: {theme['colorFont2']};
        font-size: 12px;
    }}

    #translationText {{
        color: {theme['colorFont3']};
        font-size: 13px;
    }}

    #soundButton {{
        qproperty-iconSize: 18px;
        border: none;
    }}
    '''

# Стилі для віджетів (кнопок, текстових полів тощо)
def widgetStyle(theme):
    return f'''
    QWidget {{
        background-color: {theme['mainBg']};
        color: {theme['colorFont']};
        font-size: 14px;
    }}

    QPushButton {{
        background-color: {theme['colorBtn']};
        color: white;
        border-radius: 5px;
        padding: 8px;
    }}

    QPushButton#selected {{
        background-color: {theme['colorBtnHover']};
        color: white;
        font-weight: bold;
        border: 2px solid {theme['colorFont']};
    }}

    QPushButton:hover {{
        background-color: {theme['colorBtnHover']};
    }}

    QLineEdit {{
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 5px;
        background-color: white;
        color: #2C3E50;
    }}

    #title {{
        font-weight: bold;
        color: {theme['colorFont']};
        font-size: 30px;
        text-align: center;
    }}

    #subtitle {{
        font-weight: bold;
        color: {theme['colorFont']};
        font-size: 20px;
        font-style: italic;
    }}
    .teotyBtn{{
        height:100%;
        font-size: 25px;
        font-weight: bold;
    }}
    '''

# Стилі для меню та кнопок
def menuStyle(theme):
    return f'''
    #menuLayout {{
        background-color: {theme['headerColor']};
    }}

    QPushButton.menuBtn {{
        background-color: transparent;
        border: 2px solid transparent;
        border-bottom: 2px solid transparent;
        color: {theme['colorFont']};
        font-size: 16px;
        width: 200px;
        height: 100%;
        border-radius: 0px;
        text-align: center;
    }}

    QPushButton.menuBtn:hover {{
        border-bottom: 2px solid {theme['colorBtn']};
    }}

    QPushButton.selectedBtn {{
        font-weight: bold;
        color: #fff;
        background-color: {theme['colorBtn']};
    }}
    #testBtn{{
        padding: 15px 20px;
        font-weight: bold;
        font-size: 20px;
    }}
    '''

# Стилі для таблиць
def tableStyle(theme):
    return f'''
    QTableWidget {{
        background-color: {theme['mainBg']};
        color: {theme['colorFont']};
        border: 1px solid {theme['headerColor']};
        gridline-color: {theme['headerColor']};
        font-size: 14px;
    }}
    QTableView {{
        alternate-background-color: {theme['mainBg']}; 
        background-color: {theme['headerColor']};          
    }}
    QHeaderView::section {{
        background-color: {theme['headerColor']};
        color: {theme['colorFont']};
        font-weight: bold;
        padding: 5px;
        border: 1px solid {theme['headerColor']};
    }}

    QTableWidget::item {{
        padding: 4px;
    }}

    QTableWidget::item:selected {{
        background-color: {theme['colorBtn']};
        color: red;
    }}
    '''

# Стилі для полос прокрутки
def scrollBarStyle(theme):
    return f'''
    QScrollBar:vertical {{
        width: 8px;
        background: {theme['mainBg']};
    }}

    QScrollBar::handle:vertical {{
        background: {theme['colorBtnHover']};
        border-radius: 4px;
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    '''

# Стилі для gruppi
def groupStyle(theme):
    return f'''
    QGroupBox {{
        font-size: 20px;
        font-weight: bold;
        padding: 15px;
        border: 1px solid {theme['colorFont']};
        border-radius: 8px;
        margin-top: 20px;
        background-color: {theme['mainBg']};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0;
        left: 10px;
        color: {theme['colorFont']};
    }}

    #gbLabel {{
        color: {theme['colorFont']};
        font-size: 14px;
        margin-bottom: 5px;
    }}

    #gbLabel.section {{
        font-weight: bold;
        font-size: 16px;
    }}

    .content {{
        background-color: {theme['headerColor']};
        padding: 10px;
        margin-top: 10px;
        border-radius: 8px;
        color: {theme['colorFont']};
    }}

    .content p {{
        font-size: 14px;
        margin: 5px 0;
    }}

    .groupTitle {{
        font-size: 18px;
        font-weight: bold;
        color: {theme['headerColor']};
        margin-bottom: 10px;
    }}
    '''

# Стилі для сторінок теорії
def theorySectionStyle(theme):
    return f'''
    #sectionBlock {{
        background-color: {theme['headerColor']};
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
    }}

    #sectionTitle {{
        background-color: {theme['headerColor']};
        font-size: 16px;
        font-weight: bold;
        color: {theme['colorFont']};
    }}

    #sectionDesc {{
        background-color: {theme['headerColor']};
        font-size: 14px;
        color: {theme['colorFont2']};
    }}

    #sectionExamples {{
        margin-top: 5px;
        color: {theme['colorFont3']};
        font-size: 13px;
    }}
     #Infoblock {{
                border: 1px solid {theme['colorFont']};
                border-radius: 10px;
                margin-top: 10px;
                padding: 10px;
            }}
    #InfoLabel {{
                font-size: 14px;
    }}
    '''

# стилі для тестів
def testsStyle(theme):
    return f'''
     QComboBox#customComboBox {{
        padding: 4px;
        font-size: 14px;
        min-height: 24px;
        border: 1px solid #888;
        border-radius: 4px;
    }}

'''

# Основна функція для збирання всіх стилів
def getStyle(theme):
    return f'''
    {widgetStyle(theme)}
    {menuStyle(theme)}
    {tableStyle(theme)}
    {scrollBarStyle(theme)}
    {wordCardStyle(theme)}
    {groupStyle(theme)}
    {theorySectionStyle(theme)}
    {testsStyle(theme)}
    '''
