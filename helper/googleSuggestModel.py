import requests
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant, QTimer, pyqtSignal
from PyQt6.QtGui import *

class GoogleSuggestModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderData(0, Qt.Orientation.Horizontal, "Search Suggestions")
        self.suggestions = []

    def fetch_data(self, text):
        self.clear()
        self.suggestions = []
        if not text:
            return
        response = requests.get(
            f"https://suggestqueries.google.com/complete/search?output=firefox&q={text}"
        )
        self.suggestions = response.json()[1]
        # print(text)
        # print(self.suggestions)
        for suggestion in self.suggestions:
            item = QStandardItem(suggestion)
            self.appendRow(item)