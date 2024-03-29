from PyQt5.QtGui import *
from PyQt5.Qsci import *
from PyQt5.QtCore import *


class JsonEditor(QsciScintilla):
    def __init__(self, path , parent):
        super().__init__(parent)
        
        self.language = "Json"
        self.path = path

        self.setMarginType(0, self.NumberMargin)
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.setMarginLineNumbers(0, True)
        self.setMarginsFont(QFont("Consolas", 13))
        self.setMarginWidth(0, "0000")

        self.setCaretForegroundColor(QColor("royalblue"))
        self.setCaretLineBackgroundColor(QColor("#2c313c"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(4)

        self.setIndentationsUseTabs(False)
        self.setIndentationGuides(True)
        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setTabIndents(True)

        self.setSelectionBackgroundColor(QColor("#333a46"))

        self.json_lexer = QsciLexerJSON(self)
        self.json_lexer.setDefaultColor(QColor("white"))
        self.json_lexer.setDefaultPaper(QColor("#161B21"))
        self.json_lexer.setDefaultFont(QFont("Consolas", 13))

        self.json_lexer.setPaper(QColor("#161B21"))
        self.json_lexer.setFont(QFont("Consolas", 13))

        self.json_lexer.setColor(QColor("white"))

        self.setLexer(self.json_lexer)

        self.setStyleSheet(open("./src/style/editor.css").read())
