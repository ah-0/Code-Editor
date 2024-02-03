from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.app.Editors.PythonEditor import Python_Editor
from src.app.Editors.HtmlEditor import Html_Editor
from src.app.Editors.CssEditor import Css_Editor
from src.app.TreeView import FileManager
from src.app.TabWidget import TabWidget
import pathlib
import qdarkstyle
import sys 
import os


class MyApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    self.appmenus()
    
    self.layoutv = QVBoxLayout()
    
    
    self.spliter = QSplitter()
    self.spliter.setStyleSheet(open("./src/style/splitter.css" , "r").read())
    self.spliter.setContentsMargins(0,0,0,0)
    self.spliter.setOrientation(Qt.Horizontal)
    
    self.treeview = FileManager(self)
    
    self.tabwidget = TabWidget(self)
    
    self.spliter.addWidget(self.treeview)
    self.spliter.addWidget(self.tabwidget)
    
    
    self.layoutv.addWidget(self.spliter)
    self.layoutv.setContentsMargins(0, 0, 0, 0)
    
    self.centerw = QWidget()
    self.centerw.setLayout(self.layoutv)
    
    
    self.setCentralWidget(self.centerw)
    
    self.treeview.clicked.connect(self.newTab)
    
  
    
  def newTab(self, index):
    path = self.treeview.Model.filePath(index)
    name = self.treeview.Model.fileName(index)
    if os.path.isfile(path):
      
      for i in range(self.tabwidget.count()):
        if self.tabwidget.tabText(i) == name:
          self.tabwidget.setCurrentIndex(i)
          return
      if pathlib.Path(path).suffix == ".py":
        editor = Python_Editor( path,self)
               
        with open(path , "r") as f:
          editor.setText(f.read())
        self.tabwidget.addTab(editor,QIcon("./src/icons/py.png"), name)
      
      
        self.tabwidget.setCurrentIndex(self.tabwidget.count()-1)
     
     
      elif pathlib.Path(path).suffix == ".html":
        editor = Html_Editor(self)
        with open(path , "r") as f:
          editor.setText(f.read())
        self.tabwidget.addTab(editor,QIcon("./src/icons/py.png"), name)
        self.tabwidget.setCurrentIndex(self.tabwidget.count()-1)
        
        
      elif pathlib.Path(path).suffix == ".css":
        editor = Css_Editor(self)
        with open(path , "r") as f:
          editor.setText(f.read())
        self.tabwidget.addTab(editor,QIcon("./src/icons/css.png"), name)
        self.tabwidget.setCurrentIndex(self.tabwidget.count()-1)
        
        

  


  def appmenus(self):
        
    self.menubar2 = self.menuBar()
    self.menubar2.setStyleSheet(open("./src/style/menubar.css" , "r").read())

    
    filemenu = self.menubar2.addMenu("&File")
    editmenu = self.menubar2.addMenu("Edit")
    selectionmenu = self.menubar2.addMenu("Selection")
    viewmenu = self.menubar2.addMenu("View")
    toolsmenu =self.menubar2.addMenu("Tools")
    gomenu =self.menubar2.addMenu("Go")
    Terminalmneu =self.menubar2.addMenu("Terminal")
    filemenu.addAction("&new File                                     ")

  

        
    

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MyApp()
  window.showMaximized()
  sys.exit(app.exec_())
