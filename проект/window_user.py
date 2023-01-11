from PyQt5.Qt import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import datetime
from string import ascii_letters

from table_view import TableView

rus_letters = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
spec_symblos = '!"#$%&\'()*+,-/:;<=>?@[\]^_`{|}~'


class WindowUser(QWidget):
    def __init__(self, name):
        super(WindowUser, self).__init__()
        self.resize(800, 600)

        self.buy_label = QLabel('Покупка билетов', self)
        self.ref_button = QPushButton('Справка', self)
        self.name_label = QLabel(f'Привет, {name}', self)
        self.name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.exit_button = QPushButton('Выход')

        self.start_label = QLabel('Откуда:')
        self.start_line = QLineEdit(self)
        self.route_label = QLabel('Куда:')
        self.route_line = QLineEdit(self)
        self.date_label = QLabel('Дата вылета:', self)
        self.date_line = QLineEdit(self)
        self.count_label = QLabel('Количество билетов', self)
        self.adult_count_line = QLineEdit(self)
        self.children_count_line = QLineEdit(self)
        self.baby_count_line = QLineEdit(self)
        self.search_button = QPushButton('Поиск', self)
        self.clear_button = QPushButton('Очистить', self)
        self.buy_button = QPushButton('Купить', self)

        self.h_user_layout = QHBoxLayout()
        self.h_search_layout = QHBoxLayout()
        self.h_buttons_layout = QHBoxLayout()
        self.h_buy_layout = QHBoxLayout()
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
        self.h_user_layout.addWidget(self.buy_label)
        self.h_user_layout.addWidget(self.ref_button)
        self.h_user_layout.addWidget(self.name_label)
        self.h_user_layout.addWidget(self.exit_button)

        self.h_search_layout.addWidget(self.start_label)
        self.h_search_layout.addWidget(self.start_line)
        self.h_search_layout.addWidget(self.route_label)
        self.h_search_layout.addWidget(self.route_line)
        self.h_search_layout.addWidget(self.date_label)
        self.h_search_layout.addWidget(self.date_line)

        self.h_buttons_layout.addWidget(self.search_button)
        self.h_buttons_layout.addWidget(self.clear_button)
        self.h_buttons_layout.addWidget(self.buy_button)

        self.h_buy_layout.addWidget(self.count_label)
        self.h_buy_layout.addWidget(self.adult_count_line)
        self.h_buy_layout.addWidget(self.children_count_line)
        self.h_buy_layout.addWidget(self.baby_count_line)

        self.v_layout.addLayout(self.h_user_layout)
        self.v_layout.addLayout(self.h_search_layout)
        self.v_layout.addLayout(self.h_buttons_layout)
        self.v_layout.addWidget(self.table)
        self.v_layout.addLayout(self.h_buy_layout)
        self.v_layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.v_layout)

    # Изменение текста в полях
    def lineedit_init(self):
        self.start_line.setPlaceholderText('Москва...')
        self.route_line.setPlaceholderText('Казань...')
        date_obj = datetime.datetime.today().strftime("%d.%m.%Y")
        self.date_line.setPlaceholderText(f'{date_obj}...')

        self.adult_count_line.setPlaceholderText('Взрослые (от 12 лет)...')
        self.adult_count_line.setText('1')
        self.children_count_line.setPlaceholderText('Дети (от 0 до 12 лет)...')
        self.baby_count_line.setPlaceholderText('Младенцы (до 2 лет)...')
        self.buy_button.setEnabled(False)

        self.start_line.textChanged.connect(self.check_input_func)
        self.route_line.textChanged.connect(self.check_input_func)
        self.date_line.textChanged.connect(self.check_date_func)
        self.adult_count_line.textChanged.connect(self.check_count_func)
        self.children_count_line.textChanged.connect(self.check_count_func)
        self.baby_count_line.textChanged.connect(self.check_count_func)

    # Нажатие на кнопку
    def pushbutton_init(self):
        self.ref_button.clicked.connect(self.show_ref_window)
        self.exit_button.clicked.connect(self.exit_func)
        self.search_button.clicked.connect(self.search_func)
        self.clear_button.clicked.connect(self.clear_lines_func)
        self.buy_button.clicked.connect(self.buy_func)

    # Исключение ввода букв и других символов в строки с количеством билетов
    def check_count_func(self):
        if self.adult_count_line.textEdited:
            if len(self.adult_count_line.text()) == 0:
                self.buy_button.setEnabled(False)
                return
            if self.adult_count_line.text()[-1] in ascii_letters + rus_letters + spec_symblos + '.':
                self.adult_count_line.setText(self.adult_count_line.text()[:-1])
                return
            self.buy_button.setEnabled(True)
        if self.children_count_line.textEdited:
            if len(self.children_count_line.text()) == 0:
                return
            if self.children_count_line.text()[-1] in ascii_letters + rus_letters + spec_symblos + '.':
                self.children_count_line.setText(self.children_count_line.text()[:-1])
                return
        if self.baby_count_line.textEdited:
            if len(self.baby_count_line.text()) == 0:
                return
            if self.baby_count_line.text()[-1] in ascii_letters + rus_letters + spec_symblos + '.':
                self.baby_count_line.setText(self.baby_count_line.text()[:-1])
                return

        self.check_input_func()

    # Исключение ввода букв и других символов в строку с датой
    def check_date_func(self):
        if len(self.date_line.text()) == 0:
            return
        if self.date_line.text()[-1] in ascii_letters + rus_letters + spec_symblos:
            self.date_line.setText(self.date_line.text()[:-1])

        self.check_input_func()

    # Блокировка кнопок при наличии пустых текстовых полей
    def check_input_func(self):
        start_lines = [self.start_line.text(), self.route_line.text(), self.date_line.text()]
        if all(start_lines) and self.adult_count_line.text():
            self.buy_button.setEnabled(True)
        else:
            self.buy_button.setEnabled(False)

    # Показ окна справки
    def show_ref_window(self):
        self.refWindow = QMessageBox()
        self.refWindow.setWindowIcon(QtGui.QIcon('info.ico'))
        self.refWindow.setIcon(QMessageBox.Icon.Information)
        self.refWindow.setText('1. Дата должна быть указана в корректном формате, иначе будет вызвано исключение типа "Неверная дата". \n2. Города необходимо вводить на английскои языке, иначе результат показан не будет. ')
        self.refWindow.setWindowTitle('Справка')
        self.refWindow.show()

    # Очистка текстовых полей и окна поиска
    def clear_lines_func(self):
        self.start_line.setText('')
        self.route_line.setText('')
        self.date_line.setText('')

        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Город вылета', 'Город прилёта', 'Дата', 'Количество мест'])
        self.table.setModel(self.model)

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
                    if 1 > int(day) or int(day) > 31:
                        return False
                elif int(month) in [4, 6, 9, 11]:
                    if 1 > int(day) or int(day) > 30:
                        return False
                else:
                    if 1 > int(day) or int(day) > 28:
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
            old_lines = [self.start_line.text(), self.route_line.text(), self.date_line.text()]

            if all(old_lines):
                if not self.check_date_correct(self.date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.start_line.text().title()}' 
                                AND route == '{self.route_line.text().title()}'
                                AND date == '{self.date_line.text()}'""")
            elif old_lines[0] and old_lines[1]:
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.start_line.text().title()}' 
                                AND route == '{self.route_line.text().title()}'""")
            elif old_lines[0] and old_lines[2]:
                if not self.check_date_correct(self.date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.start_line.text().title()}' 
                                AND date == '{self.date_line.text()}'""")
            elif old_lines[1] and old_lines[2]:
                if not self.check_date_correct(self.date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE route == '{self.route_line.text().title()}'
                                AND date == '{self.date_line.text()}'""")
            elif old_lines[0]:
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE start == '{self.start_line.text().title()}'""")
            elif old_lines[1]:
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE route == '{self.route_line.text().title()}'""")
            elif old_lines[2]:
                if not self.check_date_correct(self.date_line.text()):
                    QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                    return
                sql.execute(f"""SELECT * FROM flight_stats 
                                WHERE date == '{self.date_line.text()}'""")
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

    # Выполнение покупки
    def buy_func(self):
        try:
            db = sqlite3.connect('schedule.db')
            sql = db.cursor()
            if not self.check_date_correct(self.date_line.text()):
                QMessageBox.critical(self, 'Ошибка!', 'Неверный формат даты\nСмотрите указания в справке')
                return
            sql.execute(f"""SELECT * FROM flight_stats 
                            WHERE start == '{self.start_line.text().title()}'
                            AND route == '{self.route_line.text().title()}'
                            AND date == '{self.date_line.text()}'""")
            if sql.fetchone() is None:
                QMessageBox.critical(self, 'Ошибка!', 'Данного рейса не существует')
                return
            if not self.children_count_line.text():
                self.children_count_line.setText('0')
            if not self.baby_count_line.text():
                self.baby_count_line.setText('0')
            tickets = int(self.adult_count_line.text()) + int(self.children_count_line.text()) + \
                      int(self.baby_count_line.text())
            sql.execute(f"""SELECT * FROM flight_stats 
                            WHERE start == '{self.start_line.text().title()}'
                            AND route == '{self.route_line.text().title()}'
                            AND date == '{self.date_line.text()}'""")
            places = sql.fetchone()[3]
            if tickets > places:
                QMessageBox.critical(self, 'Ошибка!', 'Недостаточно билетов!')
                return
            with open('ticket.txt', 'w') as file:
                file.writelines(
                    f"""Чек\nОткуда: {self.start_line.text()}\nКуда: {self.route_line.text()}\nДата вылета: {self.date_line.text()}\nОбщее количество билетов: {tickets}\nВзрослые: {self.adult_count_line.text()}\n""")
                if int(self.children_count_line.text()) != 0:
                    file.writelines(f"Дети: {self.children_count_line.text()}\n")
                if int(self.baby_count_line.text()) != 0:
                    file.writelines(f"Младенцы: {self.baby_count_line.text()}")
                QMessageBox.information(self, 'Успешно', 'Покупка совершена!\nИнформация находится в файле ticket.txt')
                sql.execute(f"""UPDATE flight_stats SET places = '{places - tickets}' 
                                WHERE start == '{self.start_line.text().title()}'
                                AND route == '{self.route_line.text().title()}'
                                AND date == '{self.date_line.text()}'""")
                db.commit()

                self.model.clear()
                self.model.setHorizontalHeaderLabels(['Город вылета', 'Город прилёта', 'Дата', 'Свободных мест'])
                self.table.setModel(self.model)
                flight = [self.start_line.text(), self.route_line.text(), self.date_line.text(), places - tickets]
                self.model.appendRow([QtGui.QStandardItem(flight[0]), QtGui.QStandardItem(flight[1]),
                                      QtGui.QStandardItem(flight[2]), QtGui.QStandardItem(str(flight[3]))])
            sql.close()
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка!", f"Ошибка при подключении к sqlite: {error}")
        finally:
            if db:
                db.close()

    # Выход
    def exit_func(self):
        self.close()
