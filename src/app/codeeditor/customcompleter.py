from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
import os


class CustomCompleter(QListWidget):
    def __init__(self , parent=None):
        super().__init__(parent)
        
        self.editor : QsciScintilla = self.parent()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowFlags(Qt.Popup)
        self.setFocusProxy(self.editor)
        
        
        
        
        
