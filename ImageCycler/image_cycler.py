from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL import ImageQt

class ImageCyclerWidget(QWidget):

    def __init__(self):
        super().__init__()
        
        self.current_index = 0

        # Main Layout (Vertical)
        main_layout = QVBoxLayout(self)
        self.images = []

        # Image Stack (Row 1)
        self.image_stack = QStackedLayout()

        self.image_label = QLabel("Open one or more images to start")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_stack.addWidget(self.image_label)

        main_layout.addLayout(self.image_stack)


        # Navigation Controls (Row 2)
        nav_layout = QHBoxLayout()

        self.prev_button = QPushButton("←")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self.prev_image)

        self.index_label = QLabel(self.get_index_text())

        self.next_button = QPushButton("→")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.next_image)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.index_label, alignment=Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)

        # Image Name Label (Row 3)
        self.name_label = QLabel(self.get_image_name())
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.name_label)

        self.update_ui()

    def setImages(self, image_file):
        self.images.clear
        if isinstance(image_file, list):
            for i, image in enumerate(image_file):
                self.images.append(image)
        else:
            self.images[0] = image_file

        self.update_ui()
                

    def get_index_text(self):
        if(len(self.images) == 0):
            return "0/0"
        else:
            return f"{self.current_index + 1}/{len(self.images)}"

    def get_image_name(self):
        if(len(self.images) == 0):
            return "no image"
        else:
            return self.images[self.current_index].name

    def next_image(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.update_ui()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_ui()

    def update_ui(self):
        #self.image_stack.setCurrentIndex(self.current_index)
        if len(self.images) > 0 & 0 <= self.current_index < len(self.images):
            imageQt = ImageQt.ImageQt(self.images[self.current_index].image)
            pixmap = QPixmap.fromImage(imageQt)
            self.image_label.setPixmap(pixmap)

        if self.current_index == 0:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(True)
        elif self.current_index == len(self.images) - 1:
            self.next_button.setEnabled(False)
            self.prev_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)

            
        self.index_label.setText(self.get_index_text())
        self.name_label.setText(self.get_image_name())
