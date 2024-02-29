from PyQt5.QtGui import *
from PyQt5.Qsci import *
from PyQt5.QtCore import *
from .pythonlexer import PyCustomLexer
from .pythoncompleter import AutoC
from .pythonsyntaxerrors import DisplaySyntaxErrors
from .pythoncodeanalysis import CodeAnalyzer
from jedi import Script
import black
import json
import os


class PythonEditor(QsciScintilla):
    def __init__(self, path="", parent=None):
        super().__init__(parent)

        self.path = path
        setting_file_path = "./src/setting/PythonEditor.json"
        
        with open(setting_file_path , "r") as f:
            self.setting = json.load(f)
        
        
        if self.setting["Margin-Line-Number"]:
            self.setMarginType(0, self.NumberMargin)
            self.setMarginLineNumbers(0, True)
            self.setMarginWidth(0, "0000")
            
        self.setMarginsFont(QFont("Consolas", 13))
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        
        self.marker_image = QPixmap("./src/icons/warning.png").scaled(12, 12)
        self.setMarginType(1, self.SymbolMargin)
        self.markerDefine(self.marker_image, 0)
        self.setMarginSensitivity(1, True)
        self.setMarginMarkerMask(1, 0b1111)
        self.setMarginWidth(1, "0000")
        self.marginClicked.connect(self.clickedmargins)

        self.indicatorDefine(QsciScintilla.PlainIndicator, 1)
        self.setIndicatorForegroundColor(QColor("red"), 1)

        self.setCaretForegroundColor(QColor(self.setting["Caret-ForegroundColor"]))
        self.setCaretLineBackgroundColor(QColor(self.setting["Caret-Line-BackgroundColor"]))
        self.setCaretLineVisible(self.setting["Caret-Line-Visible"])
        self.setCaretWidth(self.setting["Caret-Width"])
        
        if self.setting["Auto-Completion-visible"]:
            self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
            self.setAutoCompletionThreshold(1)
            self.setAutoCompletionCaseSensitivity(False)
            self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
            

        self.setIndentationGuides(self.setting["Indentation-Guides"])
        self.setTabWidth(self.setting["Tab-Width"])
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(self.setting["Auto-Indent"])
        self.setBackspaceUnindents(True)
        
        self.setCallTipsStyle(QsciScintilla.CallTipsNoContext)
        self.setCallTipsVisible(0)
        self.setCallTipsPosition(QsciScintilla.CallTipsAboveText)
        self.setCallTipsBackgroundColor(QColor(0xFF, 0xFF, 0xFF, 0xFF))
        self.setCallTipsForegroundColor(QColor(0x50, 0x50, 0x50, 0xFF))
        self.setCallTipsHighlightColor(QColor(0xFF, 0x00, 0x00, 0xFF))

        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(self.setting["Eol-Visibility"])

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
        self.autocompleter = AutoC(self.api, self.path)
        if self.setting["Disply-Syntax-Errors"]:
            self.errorviewer = DisplaySyntaxErrors(self.path, self)
        if self.setting["Code-Analysis"]:
            self.codeanalyzer = CodeAnalyzer(self.path, self)

        self.classicon = QPixmap("./src/icons/class.png").scaled(12, 12)
        self.registerImage(0, self.classicon)



        self.setStyleSheet(open("./src/style/editor.css").read())

        self.setLexer(self.lexerpython)

        self.cursorPositionChanged.connect(self._cursorPositionChanged)


        self.setAnnotationDisplay(self.AnnotationIndented)
        

        self.SendScintilla(self.SCI_AUTOCSETMAXHEIGHT, 7)
        self.SendScintilla(self.SCI_AUTOCSETIGNORECASE , False)
        self.SendScintilla(self.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(self.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(self.SCI_SETADDITIONALSELECTIONTYPING, True)
        self.zoomTo(3)
        

    def clickedmargins(self, margin, line, key):
        if self.markersAtLine(line) == 0:
            self.markerAdd(line, 0)
        else:
            self.markerDelete(line)

    def _cursorPositionChanged(self, line: int, index: int) -> None:
        self.autocompleter.get_completions(line + 1, index, self.text())
        if self.setting["Disply-Syntax-Errors"]:
            self.errorviewer.display_errors(self.text())
        if self.setting["Code-Analysis"]:
            self.codeanalyzer.display_errors()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.text() == "f":
            line , index = self.getCursorPosition()
            format = black.format_str(self.text() , mode=black.FileMode())
            self.setText(format)
            self.setCursorPosition(line , index)
            return

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
                self.insertAt("(", selection[0], selection[1])
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

            elif (
                e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.text() == "/"
            ):

                start, srow, end, erow = self.getSelection()
                self.setSelection(start, 0, end, self.lineLength(end) - 1)

                lines = self.selectedText()
                lines = lines.split("\n")

                finally_ = []
                for i in lines:
                    if i.startswith("#"):
                        finally_.append(i[1:])
                    else:
                        finally_.append(f"#{i}")

                self.replaceSelectedText("\n".join(finally_))
                self.setSelection(start, srow, end, erow)
            else:
                super().keyPressEvent(e)

        if not self.selectedText():
            line, index = self.getCursorPosition()

            if e.text() == "(":
                self.insert("()")
                self.setCursorPosition(line, index + 1)
                self.callTip()
                return

            elif e.text() == "'":
                self.insert("''")
                self.setCursorPosition(line, index + 1)
                return

            elif e.text() == '"':
                self.insert('""')
                self.setCursorPosition(line, index + 1)
                return

            elif e.text() == "{":
                self.insert("{}")
                self.setCursorPosition(line, index + 1)
                return

            elif e.text() == "[":
                self.insert("[]")
                self.setCursorPosition(line, index + 1)
                return

            return super().keyPressEvent(e)
