#This file describe how data is presented to GUI
from PySide import QtCore

class EntityListItem(QtCore.QObject):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity

    def __str__(self):
        return str(self.entity)

    def get_entity(self):
        return self.entity
    

class EntityListModel(QtCore.QAbstractListModel):
    
    def __init__(self):
        super().__init__()
        self.entities_list = []

    def rowCount(self, index = QtCore.QModelIndex()):
        return len(self.entities_list)

    def data(self, index, role):
        if index.isValid()  and role == QtCore.Qt.DisplayRole :
            return str(self.entities_list[index.row()])

    def addElem(self, entity):
        print("adding elem", str(entity))
        self.beginInsertRows(QtCore.QModelIndex(), len(self.entities_list)\
                , len(self.entities_list))
        self.entities_list.append(EntityListItem(entity))
        self.endInsertRows()

    def get_entity(self, index):
        if index.isValid():
            return self.entities_list[index.row()].get_entity()

class MvtListItem(QtCore.QObject):
    def __init__(self, mvt):
        super().__init__()
        self.mvt = mvt

    def __str__(self):
        return str(self.mvt)
 

class MvtListModel(QtCore.QAbstractListModel):
    
    def __init__(self):
        super().__init__()
        self.mvts_list = []

    def rowCount(self, index = QtCore.QModelIndex()):
        return len(self.mvts_list)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole :
            return str(self.mvts_list[index.row()])

    def addElem(self, mvt):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.mvts_list)\
                , len(self.mvts_list))
        self.mvts_list.append(MvtListItem(mvt))
        self.endInsertRows()


