from pathlib import Path

import qrcode

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QMenu,
    QFileDialog,
    QApplication,
)
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt
from PIL.ImageQt import ImageQt, Image


def generate_qr_code(data: str):
    qr = qrcode.main.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.original_pil_image = None  # original pil image, good for saving
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def set_image(self, pixmap, original_pil_image):
        self.setPixmap(pixmap)
        self.original_pil_image = original_pil_image

    def show_context_menu(self, position):
        if self.pixmap() and not self.pixmap().isNull():
            menu = QMenu()

            save_action = QAction("Save QR Code", self)
            save_action.triggered.connect(self.save_image)
            menu.addAction(save_action)

            copy_action = QAction("Copy to Clipboard", self)
            copy_action.triggered.connect(self.copy_to_clipboard)
            menu.addAction(copy_action)

            menu.exec(self.mapToGlobal(position))

    def save_image(self):
        file_path = None
        if self.original_pil_image:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save QR Code",
                str(Path.home() / "Pictures"),
                "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
            )

        if file_path:
            # get what format to save image as
            file_format = Path(file_path).suffix
            # if no format was picked, default to png
            if not file_format:
                file_format = ".png"

            if file_format.lower() == ".jpg" or file_format.lower() == ".jpeg":
                # convert to rgb is image is rgba
                if self.original_pil_image.mode == "RGBA":
                    rgb_image = Image.new(
                        "RGB", self.original_pil_image.size, (255, 255, 255)
                    )
                    rgb_image.paste(
                        self.original_pil_image, mask=self.original_pil_image.split()[3]
                    )
                    rgb_image.save(file_path, "JPEG")
                else:
                    self.original_pil_image.save(file_path, "JPEG")
            else:
                self.original_pil_image.save(file_path)

    def copy_to_clipboard(self):
        if self.pixmap() and not self.pixmap().isNull():
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(self.pixmap())

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Paste Link Here")
        input_layout.addWidget(self.text_input)

        generate_btn = QPushButton("Generate")
        generate_btn.clicked.connect(self.generate_btn_handler)
        input_layout.addWidget(generate_btn)

        self.image_display = ImageLabel()
        self.image_display.setFixedSize(400, 400)
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.image_display)
        self.setLayout(main_layout)

    def generate_btn_handler(self):
        pil_image = generate_qr_code(self.text_input.text())
        pil_image = pil_image.get_image()
        qt_image = ImageQt(pil_image)
        pixmap = QPixmap.fromImage(qt_image)
        pixmap = pixmap.scaled(
            400,
            400,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_display.set_image(pixmap, pil_image)
