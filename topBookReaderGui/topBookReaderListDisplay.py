
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderListDisplay.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from wx import (ListView, LC_REPORT, LC_SINGLE_SEL, LC_HRULES, LC_VRULES,)
import wx.lib.mixins.listctrl as listControl

#display of the list control
class TopBookReaderListDisplay(ListView, listControl.ListCtrlAutoWidthMixin):
    '''
    class that serves as a list control which displays items as a report view.
    accepts two  parameters;
    parent: that requires the topBookReaderPanel object.
    *args: takes a list of strings to represent each column.
    '''

    def __init__(self, parent, *args):
        ListView.__init__(self, parent, -1, style=(LC_REPORT | LC_SINGLE_SEL | LC_HRULES | LC_VRULES))
        listControl.ListCtrlAutoWidthMixin.__init__(self)

        #insert the respective columns
        for number, column in enumerate(args):
            self.InsertColumn(number, column)
