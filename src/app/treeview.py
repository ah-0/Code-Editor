from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os


class FileIconProvider(QFileIconProvider):
    def icon(self, parameter):

        if isinstance(parameter, QFileInfo):
            info = parameter
            if info.isDir():
                return QIcon("./src/icons/folder.png")
            if parameter.suffix() == "py":
                return QIcon("./src/icons/python_icon.png")
            if parameter.suffix() == "css":
                return QIcon("./src/icons/css.png")
            if parameter.suffix() == "json":
                return QIcon("./src/icons/json.png")
            if parameter.suffix() == "js":
                return QIcon("./src/icons/py.js")

        return super(FileIconProvider, self).icon(parameter)


class FileManager(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(open("./src/style/treeview.css", "r").read())
        self.Model = QFileSystemModel()
        self.Model.setIconProvider(FileIconProvider())
        self.Model.setRootPath(os.getcwd())

        self.setModel(self.Model)

        self.setRootIndex(self.Model.index(os.getcwd()))

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QTreeView.SelectRows)
        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.setIndentation(20)
        self.setAnimated(True)

        self.setHeaderHidden(True)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)

    def show_context_menu(self, pos: QPoint):
        ix = self.indexAt(pos)
        menu =  QMenu()
        
        if self.Model.isDir(ix):
           new_file_action = menu.addAction("New File")
           new_folder_action = menu.addAction("New Folder")
           open_in_file_manager_action = menu.addAction("Open In File Manager")
           folder_copy_action = menu.addAction("Copy")
           folder_cut_action = menu.addAction("Cut")
           folder_copy_path_action = menu.addAction("Copy Path")
           folder_rename_action = menu.addAction("Rename")
           folder_delete_action = menu.addAction("Delete")
           
        elif self.Model.fileInfo(ix).isFile():
             file_open_action = menu.addAction("Open")
             file_copy_path_action = menu.addAction("Copy Path")
             file_run_action = menu.addAction("Run")
             file_copy_action = menu.addAction("Copy")
             file_cut_action = menu.addAction("Cut")
             open_in_file_manager_action = menu.addAction("Open In File Manager")
             file_rename_action = menu.addAction("Rename")
             file_delete_action = menu.addAction("Delete")
             
    
        action = menu.exec_(self.viewport().mapToGlobal(pos))
    