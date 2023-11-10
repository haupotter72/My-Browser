from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtCore import Qt
import requests
from GPT import gpt_gen_img, gpt_talk
from googletrans import Translator
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtNetwork import QNetworkProxy
class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set dialog title
        self.setWindowTitle("Loading....")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.showMaximized()
        
        # Create a layout for the dialog
        layout = QVBoxLayout()
        self.setFixedWidth(500)
        
        # Create a label to display the text
        self.label = QLabel("Loading....")
        self.label.setWordWrap(True)
        
        # Add the label to the layout
        layout.addWidget(self.label)
        
        # Set the dialog layout
        self.setLayout(layout)
    def show(self):
        pixmap = QPixmap()
        super().show()
        mouse_pos = QCursor.pos()
        self.label.setPixmap(pixmap)
        self.updateLabel("Loading....")
        self.move(mouse_pos)

    def updateLabel(self, message):
        self.label.setText(message)
        self.adjustSize()
    def showImageToLabel(self, pixmap):
        self.label.setPixmap(pixmap)
        self.adjustSize()

    def translate(self, text):
        self.setWindowTitle("Dịch")
        
        self.thread = RequestTranslateThread(text)
        self.thread.response_received.connect(self.handle_trans_response)
        self.thread.start()
    def handle_trans_response(self, text):
        self.updateLabel(text)
        
        
    def gpt_ask(self, message):
        self.setWindowTitle(message)

        self.thread = RequestThread(message)
        self.thread.response_received.connect(self.handle_response)
        self.thread.start()
    def handle_response(self, response_text):
        self.updateLabel(response_text)

    
    def gpt_gen_img(self, text):
        self.updateLabel("Loading....")
        self.setWindowTitle(text)

        self.thread = RequestImgThread(text)
        self.thread.response_received.connect(self.handle_image_result)
        self.thread.start()

    def handle_image_result(self, response):
        response = requests.get(response)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.showImageToLabel(pixmap)


class RequestImgThread(QThread):
    response_received = pyqtSignal(str)
    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        # Perform the HTTP request in the background
        result = gpt_gen_img(self.message)

        # Emit the signal with the response data
        self.response_received.emit(result)
class RequestThread(QThread):
    response_received = pyqtSignal(str)
    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        # Perform the HTTP request in the background
        result = gpt_talk(self.message)

        # Emit the signal with the response data
        self.response_received.emit(result)

class RequestTranslateThread(QThread):
    response_received = pyqtSignal(str)
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.translator = Translator()

    def run(self):
        # Perform the HTTP request in the background
        result = self.translator.translate(self.text, dest='vi')

        # Emit the signal with the response data
        self.response_received.emit(result.text)

class ProxyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set dialog title
        self.setWindowTitle("VPN")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.proxyStatus = False
        
        # Create a QWidget as the parent widget
        widget = QWidget()

        # Create a QVBoxLayout for the layout
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a QLabel for the text
        label = ClickableLabel("Disabled")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                background-color: rgb(171, 171, 171);
                color: #FFFFFF;
                border-radius: 50px;
                font-size: 24px;
                font-weight: bold;
                padding: 40px;
            }
        """)
        label.clicked.connect(self.vpnClicked)

        self.label = label
        layout.addWidget(label)
        self.setFixedSize(200,300)

        self.setLayout(layout)
    def vpnClicked(self):
        if self.proxyStatus:
            print(f"Proxy status {self.proxyStatus} => Turn off")
            self.disable()
        else:
            print(f"Proxy status {self.proxyStatus} => Turn on")
            self.enable()
            
    def enable(self):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.ProxyType.HttpProxy)
        proxy.setHostName("194.233.83.119")
        proxy.setPort(3128)
        proxy.setPassword("trung")
        proxy.setUser("trungbmt")
        QNetworkProxy.setApplicationProxy(proxy)

        self.proxyStatus = True
        self.label.setText("Enabled")
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgb(53, 204, 37);
                color: #FFFFFF;
                border-radius: 50px;
                font-size: 24px;
                font-weight: bold;
                padding: 40px;
            }
        """)

    def disable(self):
        QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.ProxyType.DefaultProxy))

        self.proxyStatus = False
        self.label.setText("Disabled")
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgb(171, 171, 171);
                color: #FFFFFF;
                border-radius: 50px;
                font-size: 24px;
                font-weight: bold;
                padding: 40px;
            }
        """)
        

    
    def show(self, position):

        # Move the dialog to the calculated position
        self.move(position.x(), position.y())
        super().show()

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
