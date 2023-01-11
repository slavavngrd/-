import sys
from PyQt5 import QtGui
from PyQt5.Qt import *
import sqlite3

from signing_page import SigningPage
from window_admin import WindowAdmin
from window_user import WindowUser


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()

        self.user_label = QLabel('Имя пользователя:', self)
        self.pwd_label = QLabel('Пароль:', self)
        self.user_line = QLineEdit(self)
        self.user_line.setClearButtonEnabled(True)
        self.pwd_line = QLineEdit(self)
        self.pwd_line.setClearButtonEnabled(True)
        self.login_button = QPushButton('Войти', self)
        self.signing_button = QPushButton('Зарегистрироваться', self)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()
        self.signing_page = SigningPage()

    # Изменение текста в полях
    def lineedit_init(self):
        self.user_line.setPlaceholderText('Пожалуйста, введите ваше имя')
        self.pwd_line.setPlaceholderText('Пожалуйста, введите ваш пароль')
        self.pwd_line.setEchoMode(QLineEdit.Password)

        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)

    # Нажатие на кнопку
    def pushbutton_init(self):
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.check_login_func)
        self.signing_button.clicked.connect(self.show_signing_page_func)

    # GUI
    def layout_init(self):
        self.grid_layout.addWidget(self.user_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.user_line, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.pwd_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.pwd_line, 1, 1, 1, 1)
        self.h_layout.addWidget(self.login_button)
        self.h_layout.addWidget(self.signing_button)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    # Авторизация
    def check_login_func(self):
        try:
            db = sqlite3.connect('schedule.db')
            sql = db.cursor()
            sql.execute(f"SELECT user, pwd FROM user_pwd WHERE user == '{self.user_line.text()}'")
            result = sql.fetchone()
            if result is None:
                QMessageBox.critical(self, 'Ошибка!', 'Неверное имя пользователя или пароль!')
                self.user_line.setText('')
                self.pwd_line.setText('')
                return
            else:
                if result[1] != self.pwd_line.text():
                    QMessageBox.critical(self, 'Ошибка!', 'Неверное имя пользователя или пароль!')
                    self.user_line.setText('')
                    self.pwd_line.setText('')
                    return
                user = self.user_line.text()
                if user == 'admin':
                    self.windowAdmin = WindowAdmin(user)
                    self.windowAdmin.setWindowTitle("Admin Config")
                    self.windowAdmin.setWindowIcon(QtGui.QIcon("settings.ico"))
                    self.windowAdmin.show()
                else:
                    self.windowUser = WindowUser(user)
                    self.windowUser.setWindowTitle("A&A Airlines")
                    self.windowUser.setWindowIcon(QtGui.QIcon("logo.ico"))
                    self.windowUser.show()

                self.user_line.setText('')
                self.pwd_line.setText('')
                # self.close()
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка!", f"Ошибка при подключении к sqlite: {error}")
        finally:
            if db:
                db.close()

    # Показ окна регистрации
    def show_signing_page_func(self):
        self.signing_page = SigningPage()
        self.signing_page.setWindowTitle("Registration")
        self.signing_page.setWindowIcon(QtGui.QIcon("settings.ico"))
        self.signing_page.show()

    # Блокировка кнопки при наличии пустых текстовых полей
    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text():
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Login()
    w.setWindowTitle("A&A Airlines")
    w.resize(640, 200)
    w.setWindowIcon(QtGui.QIcon("logo.ico"))
    w.show()
    sys.exit(app.exec_())
