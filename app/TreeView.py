from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

class FileIconProvider(QFileIconProvider):
    def icon(self, parameter):
  
        if isinstance(parameter, QFileInfo):
            info = parameter
            if info.isDir():
              return QIcon("./icons/folder.png")
            if parameter.suffix() == "py":
              return QIcon("./icons/py.png")
            if parameter.suffix() == "css":
              return QIcon("./icons/css.png")
            if parameter.suffix() == "json":
              return QIcon("./icons/json.png")
            if parameter.suffix() == "js":
              return QIcon("./icons/py.js")
              
                
        return super(FileIconProvider, self).icon(parameter)
class FileManager(QTreeView):
  def __init__(self ,  parent=None):
    super().__init__(parent)
    
    
    self.setStyleSheet(open("./style/treeview.css" ,"r").read())
    self.Model = QFileSystemModel()
    self.Model.setIconProvider(FileIconProvider())
    self.Model.setRootPath(os.getcwd())
    
    
    self.setModel(self.Model)
    
    self.setRootIndex(self.Model.index(os.getcwd()))
    self.setIndentation(20)
    self.setAnimated(True)
    self.setDragEnabled(True)
    self.setHeaderHidden(True)
    self.setColumnHidden(1,True)
    self.setColumnHidden(2,True)
    self.setColumnHidden(3,True)
    self.setDragDropMode(QAbstractItemView.InternalMove)
    
    
      
    