from PyQt5.QtCore import *
from PyQt5.Qsci import *
from jedi import Script
from jedi.api import Completion
import re
import os


class ToolTip(QThread):
    def __init__(self, parent=None ,path=""):
        super(ToolTip, self).__init__(None)
        
        self.parent = parent
        self.script: Script = None
        self.api: QsciAPIs = api
        self.completions: list[Completion] = None
        self.path = path
        

        self.line = 0
        self.index = 0
        self.text = ""

    def run(self):
        try:
            QToolTip.hideText()
            self.script = Script(self.text, path=self.path)
            self.get_info = self.script.infer(self.line, self.index)
            
            pos = self.parent.SendScintilla(SCI_GETCURRENTPOS)
            x = self.parent.SendScintilla(SCI_POINTXFROMPOSITION ,0 , pos)
            y = self.parent.SendScintilla(SCI_POINTYFROMPOSITION ,0 , pos)
            
            global_pos = self.parent.mapToGlobal(QPoint(x , y))
            
            for i in self.get_info:
                QToolTip.showText(global_pos,i.docstring())
            
            
        except Exception as err:
            print(err)

        self.finished.emit() 



    def start_threading(self, line: int, index: int, text: str):
        self.line = line
        self.index = index
        self.text = text
        self.start()


        