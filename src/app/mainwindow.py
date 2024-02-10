from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from codeeditor.pythoneditor import PythonEditor
from codeeditor.htmleditor import HtmlEditor
from codeeditor.csseditor import CssEditor
from codeeditor.jsoneditor import JsonEditor
from treeview import FileManager
from tabwidget import TabWidget
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

    def appmenus(self):

        self.menubar2 = self.menuBar()
        self.menubar2.setStyleSheet("""
        QMenuBar{
            background-color: 161B21;
        }
        QMenuBar::item{
            padding: 10px;
            
            
            padding-right: 20px;
        }
        
        """)

        filemenu = self.menubar2.addMenu("&File")
        editmenu = self.menubar2.addMenu("Edit")
        selectionmenu = self.menubar2.addMenu("Selection")
        viewmenu = self.menubar2.addMenu("View")
        toolsmenu = self.menubar2.addMenu("Tools")
        gomenu = self.menubar2.addMenu("Go")
        Terminalmneu = self.menubar2.addMenu("Terminal")
        filemenu.addAction("&new File                                     ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())
