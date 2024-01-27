from PyQt5.QtWidgets import QTabWidget


class TabWidget(QTabWidget):
  def __init__(self , parent=None):
    super().__init__(parent)
    
    
    self.setStyleSheet(open("./style/tabwidget.css" , "r").read())   
    self.setContentsMargins(0, 0, 0, 0)
    self.setMouseTracking(True)
    self.setMovable(True)
    self.setDocumentMode(True)
    self.setTabsClosable(True)
    self.tabCloseRequested.connect(lambda index : self.removeTab(index))
     