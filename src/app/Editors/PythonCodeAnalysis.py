from PyQt5.QtCore import QThread
from jedi import Script
import re
import os


class CodeAnalyzer(QThread):
    def __init__(self,path, parent=None):
        super(AutoC, self).__init__(parent)
        
        self.script: Script = None
        self.path = path
        self.text = ""

    def run(self):
        try:
            self.script = Script(self.text, path=self.path)
            self.code_analysis = self.script._analysis()
            
            self.load_code_analysis(self.code_analysis)
        except Exception as err:
            print(err)

        self.finished.emit() 

    def load_code_analysis(self, analysis):
        
       
        self.parent().markerDeleteAll(0)
    
        for i in analysis:
            self.parent().markerAdd(i.line-1 , 0)
     


    def display_errors(self, text: str):
        self.text = text
        self.start()


        