from PyQt5.QtCore import QThread
from PyQt5.Qsci import QsciAPIs
from jedi import Script
from jedi.api import Completion
import re
import os


class AutoC(QThread):
    def __init__(self, api):
        super(AutoC, self).__init__(None)
        
        self.script: Script = None
        self.api: QsciAPIs = api
        self.completions: list[Completion] = None
        

        self.line = 0
        self.index = 0
        self.text = ""

    def run(self):
        try:
            self.script = Script(self.text, path=os.getcwd())
            self.completions = self.script.complete(self.line, self.index)
            self.load_autocomplete(self.completions)
        except Exception as err:
            print(err)

        self.finished.emit() 

    def load_autocomplete(self, completions):
        self.api.clear()
        [self.api.add(f"{i.name}?0") for i in completions]
        
        self.api.prepare() 

    def get_completions(self, line: int, index: int, text: str):
        self.line = line
        self.index = index
        self.text = text
        self.start()


        