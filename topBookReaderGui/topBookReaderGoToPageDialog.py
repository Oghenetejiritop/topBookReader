
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderGoToPageDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''

from  wx import (BoxSizer, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON, Font, FONTFAMILY_DEFAULT, FONTSTYLE_ITALIC, FONTWEIGHT_BOLD,
    Dialog, Panel, StaticText, ID_CANCEL,
    TextCtrl, EVT_TEXT_ENTER, TE_PROCESS_ENTER,)

#dialog for navigating to a specific page
class TopBookReaderGoToPageDialog(Dialog):
    '''
    this class presents the go to page feature
    Has  a parameter (parent)  that requires the topBookReaderPanel object.
    '''

    def __init__(self, parent):
        super().__init__(None, title='Select A Page', size=(260, 240))

        self.__parent = parent
        self.__displayedContent = self.__parent.pnl.cloneDisplayedText()    #gets the reference to the displayedContent component of the app
        self.__bookPageInfo = self.__parent.pnl.getPageInfo()    #store both the current page number and the total pages.

        #instantiate the vertical box sizer
        vSizer = BoxSizer(VERTICAL)

        pnl = Panel(self)

        label = StaticText(pnl, -1, f'Enter the page from 1-{self.__bookPageInfo[1]} pages:')
        vSizer.Add(label, 0, ALL | LEFT, 10)

        self.__pageNumberEntry = TextCtrl(pnl, -1, size=(100, 25), style=TE_PROCESS_ENTER)
        #set the current page number as the default value
        self.__pageNumberEntry.SetValue(f'{self.__bookPageInfo[0]}')
        self.Bind(EVT_TEXT_ENTER, self.on_goToPageNumber, self.__pageNumberEntry)
        vSizer.Add(self.__pageNumberEntry, 0, ALL | LEFT, 5)

        goToPageBtn = Button(pnl, -1, '&Navigate to page ')
        goToPageBtn.Bind(EVT_BUTTON, self.on_goToPageNumber)
        vSizer.Add(goToPageBtn, 0, ALL | LEFT, 5)
  
        cancelBtn = Button(pnl, ID_CANCEL, 'Cancel')
        vSizer.Add(cancelBtn, 0, ALL | LEFT, 10)

        vSizer.SetSizeHints(pnl)
        pnl.SetSizer(vSizer)

    #event associated with this class

    #event that performs the goto page action
    def on_goToPageNumber(self, event):
        pageNumber = int(self.__pageNumberEntry.GetValue())    #convert the value of the pageNumberEntry to int, and store it.
        #open the specified page if it is within the range of pages
        if(pageNumber >= 1) and (pageNumber <= self.__bookPageInfo[1]):
            self.__parent.pnl.setPageNumber(pageNumber-1)
            self.__parent.pnl.pageNavigator(self.__parent.pnl.getBookContent())
            self.Destroy()
            return

        #otherwise, set focus to the pageNumber entry
        self.__pageNumberEntry.SetFocus()