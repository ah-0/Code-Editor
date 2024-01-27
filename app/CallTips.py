from PyQt5.QtCore import QThread
from PyQt5.Qsci import QsciScintilla
from jedi import Script

class CAllTIP(QThread):
    def __init__(self , editor=None):
        super().__init__(None)
        
        self.sci:QsciScintilla = editor 
        self.text = ""

    def run(self):
        try:
            script = Script(self.text , "main.py")
            analy = script._analysis()
            self.loadana(analy)
        except:
            print(" ")

        self.finished.emit()

    def loadana(self , ana):
        
        for i in ana:
            self.sci.annotate(i.line-1 , f"{i.message}" , 1)

    def getanay(self , text:str) ->None:
        self.text = text
        self.start()