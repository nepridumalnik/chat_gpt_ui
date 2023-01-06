from .open_ai_settings import oaiSettings

from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

import threading


class OpenAICompletion(QWidget):
    insertTextSignal: pyqtSignal = pyqtSignal([str])

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.input: QPlainTextEdit = QPlainTextEdit(self)
        self.output: QPlainTextEdit = QPlainTextEdit(self)
        self.submit: QPushButton = QPushButton('Выполнить', self)

        self.output.setReadOnly(True)

        vBoxLayout: QVBoxLayout = QVBoxLayout(self)
        hBoxLayout: QHBoxLayout = QHBoxLayout()

        vBoxLayout.addLayout(hBoxLayout)
        vBoxLayout.addWidget(self.submit)
        vBoxLayout.setAlignment(self.submit, Qt.AlignLeft)

        hBoxLayout.addWidget(self.input)
        hBoxLayout.addWidget(self.output)

        self.submit.clicked.connect(self.__onSubmitClicked)
        self.insertTextSignal.connect(self.output.setPlainText)

    def __onSubmitClicked(self) -> None:
        t = threading.Thread(target=self.__getCompletion)
        t.daemon = True
        t.start()

    def __getCompletion(self) -> None:
        prompt: str = self.input.toPlainText()
        if not prompt:
            return

        try:
            self.submit.setDisabled(True)

            respond: str = oaiSettings.makeCompletion(prompt=prompt)

            self.insertTextSignal.emit(f'Ответ:\n{respond}')
        finally:
            self.submit.setDisabled(False)
