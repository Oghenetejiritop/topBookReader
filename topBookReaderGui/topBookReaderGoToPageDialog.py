
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderGoToPageDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

#dialog for navigating to a specific page
class TopBookReaderGoToPageDialog(wx.Dialog):
    '''
    this class presents the go to page feature
    Has  a parameter (parent)  that requires the topBookReaderPanel object.
    '''

    def __init__(self, parent):
        super().__init__(None, title='Select A Page')

        self.__parent = parent
        self.__displayedContent = self.__parent.pnl.cloneDisplayedText()    #gets the reference to the displayedContent component of the app
        self.__bookPageInfo = self.__parent.pnl.getPageInfo()    #store both the current page number and the total pages.

        #instantiate the vertical box sizer
        vSizer = wx.BoxSizer(wx.VERTICAL)

        pnl = wx.Panel(self)

        label = wx.StaticText(pnl, -1, f'Enter the page from 1-{self.__bookPageInfo[1]} pages:')
        vSizer.Add(label, 0, wx.ALL | wx.LEFT, 10)

        self.__pageNumberEntry = wx.TextCtrl(pnl, wx.ID_ANY, size=(100, 25), style=wx.TE_PROCESS_ENTER)
        #set the current page number as the default value
        self.__pageNumberEntry.SetValue(f'{self.__bookPageInfo[0]}')
        self.Bind(wx.EVT_TEXT_ENTER, self.on_goToPageNumber, self.__pageNumberEntry)
        vSizer.Add(self.__pageNumberEntry, 0, wx.ALL | wx.LEFT, 5)

        goToPageBtn = wx.Button(pnl, wx.ID_ANY, '&Navigate to page ')
        goToPageBtn.Bind(wx.EVT_BUTTON, self.on_goToPageNumber)
        vSizer.Add(goToPageBtn, 0, wx.ALL | wx.LEFT, 5)
  
        cancelBtn = wx.Button(pnl, wx.ID_CANCEL, 'Cancel')
        vSizer.Add(cancelBtn, 0, wx.ALL | wx.LEFT, 10)

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