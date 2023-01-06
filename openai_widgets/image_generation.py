from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage

from PyQt5.QtCore import Qt

import threading
import requests
import openai
import os


API_KEY: str = os.environ['OPENAI_API_KEY']

openai.api_key = API_KEY


class OpenAIImageGeneration(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.input: QPlainTextEdit = QPlainTextEdit(self)
        self.label: QLabel = QLabel()
        self.scrollArea: QScrollArea = QScrollArea(self)
        self.submit: QPushButton = QPushButton('Выполнить', self)
        self.save: QPushButton = QPushButton('Сохранить', self)

        vBoxLayout: QVBoxLayout = QVBoxLayout(self)
        hBoxLayout: QHBoxLayout = QHBoxLayout()
        buttonsLayout: QHBoxLayout = QHBoxLayout()

        vBoxLayout.addLayout(hBoxLayout)
        vBoxLayout.addLayout(buttonsLayout)

        buttonsLayout.addWidget(self.submit)
        buttonsLayout.addWidget(self.save)
        buttonsLayout.setAlignment(self.submit, Qt.AlignLeft)
        buttonsLayout.setAlignment(self.save, Qt.AlignLeft)
        buttonsLayout.addStretch(10)

        self.save.setVisible(False)

        hBoxLayout.addWidget(self.input)
        hBoxLayout.addWidget(self.scrollArea)

        self.submit.clicked.connect(self.__onSubmitClicked)
        self.save.clicked.connect(self.__saveImage)

    def __onSubmitClicked(self) -> None:
        t = threading.Thread(target=self.__getGeneratedImage)
        t.daemon = True
        t.start()

    def __getGeneratedImage(self) -> None:
        prompts: str = self.input.toPlainText()
        if not prompts:
            return

        try:
            self.submit.setDisabled(True)

            response = openai.Image.create(
                prompt=prompts,
                n=1,
                size='1024x1024'
            )

            request = requests.get(response['data'][0]['url'])

            image: QImage = QImage()
            image.loadFromData(request.content)

            self.label.setPixmap(QPixmap(image))

            self.scrollArea.setWidget(self.label)
        finally:
            self.save.setVisible(True)
            self.submit.setDisabled(False)

    def __saveImage(self):
        fileName = QFileDialog.getSaveFileName(
            self, 'Сохранить изображение', 'image.png', 'Изображение (*.png)')

        self.label.pixmap().save(fileName[0])
