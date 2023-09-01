
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderListDisplay.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx
import wx.lib.mixins.listctrl as listControl

#display of the list control
class TopBookReaderListDisplay(wx.ListView, listControl.ListCtrlAutoWidthMixin):
    '''
    class that serves as a list control which displays report view of items.
    accepts two  parameters;
    parent: that requires the topBookReaderPanel object.
    *args: takes a list of strings to represent each column.
    '''

    def __init__(self, parent, *args):
        wx.ListView.__init__(self, parent, wx.ID_ANY, style=(wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES))
        listControl.ListCtrlAutoWidthMixin.__init__(self)

        #insert the respective columns
        for number, column in enumerate(args):
            self.InsertColumn(number, column)
