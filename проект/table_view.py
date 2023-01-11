from PyQt5 import QtWidgets


class TableView(QtWidgets.QTableView):
    def __init__(self):
        super(TableView, self).__init__()
        self.setSortingEnabled(True)
