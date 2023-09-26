
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderBookContentTreeDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from  wx import (Bitmap, BITMAP_TYPE_PNG,
    BoxSizer, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON, EVT_LIST_ITEM_ACTIVATED, Font, FONTFAMILY_DEFAULT, FONTSTYLE_ITALIC, FONTWEIGHT_BOLD, ID_CANCEL,
    Dialog, ICON_EXCLAMATION, MessageDialog,
    StaticText,)

from topBookReaderGui.topBookReaderListDisplay import TopBookReaderListDisplay as ListDisplay


#dialog that accesses the table of content on an opened document
class TopBookReaderTableOfContentDialog(Dialog):
    '''for future release'''
    def __init__(self, bookTitle=''):
        bookTitle = bookTitle
        super().__init__(None, -1, title=f'Table Of Content for {bookTitle}', size=(500, 400))

        #instantiate the box sizers for the components 
        self.__vSizer = BoxSizer(VERTICAL)
        hSizer1 = BoxSizer(HORIZONTAL)
        self.__hSizer2 = BoxSizer(HORIZONTAL)

        hSizer1.Add(StaticText(self, -1, 'Head to :'), 0,  ALL, 5)
        self.__tableOfContent= ListDisplay(self, 'S/N', 'Title', 'Page No')    #instantiate the ListDisplay object to show recently opened books.
        hSizer1.Add(self.__tableOfContent, 1, EXPAND | ALL, 10)
        self.__vSizer.Add(hSizer1, 0, ALL)
        self.__hSizer2.Add(Button(self, ID_CANCEL, 'Cancel', style=BU_EXACTFIT), 0, ALL | CENTER, 5)
        self.__vSizer.Add(self.__hSizer2, 0, EXPAND)
        self.__vSizer.SetSizeHints(self)
        self.SetSizer(self.__vSizer)
