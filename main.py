from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
import qtawesome as qta
import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow
from browser import Browser
import subprocess
import argparse

from helper.strToBoolean import str2bool


class Main():
    browsers = []
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--incognito', type=str2bool, nargs='?', const=True, default=False, help='Enable incognito mode')
        args = parser.parse_args()

        if args.incognito:
            self.new_incognito_window_process()
        else: 
            self.new_window()

        sys.exit(self.app.exec())

    def new_window(self):
        browser = Browser(self)
        browser.show()
        self.browsers.insert(0, browser)
    def new_incognito_window_process(self):
        browser = Browser(self, isIncognito = True)
        browser.show()
        self.browsers.insert(0, browser)

    def new_incognito_window(self):
        subprocess.Popen(['python', 'main.py', '--incognito', 'True'])

if __name__ == '__main__':
    asyncio.run(Main())