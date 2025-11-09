import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
import cv2
import face_recognition
from database import get_face_encodings, check_login
from logic import recognize_face
from main_menu_gui import MainWindow

class FaceLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.login = None
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Логин фейс айди")
        self.resize(640, 480)

        self.layout = QVBoxLayout()

        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.start_button = QPushButton("Старт захват лица")
        self.start_button.clicked.connect(self.start_recognition)
        self.layout.addWidget(self.start_button)

        self.back_button = QPushButton("Вернутся во вход по паролю")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_recognition(self):
        login, ok = QtWidgets.QInputDialog.getText(self, "Login", "Введите логин")
        if not ok or not login:
            return

        if not check_login(login):
            QMessageBox.warning(self, "Error", "Пользователь не найден")
            return

        encodings = get_face_encodings(login)
        if not encodings:
            QMessageBox.warning(self, "Error", "Лицо не зарегистрировано")
            return

        self.login = login
        self.known_encodings = encodings

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.warning(self, "Error", "Невозможно открыть камеру")
            return

        self.timer.start(5)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

            face_locations = face_recognition.face_locations(rgb_frame)
            if face_locations:
                encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                for encoding in encodings:
                    matches = face_recognition.compare_faces(self.known_encodings, encoding)
                    if True in matches:
                        self.timer.stop()
                        self.cap.release()
                        QMessageBox.information(self, "Success", f"Добро пожаловать, {self.login}!")
                        self.mmenu = MainWindow(self.login)
                        self.mmenu.show()
                        self.close()
                        return

    def go_back(self):
        if self.cap:
            self.cap.release()
        self.timer.stop()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceLoginWindow()
    window.show()
    sys.exit(app.exec())