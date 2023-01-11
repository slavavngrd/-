import sqlite3

from PyQt5.Qt import *


class SigningPage(QWidget):
    def __init__(self):
        super(SigningPage, self).__init__()
        self.signing_user_label = QLabel('Имя пользователя:')
        self.signing_pwd_label = QLabel('Введите пароль:')
        self.signing_pwd2_label = QLabel('Повторите пароль:')
        self.signing_user_line = QLineEdit()
        self.signing_pwd_line = QLineEdit()
        self.signing_pwd2_line = QLineEdit()
        self.signing_button = QPushButton('Зарегистрироваться')

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    # Изменение текста в полях
    def lineedit_init(self):
        self.signing_pwd_line.setEchoMode(QLineEdit.Password)
        self.signing_pwd2_line.setEchoMode(QLineEdit.Password)

        self.signing_user_line.textChanged.connect(self.check_input_func)
        self.signing_pwd_line.textChanged.connect(self.check_input_func)
        self.signing_pwd2_line.textChanged.connect(self.check_input_func)

    # Нажатие на кнопку
    def pushbutton_init(self):
        self.signing_button.setEnabled(False)
        self.signing_button.clicked.connect(self.check_signing_func)

    # GUI
    def layout_init(self):
        self.user_h_layout.addWidget(self.signing_user_label)
        self.user_h_layout.addWidget(self.signing_user_line)
        self.pwd_h_layout.addWidget(self.signing_pwd_label)
        self.pwd_h_layout.addWidget(self.signing_pwd_line)
        self.pwd2_h_layout.addWidget(self.signing_pwd2_label)
        self.pwd2_h_layout.addWidget(self.signing_pwd2_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addWidget(self.signing_button)

        self.setLayout(self.all_v_layout)

    # Блокировка кнопки при наличии пустых текстовых полей
    def check_input_func(self):
        if self.signing_user_line.text() and \
                self.signing_pwd_line.text() and \
                self.signing_pwd2_line.text():
            self.signing_button.setEnabled(True)
        else:
            self.signing_button.setEnabled(False)

    # Процесс регистрации
    def check_signing_func(self):
        try:
            db = sqlite3.connect('schedule.db')
            sql = db.cursor()
            if self.signing_pwd_line.text() != self.signing_pwd2_line.text():
                QMessageBox.critical(self, 'Ошибка!', 'Пароли не совпадают!')
                self.signing_pwd_line.setText('')
                self.signing_pwd2_line.setText('')
                return
            sql.execute(f"SELECT user FROM user_pwd WHERE user == '{self.signing_user_line.text()}'")
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO user_pwd VALUES (?, ?)",
                            (self.signing_user_line.text(), self.signing_pwd_line.text()))
                db.commit()
                QMessageBox.information(self, 'Успешно', 'Пользователь зарегистрирован!')
                self.close()
            else:
                QMessageBox.critical(self, 'Ошибка!', 'Пользователь с таким именем уже зарегистрирован!')
        except sqlite3.Error as error:
            QMessageBox.critical(self, 'Ошибка!', f'Ошибка при подключении к sqlite: {error}')
        finally:
            if db:
                db.close()

        self.signing_user_line.clear()
        self.signing_pwd_line.clear()
        self.signing_pwd2_line.clear()
