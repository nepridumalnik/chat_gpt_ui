from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt

import threading
import openai
import os


API_KEY: str = os.environ['OPENAI_API_KEY']

openai.api_key = API_KEY


class OpenAICompletion(QWidget):
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

    def __onSubmitClicked(self) -> None:
        t = threading.Thread(target=self.__getCompletion)
        t.daemon = True
        t.start()

    def __getCompletion(self) -> None:
        prompts: str = self.input.toPlainText()
        if not prompts:
            return

        try:
            self.submit.setDisabled(True)

            completion = openai.Completion.create(
                engine="text-davinci-003", prompt=prompts, max_tokens=2000)

            respond: str = completion.choices[0].text

            self.output.setPlainText(f'Ответ:\n{respond}')
        finally:
            self.submit.setDisabled(False)
