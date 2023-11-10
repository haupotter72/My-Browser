from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
import qtawesome as qta
import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow
from normalTab import NormalTab as BrowserTab
from incognitoTab import IncognitoTab
from customTabBar import CustomTabWidget
from PyQt6 import QtCore
from PyQt6.QtWebEngineCore import QWebEngineHistoryItem
from PyQt6.QtWebEngineWidgets import QWebEngineView
from historyTab import HistoryWidget
import datetime
from PyQt6.QtGui import QGuiApplication

class Browser(QMainWindow):
    def __init__(self, main, isIncognito = False):
        super().__init__()
        self.setFocus()
        
        self.history = None
        self.isIncognito = isIncognito
        

        self.main = main
        
        self.profile = QWebEngineView(self).page().profile()


        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.oldPos = self.pos()

        self._keys = {Qt.Key.Key_Control: False, Qt.Key.Key_T: False, Qt.Key.Key_W: False, Qt.Key.Key_Shift: False, Qt.Key.Key_N: False, Qt.Key.Key_H: False}
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.add_new_tab_button = QPushButton("+")
        self.add_new_tab_button.clicked.connect(self.add_tab)
        # Get the index of the last tab
        last_tab_index = self.tabs.count() - 1
        # Insert the 'Add Tab' button next to the last tab
        # self.tabs.tabBar().setTabButton(last_tab_index, QTabBar.ButtonPosition.RightSide, self.add_new_tab_button)
        # self.tabs.addTab(self.add_new_tab_button, "")
        # self.tabs.setTabEnabled(self.tabs.count(), False)
        # Create the buttons
        self.minimizeButton = QPushButton()
        self.maximizeButton = QPushButton()
        self.closeButton = QPushButton()

        self.minimizeButton.setIcon(QIcon(qta.icon("fa5s.window-minimize")))
        self.maximizeButton.setIcon(QIcon(qta.icon("fa5s.window-maximize")))
        self.closeButton.setIcon(QIcon(qta.icon("fa5s.window-close")))
        
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.maximizeButton.clicked.connect(lambda: self.showMaximized() if not self.isMaximized() else self.showNormal())
        self.closeButton.clicked.connect(lambda: self.close())
        # Create the layouts
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_widget = QWidget()
        self.button_layout.addWidget(self.minimizeButton)
        self.button_layout.addWidget(self.maximizeButton)
        self.button_layout.addWidget(self.closeButton)
        self.button_widget.setLayout(self.button_layout)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tabs, 0, 0)
        layout.addWidget(self.button_widget, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        widget = QWidget()
        widget.setLayout(layout)

        width = 800
        height = 600
        self.setCentralWidget(widget)
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2

        self.setGeometry(x, y, width, height)
        # self.showFullScreen()

        if isIncognito:
            self.add_incognito_tab()
        else:
            self.add_tab()

        icon = QIcon('resources\images\logo.png')
        self.setWindowTitle("My Potter  Browser")
        self.setWindowIcon(icon)
        self.showMaximized()
        self.show()

        self.buttons = []
        self.buttons.append(self.minimizeButton)
        self.buttons.append(self.maximizeButton)
        self.buttons.append(self.closeButton)

        for button in self.buttons:
            button.setIconSize(QSize(18, 18))
            button.setStyleSheet("""
            QPushButton {
                background-color: rgba(128, 128, 128, 0.0);
            }
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.5);
            };
            border-radius: 1px; padding: 3px;
        """)
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(128, 128, 128, 0.0);
            }
            QPushButton:hover {
                background-color: rgba(255, 51, 51, 0.8);
            };
            border-radius: 1px; padding: 3px;
        """)
    
    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())
    def save_history(self, title, url):
        # Save the browsing history to a file
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open("history.txt", "a", encoding='utf-8') as f:
            f.write(f"{title}\t{url}\t{formatted_time}\n")
    def show_history(self):
        # self.save_history("test site", "https://chat.openai.com/c/5bcad6a2-cba2-4c75-9a52-388bd7a860af")
        with open("history.txt", encoding='utf-8') as f:
            lines = f.readlines()

        self.history = []
        for line in lines:
            parts = line.strip().split("\t")
            title, url, date = parts
            self.history.insert(0, {'title': title, 'date': date, 'url': url})

        history_widget = HistoryWidget(self.history, self)
        clear_button = QPushButton("Clear History")
        clear_button.clicked.connect(history_widget.clear_history)
        # dialog = QDialog()
        # dialog.setLayout(layout)
        # dialog.exec_()
        self.tabs.addTab(history_widget, "History")
        self.tabs.setCurrentWidget(history_widget)
    def clear_history(self):
        print("Clearing...")
        try:
            with open("history.txt", "w", encoding='utf-8') as file:
                file.write('')
            print(f"File cleared successfully.")
        except FileNotFoundError:
            print(f"File not found.")
        except Exception as e:
            print(f"An error occurred while clearing the file: {e}")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition()

    def mouseMoveEvent(self, event):
        pos = event.globalPosition() - self.oldPos
        delta = QPoint(pos.toPoint())
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition()

    def open_new_window(self):
        self.main.new_window()
    def open_new_incognito_window(self):
        self.main.new_incognito_window()

    def open_incognito_tab(self):
        icon = QIcon(qta.icon("fa5s.hat-cowboy"))
        tab = IncognitoTab()
        # self.tabs.setTabText(self.tabs.indexOf(tab), "Incognito Tab")
        self.tabs.addTab(tab, "Incognito Tab")
        self.tabs.setTabIcon(self.tabs.indexOf(tab), icon)
        self.tabs.setCurrentWidget(tab)

    def add_tab(self, url="https://www.google.com"):
        tab = BrowserTab(url, self)
        self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentWidget(tab)

    def add_incognito_tab(self, url=""):
        icon = QIcon(qta.icon("fa5s.hat-cowboy"))
        tab = IncognitoTab()
        # self.tabs.setTabText(self.tabs.indexOf(tab), "Incognito Tab")
        self.tabs.addTab(tab, "Incognito Tab")
        self.tabs.setTabIcon(self.tabs.indexOf(tab), icon)
        self.tabs.setCurrentWidget(tab)

    def close_tab(self, index):
        if self.tabs.count() < 2:
            sys.exit()

        self.tabs.removeTab(index)

    def keyPressEvent(self, event):
        if event.key() in self._keys:
            self._keys[event.key()] = True
            if self._keys[Qt.Key.Key_Control] and self._keys[Qt.Key.Key_T]:
                
                if self.isIncognito:
                    self.add_incognito_tab()
                else:
                    self.add_tab()
            elif self._keys[Qt.Key.Key_Control] and self._keys[Qt.Key.Key_W]:
                self.close_tab(self.tabs.count() - 1)
            elif self._keys[Qt.Key.Key_Control] and self._keys[Qt.Key.Key_Shift] and self._keys[Qt.Key.Key_N]:
                self.open_new_incognito_window()
            elif self._keys[Qt.Key.Key_Control] and self._keys[Qt.Key.Key_N]:
                self.open_new_window()
    def keyReleaseEvent(self, event):
        if event.key() in self._keys:
            self._keys[event.key()] = False