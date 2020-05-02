"""
@Description:
This module has the aim to construct a QTableView  who'll be insert into mainWindow.
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"


from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QAbstractTableModel, Qt
import ctypes


myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class ModelShaft(QAbstractTableModel):
    """ This class'll embed the pandas DataFrame object.
    """

    def __init__(self, data: dict):
        """:parameter data: table DataFrame type."""
        QAbstractTableModel.__init__(self)
        self._data = data
        self._keys = self._data.keys()


    def rowCount(self, parent=None):
        """:return int"""
        return len(list(self._data.values())[0])

    def columnCount(self, parnet=None):
        """:return int"""
        return len(self._data.keys())

    def data(self, index, role=Qt.DisplayRole):
        """
        :parameter index: table's index
        :parameter role: basically that'll quantify the data type.
        """
        item = self._data[list(self._data.keys())[index.column()]][index.row()]
        if role == QtCore.Qt.BackgroundRole:
            if index.row() % 2 and not(index.column() == 1 and (index.row() == 13 or index.row() == 15)):
                return QtCore.QVariant(QtGui.QColor("#E9E9E9"))
            elif index.row() % 2 and (index.column() == 1 and (index.row() == 13 or index.row() == 15)):
                if isinstance(item, float):
                    if float(item) >= 1 and (index.row() == 15 or index.row() == 13):
                        return QtGui.QBrush(Qt.green)
                    else:
                        return QtGui.QBrush(Qt.red)

            else:
                if not(index.column() == 4 or index.column() == 5):
                    return QtCore.QVariant(QtGui.QColor(QtCore.Qt.gray))
                else:
                    if isinstance(item, float):
                        if float(item) >= 1 and (index.column() == 4 or index.column() == 5):
                            return QtGui.QBrush(Qt.darkGreen)
                        else:
                            return QtGui.QBrush(Qt.darkRed)
        if not index.isValid():
            return QtCore.QVariant(item)
        elif role == Qt.DisplayRole and index.column() != 1:
            return str(item)
        elif role == Qt.DisplayRole and index.column() == 1:
            try:
                item = '{:.4f}'.format(float(self._data[list(self._data.keys())[index.column()]][index.row()]))
                return str(item)
            except TypeError:
                item = self._data[list(self._data.keys())[index.column()]][index.row()]
                return item
        return QtCore.QVariant()

    def headerData(self, p_int, Qt_Orientation, role):
        """:return None"""
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return list(self._data.keys())[p_int]
        return None
