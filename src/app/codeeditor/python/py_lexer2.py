from PyQt5.QtGui import *
from PyQt5.Qsci import *
from PyQt5.QtCore import *
import keyword

class PythonLexer(QsciLexerPython):
    def __init__(self, parent=None):
        super().__init__(parent)
        
         self.setHighlightSubidentifiers(False)
      
        self.setDefaultColor(QColor("#abb2bf"))
        self.setDefaultPaper(QColor("#1e1f22"))
        self.setDefaultFont(QFont("Consolas", 13))
        
        self.setColor(QColor("#abb2bf"))
        self.setColor(QColor("#abb2bf") , QsciLexerPython.Default)
        self.setColor(QColor("#EB827C") , QsciLexerPython.Keyword)
        self.setColor(QColor("#777777") , QsciLexerPython.Comment)
        self.setColor(QColor("#56b6c2") , QsciLexerPython.Number)
        self.setColor(QColor("#98c379") , QsciLexerPython.DoubleQuotedString)
        self.setColor(QColor("#98c379") , QsciLexerPython.SingleQuotedString)
        self.setColor(QColor("#98c379") , QsciLexerPython.TripleSingleQuotedString)
        self.setColor(QColor("#98c379") , QsciLexerPython.TripleDoubleQuotedString)
        self.setColor(QColor("#C68F55") , QsciLexerPython.ClassName)
        self.setColor(QColor("#61afd1") , QsciLexerPython.FunctionMethodName)
        self.setColor(QColor("#B799DA") , QsciLexerPython.HighlightedIdentifier)
        self.setColor(QColor("#c678dd") , QsciLexerPython.Operator)
        
        self.setFont(QFont("Consolas",13))
        self.setPaper(QColor("#1e1f22"))
        

    def keywords(self, flag):
        if flag == 1:
            kws = keyword.kwlist + ["self", "cls"]
        elif flag == 2:
            kws = dir(__builtins__)
        else:
            return None
        return " ".join(kws)