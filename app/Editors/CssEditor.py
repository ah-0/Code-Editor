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
    
    self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
    
    self.css_lexer = QsciLexerCSS(self)
    self.css_lexer.setDefaultColor(QColor("white"))
    self.css_lexer.setDefaultPaper(QColor("#161B21"))
    self.css_lexer.setDefaultFont(QFont("Consolas" , 13))
    
    self.css_lexer.setColor(QColor("white"))
    self.css_lexer.setColor(QColor("white"), QsciLexerCSS.Default)
    self.css_lexer.setColor(QColor("#64D6E8"), QsciLexerCSS.CSS3Property)
    self.css_lexer.setColor(QColor("#64D6E8"), QsciLexerCSS.CSS2Property)
    self.css_lexer.setColor(QColor("#64D6E8"), QsciLexerCSS.CSS1Property)
    self.css_lexer.setColor(QColor("#64D6E8"), QsciLexerCSS.Value)
    self.css_lexer.setColor(QColor("#CA2760"), QsciLexerCSS.Tag)
    self.css_lexer.setColor(QColor("#CA2760"), QsciLexerCSS.ClassSelector)
    self.css_lexer.setColor(QColor("#CA2760"), QsciLexerCSS.IDSelector)
    self.css_lexer.setColor(QColor("#CA2760"), QsciLexerCSS.PseudoClass)
    
    
    
    
    
    self.css_lexer.setPaper(QColor("#161B21"))
    self.css_lexer.setFont(QFont("Consolas" , 13))
    
    self.api = QsciAPIs(self.css_lexer)
    
    self.completer_icon = QPixmap("./icons/class.png").scaled(12,12)
    self.registerImage(0,self.completer_icon)
    
    with open("./autocompletion items/css.txt" , "r") as css:
      auto_complete_list = css.readlines()
      
      for i in auto_complete_list:
        self.api.add(f"{i}?0")
      self.api.prepare()
    
    
    self.setLexer(self.css_lexer)
    
    self.setStyleSheet(open("./style/editor.css").read())
    
  def keyPressEvent(self, e: QKeyEvent) -> None:
      
      if self.selectedText():
        selection = list(self.getSelection())
        if e.key() == Qt.Key.Key_QuoteDbl:
          self.insertAt('"', selection[0], selection[1])
          self.insertAt('"', selection[2], selection[3] + 1)
          selection[1] += 1
          selection[3] += 1
          self.setSelection(*selection)
          return
        
        elif e.key() == Qt.Key.Key_Apostrophe:
          self.insertAt("'", selection[0], selection[1])
          self.insertAt("'", selection[2], selection[3] + 1)
          selection[1] += 1
          selection[3] += 1
          self.setSelection(*selection)
          return
        
        elif e.key() == Qt.Key.Key_ParenLeft:
          self.insertAt("(", selection[0],selection[1])
          self.insertAt(")", selection[2], selection[3] + 1)
          selection[1] += 1
          selection[3] += 1
          self.setSelection(*selection)
          return
          
        elif e.key() == Qt.Key.Key_BracketLeft:
          self.insertAt("[", selection[0], selection[1])
          self.insertAt("]", selection[2], selection[3] + 1)
          selection[1] += 1
          selection[3] += 1
          self.setSelection(*selection)
          return
        
        elif e.key() == Qt.Key.Key_BraceLeft:
          self.insertAt("{", selection[0], selection[1])
          self.insertAt("}", selection[2], selection[3] + 1)
          selection[1] += 1
          selection[3] += 1
          self.setSelection(*selection)
          return
        
        elif e.key() == Qt.Key.Key_Tab and selection[0] == selection[2]:
          tabWidth = self.tabWidth()
          self.insertAt(" " * tabWidth, selection[0], 0)
          selection[1] = selection[3] + tabWidth
          selection[3] = 0
          self.setSelection(*selection)
          return
        else:
          super().keyPressEvent(e)
      
      
      
      else:
        line , index =  self.getCursorPosition()
        if e.text() == "(":
          self.insert("()")
          self.setCursorPosition(line, index+1)
          self.callTip()
          return
        
        elif e.text() == "'":
          self.insert("''")
          self.setCursorPosition(line ,index+1)
          return
        
        elif e.text() == '"':
          self.insert('""')
          self.setCursorPosition(line, index+1)
          return
        
        elif e.text() == "{":
          self.insert("{}")
          self.setCursorPosition(line ,index+1)
          return
        
        elif e.text() == "[":
          self.insert("[]")
          self.setCursorPosition(line ,index+1)
          return
    
        
        return super().keyPressEvent(e)
          
    
  
  
  
  