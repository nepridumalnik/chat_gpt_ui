from .completion import OpenAICompletion
from .image_generation import OpenAIImageGeneration

from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtGui import QFont


class OpenAIApi(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle('OpenAI')
        self.setMinimumSize(600, 480)
        self.resize(1280, 800)

        font: QFont = QFont("Times", 16)
        self.setFont(font)

        self.__setupTabs()

    def __setupTabs(self) -> None:
        self.tabWidget: QTabWidget = QTabWidget(self)

        self.tabWidget.addTab(OpenAICompletion(self), 'Автодополнение')
        self.tabWidget.addTab(OpenAIImageGeneration(self),
                              'Генерация картинки')

    def resizeEvent(self, event):
        self.tabWidget.setFixedSize(self.size())
