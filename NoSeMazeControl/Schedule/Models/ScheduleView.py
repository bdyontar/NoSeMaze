"""
This module contains the model of the table in Schedule Generator UI.
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

from PyQt5 import QtCore, QtGui, QtWidgets


class ScheduleModel(QtCore.QAbstractTableModel):
    """An abstract table model for trials table.
    
    Attributes
    ----------
    headerdata : list
        Header of the table.
    
    arraydata : list
        Data in the table.
    """
    def __init__(self, headerdata : list, arraydata : list, parent : QtWidgets.QWidget = None, *args):
        """
        Parameters
        ----------
        headerdata : list
            Header of the table.

        arraydata : list
            Data of the table.
        
        parent : QtWidgets.QtWidget
        """
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.headerdata : list = headerdata
        self.arraydata : list = arraydata

    def rowCount(self, parent):
        """Return the number of row available.

        Parameters
        ----------
        parent : QWidget
            Not used.
        
        Returns
        -------
        len : int
            Number of row in table.
        """
        return len(self.arraydata)

    def columnCount(self, parent):
        """Return number of column in the table.
        
        Parameters
        ----------
        parent : QWidget
            Not used.
        
        Returns
        -------
        len : int
            Number of columns in the table.
        """
        return len(self.arraydata[0])

    def data(self, index : QtCore.QModelIndex, role : int):
        """Return selected data in the index.
        
        Parameters
        ----------
        index : QModelIndex
            Index of data to be retrieved.
        
        role : int
            Role of data.
        
        Returns
        -------
        data : QVariant
            Data to be retrieved from the index.
        """
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(str(self.arraydata[index.row()][index.column()]))

    def headerData(self, col : int, orientation : int, role : int):
        """Get header data of the table.
        
        Parameters
        ----------
        col : int
            Column index for the table.
        
        orientation : int
            Orientation of the header in the table.
        
        role : int
            Role of data.
        
        Returns
        -------
        header data : QVariant | int
            Header data of current table.
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return int(col)
        return QtCore.QVariant()
