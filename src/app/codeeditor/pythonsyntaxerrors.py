from PyQt5.QtCore import QThread
from jedi import Script
import re
import os


class DisplaySyntaxErrors(QThread):
    def __init__(self ,path, parent=None):
        super(DisplaySyntaxErrors, self).__init__(parent)
        
        self.script: Script = None
        self.path = path
        self.text = ""

    def run(self):
        try:
            self.script = Script(self.text, path=self.path)
            self.syntax_errora = self.script.get_syntax_errors()
            
            self.load_syntax_errors(self.syntax_errors)
        except Exception as err:
            print(err)

        self.finished.emit() 

    def load_syntax_errors(self, _errors):
        
        self.parent().clearIndicatorRange(
                    0,
                    0,
                    self.lines(),
                    self.lineLength(self.lines()-1),
                    1
                )
                

        for i in _errors:
            self.parent().fillIndicatorRange(i.line-1 , 0 ,i.line-1 , len(self.parent().text(i.line-1))-1,1)

    def display_errors(self,text: str):
        self.text = text
        self.start()


        