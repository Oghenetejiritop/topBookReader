
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderFrame.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

from topBookReaderGui.topBookReaderPanel import TopBookReaderPanel
from topBookReaderGui.topBookReaderMenubar import TopBookReaderMenuBar
from topBookReaderGui.topBookReaderExitDialog import TopBookReaderExitDialog

#the main frame/window of the app
class TopBookReaderFrame(wx.Frame):
    '''  this class serves as the main window of the app.  '''

    def __init__(self):
        super().__init__(None, wx.ID_ANY, 'TOP Book Reader', )

        self.toolBar = self.CreateToolBar()    #instantiates the toolbar object

        self.pnl = TopBookReaderPanel(self)    #instantiates the TopBookReaderPanel object

        self.__menuBar = TopBookReaderMenuBar(self)    #instantiate the EbarMenuBar object
        self.SetMenuBar(self.__menuBar)    #add it to the main window

        self.Show()
