from PyQt5.QtGui import *
from PyQt5.Qsci import *
from PyQt5.QtCore import *


class Css_Editor(QsciScintilla):
  def __init__(self, parent):
    super().__init__(parent)
    
    self.setMarginType(0 , self.NumberMargin)
    self.setMarginsForegroundColor(QColor("#ff888888"))
    self.setMarginsBackgroundColor(QColor("#161B21"))
    self.setMarginLineNumbers(0,True)
    self.setMarginsFont(QFont("Consolas", 13))
    self.setMarginWidth(0,"0000")
   
   
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
    
    self.css_lexer = QsciLexerCss(self)
    self.css_lexer.setDefaultColor(QColor("white"))
    self.css_lexer.setDefaultPaper(QColor("#161B21"))
    self.css_lexer.setDefaultFont(QFont("Consolas" , 13))
    
    
    self.css_lexer.setPaper(QColor("#161B21"))
    self.css_lexer.setFont(QFont("Consolas" , 13))
    
    self.api = QsciAPIs(self.css_lexer)
    
    with open("./autocompletion items/css.txt" , "r") as html:
      auto_complete_list = html_lexer.readlines()
      
      for i in auto_complete_list:
        self.api.add(f"{i}")
      self.api.prepare()
    
    
    self.setLexer(self.css_lexer)
    
    self.setStyleSheet(open("./style/editor.css").read())
  
  
  
  