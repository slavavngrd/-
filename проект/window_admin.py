from PyQt5.Qt import *
from PyQt5 import QtGui
import sqlite3
import datetime
from string import ascii_letters

from table_view import TableView

rus_letters = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
spec_symblos = '!"#$%&\'()*+,-/:;<=>?@[\]^_`{|}~'


class WindowAdmin(QWidget):
    def __init__(self, name):
        super(WindowAdmin, self).__init__()
        self.resize(800, 600)

        self.mode_drop_box = QComboBox()
        self.mode_drop_box.addItem('Регистрация рейсов')
        self.mode_drop_box.addItem('Изменение текущей информации')
        self.mode_drop_box.addItem('Удаление рейсов')
        self.ref_button = QPushButton('Справка', self)
        self.name_label = QLabel(f'Привет, {name}', self)
        self.name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.exit_button = QPushButton('Выход')
        self.search_button = QPushButton('Поиск', self)
        self.clear_button = QPushButton('Очистить', self)
        self.execute_button = QPushButton('Выполнить', self)

        self.old_start_label = QLabel('Откуда:')
        self.old_start_line = QLineEdit(self)
        self.old_route_label = QLabel('Куда:')
        self.old_route_line = QLineEdit(self)
        self.old_date_label = QLabel('Дата вылета:', self)
        self.old_date_line = QLineEdit(self)

        self.after_label = QLabel('Изменить на')
        self.after_label.setAlignment(Qt.AlignHCenter)
        self.new_start_label = QLabel('Откуда:')
        self.new_start_line = QLineEdit(self)
        self.new_route_label = QLabel('Куда:')
        self.new_route_line = QLineEdit(self)
        self.new_date_label = QLabel('Дата вылета:', self)
        self.new_date_line = QLineEdit(self)

        self.h_user_layout = QHBoxLayout()
        self.h_old_layout = QHBoxLayout()
        self.h_new_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.table = TableView()
        self.v_layout = QVBoxLayout()

        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['Город вылета', 'Город прилёта', 'Дата', 'Количество мест'])
        self.table.setModel(self.model)

        self.layout_init()
        self.lineedit_init()
        self.pushbutton_init()

    # GUI
    def layout_init(self):
        self.h_user_layout.addWidget(self.mode_drop_box)
        self.h_user_layout.addWidget(self.ref_button)
        self.h_user_layout.addWidget(self.name_label)
        self.h_user_layout.addWidget(self.exit_button)

        self.h_old_layout.addWidget(self.old_start_label)
        self.h_old_layout.addWidget(self.old_start_line)
        self.h_old_layout.addWidget(self.old_route_label)
        self.h_old_layout.addWidget(self.old_route_line)
        self.h_old_layout.addWidget(self.old_date_label)
        self.h_old_layout.addWidget(self.old_date_line)

        self.h_new_layout.addWidget(self.new_start_label)
        self.h_new_layout.addWidget(self.new_start_line)
        self.h_new_layout.addWidget(self.new_route_label)
        self.h_new_layout.addWidget(self.new_route_line)
        self.h_new_layout.addWidget(self.new_date_label)
        self.h_new_layout.addWidget(self.new_date_line)

        self.buttons_layout.addWidget(self.search_button)
        self.buttons_layout.addWidget(self.clear_button)
        self.buttons_layout.addWidget(self.execute_button)

        self.v_layout.addLayout(self.h_user_layout)
        self.v_layout.addLayout(self.h_old_layout)
        self.v_layout.addWidget(self.after_label)
        self.v_layout.addLayout(self.h_new_layout)
        self.v_layout.addLayout(self.buttons_layout)
        self.v_layout.addWidget(self.table)
        self.v_layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.v_layout)

    # Изменение текста в полях
    def lineedit_init(self):
        self.new_start_line.setEnabled(False)
        self.new_route_line.setEnabled(False)
        self.new_date_line.setEnabled(False)
        self.execute_button.setEnabled(False)

        self.old_start_line.textChanged.connect(self.check_input_func)
        self.old_route_line.textChanged.connect(self.check_input_func)
        self.old_date_line.textChanged.connect(self.check_date_func)
        self.new_start_line.textChanged.connect(self.check_input_func)
        self.new_route_line.textChanged.connect(self.check_input_func)
        self.new_date_line.textChanged.connect(self.check_date_func)
        self.mode_drop_box.currentTextChanged.connect(self.change_mode_drop_box)

    # Нажатие на кнопку
    def pushbutton_init(self):
        self.ref_button.clicked.connect(self.show_ref_window)
        self.exit_button.clicked.connect(self.exit_func)
        self.search_button.clicked.connect(self.search_func)
        self.clear_button.clicked.connect(self.clear_lines_func)
        self.execute_button.clicked.connect(self.execute_func)

    # Изменение режима
    def change_mode_drop_box(self):
        if self.mode_drop_box.currentText() == 'Изменение текущей информации':
            self.new_start_line.setEnabled(True)
            self.new_route_line.setEnabled(True)
            self.new_date_line.setEnabled(True)
        else:
            self.new_start_line.setText('')
            self.new_route_line.setText('')
            self.new_date_line.setText('')
            self.new_start_line.setEnabled(False)
            self.new_route_line.setEnabled(False)
            self.new_date_line.setEnabled(False)
        self.check_input_func()

    # Исключение ввода букв и других символов
    def check_date_func(self):
        if len(self.old_date_line.text()) == 0:
            return
        if self.old_date_line.text()[-1] in ascii_letters + rus_letters + spec_symblos:
            self.old_date_line.setText(self.old_date_line.text()[:-1])

        if self.new_date_line.isEnabled() and len(self.new_date_line.text()) == 0:
            return
        if self.new_date_line.isEnabled() and self.new_date_line.text()[-1] \
                in ascii_letters + rus_letters + spec_symblos:
            self.new_date_line.setText(self.new_date_line.text()[:-1])
        self.check_input_func()

    # Блокировка кнопок при наличии пустых текстовых полей
    def check_input_func(self):
        self.execute_button.setEnabled(False)
        old_lines = [self.old_start_line.text(), self.old_route_line.text(), self.old_date_line.text()]
        new_lines = [self.new_start_line.text(), self.new_route_line.text(), self.new_date_line.text()]

        if all(old_lines):
            if self.mode_drop_box.currentText() == 'Изменение текущей информации':
                self.new_start_line.setEnabled(True)
                self.new_route_line.setEnabled(True)
                self.new_date_line.setEnabled(True)
                if all(new_lines):
                    self.execute_button.setEnabled(True)
            else:
                self.new_start_line.setEnabled(False)
                self.new_route_line.setEnabled(False)
                self.new_date_line.setEnabled(False)
                self.search_button.setEnabled(True)
                self.execute_button.setEnabled(True)

    # Показ окна справки
    def show_ref_window(self):
        self.refWindow = QMessageBox()
        self.refWindow.setWindowIcon(QtGui.QIcon('info.ico'))
        self.refWindow.setIcon(QMessageBox.Icon.Information)
        self.refWindow.setText('1. Необходимо вводить данные полностью, не оставляя пустых полей. \n2. Дата в формате: ДД.ММ.ГГГГ, корректное количество дней в каждом месяце, месяцев максимальное число - 12, меньше чем 2022 год ставить запрещено')
        self.refWindow.setWindowTitle('Справка')
        self.refWindow.show()

    # Очистка текстовых полей и окна поиска
    def clear_lines_func(self):
        self.old_start_line.setText('')
        self.old_route_line.setText('')
        self.old_date_line.setText('')
        self.new_start_line.setText('')
        self.new_route_line.setText('')
        self.new_date_line.setText('')

        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Город вылета', 'Город прилёта', 'Дата', 'Количество мест'])
        self.table.setModel(self.model)

    # Проверка даты на корректность ввода
    @staticmethod
    def check_date_correct(date):
        if len(date) < 10 or '.' in [date[0], date[1], date[3], date[4], date[6], date[7], date[8], date[9]]:
            return False
        if len(date) == 10 and date[2] == '.' and date[5] == '.':
            day, month, year = date.split('.')
            if int(month) < 1 or int(month) > 12:
                return False
            else:
                if int(month) in [1, 3, 5, 7, 8, 10, 12]:
                    if 1 > int(day) and int(day) > 31:
                        return False
                elif int(month) in [4, 6, 9, 11]:
                    if 1 > int(day) and int(day) > 30:
                        return False
                else:
                    if 1 > int(day) and int(day) > 28:
                        return False
            date_obj = datetime.datetime.strptime(f"{year}-{month}-{day} {datetime.datetime.today().time()}",
                                                  '%Y-%m-%d %H:%M:%S.%f')
            if date_obj.date() < datetime.datetime.now().date():
                return False
            else:
                return True
        else:
            return False

    # Выполнение поиска
    def search_func(self):
        try:
            db = sqlite3.connect('schedule.db')
            sql = db.cursor()
            old_lines = [self.old_start_line.text(), self.old_route_line.text(), self.old_date_line.text()]

            if all(old_lines):
                if not self.check_date_correct(self.old_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.old_start_line.text().title()}' 
                                AND route == '{self.old_route_line.text().title()}'
                                AND date == '{self.old_date_line.text()}'""")
            elif old_lines[0] and old_lines[1]:
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.old_start_line.text().title()}' 
                                AND route == '{self.old_route_line.text().title()}'""")
            elif old_lines[0] and old_lines[2]:
                if not self.check_date_correct(self.old_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.old_start_line.text().title()}' 
                                AND date == '{self.old_date_line.text()}'""")
            elif old_lines[1] and old_lines[2]:
                if not self.check_date_correct(self.old_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE route == '{self.old_route_line.text().title()}'
                                AND date == '{self.old_date_line.text()}'""")
            elif old_lines[0]:
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.old_start_line.text().title()}'""")
            elif old_lines[1]:
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE route == '{self.old_route_line.text().title()}'""")
            elif old_lines[2]:
                if not self.check_date_correct(self.old_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE date == '{self.old_date_line.text()}'""")
            else:
                sql.execute(f"""SELECT * FROM flight_stats""")

            self.model.clear()
            self.model.setHorizontalHeaderLabels(['Город вылета', 'Город прилёта', 'Дата', 'Свободных мест'])
            self.table.setModel(self.model)
            for flight in sql.fetchall():
                self.model.appendRow(
                    [QtGui.QStandardItem(flight[0]), QtGui.QStandardItem(flight[1]),
                     QtGui.QStandardItem(flight[2]), QtGui.QStandardItem(str(flight[3]))])
        except sqlite3.Error as error:
            QMessageBox.critical(self, 'Ошибка!', f"Ошибка при подключении к sqlite: {error}")
        finally:
            if db:
                db.close()

    # Выполнение запроса
    def execute_func(self):
        try:
            db = sqlite3.connect('schedule.db')
            sql = db.cursor()

            if self.mode_drop_box.currentText() == 'Регистрация рейсов':
                if not self.check_date_correct(self.old_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"INSERT INTO flight_stats VALUES (?, ?, ?, ?)", (
                    self.old_start_line.text().title(),
                    self.old_route_line.text().title(),
                    self.old_date_line.text(),
                    200))
                db.commit()
                QMessageBox.information(self, 'Успешно', 'Рейс добавлен')

            elif self.mode_drop_box.currentText() == 'Удаление рейсов':
                if not self.check_date_correct(self.old_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT start, route, date FROM flight_stats 
                WHERE start == '{self.old_start_line.text().title()}' 
                AND route == '{self.old_route_line.text().title()}' 
                AND date == '{self.old_date_line.text()}'""")
                if sql.fetchone() is None:
                    QMessageBox.critical(self, 'Ошибка!', 'Данный рейс отсутствует!')
                else:
                    sql.execute(f"""DELETE FROM flight_stats
                    WHERE start == '{self.old_start_line.text().title()}' 
                    AND route == '{self.old_route_line.text().title()}' 
                    AND date == '{self.old_date_line.text()}'""")
                    db.commit()
                    QMessageBox.information(self, 'Успешно', 'Рейс удалён!')
            elif self.mode_drop_box.currentText() == 'Изменение текущей информации':
                if not self.check_date_correct(self.old_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                if not self.check_date_correct(self.new_date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT start, route, date FROM flight_stats 
                                WHERE start == '{self.old_start_line.text().title()}' 
                                AND route == '{self.old_route_line.text().title()}' 
                                AND date == '{self.old_date_line.text()}'""")
                if sql.fetchone() is None:
                    QMessageBox.critical(self, 'Ошибка!', 'Изменяемый рейс отсутствует!')
                else:
                    sql.execute(f"""UPDATE flight_stats
                                    SET start = '{self.new_start_line.text().title()}',
                                    route = '{self.new_route_line.text().title()}',
                                    date = '{self.new_date_line.text()}'
                                    WHERE start == '{self.old_start_line.text().title()}' 
                                    AND route == '{self.old_route_line.text().title()}' 
                                    AND date == '{self.old_date_line.text()}'""")
                    db.commit()
                    QMessageBox.information(self, 'Успешно', 'Рейс изменён!')
            sql.close()
        except sqlite3.Error as error:
            QMessageBox.critical(self, 'Ошибка!', f"Ошибка при подключении к sqlite: {error}")
        finally:
            if db:
                db.close()

    # Выход
    def exit_func(self):
        self.close()
