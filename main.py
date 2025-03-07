#from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog
#import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QMessageBox, QLabel, QMenuBar, QMainWindow, QMenu
from PyQt6.QtGui import QFont, QPixmap, QAction, QIcon
from PyQt6.QtCore import Qt
from PIL import Image, ImageQt
from ImageCycler import ImageCyclerWidget, ImageFile
import sys, os
from ImageConverter import TextWindow, ImageConverter

class MainWindow(QMainWindow):
    class Actions:
        def __init__(self, parent):
            self.to565 = QAction(QIcon("bug.png"), "&Generate 565 array(s)", parent)
            self.to565.setStatusTip("Open one or more images")
            self.to565.triggered.connect(parent.to565Array)
            self.to565.setEnabled(False)

            self.to5bit = QAction(QIcon("bug.png"), "&Generate 5 bit grayscale array(s)",  parent)
            self.to5bit.setStatusTip("Open one or more images")
            self.to5bit.triggered.connect(parent.to5bitArray)
            self.to5bit.setEnabled(False)

            self.to8bit = QAction(QIcon("bug.png"), "&Generate 8 bit grayscale array(s)", parent)
            self.to8bit.setStatusTip("Open one or more images")
            self.to8bit.triggered.connect(parent.to8bitArray)
            self.to8bit.setEnabled(False)


    def __init__(self):
        super().__init__()

        self.images = []

        self.setFixedSize(300, 400)
        self.act = self.Actions(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Embedded Image Tool")

        self.childWindows = []

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&Actions")

        # Add Actions to Menu
        file_menu.addAction("Open file(s)", self.openImages)
        file_menu.addSeparator()
        file_menu.addAction(self.act.to565)
        file_menu.addAction(self.act.to5bit)
        file_menu.addAction(self.act.to8bit)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        # Create Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create Image Label
        self.image_cycler = ImageCyclerWidget()#QLabel("Open one or more images to start")
        #self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.image_label.setMaximumSize(100,100)

        self.layout.addWidget(self.image_cycler)
        self.central_widget.setLayout(self.layout)
    
    def openImages(self):
        file_path, _ = QFileDialog.getOpenFileNames(self, "Open Image(s)", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        images = []

        for file in file_path:
            image = Image.open(file)#.thumbnail((300, 300))#.convert("RGBA")

            self.images.append(ImageFile(image, os.path.basename(file)))
            image.thumbnail((300,300))
            images.append(ImageFile(image, os.path.basename(file)))

        if len(file_path) != 0:
            self.image_cycler.setImages(images)
            self.act.to565.setEnabled(True)
            self.act.to5bit.setEnabled(True)
            self.act.to8bit.setEnabled(True)
        
    def saveFile(self):
        options = QFileDialog.Option.ShowDirsOnly
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py);;All Files (*)", options=options)
        if filePath:
            try:
                with open(filePath, 'w', encoding='utf-8') as file:
                    file.write(self.textEdit.toPlainText())
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def to565Array(self):
        self.childWindows.append(TextWindow("565 C Array", ImageConverter.convert(self.images, ImageConverter.Algorythm.to565)))
        self.childWindows[-1].show()

    def to8bitArray(self):
            self.childWindows.append(TextWindow("8-bit greyscale C Array", ImageConverter.convert(self.images, ImageConverter.Algorythm.to8bit)))
            self.childWindows[-1].show()
    def to5bitArray(self):
            self.childWindows.append(TextWindow("5 bit greyscale C Array", ImageConverter.convert(self.images, ImageConverter.Algorythm.to5bit)))
            self.childWindows[-1].show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())