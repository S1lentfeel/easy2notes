import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMenuBar, QMainWindow
from main_menu_gui import MainWindow
from database import add_new_user, check_login, login_user, check_email, update_password
from logic import detect_lang
from face_login_gui import FaceLoginWindow

class RegisterMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.login_window = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("RegisterDialog")
        self.resize(560, 520) 
        self.setWindowTitle("Регистрация")

        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setGeometry(QtCore.QRect(0, 20, 560, 51))
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24pt; font-weight: 600;")
        self.title_label.setText("Регистрация")

        self.input_login = QtWidgets.QLineEdit(self)
        self.input_login.setGeometry(QtCore.QRect(120, 100, 321, 41))
        self.input_login.setPlaceholderText("Введите новый логин")

        self.email = QtWidgets.QLineEdit(self)
        self.email.setGeometry(QtCore.QRect(120, 170, 321, 41))
        self.email.setPlaceholderText("Введите вашу почту")

        self.input_password = QtWidgets.QLineEdit(self)
        self.input_password.setGeometry(QtCore.QRect(120, 240, 321, 41))
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Введите пароль")

        self.input_password_confirm = QtWidgets.QLineEdit(self)
        self.input_password_confirm.setGeometry(QtCore.QRect(120, 310, 321, 41))
        self.input_password_confirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password_confirm.setPlaceholderText("Подтвердите пароль")

        self.register_button = QtWidgets.QPushButton(self)
        self.register_button.setGeometry(QtCore.QRect(190, 390, 161, 51))
        self.register_button.setText("Зарегистрироваться")
        self.register_button.clicked.connect(self.attempt_registration)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(190, 450, 161, 31))
        self.back_button.setText("Назад ко входу")
        self.back_button.clicked.connect(self.go_back_to_login)

    def attempt_registration(self):
        login = self.input_login.text()
        password = self.input_password.text()
        email = self.email.text()
        
        if not login or not password or not email:
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "Кажется, какое-то из полей не заполнено."
            )
            return   

        elif "@" not in email or "." not in email:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Кажется вы указали неправильный email"
            )

        elif detect_lang(login) == "ru":
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "ЛОГИН должен быть написан на английском языке."
            )
            return
        
        elif detect_lang(password) == "ru":
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "ПАРОЛЬ должен быть написан на английском языке."
            )
            return

        elif not login or not password:
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "Логин и пароль не могут быть пустыми."
            )
            return

        elif password != self.input_password_confirm.text():
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "Пароли не совпадают."
            )
            return
        
        elif check_login(login):
            QMessageBox.warning(
                self,
                "Ошибка регистрации",
                f"Пользователь с логином '{login}' уже существует. Попробуйте другой."
            )
        else:
            add_new_user(login, password, email)
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
        self.resize(560, 430)

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

        self.face_login_button = QtWidgets.QPushButton(self)
        self.face_login_button.setGeometry(QtCore.QRect(190, 340, 161, 31))
        self.face_login_button.setText("Войти по Face ID")
        self.face_login_button.clicked.connect(self.open_face_login)

        self.forgot_password_button = QtWidgets.QPushButton(self)
        self.forgot_password_button.setGeometry(QtCore.QRect(190, 380, 161, 31))
        self.forgot_password_button.setText("Восстановить пароль")
        self.forgot_password_button.clicked.connect(self.open_forgot_password_window)

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

    def open_face_login(self):
        self.face_window = FaceLoginWindow()
        self.face_window.show()
        self.close()

    def open_forgot_password_window(self):
        self.forgot_password_window = ForgotPasswordWindow()
        self.forgot_password_window.show()
        self.close()

    def go_to_main_menu(self):
        self.mmenu = MainWindow(username=self.active_user)
        self.mmenu.show()
        self.close()


class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ForgotPasswordWindow")
        self.resize(400, 200)
        self.setWindowTitle("Восстановление пароля")

        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setGeometry(QtCore.QRect(0, 20, 400, 31))
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: 600;")
        self.title_label.setText("Введите вашу почту")

        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setGeometry(QtCore.QRect(40, 70, 321, 41))
        self.email_input.setPlaceholderText("example@example.com")

        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.setGeometry(QtCore.QRect(120, 130, 161, 41))
        self.submit_button.setText("Подтвердить")
        self.submit_button.clicked.connect(self.check_email)

    def check_email(self):
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Ошибка", "Поле не может быть пустым.")
            return

        if check_email(email):
            self.reset_password_window = ResetPasswordWindow(email)
            self.reset_password_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с такой почтой не найден.")


class ResetPasswordWindow(QWidget):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ResetPasswordWindow")
        self.resize(400, 300)
        self.setWindowTitle("Сброс пароля")

        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setGeometry(QtCore.QRect(0, 20, 400, 31))
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: 600;")
        self.title_label.setText("Введите новый пароль")

        self.new_password_input = QtWidgets.QLineEdit(self)
        self.new_password_input.setGeometry(QtCore.QRect(40, 70, 321, 41))
        self.new_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Новый пароль")

        self.confirm_password_input = QtWidgets.QLineEdit(self)
        self.confirm_password_input.setGeometry(QtCore.QRect(40, 130, 321, 41))
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")

        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.setGeometry(QtCore.QRect(120, 200, 161, 41))
        self.submit_button.setText("Сбросить пароль")
        self.submit_button.clicked.connect(self.reset_password)

    def reset_password(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароль не может быть пустым.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return
        
        if detect_lang(new_password) == "ru":
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "ПАРОЛЬ должен быть написан на английском языке."
            )
            return

        update_password(self.email, new_password)
        QMessageBox.information(self, "Успех", "Пароль успешно изменен.")
        self.login_window = LoginMenu()
        self.login_window.show()
        self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginMenu()
    window.show()
    sys.exit(app.exec())