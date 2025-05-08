import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from qr_code_generator.qr_code_generator import QRCodeGenerator


class MainWindow(QMainWindow):
    features = {
        "qr-code-generator": {
            "name": "QR Code Generator",
            "class": QRCodeGenerator,
            "window": None,
        }
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Useful Python Tools")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.qr_code_btn = QPushButton(MainWindow.features["qr-code-generator"]["name"])
        self.qr_code_btn.clicked.connect(
            lambda _: self.launch_widget("qr-code-generator")
        )
        layout.addWidget(self.qr_code_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def launch_widget(self, feature: str):
        if MainWindow.features[feature]["window"] is None:
            new_window = self.features[feature]["class"]()
            new_window.show()
            MainWindow.features[feature]["window"] = new_window
        MainWindow.features[feature]["window"].show()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
app.exec()
