from PyQt5.QtGui import *
from PyQt5.Qsci import *
from PyQt5.QtCore import *
from src.app.Editors.PythonLexer import PyCustomLexer
from src.app.Editors.PythonCompleter import AutoC
from jedi import Script

import os

class Python_Editor(QsciScintilla):
  def __init__(self , path="", parent=None):
    super().__init__(parent)
    
    
    self.FILE_PATH = path

    self.setMarginType(0 , self.NumberMargin)
    self.setMarginsForegroundColor(QColor("#ff888888"))
    self.setMarginsBackgroundColor(QColor("#161B21"))
    self.setMarginLineNumbers(0,True)
    self.setMarginsFont(QFont("Consolas", 13))
    self.setMarginWidth(0,"0000")

    self.merker_image = QPixmap("./icons/red_circle.png").scaled(12,12)
    self.setMarginType(1 , self.SymbolMargin)
    self.markerDefine(self.merker_image , 0)
    self.setMarginSensitivity(1,True)
    self.setMarginMarkerMask(1, 0b1111)
    self.setMarginWidth(1,"0000")
    self.marginClicked.connect(self.clickedmargins)  

    self.indicatorDefine(QsciScintilla.PlainIndicator ,1)
    self.setIndicatorForegroundColor(QColor("red") , 1)
    

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
    
    
    self.setCallTipsStyle(QsciScintilla.CallTipsNoContext)
    self.setCallTipsVisible(0)
    self.setCallTipsPosition(QsciScintilla.CallTipsAboveText)
    self.setCallTipsBackgroundColor(QColor(0xff, 0xff, 0xff, 0xff))
    self.setCallTipsForegroundColor(QColor(0x50, 0x50, 0x50, 0xff))
    self.setCallTipsHighlightColor(QColor(0xff, 0x00, 0x00, 0xff))

    
    self.setEolMode(QsciScintilla.EolWindows)
    self.setEolVisibility(False)
    
    
    
    self.setBraceMatching(QsciScintilla.StrictBraceMatch)
    self.setMatchedBraceBackgroundColor(QColor("#c678dd"))
    self.setMatchedBraceForegroundColor(QColor("#F2E3E3"))
    
    
    
    self.setEdgeColor(QColor("#2c313c"))
    self.setEdgeMode(QsciScintilla.EdgeLine)
    
    self.setWhitespaceBackgroundColor(QColor("#2c313c"))
    self.setWhitespaceForegroundColor(QColor("#ffffff"))
    self.setContentsMargins(0, 0, 0, 0)
    
    self.setSelectionBackgroundColor(QColor("#333a46"))
    
    self.lexerpython = PyCustomLexer(self)
    
    self.api = QsciAPIs(self.lexerpython)
    
    self.AutoCompleter = AutoC(self.api,self.FILE_PATH, self)
    
    self.classicon = QPixmap("./icons/class.png").scaled(12,12)
    self.registerImage(0,self.classicon)
    
    self.functionicon = QPixmap("./icons/function.png").scaled(12,12)
    self.registerImage(1,self.functionicon)
    
    self.Other = QPixmap("./icons/multiply.png").scaled(12,12)
    self.registerImage(2,self.Other)
    
    
 
    
    self.setStyleSheet(open("./style/editor.css").read())
    
    self.setLexer(self.lexerpython)
    
    self.cursorPositionChanged.connect(self._cursorPositionChanged)

    
    
    # self.SendScintilla(self.SCI_STYLESETHOTSPOT, 1, True)
    # self.SendScintilla(self.SCI_SETHOTSPOTACTIVEBACK, True, 0xaaaaaa)
    # self.setHotspotUnderline(True)
    # self.setHotspotBackgroundColor(QColor("red"))

    self.setAnnotationDisplay(self.AnnotationIndented)

    self.
    
    self.SendScintilla(self.SCI_AUTOCSETMAXHEIGHT , 7)

  def clickedmargins(self,margin , line , key):
    if self.markersAtLine(line) == 0:

      self.markerAdd(line , 0)
    else:
      self.markerDelete(line)
    
  def _cursorPositionChanged(self , line:int , index:int)-> None:
    self.AutoCompleter.get_completions(line+1 , index , self.text()) 
    # self.clearAnnotations(line)
    # self.annotate(line , "ahmet is king" , 0
    


    

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
      
      elif e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.text() == "/":
        lines = self.selectedText()
        lines = lines.split("\n")

        finally_ = []
        for i in lines:
          if i.startswith("#"):
            finally_.append(i[1:])
          else:
            finally_.append(f"#{i}")

        self.replaceSelectedText("\n".join(finally_))
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
        
  
          
          
        
      
        
        
        
      
        
    
    
