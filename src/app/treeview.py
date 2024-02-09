from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyperclip
import os


class FileIconProvider(QFileIconProvider):
    def icon(self, parameter):

        if isinstance(parameter, QFileInfo):
            info : QFileInfo = parameter
            if info.isDir():
                return QIcon("./src/icons/folder.png")
            if info.suffix() == "py":
                return QIcon("./src/icons/python_icon.png")
            if info.suffix() == "css":
                return QIcon("./src/icons/css.png")
            if info.suffix() == "json":
                return QIcon("./src/icons/json.png")
            if info.suffix() == "js":
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
            copy_action = menu.addAction("Copy")
            paste_action = menu.addAction("Paste")
            cut_action = menu.addAction("Cut")
            copy_path_action = menu.addAction("Copy Path")
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
           
           
            new_file_action.triggered.connect(lambda : self.newfile(ix))
            new_folder_action.triggered.connect(lambda : self.newfolder(ix))
            paste_action.triggered.connect(lambda : self.paste(ix) )
           
           
           
        elif self.Model.fileInfo(ix).isFile():
            
            file_open_action = menu.addAction("Open")
            copy_path_action = menu.addAction("Copy Path")
            file_run_action = menu.addAction("Run")
            copy_action = menu.addAction("Copy")
            cut_action = menu.addAction("Cut")
            open_in_file_manager_action = menu.addAction("Open In File Manager")
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
             
             
            file_open_action.triggered.connect(lambda : self.openfile(ix))
            file_run_action.triggered.connect(lambda : self.runfile(ix))
             
        try:     
            open_in_file_manager_action.triggered.connect(lambda : self.open_in_file_manager(ix))
            copy_action.triggered.connect(lambda : self.copy(ix))
            cut_action.triggered.connect(lambda : self.cut(ix))
            copy_path_action.triggered.connect(lambda : self.copypath(ix))
            rename_action.triggered.connect(lambda : self.rename(ix))
            delete_action.triggered.connect(lambda : self.delete(ix))
        except:
            pass
             
    
        menu.exec_(self.viewport().mapToGlobal(pos))
        
        
    def newfile(self, index):
        _path = self.Model.filePath(index)
    
    def newfolder(self, index):
        _path = self.Model.filePath(index)
    
    def open_in_file_manager(self , index):
        _path = self.Model.filePath(index)
    
    def copy(self, index):
        _path = self.Model.filePath(index)
        
    def paste(self , index):
        pass
    
    def cut(self, index):
        _path = self.Model.filePath(index)
        
    def copypath(self, index):
        _path = self.Model.filePath(index)
        pyperclip.copy(_path)
    
    def rename(self, index):
        _path = self.Model.filePath(index)
    
    def delete(self , index):
        _path = self.Model.filePath(index)
    
    def runfile(self , index):
        _path = self.Model.filePath(index)
    
    def openfile(self, index):
        self.parent().newTab(index)
        
                
                
                