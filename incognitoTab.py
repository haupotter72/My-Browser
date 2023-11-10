from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineCore import QWebEngineProfile
import qtawesome as qta
from PyQt6.QtNetwork import QNetworkProxy
from normalTab import NormalTab
from dialog import ProxyDialog
import qdarktheme

class IncognitoTab(NormalTab):
    def __init__(self, url=""):
        
        super(IncognitoTab, self).__init__(url)
        self.layout = QVBoxLayout()
        self.webview.page().loadStarted.disconnect()
        self.webview.page().loadFinished.disconnect()
        self.webview.page().titleChanged.disconnect()
        self.proxyDialog = None

        self.vpn_button = QPushButton()
        self.vpn_button.setIcon(QIcon(qta.icon("fa5s.globe")))
        self.vpn_button.clicked.connect(self.showProxyDialog)

        self.toolbar.removeAction(self.toolbar.actions()[3])
        self.toolbar.removeAction(self.toolbar.actions()[3])
        self.toolbar.removeAction(self.toolbar.actions()[3])
        self.toolbar.removeAction(self.toolbar.actions()[3])
        self.toolbar.addWidget(self.vpn_button)

        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search term")
        self.url_bar.setText(url)
        self.toolbar.addWidget(self.url_bar)
        self.webview.setContent
        
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        profile = self.webview.page().profile()
        profile.setSpellCheckEnabled(True)
        qdarktheme.setup_theme()
        self.load_image()

    def load_image(self):
        # Define the HTML string with the image
        html = """
            <html>
                <head>
                    <style>
                        body {
                            background-color: black;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            padding: 0;
                        }

                        img {
                            max-width: 100%;
                            max-height: 100%;
                        }
                    </style>
                </head>
                <body>
                    <img src="https://mediamart.vn/images/uploads/2022/713193b6-a8b3-471d-ab04-c38dae2c1da4.jpg" alt="Image">
                </body>
            </html>
        """

        # Load the HTML string into the web view
        self.webview.setHtml(html, QUrl("https://google.com/"))
    def showProxyDialog(self):
        if not self.proxyDialog:
            self.proxyDialog = ProxyDialog(self)
        
        global_position = self.vpn_button.mapToGlobal(self.vpn_button.rect().bottomRight())
        self.proxyDialog.show(global_position)
        
    def enableProxy(self):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.ProxyType.HttpProxy)
        proxy.setHostName("194.233.83.119")
        proxy.setPort(3128)
        proxy.setPassword("trung")
        proxy.setUser("trungbmt")
        QNetworkProxy.setApplicationProxy(proxy)
        # QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.DefaultProxy))
