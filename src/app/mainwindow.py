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

        self.resize(600,600)
        css_ = """
        QSplitter {
            background-color: #161B21;
        }
        
        QSplitter::handle {
            background-color: #161B21;
        }
        
        QMenuBar{
            background-color: #161B21;
        }
        
        QMenuBar::item{
            padding: 10px;
            padding-right: 15px;
        }
        
        QMenu:item{
            min-width : 250px;
            height: 26px;
            background-color: #2c2d30;
        }

        QTabBar::tab::selected {
            color: #d3d3d3;
            border-style: none;
            background-color: #2d2d2d;
            border-bottom: 3px solid cornflowerblue;
        }
        
        """
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5() + css_)

        self.init_menubar()

        self.layoutv = QVBoxLayout()

        self.spliter = QSplitter()
        
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
        if self.tabwidget.count() > 0:
            current_tab_path = self.tabwidget.widget(index).path
            file_index = self.treeview.Model.index(current_tab_path)
            file_index = self.treeview.proxy.mapFromSource(file_index)
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
            with open(path, "r") as f:
                file_text = f.read()
            if pathlib.Path(path).suffix == ".py":
                editor = PythonEditor(path, self)
                editor.setText(file_text)
                self.tabwidget.addTab(editor, QIcon("./src/icons/python_icon.png"), name)
                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)
                

            elif pathlib.Path(path).suffix == ".html":
                editor = HtmlEditor(path,self)
                editor.setText(file_text)
                self.tabwidget.addTab(editor, QIcon("./src/icons/py.png"), name)
                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)
                

            elif pathlib.Path(path).suffix == ".css":
                editor = CssEditor(path,self)
                editor.setText(file_text)
                self.tabwidget.addTab(editor, QIcon("./src/icons/css.png"), name)
                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)
                

            elif pathlib.Path(path).suffix == ".json":
                editor = JsonEditor(path,self)
                editor.setText(file_text)
                self.tabwidget.addTab(editor, QIcon("./src/icons/json.png"), name)
                self.tabwidget.setCurrentIndex(self.tabwidget.count() - 1)

    def init_menubar(self):

        self.menubar_ = self.menuBar()

        file_menu = self.menubar_.addMenu("&File")
        edit_menu = self.menubar_.addMenu("Edit")
        view_menu = self.menubar_.addMenu("View")
        run_menu = self.menubar_.addMenu("Run")
        tools_menu = self.menubar_.addMenu("Tools")
        github_menu = self.menubar_.addMenu("GitHub")
        Terminal_menu = self.menubar_.addMenu("Terminal")
        
        new_project_action = file_menu.addAction("&New Project")
        
        open_project_action = file_menu.addAction("&Open Project")
        open_project_action.setShortcut("Ctrl+K")
        open_project_action.triggered.connect(self.open_project)
        
        
        sava_as_action = file_menu.addAction("&Save as")
        
        setting_action = file_menu.addAction("Setting")
        
        exit_action = file_menu.addAction("&Exit")
        
        
        
    def open_project(self):
        dialog = QFileDialog.getExistingDirectory(self , "Open a folder ","" ,options= QFileDialog.Options())
        
        if dialog:
            parent_dir = os.path.abspath(os.path.join(dialog, os.pardir))
            self.treeview.Model.setRootPath(dialog)
            self.treeview.proxy.setIndexPath(QPersistentModelIndex(self.treeview.Model.index(dialog)))
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
                self.treeview.proxy.setIndexPath(QPersistentModelIndex(self.treeview.Model.index(setting["Last-Project"]))
                self.treeview.setRootIndex(self.treeview.proxy.mapFromSource(self.treeview.Model.index(parent_dir)))
                
                if setting["List-Of-Tab-Paths"]:
                    for i in setting["List-Of-Tab-Paths"]:
                        with open(i , "r") as rr:
                            if pathlib.Path(i).suffix == ".py":
                                editor = PythonEditor(i , self)
                                editor.setText(rr.read())
                                self.tabwidget.addTab(editor,QIcon("./src/icons/python_icon.png") , os.path.basename(i))
                            elif pathlib.Path(i).suffix == ".html":
                                editor = HtmlEditor(i,self)
                                editor.setText(rr.read())
                                self.tabwidget.addTab(editor, QIcon("./src/icons/py.png"), os.path.basename(i))
                            elif pathlib.Path(i).suffix == ".css":
                                editor = CssEditor(i,self)
                                editor.setText(rr.read())
                                self.tabwidget.addTab(editor, QIcon("./src/icons/css.png"), os.path.basename(i))
                    
                    
                    
                            
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
               
            setting["List-Of-Tab-Paths"] = _path_list
            if self.tabwidget.count() > 0:
                setting["Current-Tab-Number"] = self.tabwidget.currentIndex()
        
            
            
                
            
              
        init_setting = json.dumps(setting , indent=4)
        
        with open(setting_file_path, "w") as fr:
            fr.write(init_setting)
            
                
        
        
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())
