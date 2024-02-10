from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path
import subprocess
import pyperclip
import shutil
import sys
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
                return QIcon("./src/icons/js.png")
            if info.suffix() == "java":
                return QIcon("./src/icons/...")
            if info.suffix() == "cpp":
                return QIcon("./src/icons/...")
            if info.suffix() == "c":
                return QIcon("./src/icons/...")  
            if info.suffix() == "png" or info.suffix() == "jpg":
                return QIcon("./src/icons/...")
            if info.suffix() == "c#":
                return QIcon("./src/icons/...")  
                
              
                

        return super(FileIconProvider, self).icon(parameter)


class FileManager(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        with open("./src/style/treeview.css" , "r") as f:
            self.setStyleSheet(f.read())

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
        
        _name, ok = QInputDialog.getText(self, 'Create file', 'Enter the file name:')
        if ok:
            f = Path(_path) / _name
            count = 1
            while f.exists():
                f = Path(f.parent / f"{_name}{count}")
                count += 1
            f.touch()
            
                    
    
    def newfolder(self, index):
        _path = self.Model.filePath(index)
        
        _name, ok = QInputDialog.getText(self, 'Create folder', 'Enter the folder name:')
        if ok:
            f = Path(_path) / _name
            count = 1
            while f.exists():
                f = Path(f.parent / f"{_name}{count}")
                count += 1
            self.Model.mkdir(index , f.name)
            
        
    
    def open_in_file_manager(self , index):
        _path = os.path.abspath(self.model.filePath(index))
        is_dir = self.model.isDir(index)
        if os.name == "nt":
            # Windows
            if is_dir:
                subprocess.Popen(f'explorer "{_path}"')
            else:
                subprocess.Popen(f'explorer /select,"{_path}"')
        elif os.name == "posix":
            # Linux or Mac OS
            if sys.platform == "darwin":
                # macOS
                if is_dir:
                    subprocess.Popen(["open", _path])
                else:
                    subprocess.Popen(["open", "-R", _path])
            else:
                # Linux
                subprocess.Popen(["xdg-open", os.path.dirname(_path)])
        else:
            raise OSError(f"Unsupported platform {os.name}")

    # drag and drop functionality
    
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
        _oldname = self.Model.fileName(index)
        newname , ok = QInputDialog.getText(self, 'Rename', 'Enter the new name:')
        
        if ok:
            new_path = _path.split("/")[:-1]
            new_path = new_path + [newname]
            new_path = "/".join(new_path)
            os.rename(_path, new_path)
            
            _tabwidget = self.parent().tabwidget()
            for i in range(_tabwidget.count()):
                if _tabwidget.tabText(i) == _oldname:
                    _tabwidget.setTabText(i, newname)
                    
                    _tabwidget.widget(i).path = new_path
                
        
    
    def delete(self , index):
        if self.selectionModel().selectedRows():
            for i in self.selectionModel().selectedRows():
                if self.Model.isDir(i):
                    self.rmdir(i)
                else:
                    self.remove(i)
                    _tabwidget = self.parent().tabwidget()
                    for n in range(_tabwidget.count()):
                        if _tabwidget.tabText(n) == self.Model.fileName(i):
                            _tabwidget.removeTab(n)
                
        
        
            
    def runfile(self , index):
        _path = self.Model.filePath(index)
    
    def openfile(self, index):
        self.parent().newTab(index)
        