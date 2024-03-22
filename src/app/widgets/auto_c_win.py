from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path
from jedi import Script
from jedi.api import Completion
from jedi import settings
import re
import os

class AutoC(QThread):
    def __init__(self, api ,path):
        super(AutoC, self).__init__(None)

        self.script: Script = None
        self.api: QListWidget = api
        self.completions: list[Completion] = None
        
        settings.add_bracket_after_function = True
        self.path = path
        self.line = 0
        self.index = 0
        self.text = ""

    def run(self):
        try:
            self.script = Script(self.text, path=self.path)
            self.completions = self.script.complete(self.line, self.index)
            
            self.load_autocomplete(self.completions)
        except Exception as err:
            print(err)

        self.finished.emit() 

    def load_autocomplete(self, completions):
        self.api.clear()
        for i in completions:
            item = QListWidgetItem(i.name)
            item.setIcon(QIcon("./src/icons/svg/autocompletion.svg"))
            item.setToolTip(i.docstring())
            self.api.addItem(item)
        
        # get the parameters using re.findall("(\w*):" , text)
        

    def get_completions(self, line: int, index: int, text: str):
        self.line = line
        self.index = index
        self.text = text
        self.start()




class Completer(QListWidget):
    def __init__(self , parent=None):
        super().__init__(parent)
        
        self.code_editor = parent
        self.setHidden(True)
        self.code_editor.cursorPositionChanged.connect(self._cursorPositionChanged)
        self.itemClicked.connect(self._itemClicked)
        self.completer = AutoC(self, self.code_editor.path)
        
    def _itemClicked(self , item):
        text = item.text()
        self.code_editor.SendScintilla(self.code_editor.SCI_DELWORDLEFT)
        self.code_editor.insert(text)
        self.setHidden(True)
        self.code_editor.setFocus()
        
        
        
    def _cursorPositionChanged(self , line:int , index:int):
        self.completer.get_completions(line+1, index , self.code_editor.text())
        word = self.code_editor.wordAtLineIndex(line , index)
        if len(word) >= 1:
            self.setHidden(False)
        pos = self.code_editor.SendScintilla(self.code_editor.SCI_GETCURRENTPOS)
        x = self.code_editor.SendScintilla(self.code_editor.SCI_POINTXFROMPOSITION , 0 , pos)
        y = self.code_editor.SendScintilla(self.code_editor.SCI_POINTYFROMPOSITION , 0 , pos)
        
        self.move(x , y)
        
        if self.count() <= 10:
           self.resize(400, self.count() * 30)
        else:
            self.resize(400, 300)
            
