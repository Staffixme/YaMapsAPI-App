import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
import requests


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        loadUi("main_window.ui", self)
        self.search_button.clicked.connect(lambda: self.update_map(float(self.line_x.text()),
                                                                   float(self.line_y.text()),
                                                                   int(self.line_z.text())))

        self.update_map(5, 5, 12)

    def update_map(self, x, y, size):
        try:
            link = (f"https://static-maps.yandex.ru/v1?lang=ru_RU&ll={x},{y}"
                    f"&z={size}&apikey={self.apikey}")
            print(self.line_x.text(), self.line_y.text(), self.line_z.text())
            result = requests.get(link)
            content = result.content
            status = result.status_code
            if status == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(content)
                self.map.setPixmap(pixmap)
            else:
                print(status, "Что-то пошло не так: ", result.reason)
        except Exception as e:
            print("Получено исключение:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
