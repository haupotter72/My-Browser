from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
from helper.urlHelper import is_valid_domain
from helper.googleSuggestModel import GoogleSuggestModel

import asyncio

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

        self.model = GoogleSuggestModel(self)
        self.completer = QCompleter(self.model, self)
        self.completer.setPopup(QListView())
        self.completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setCompleter(self.completer)

        self.timer = QTimer(self)
        self.timer.setInterval(150)  # Set the delay time to 500ms
        self.timer.setSingleShot(True)  # Make the timer a single-shot timer

        self.textChanged.connect(self.on_text_changed)
        self.timer.timeout.connect(self.process_text_changed)
        
        
        

    def on_text_changed(self):
        self.timer.start()

    def process_text_changed(self):
        text = self.text()
        if not text.startswith('http') and not text.startswith('https'):
            self.model.fetch_data(self.text())
    

    # def update_suggestions(self, text):
    #     suggestions = []
    #     for suggestion in search(text):
    #         if suggestion not in suggestions:
    #             suggestions.append(suggestion)
    #     model = self.completer.model()
    #     model.clear()
    #     for suggestion in suggestions:
    #         item = QStandardItem(suggestion)
    #         model.appendRow(item)
    #     self.completer.setModel(model)
        