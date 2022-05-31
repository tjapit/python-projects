import requests
import pandas as pd
import sys, urllib3
from PyQt5 import QtWidgets, QtGui, QtCore

class PokeDex(QtWidgets.QWidget):

    def __init__(self):
        super(PokeDex,self).__init__()

        self.initUI()

    def initUI(self):
        '''Initial UI'''

        #Grid Layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #Parse JSON for DataFrame
        self.df = pd.read_json('PokemonData.json')
        self.df = self.df.set_index(['#'])

        #Drop Down
        self.dropdown = QtGui.QComboBox(self)
        self.names = self.df['Name'].values
        self.dropdown.addItems(self.names)
        self.grid.addWidget(self.dropdown, 0,0,1,1)





