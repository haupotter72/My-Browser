from PyQt6.QtWidgets import QTabWidget, QPushButton, QHBoxLayout
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
import qtawesome as qta

class CustomTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.tab_bar = QTabBar(self)
        label = QLabel("hello")
        layout.addWidget(label, 100, QtCore.Qt.AlignmentFlag.ad)
        self.setLayout(layout)
        self.setTabBar(self.tab_bar)