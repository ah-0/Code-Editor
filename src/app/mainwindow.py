from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from codeeditor.pythoneditor import PythonEditor
from codeeditor.htmleditor import HtmlEditor
from codeeditor.csseditor import CssEditor
from codeeditor.jsoneditor import JsonEditor
from treeview import FileManager
from tabwidget import TabWidget
from PyQt5.Qsci import QsciScintilla
import pathlib
import qdarkstyle
import json
import sys
import os


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.init_menubar()

        self.layoutv = QVBoxLayout()

        self.spliter = QSplitter()
        self.spliter.setStyleSheet("""
        QSplitter {
        
            background-color: #161B21;
        
        }
        
        QSplitter::handle {
            background-color: #161B21;
        }
        
        
        """)
        self.spliter.setContentsMargins(0, 0, 0, 0)
        self.spliter.setOrientation(Qt.Horizontal)

        

        self.tabwidget = TabWidget(self)
        self.treeview = FileManager(self.tabwidget)
        self.openEvnt_()

        self.spliter.addWidget(self.treeview)
        self.spliter.addWidget(self.tabwidget)

        self.layoutv.addWidget(self.spliter)
        self.layoutv.setContentsMargins(0, 0, 0, 0)

        self.centerw = QWidget()
        self.centerw.setLayout(self.layoutv)

        self.setCentralWidget(self.centerw)

        self.treeview.clicked.connect(self.newTab)
        self.tabwidget.currentChanged.connect(self._tab_widget_current_change)
        
    def _tab_widget_current_change(self, index):
        current_tab_path = self.tabwidget.widget(index).path
        file_index = self.treeview.Model.index(current_tab_path)
        self.treeview.setCurrentIndex(file_index)

    def newTab(self, ix):
        index = self.treeview.proxy.mapToSource(ix)
        path = self.treeview.Model.filePath(index)
        name = self.treeview.Model.fileName(index)
        if os.path.isfile(path):

            for i in range(self.tabwidget.count()):
                if self.tabwidget.tabText(i) == name:
                    self.tabwidget.setCurrentIndex(i)
                    return
            if pathlib.Path(path).suffix == ".py":
                editor = PythonEditor(path, self)

                with open(path, "r") as f:
                    editor.setText(f.read())
                self.tabwidget.addTab(editor, QIcon("./src/icons/py.png"), name)

                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)

            elif pathlib.Path(path).suffix == ".html":
                editor = HtmlEditor(path,self)
                with open(path, "r") as f:
                    editor.setText(f.read())
                self.tabwidget.addTab(editor, QIcon("./src/icons/py.png"), name)
                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)

            elif pathlib.Path(path).suffix == ".css":
                editor = CssEditor(path,self)
                with open(path, "r") as f:
                    editor.setText(f.read())
                self.tabwidget.addTab(editor, QIcon("./src/icons/css.png"), name)
                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)

            elif pathlib.Path(path).suffix == ".json":
                editor = JsonEditor(path,self)
                with open(path, "r") as f:
                    editor.setText(f.read())
                self.tabwidget.addTab(editor, QIcon("./src/icons/json.png"), name)
                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)

    def init_menubar(self):

        self.menubar2 = self.menuBar()
        self.menubar2.setStyleSheet("""
        QMenuBar{
            background-color: 161B21;
        }
        QMenuBar::item{
            padding: 10px;
            
            
            padding-right: 20px;
        }
        QMenu{
            min-width : 300px;
        }
        
        """)

        filemenu = self.menubar2.addMenu("&File")
        editmenu = self.menubar2.addMenu("Edit")
  
        viewmenu = self.menubar2.addMenu("View")
        toolsmenu = self.menubar2.addMenu("Tools")
        gomenu = self.menubar2.addMenu("Go")
        Terminalmneu = self.menubar2.addMenu("Terminal")
        filemenu.addAction("&New Project")
        open_project_action = filemenu.addAction("&Open Project")
        filemenu.addAction("&Rename Project")
        filemenu.addAction("&Save as")
        filemenu.addAction("&Exit")
        
        open_project_action.triggered.connect(self.open_project)
        
    def open_project(self):
        dialog = QFileDialog.getExistingDirectory(self , "Open a folder ","" ,options= QFileDialog.Options())
        
        if dialog:
            parent_dir = os.path.abspath(os.path.join(dialog, os.pardir))
            self.treeview.Model.setRootPath(dialog)
            self.treeview.setRootIndex(self.treeview.proxy.mapFromSource(self.treeview.Model.index(parent_dir)))
            
            for i in range(self.tabwidget.count()):
                self.tabwidget.removeTab(i)
        
        
    def openEvnt_(self):
        setting_file_path = "./src/setting/App.json"
        with open(setting_file_path , "r") as f:
            setting = json.load(f)
            
            if setting["Last-Project"] != "":
                parent_dir = os.path.abspath(os.path.join(setting["Last-Project"], os.pardir))
                self.treeview.Model.setRootPath(setting["Last-Project"])
                
                
                self.treeview.setRootIndex(self.treeview.proxy.mapFromSource(self.treeview.Model.index(parent_dir)))
                
                if setting["List-Of-Opened-Tabs-Paths"]:
                    for i in setting["List-Of-Opened-Tabs-Paths"]:
                        with open(i , "r") as rr:
                            editor = PythonEditor(i , self)
                            editor.setText(rr.read())
                            self.tabwidget.addTab(editor , os.path.basename(i))
                            
                    self.tabwidget.setCurrentIndex(setting["Current-Tab-Number"])
                    
                    self.tabwidget.widget(setting["Current-Tab-Number"]).SendScintilla(QsciScintilla.SCI_SCROLLTOSTART)

                            
        
        
    def closeEvent(self,event):
        setting_file_path = "./src/setting/App.json"
        with open(setting_file_path , "r") as f:
            setting = json.load(f)
            
            setting["Last-Project"] = self.treeview.Model.rootPath()
            
            _path_list = []
            for i in range(self.tabwidget.count()):
                path = self.tabwidget.widget(i).path
                _path_list.append(path)
               
            setting["List-Of-Opened-Tabs-Paths"] = _path_list
            if self.tabwidget.count() > 0:
                setting["Current-Tab-Number"] = self.tabwidget.currentIndex()
                
            current_file_index = self treeview.currentIndex()
            current_file_path = self.treeview.Model.filePath(current_file_path)
            
            setting["File-Manager-Current-File"] = current_file_path
                
            
              
        init_setting = json.dumps(setting , indent=4)
        
        with open(setting_file_path, "w") as fr:
            fr.write(init_setting)
            
                
        
        
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())
