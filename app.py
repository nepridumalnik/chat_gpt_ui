if '__main__' == __name__:
    from openai_widgets import OpenAIApi
    from PyQt5.QtWidgets import QApplication

    app: QApplication = QApplication([])
    api: OpenAIApi = OpenAIApi()

    api.show()

    exit(app.exec())
