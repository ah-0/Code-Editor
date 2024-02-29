from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import git
from git import Repo
import sys
import os 


class CloneReopWin(QDialog):
    def __init__(self , window):
        super().__init__()
        self.window = window
        
        self.lable = QLable(self)
        self.lable.setText("Enter the repo url")
        self.lable.move(100,100)
        
        self.repo_url = QLineEdit(self)
        self.repo_url.move(100,150)
        
        self.lable2 = QLable(self)
        self.lable2.setText("Enter the path where you want to save the repo")
        self.lable2.move(100, 250)
        
        self.to_path = QLineEdit(self)
        self.to_path.move(100,300)
        
        
        self.btn_1 = QPushButton("&Cancel" , self)
        self.btn_1.resize(100 , 30)
        self.btn_1.move(380 , 400)
        self.btn_1.clicked.connect(lambda : self.exit())
        
        self.btn_2 = QPushButton("Clone")
        self.btn_2.resize(100,30)
        self.btn_2.move(500 , 400)
        self.btn_2.clicked.connect(self.clone_reop_)
        
        self.setStyleSheet("""
        QDialog{
            max-width:  600px;
            min-width:  600px;
            max-height: 420px;
            min-height: 420px;
        }
        
        """)
    def clone_reop_(self):
        Repo.clone_from(self.repo_url.text() , self.to_path.text())
        path = self.to_path.text()
        self.close()