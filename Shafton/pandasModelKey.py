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
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ctypes


myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class PandasModelKey(QAbstractTableModel):
    """ This class'll embed the pandas DataFrame object.
    """

    def __init__(self, data, shaft_safety_factor=2.5):
        """:parameter data: table DataFrame type."""
        QAbstractTableModel.__init__(self)
        self._data = data
        self._keys = self._data.columns
        self.shaftSafetyFactor = shaft_safety_factor

    def rowCount(self, parent=None):
        """:return int"""
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        """:return int"""
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        """
        :parameter index: table's index
        :parameter role: basically that'll quantify the data type.
        """
        item = self._data.iloc[index.row(), index.column()]
        if not index.isValid():
            return QtCore.QVariant(item)

        if role == QtCore.Qt.DisplayRole:
            if index.column() != 0 and index.column() != 3 and index.column() != 4 and index.column() != 5:
                item = '{:.3f}'.format(self._data.iloc[index.row(), index.column()])
                return str(item)
            elif index.column() == 0:
                item = '{:.1f}'.format(self._data.iloc[index.row(), index.column()])
                return str(item)
            else:
                item = '{:.2f}'.format(self._data.iloc[index.row(), index.column()])
                return str(item)

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

        if role == QtCore.Qt.TextColorRole:
            return QtCore.QVariant(QtGui.QColor(QtCore.Qt.black))

        if role == QtCore.Qt.BackgroundRole:
            if index.row() % 2 and not(index.column() == 4 or index.column() == 5):
                return QtCore.QVariant(QtGui.QColor("#E9E9E9"))
            elif index.row() % 2 and (index.column() == 4 or index.column() == 5):
                if isinstance(item, float):
                    if self.shaftSafetyFactor > float(item):
                        if float(item) >= 1 and (index.column() == 4 or index.column() == 5):
                            return QtGui.QBrush(Qt.green)
                        else:
                            return QtGui.QBrush(Qt.red)
                    else:
                        if float(item) >= 1 and (index.column() == 4 or index.column() == 5):
                            return QtGui.QBrush(QtGui.QColor(255, 255, 0))
                        else:
                            return QtGui.QBrush(Qt.red)

            else:
                if not(index.column() == 4 or index.column() == 5):
                    return QtCore.QVariant(QtGui.QColor(QtCore.Qt.gray))
                else:
                    if isinstance(item, float):
                        if self.shaftSafetyFactor > float(item):
                            if float(item) >= 1 and (index.column() == 4 or index.column() == 5):
                                return QtGui.QBrush(Qt.darkGreen)
                            else:
                                return QtGui.QBrush(Qt.darkRed)
                        else:
                            if float(item) >= 1 and (index.column() == 4 or index.column() == 5):
                                return QtGui.QBrush(QtGui.QColor(255, 230, 0))
                            else:
                                return QtGui.QBrush(Qt.darkRed)


        return QtCore.QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """

        :param section: the coordinates
        :param orientation: the orientation
        :param role: The type of role
        :return: None
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self._data.columns[section])
        else:
            return QtCore.QVariant()
