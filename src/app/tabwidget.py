from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(open("./src/style/tabwidget.css", "r").read())
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)

    def closeTab(self, index):
        self.removeTab(index)

    def keyPressEvent(self, e: QKeyEvent):
        if e.modifiers() == Qt.AltModifier and e.key() == Qt.Key_Left:
            self.setCurrentIndex(self.currentIndex() - 1)
            return

        elif e.modifiers() == Qt.AltModifier and e.key() == Qt.Key_Right:
            self.setCurrentIndex(self.currentIndex() + 1)
            return

        elif e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F4:
            self.removeTab(self.currentIndex())
            return

        return super().keyPressEvent(e)
