"""
This module contains the model of the table shown in controller UI.
"""
"""
Copyright (c) 2019, 2022 [copyright holders here]

This file is part of NoSeMaze.

NoSeMaze is free software: you can redistribute it and/or 
modify it under the terms of GNU General Public License as 
published by the Free Software Foundation, either version 3 
of the License, or (at your option) at any later version.

NoSeMaze is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public 
License along with NoSeMaze. If not, see https://www.gnu.org/licenses.
"""

from typing import Any
from collections import deque
from PyQt5 import QtCore, QtGui


class TableModel(QtCore.QAbstractTableModel):
    """Abstract model used for trial results table shown in the MainApp.

    Attributes
    ----------
    headerdata : list
        Header of the table.
    
    arraydata : deque
        Data of the table.
    """
    def __init__(self, headerdata : list, arraydata : deque, parent=None, *args):
        """
        """
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.headerdata : list = headerdata
        self.arraydata : deque = arraydata

    def rowCount(self, parent:Any):
        """Return the number of rows in the table.

        Parameters
        ----------
        parent : Any
            Not in used.
        
        Returns
        -------
        len : int
            Number of row availables.
        """
        return len(self.arraydata)

    def columnCount(self, parent:Any):
        """Return the number of column in a row.

        Parameters
        ----------
        parent : Any
            Not in used.
        
        Returns
        -------
        len : int
            Number of column availables.
        """
        return len(self.arraydata[0])

    def data(self, index : QtCore.QModelIndex, role : int):
        """Get data on index.
        
        Parameters
        ----------
        index : QtCore.QModelIndex
            Index of data to be retreived.
        
        role : int
            Role of data.
        
        Returns
        -------
        data : QtCore.QVariant
            Data retrieved from index.row() and index.column()

        """
        if not index.isValid():
            return QtCore.QVariant()
        # TODO - Specific case for main table, colouring true / false correct, doesn't work for animal table
        # elif role == QtCore.Qt.BackgroundRole:
        #     row = index.row()
        #     if self.arraydata[row][6]:
        #         return QtGui.QBrush(QtCore.Qt.green)
        #     else:
        #         return QtGui.QBrush(QtCore.Qt.red)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(str(self.arraydata[index.row()][index.column()]))

    def headerData(self, col, orientation : int, role : int):
        """Get header data.
        
        Parameters
        ----------
        col : int
            Selected column.
        
        orientation : int
            Orientation of the header.
        
        role : int
            Role of header.

        Returns
        -------
        header : QtCoreVariant | int
            Header of the data.

        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return int(col)
        return QtCore.QVariant()
