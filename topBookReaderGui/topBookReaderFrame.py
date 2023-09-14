
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderFrame.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from wx import (BoxSizer, VERTICAL, ALL, EXPAND,
    Frame,)

from topBookReaderGui.topBookReaderMenubar import TopBookReaderMenuBar
from topBookReaderGui.topBookReaderPanel import TopBookReaderPanel

#the main frame/window of the app
class TopBookReaderFrame(Frame):
    '''  this class serves as the main window of the app.  '''

    def __init__(self):
        super().__init__(None, -1, 'TOP Book Reader', )

        #self.__vSizer = BoxSizer(VERTICAL)
        #instantiate the toolbar object
        self.toolBar = self.CreateToolBar()
        self.pnl = TopBookReaderPanel(self)    #instantiates the TopBookReaderPanel object
        self.__menuBar = TopBookReaderMenuBar(self)    #instantiate the EbarMenuBar object
        self.SetMenuBar(self.__menuBar)    #add it to the main window
        #self.__vSizer.Add(self.pnl, 0, ALL | EXPAND, 5)
        #self.__vSizer.SetSizeHints(self)
        #self.SetSizer(self.__vSizer)

        self.Show()
