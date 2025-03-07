from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QMessageBox, QLabel, QMenuBar, QMainWindow, QMenu
from PyQt6.QtGui import QFont, QPixmap, QAction, QIcon
from PyQt6.QtCore import Qt
from PIL import Image, ImageQt
from .code_editor import CodeEditor
import sys, os

class TextWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, title, text):
        super().__init__()
        self.setMinimumSize(400,300)
        self.setWindowTitle(title)
        layout = QVBoxLayout()#CodeEditor(self)
        self.code_editor = CodeEditor(self)#QLabel("Another Window")
        self.code_editor.setPlainText(text)

        layout.addWidget(self.code_editor)
        self.setLayout(layout)