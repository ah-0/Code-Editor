from PyQt5.QtCore import QThread
from PyQt5.Qsci import QsciAPIs
from jedi import Script
from jedi.api import Completion
import re
import os


class AutoC(QThread):
    def __init__(self, api ,path, parent=None):
        super(AutoC, self).__init__(parent)
        
        self.script: Script = None
        self.api: QsciAPIs = api
        self.completions: list[Completion] = None
        self.path = path
        

        self.line = 0
        self.index = 0
        self.text = ""

    def run(self):
        try:
            self.script = Script(self.text, path=self.path)
            print(self.path)
            self.completions = self.script.complete(self.line, self.index)
            
            self.load_autocomplete(self.completions , None)
        except Exception as err:
            print(err)

        self.finished.emit() 

    def load_autocomplete(self, completions , analysis):
        self.api.clear()
        
        # Code analysis
        # self.parent().markerDeleteAll(0)
        # print(self.parent().lines())
        # for i in range(self.parent().lines()):
        #     self.parent().clearAnnotations(i)
    
        # for i in analysis:
        #     self.parent().markerAdd(i.line-1 , 0)
            #self.parent().annotate(i.line-1 , f"{i.message}" , 0)
 

        [self.api.add(f"{i.name}?0") for i in completions]
        
        self.api.prepare() 

    def get_completions(self, line: int, index: int, text: str):
        self.line = line
        self.index = index
        self.text = text
        self.start()


        