if '__main__' == __name__:
    from oai_ui import OpenAIApi
    from PyQt5.QtWidgets import QApplication

    app: QApplication = QApplication([])
    api: OpenAIApi = OpenAIApi()

    api.show()

    exit(app.exec())
