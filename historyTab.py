from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QApplication, QLineEdit, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen, QGuiApplication
from helper.urlHelper import is_valid_url

class HistoryWidget(QWidget):
    def __init__(self, history, browser=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = history
        self.browser = browser

        widget = QWidget()
        widgetLayout = QHBoxLayout(widget)
        header_label = QLabel("Tìm kiếm")
        input_field = QLineEdit()
        button = QPushButton("SEARCH")
        button.clicked.connect(lambda: self.search_table(input_field.text()))
        widgetLayout.addWidget(input_field)
        widgetLayout.addWidget(button)
        widget.setLayout(widgetLayout)
        

        self.table = QTableWidget()
        self.table.setStyleSheet("QTableWidget { border-radius: 8px; border: 1px solid gray }")
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Title', 'URL', 'Date'])
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 400)
        self.table.setColumnWidth(2, 150)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.itemClicked.connect(self.handle_item_clicked)
        self.populate_table()

        self.layout = QVBoxLayout()
        self.layout.addWidget(header_label)
        self.layout.addWidget(widget)
        self.layout.addWidget(self.table)

        
        deleteHistory = QPushButton("Xóa lịch sử")
        deleteHistory.setFixedWidth(int(widget.width() * 0.5))
        deleteHistory.clicked.connect(lambda: self.clear_history())
        self.layout.addWidget(deleteHistory)
        self.layout.setAlignment(deleteHistory, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.setWindowTitle("History")

        widgetToRounded = [input_field, button, deleteHistory]
        for button in widgetToRounded:
            button.setStyleSheet("padding: 5px; border-radius: 7px; border: 1px solid gray")


    def populate_table(self):
        # Populate the table with the browsing history
        for item in self.history:
            title = item['title'] or item['url']
            url = item['url']
            date = item['date']
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(title))
            self.table.setItem(row_position, 1, QTableWidgetItem(url))
            self.table.setItem(row_position, 2, QTableWidgetItem(date))

    def search_table(self, text):
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if text.lower() in item.text().lower():
                    match = True
                    break

            self.table.setRowHidden(row, not match)
    def clear_history(self):
        self.browser.clear_history()
        self.table.clearContents()


    def handle_item_clicked(self, item):
        text = item.text()
        if is_valid_url(text):
            self.browser.add_tab(url=text)

