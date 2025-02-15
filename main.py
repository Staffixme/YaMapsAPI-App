import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
import requests


# Задача 5
class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.static_apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        self.geocode_apikey = "8013b162-6b42-4997-9691-77b7074026e0"
        loadUi("main_window.ui", self)
        self.go_button.clicked.connect(lambda: self.update_map(float(self.line_x.text()),
                                                               float(self.line_y.text()),
                                                               int(self.line_z.text())))

        self.dark_theme.clicked.connect(lambda: self.update_map(self.x, self.y, self.z))

        self.search_button.clicked.connect(lambda: self.find_place(self.lineEdit.text()))

        self.z = None
        self.x = None
        self.y = None

        self.update_map(32, 32, 3)

    def find_place(self, text):
        try:
            address = "+".join(text.split())
            link = f"https://geocode-maps.yandex.ru/1.x/?apikey={self.geocode_apikey}&geocode={address}&format=json"
            print(link)
            result = requests.get(link)
            content = result.json()
            status = result.status_code
            if status == 200:
                pos = content["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
                position = [float(i) for i in pos.split()]
                self.update_map(*position, 10)
            else:
                print(status, "Что-то пошло не так:", result.reason)
        except Exception as e:
            print("Получено исключение:", e)

    def update_map(self, x, y, size):
        try:
            self.x, self.y, self.z = x, y, size
            if self.dark_theme.isChecked():
                mode = "dark"
            else:
                mode = "light"

            link = (f"https://static-maps.yandex.ru/v1?lang=ru_RU&ll={x},{y}"
                    f"&z={size}&theme={mode}&apikey={self.static_apikey}")
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

    def keyPressEvent(self, event):
        self.line_z.clearFocus()
        if event.key() == Qt.Key.Key_PageUp:
            if self.z is not None:
                self.z = min(self.z + 1, 21)
                print('Увеличиваем масштаб')
                self.update_map(self.x, self.y, self.z)
        elif event.key() == Qt.Key.Key_PageDown:
            if self.z is not None:
                self.z = max(self.z - 1, 1)
                print('Уменьшаем масштаб')
                self.update_map(self.x, self.y, self.z)

        elif event.key() == Qt.Key.Key_Up:
            if self.y is not None:
                self.y = min(self.y + 10, 90)
                print('Перемещяем вверх')
                self.update_map(self.x, self.y, self.z)
        elif event.key() == Qt.Key.Key_Down:
            if self.y is not None:
                self.y = max(self.y - 10, -90)
                print('Перемещяем вниз')
                self.update_map(self.x, self.y, self.z)
        elif event.key() == Qt.Key.Key_Left:
            if self.x is not None:
                self.x = max(self.x - 10, -180)
                print('Перемещяем влево')
                self.update_map(self.x, self.y, self.z)
        elif event.key() == Qt.Key.Key_Right:
            if self.x is not None:
                self.x = min(self.x + 10, 180)
                print('Перемещяем вправо')
                self.update_map(self.x, self.y, self.z)

        elif event.key() in (Qt.Key.Key_Enter, 16777220):
            print("Поиск места")
            self.find_place(self.lineEdit.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
