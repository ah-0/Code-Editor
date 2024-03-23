from PyQt5.QtGui import *
from PyQt5.Qsci import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup


class HtmlEditor(QsciScintilla):
    def __init__(self, path, parent):
        super().__init__(parent)
        
        self.language = "Html"
        self.path = path

        self.setMarginType(0, self.NumberMargin)
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#161B21"))
        self.setMarginLineNumbers(0, True)
        self.setMarginsFont(QFont("Consolas", 13))
        self.setMarginWidth(0, "0000")

        self.setCaretForegroundColor(QColor("royalblue"))
        self.setCaretLineBackgroundColor(QColor("#2c313c"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(4)

        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
        self.setAutoCompletionFillupsEnabled(True)

        self.setIndentationsUseTabs(False)
        self.setIndentationGuides(True)
        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setTabIndents(True)

        self.setSelectionBackgroundColor(QColor("#333a46"))

        self.html_lexer = QsciLexerHTML(self)
        self.html_lexer.setDefaultColor(QColor("white"))
        self.html_lexer.setDefaultPaper(QColor("#161B21"))
        self.html_lexer.setDefaultFont(QFont("Consolas", 13))

        self.html_lexer.setPaper(QColor("#161B21"))
        self.html_lexer.setFont(QFont("Consolas", 13))

        self.html_lexer.setColor(QColor("white"))

        self.api = QsciAPIs(self.html_lexer)

        self.completer_icon = QPixmap("./icons/class.png").scaled(12, 12)
        self.registerImage(0, self.completer_icon)

        with open("./src/app/codeeditor/autocompletion items/html.txt", "r") as html:
            auto_complete_list = html.readlines()

            for i in auto_complete_list:
                self.api.add(f"{i}?0")
            self.api.prepare()

        self.setLexer(self.html_lexer)

        self.setStyleSheet(open("./src/style/editor.css").read())
        
    def keyPressEvent(self, e: QKeyEvent) -> None:
        
        return super().keyPressEvent(e)

