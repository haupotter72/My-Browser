from PyQt6.QtWebEngineWidgets import QWebEngineProfile

proxy_host = '101.42.107.214'
proxy_port = 2080

profile = QWebEngineProfile("my_profile")
profile.setHttpProxy(f"{proxy_host}:{proxy_port}")