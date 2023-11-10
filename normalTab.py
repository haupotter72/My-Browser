from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
import qtawesome as qta
from addressBar import AddressBar
from helper.urlHelper import is_valid_domain
import requests
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from GPT import gpt_talk
import asyncio
from dialog import CustomDialog
import qdarktheme,os
from PyQt6.QtPrintSupport import QPrintPreviewDialog


class NormalTab(QWidget):
    def __init__(self, url="about:blank", browser = None):
        super().__init__()
        self.browser = browser

        self.layout = QVBoxLayout()

        self.toolbar = QToolBar()
        self.layout.addWidget(self.toolbar)
        self.buttons = []
        self.dialog = None

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(qta.icon("fa5s.chevron-left")))
        self.toolbar.addWidget(self.back_button)
        self.buttons.append(self.back_button)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon(qta.icon("fa5s.chevron-right")))
        self.toolbar.addWidget(self.forward_button)
        self.buttons.append(self.forward_button)

        self.reload_button = QPushButton()
        self.reload_button.setIcon(QIcon(qta.icon("fa5s.redo-alt")))
        self.toolbar.addWidget(self.reload_button)
        self.buttons.append(self.reload_button)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon(qta.icon("fa5s.home")))
        self.toolbar.addWidget(self.stop_button)
        self.buttons.append(self.stop_button)

        self.incognito_button = QPushButton()
        self.incognito_button.setIcon(QIcon(qta.icon("fa5s.hat-cowboy")))
        self.toolbar.addWidget(self.incognito_button)
        self.buttons.append(self.incognito_button)


        self.url_bar = AddressBar()
        self.url_bar.setPlaceholderText("Enter URL or search term")
        self.url_bar.setText(url)
        self.url_bar.setStyleSheet("padding: 5px; border-radius: 10px; border: 1px solid gray")
        self.url_bar.setFixedHeight(30)
        self.toolbar.addWidget(self.url_bar)

        self.more_button = QPushButton()
        self.more_button.setIcon(QIcon(qta.icon("fa5s.ellipsis-h")))
        self.toolbar.addWidget(self.more_button)
        self.buttons.append(self.more_button)

        gray_color = QColor.fromRgbF(0.5, 0.5, 0.5, 0.5)
        for button in self.buttons:
            button.setIconSize(QSize(24, 24))
            button.setStyleSheet("""
            QPushButton {
                background-color: white;
            }
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.5);
            };
            border-radius: 1px; padding: 5px;
        """)

        history_action = QAction('History', self)
        history_action.triggered.connect(lambda: self.browser.show_history())
        
        print_action = QAction('Print', self)
        print_action.triggered.connect(lambda: self.print_page())

        theme1 = QAction('Theme 1', self)
        theme1.triggered.connect(lambda: qdarktheme.setup_theme("light"))

        theme2 = QAction('Theme 2', self)
        theme2.triggered.connect(lambda: qdarktheme.setup_theme("dark"))

        self.menu = QMenu(self)
        self.menu.setFixedSize(200, 400)
        self.menu.addAction("Settings")
        self.menu.addAction(history_action)
        self.menu.addAction(print_action)
        self.menu.addAction("Help")
        self.menu.addAction("About")
        self.menu.addAction(theme1)
        self.menu.addAction(theme2)
        font = QFont()
        font.setPointSize(12)
        self.set_font_size(self.menu, font)

        self.more_button.setMenu(self.menu)
        self.more_button.setStyleSheet("""
            QPushButton::menu-indicator {
                image: none;
                width: 0px;
            };
            border-radius: 1px; padding: 5px;
        """)


        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)

        self.setLayout(self.layout)

        self.back_button.clicked.connect(self.webview.back)
        self.forward_button.clicked.connect(self.webview.forward)
        self.reload_button.clicked.connect(self.webview.reload)
        self.stop_button.clicked.connect(self.webview.stop)
        self.incognito_button.clicked.connect(self.open_incognito_tab)

        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.webview.load(QUrl(url))

        self.webview.urlChanged.connect(self.update_url)
        self.webview.page().titleChanged.connect(self.update_title)

        self.icon = QMovie('resources/images/spinner.gif')
        self.icon.frameChanged.connect(self.set_icon)
        self.webview.page().loadStarted.connect(self.start_loading)
        self.webview.page().loadFinished.connect(self.stop_loading)

        self.webview.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.webview.customContextMenuRequested.connect(self.show_context_menu)
        self.webview.page().profile().downloadRequested.connect(self.handle_download_request)


        # self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        # self.webview.page().profile().settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # self.webview.page().profile().settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    def print_page(self):
        print("printing...")
        # Create a print preview dialog
        preview_dialog = QPrintPreviewDialog()
        preview_dialog.setWindowTitle("Print Preview")

        # Connect the print action
        preview_dialog.paintRequested.connect(self.webview.print)

        # Show the print preview dialog
        preview_dialog.exec()
    def set_font_size(self, menu, font):
    # Set the font size for all actions in the menu
        for action in menu.actions():
            action.setFont(font)
            if action.menu():
                # Recursively set the font size for submenus
                self.set_font_size(action.menu(), font)
    def show_context_menu(self, pos: QPoint):
        menu = QMenu(self)
    
        selectedText = self.webview.page().selectedText()
        if selectedText:
            text = selectedText if not selectedText.__len__()>30 else f"{selectedText[:30]}..."

            gpt_action = QAction(f"Định nghĩa của từ: {text}", self)
            gpt_action.triggered.connect(lambda: self.handleGptClicked(f"Định nghĩa của từ: {selectedText}"))
            menu.addAction(gpt_action)

            
            translate_action = QAction(f"Dịch từ này: {text}", self)
            translate_action.triggered.connect(lambda: self.handleTranslateClicked(selectedText))
            menu.addAction(translate_action)

            
            generate_image_action = QAction(f"Nhờ AI tạo ra hình ảnh cho từ này: {text}", self)
            generate_image_action.triggered.connect(lambda: self.handleGptGenerateImage(selectedText))
            menu.addAction(generate_image_action)

        save_screen_action = QAction(f"Lưu ảnh màn hình", self)
        save_screen_action.triggered.connect(lambda: self.save_screen())

        menu.addAction("Back", self.webview.back)
        menu.addAction("Forward", self.webview.forward)
        menu.addAction("Reload", self.webview.reload)
        menu.addAction("Stop", self.webview.stop)
        menu.addAction(save_screen_action)
        menu.exec_(self.webview.mapToGlobal(pos))
    
    def save_screen(self):
        image = self.webview.grab()
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix("png")
        file_dialog.setNameFilter("PNG Image (*.png)")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if file_dialog.exec() != QFileDialog.DialogCode.Accepted:
            return
        file_path = file_dialog.selectedFiles()[0]
        image.save(file_path)
        # Notify the user about the successful save
        print(f"Image saved to {file_path}")
    def handle_download_request(self, download_item):
        download_item.accept()

    def handleGptGenerateImage(self, text):
        if(self.dialog):
            self.dialog.show()
            self.dialog.gpt_gen_img(text)
        else:
            self.dialog = CustomDialog(self)
            self.dialog.show()
            self.dialog.gpt_gen_img(text)
        
    def handleGptClicked(self, message):
        if(self.dialog):
            self.dialog.show()
            self.dialog.gpt_ask(message)
        else:
            self.dialog = CustomDialog(self)
            self.dialog.show()
            self.dialog.gpt_ask(message)
    def handleTranslateClicked(self, text):
        if(self.dialog):
            self.dialog.show()
            self.dialog.translate(text)
        else:
            self.dialog = CustomDialog(self)
            self.dialog.show()
            self.dialog.translate(text)

    def open_incognito_tab(self):
        self.browser.open_new_incognito_window()

    def start_loading(self):
        self.icon.start()

    def stop_loading(self):
        self.icon.stop()
        self.icon.jumpToFrame(0)
        self.set_icon()
        self.update_tab_icon()
        self.browser.save_history(self.webview.title(), self.webview.url().toString())
    def set_icon(self):
        self.parent().parent().setTabIcon(self.parent().indexOf(self), QIcon(self.icon.currentPixmap()))

    def update_title(self, title):
        # Update the title of the tab to match the web view's title
        self.parent().parent().setTabText(self.parent().indexOf(self), title)
    def update_tab_icon(self):
        # get the favicon of the website
        url = self.webview.url().toString()
        if not url.startswith('http'):
            return
        domain = url.split('/')[2]
        favicon_url = f'https://www.google.com/s2/favicons?domain={domain}'
        response = requests.get(favicon_url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        # set the tab icon
        icon = QIcon(pixmap)
        # icon.addPixmap(response.content)
        self.parent().parent().setTabIcon(self.parent().indexOf(self), icon)

    def navigate_to_url(self):
        url_text = self.url_bar.text().strip()
        print(url_text)     
        is_valid = is_valid_domain(url_text)
        if not url_text.startswith("http://") and not url_text.startswith("https://"):
            if is_valid:
                url_text = "http://" + url_text
            else:
                # Construct a Google search URL with the entered query
                url_text = "https://www.google.com/search?q=" + url_text.replace(" ", "+")

        url = QUrl(url_text)

        self.webview.load(url)
        self.url_bar.clearFocus()
    def update_url(self, q):
        url = q.toString()
        # url_obj = QUrl(url)
        # url_obj.setQuery("")  # remove query parameters
        if '?' in url:
            url = url.split('?')[0]
        self.url_bar.setText(url)

