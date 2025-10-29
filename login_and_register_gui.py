import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMenuBar, QMainWindow
from main_menu_gui import MainWindow
from database import add_new_user, check_login, login_user


class RegisterMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.login_window = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("RegisterDialog")
        self.resize(560, 450)
        self.setWindowTitle("Регистрация")

        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setGeometry(QtCore.QRect(0, 20, 560, 51))
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24pt; font-weight: 600;")
        self.title_label.setText("Регистрация")

        self.input_login = QtWidgets.QLineEdit(self)
        self.input_login.setGeometry(QtCore.QRect(120, 100, 321, 41))
        self.input_login.setPlaceholderText("Введите новый логин")

        self.input_password = QtWidgets.QLineEdit(self)
        self.input_password.setGeometry(QtCore.QRect(120, 170, 321, 41))
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Введите пароль")

        self.input_password_confirm = QtWidgets.QLineEdit(self)
        self.input_password_confirm.setGeometry(QtCore.QRect(120, 240, 321, 41))
        self.input_password_confirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password_confirm.setPlaceholderText("Подтвердите пароль")

        self.register_button = QtWidgets.QPushButton(self)
        self.register_button.setGeometry(QtCore.QRect(190, 320, 161, 51))
        self.register_button.setText("Зарегистрироваться")
        self.register_button.clicked.connect(self.attempt_registration)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(190, 380, 161, 31))
        self.back_button.setText("Назад ко входу")
        self.back_button.clicked.connect(self.go_back_to_login)

    def attempt_registration(self):
        login = self.input_login.text()
        password = self.input_password.text()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми.")
            return

        if password != self.input_password_confirm.text():
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return
        
        if check_login(login):
            QMessageBox.warning(
                self,
                "Ошибка регистрации",
                f"Пользователь с логином '{login}' уже существует. Попробуйте другой."
            )
        else:
            add_new_user(login, password)
            QMessageBox.information(self, "Успех", "Вы успешно зарегистрированы! Теперь можете войти.")
            self.go_back_to_login()

    def go_back_to_login(self):
        self.login_window = LoginMenu()
        self.login_window.show()
        self.close()


class LoginMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.register_window = None
        self.main_app_window = None 
        self.active_user = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(560, 350)

        self.text_login = QtWidgets.QLabel(self)
        self.text_login.setGeometry(QtCore.QRect(0, 10, 560, 51))
        self.text_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_login.setStyleSheet("font-size:22pt; font-weight:600;")
        self.text_login.setText("Логин")

        self.input_login = QtWidgets.QLineEdit(self)
        self.input_login.setGeometry(QtCore.QRect(120, 70, 321, 41))
        self.input_login.setPlaceholderText("Введите ваш логин")

        self.text_password = QtWidgets.QLabel(self)
        self.text_password.setGeometry(QtCore.QRect(0, 120, 560, 51))
        self.text_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_password.setStyleSheet("font-size:22pt; font-weight:600;")
        self.text_password.setText("Пароль")

        self.input_password = QtWidgets.QLineEdit(self)
        self.input_password.setGeometry(QtCore.QRect(120, 180, 321, 41))
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Введите ваш пароль")

        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setGeometry(QtCore.QRect(190, 240, 161, 51))
        self.login_button.setText("Войти")
        self.login_button.clicked.connect(self.attempt_login)

        self.goto_register_button = QtWidgets.QPushButton(self)
        self.goto_register_button.setGeometry(QtCore.QRect(190, 300, 161, 31))
        self.goto_register_button.setText("Зарегистрироваться")
        self.goto_register_button.clicked.connect(self.open_register_window)
        
        self.setWindowTitle("Вход")

    def attempt_login(self):
        login = self.input_login.text()
        password = self.input_password.text()

        if not check_login(login):
            QMessageBox.warning(
                self,
                'Пользователь не найден',
                f"Пользователь '{login}' не найден. Проверьте логин или зарегистрируйтесь."
            )
        else:
            if login_user(login, password):
                QMessageBox.information(self, "Успех", f"Добро пожаловать, {login}!")
                self.active_user = login
                self.go_to_main_menu()
            else:
                QMessageBox.warning(self, "Ошибка входа", "Неверный пароль.")   

    def open_register_window(self):
        self.register_window = RegisterMenu()
        self.register_window.show()
        self.close()

    def go_to_main_menu(self):
        self.mmenu = MainWindow(username=self.active_user) 
        self.mmenu.show()
        self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginMenu()
    window.show()
    sys.exit(app.exec())